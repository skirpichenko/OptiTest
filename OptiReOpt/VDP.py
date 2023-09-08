from ORConstants import *
from ORCore import *
from typing import *
import numpy as np
import numpy.typing as npt
import ORLogging
from ORContext import Instance, ORCache
import datetime
import os

# "Gaussian Shifted Mean Process" (GSMP)
# TODO: describe the model
class GSMP(object):
    def __init__(self
            , mean: np.float64, std: np.float64
            , meanTime: np.float64, stdTime: np.float64
            , bPositive = False):
        if mean < 0:
            raise ValueError('mean must be non-negative')
        if meanTime <= 0:
            raise ValueError('meanTime must be positive')
        if std < 0:
            raise ValueError('std must be non-negative')
        if stdTime < 0:
            raise ValueError('stdTime must non-negative')
        self.bPositive = bPositive
        self.mean = np.float64(mean)
        self.std = np.float64(std)
        self.meanTime = np.float64(meanTime)
        self.stdTime = np.float64(stdTime)
        self._value = self.sampleValue()
        self._nextValue = self.sampleValue()
        self._time = 0.0
        self._timeSwitch = self.sampleTime2Switch()
        
    def sampleValue(self):
        value = np.clip(np.random.normal(self.mean, self.std)
                        , self.mean - 3 * self.std
                        , self.mean + 3 * self.std)
        if self.bPositive:
            value = max(value, 0)
        return value
    
    def sampleTime2Switch(self):
        time2switch = 0.0
        # time2switch be positive
        while time2switch <= 0:
            time2switch = np.clip(np.random.normal(self.meanTime, self.stdTime)
                                  , self.meanTime - 3 * self.stdTime
                                  , self.meanTime + 3 * self.stdTime)
        return time2switch

    # dt is a time increament in seconds, returns area under the curve
    def GetAUC(self, dt: np.float64) -> np.float64:
        auc = 0.0
        while self._time + dt >= self._timeSwitch:
            auc += (self._timeSwitch - self._time) * (self._value + self._nextValue) / 2.0
            dt -= (self._timeSwitch - self._time)
            self._time = self._timeSwitch
            self._value = self._nextValue
            self._nextValue = self.sampleValue()
            self._timeSwitch += self.sampleTime2Switch()
        value = self._value + (self._nextValue - self._value) * dt / (self._timeSwitch - self._time)
        auc += dt * (self._value + value) / 2.0
        self._time += dt
        self._value = value
        return auc

    def IncreaseTime(self, dt: np.float64):
        while self._time + dt >= self._timeSwitch:
            dt -= (self._timeSwitch - self._time)
            self._time = self._timeSwitch
            self._value = self._nextValue
            self._nextValue = self.sampleValue()
            self._timeSwitch += self.sampleTime2Switch()
        self._value += (self._nextValue - self._value) * dt / (self._timeSwitch - self._time)
        self._time += dt
    
    @property
    def value(self) -> np.float64:
        return self._value


class DepositionModel(GSMP):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def get_thickness(self, dt: np.float64) -> np.float64:
        return self.GetAUC(dt)
    
    def __str__(self) -> str:
       return '<v> = {:10.5f} A/s, rms_v = {:10.5f} A/s, <t> = {:10.5f} s, rms_t = {:10.5f} s'.format(self.mean, self.std, self.meanTime, self.stdTime)

class FluctuactionModel(GSMP):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def __str__(self) -> str:
        return f'Drift = {self.mean} {RTUnits.DEFAULT}, Mean_Time = {str(self.meanTime)} sec, RMS_Time = {self.stdTime} sec'

    
class DepositedLayer(Layer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tsec = np.float64(0.0)
        
        
class VDP(Instance):
    def __init__(self, logFileName: str):
        super().__init__()
        self.logger = ORLogging.get_logger(f"vdp{self.id}", logFileName)
        self.l_units = LightUnits.DEFAULT
        self.rt_units = RTUnits.DEFAULT
        self.th_units = ThicknessUnits.DEFAULT
        self.rt_data = DataType.DEFAULT
        self.abbr2material: Dict[str, Material] = {}
        self.abbr2depModel: Dict[str, DepositionModel] = {}
        self.name2chip: Dict[str, WitnessChip] = {}
        self.incidenceAngle = np.float64(0.0) # normal incidence case  
        self.pol: Polarization = Polarization.DEFAULT
        self.tsecTotal = np.float64(0.0)
        self.na = np.complex128(1.0) # index of refraction of the ambient medium
        self.coating: List[DepositedLayer] = []
        self.noiseTR: np.float64 = np.float64(0.0)
        self.curChipName: str = None
        self.curMaterialAbbr: str = None
        self.hasStarted = False
        self.layer: DepositedLayer = None
        # Fluctuations in a spectrum level 
        self.levelFluct: Optional[FluctuactionModel] = None
        # Calibration drift
        self.calibrDriftRate = np.float64(0)
        self.recalibrTime = np.float64(60)
        # Input data correction 
        self.corrMethod = InputDataCorrectionMethod.DEFAULT
        # Random errors
        self.errPsi = np.float64(0)
        self.errDelta = np.float64(0)
        # BackSide effect
        self.hasBackSide = True
        self.backSideThickness = np.float64(1.0)
        # Cache for GetScan
        self.cache = {}
        self.logger.info("VDP instance created", {
            'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'id': self.id,
            'logFileName': logFileName
        })

    @property
    def curLayer(self) -> int:
        return len(self.coating) # NOTE: layer numbering starts from 1

    @property
    def chip(self) -> WitnessChip:
        if self.curChipName is not None:
            return self.name2chip[self.curChipName]
        elif len(self.name2chip) > 0:
            return next(iter(self.name2chip.values()))
        else:
            raise Exception("No witness chip defined")

    @property
    def material(self) -> Material:
        if not self.hasStarted:
            raise Exception("Deposition has not started")
        return self.abbr2material[self.curMaterialAbbr]

    @property
    def depModel(self) -> DepositionModel:
        if not self.hasStarted:
            raise Exception("Deposition has not started")
        if self.curMaterialAbbr not in self.abbr2depModel:
            raise Exception(f"Deposition model for {self.curMaterialAbbr} is not defined")
        return self.abbr2depModel[self.curMaterialAbbr]

    @property
    def depositedThicknesses(self) -> npt.NDArray[np.float64]:
        thicknesses = np.array([layer.thickness for layer in self.coating])
        # convert to the specified units
        return self.l_units.fromdef(thicknesses)


    def StartDeposition(self, chipName: str, materialAbbr: str):
        chipName = str(chipName)
        if chipName not in self.name2chip:
            raise Exception(f"Chip {chipName} is not defined")
        if materialAbbr not in self.abbr2material:
            raise Exception(f"Material {materialAbbr} to be deposited is not defined")
        self.curChipName = chipName
        self.curMaterialAbbr = materialAbbr
        self.hasStarted = True
        # create a new layer to be deposited
        self.layer = DepositedLayer(self.material, 0.0)
        self.chip.layers.append(self.layer)
        self.coating.append(self.layer)
        # log the deposition start
        self.logger.info("Deposition started", {'chip': self.curChipName, 'material': self.curMaterialAbbr})
        self.cache = {}


    def StopDeposition(self):
        if not self.hasStarted:
            raise Exception("Deposition has not started")
        self.hasStarted = False
        self.layer = None
        self.curChipName = None
        self.curMaterialAbbr = None
        self.logger.info("Deposition stopped", {
            'nLayers': len(self.coating),
            'tsecTotal': self.tsecTotal,
            'thickness': self.chip.thicknesses,
        })
        self.cache = {}


    def ResetDeposition(self):
        self.tsecTotal = np.float64(0.0)
        self.curChipName = None
        self.curMaterialAbbr = None
        self.hasStarted = False
        self.layer = None
        for chip in self.name2chip.values():
            chip.Reset()
        self.coating = []
        self.logger.info("Deposition reset")
        self.cache = {}

        
    def IncreaseTime(self, tsec: np.float64):
        if not self.hasStarted:
            raise Exception("Deposition has not started")
        if tsec < 0:
            raise ValueError("Time must be positive")
        if tsec == 0:
            return
        self.layer.tsec += tsec
        self.tsecTotal += tsec
        # model the thickness increase
        self.layer.thickness += self.depModel.get_thickness(tsec)
        if self.levelFluct is not None:
            self.levelFluct.IncreaseTime(tsec)
        self.logger.info("IncreaseTime", {
            'thickness': self.layer.thickness, 
            'self.layer.tsec': self.layer.tsec,
            'tsec': tsec
        })


    def LoadChipFile(self, chipName: str, chThick: np.float64, fname: str):
        chipName = str(chipName)
        if chipName in self.name2chip:
            self.logger.warning(f"Chip is already defined", extra={'chipName': chipName})
        material = Material.FromFile(fname, abbr = chipName, isVacuum = True)
        self.name2chip[chipName] = WitnessChip(material, chThick)
        self.logger.info("Chip loaded", {'chipName': chipName, 'chThick': chThick, 'fname': fname})
        self.cache = {}


    def LoadChipTable(self
            , chipName: str
            , name: Optional[str]
            , chipThickness: np.float64
            , wavelength: npt.NDArray[np.float64]
            , n: npt.NDArray[np.float64]
            , k: npt.NDArray[np.float64]
        ):
        if chipName in self.name2chip:
            self.logger.warning("Loaded chip will be replaced.", {'chipName': chipName, 'name': name})
        ri = RefractiveIndex(
            nType = MaterialNType.TABLE,
            kType = MaterialKType.TABLE,
            wavelength = wavelength,
            n = n,
            k = k,
            name = name
        )
        material = Material(abbr = chipName, vacuum = ri)
        self.name2chip[chipName] = WitnessChip(material, chipThickness)
        self.cache = {}


    def LoadChipFormula(self
            , chipName: str
            , chipThickness: np.float64
            , nType: MaterialNType, nFormulaCoef: Optional[npt.NDArray[np.float64]]
            , kType: MaterialKType, kFormulaCoef: Optional[npt.NDArray[np.float64]]
            , name: Optional[str] = None
        ):
        if chipName not in self.name2chip:
            # create a new material
            ri = RefractiveIndex(nType = nType, kType = kType, nFormulaCoef = nFormulaCoef, kFormulaCoef = kFormulaCoef, name = name)
            material = Material(abbr = chipName, vacuum = ri)
            self.name2chip[chipName] = WitnessChip(material, chipThickness)
        else:
            # modify the existing material
            chip = self.name2chip[chipName]
            if chip.substrate.thickness != chipThickness:
                self.logger.warning("Chip thickness will be replaced.", {'chipName': chipName, 'chipThickness': chipThickness})
            chip.substrate.thickness = chipThickness
            ri = chip.substrate.material.vacuum
            ri.ApplyFormula(nType, nFormulaCoef, kType, kFormulaCoef)
        self.cache = {}


    def LoadMaterialFile(self, abbr: str, fname: str):
        self.logger.info("Loading material", {'abbr': abbr, 'fname': fname})
        ri = RefractiveIndex.FromFile(fname)
        self.LoadMaterial(abbr, ri)


    def LoadMaterialTable(self
            , abbr: str
            , name: str
            , wavelength: npt.NDArray[np.float64]
            , n: npt.NDArray[np.float64]
            , k: npt.NDArray[np.float64]
        ):
        # self.logger.info("Loading material", {'abbr': abbr, 'name': name, 'wavelength': str(wavelength), 'n': str(n), 'k': str(k)})
        ri = RefractiveIndex(
            nType = MaterialNType.TABLE,
            kType = MaterialKType.TABLE,
            wavelength = wavelength,
            n = n,
            k = k,
            name = name
        )
        self.LoadMaterial(abbr, ri)


    def LoadMaterialFormula(self
            , abbr: str
            , name: Optional[str]
            , nType: MaterialNType, nFormulaCoef: npt.NDArray[np.float64]
            , kType: MaterialKType, kFormulaCoef: npt.NDArray[np.float64]
        ):
        if abbr in self.abbr2material and self.abbr2material[abbr].GetRI(inVacuum = True) is not None:
            self.abbr2material[abbr].GetRI(inVacuum = True).ApplyFormula(
                nType = nType, 
                nFormulaCoef = nFormulaCoef,
                kType = kType,
                kFormulaCoef = kFormulaCoef
            )
        else:
            ri = RefractiveIndex(
                nType = nType,
                kType = kType,
                nFormulaCoef = nFormulaCoef,
                kFormulaCoef = kFormulaCoef,
                name = name
            )
            self.LoadMaterial(abbr, ri)


    def LoadMaterial(self, abbr: str, ri: RefractiveIndex):
        if len(abbr) != 1:
            raise ValueError(f"Material abbreviation has to be a single character string; given {abbr}")
        if abbr not in self.abbr2material:
            # VDP assumes that the material is vacuum
            mat = Material(abbr, vacuum = ri)
            self.abbr2material[abbr] = mat
        else:
            mat = self.abbr2material[abbr]
            if mat.vacuum != None:
                self.logger.warning("Loaded material will be replaced.", {'Abbr': abbr, 'ri.name': ri.name})
            mat.vacuum = ri
        self.logger.info("Material loaded", {'abbr': abbr, 'ri.name': ri.name})
        self.cache = {}


    def LoadMaterialDeposition(self, abbr: str, dep: DepositionModel):
        if abbr not in self.abbr2material:
            raise Exception(f"Material {abbr} is not defined")
        if abbr in self.abbr2depModel:
            self.logger.warning(f"Material deposition model is already defined", extra={'abbr': abbr})
        self.abbr2depModel[abbr] = dep
        self.logger.info("Material deposition model loaded", {'abbr': abbr})


    def GetScan(self, lam: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        if len(lam) == 0:
            return np.array([])

        if 'GetScan' in self.cache \
                and np.array_equal(self.cache['GetScan'].wavelength, lam) \
                and self.cache['GetScan'].meta['chip'] == self.curChipName \
                and self.cache['GetScan'].meta['curLayer'] == self.curLayer \
                and self.cache['GetScan'].backSideMatters == self.hasBackSide \
                and self.cache['GetScan'].backSideThickness == self.backSideThickness \
                and self.cache['GetScan'].pol == self.pol \
                and self.cache['GetScan'].incidenceAngle == self.incidenceAngle:
            op = self.cache['GetScan']
        else:
            op = OptiProps(
                thicknesses = self.chip.thicknesses
                , wavelength = lam
                , refractiveIndices = self.chip.GetLayersN(lam)
                , substrateRefractiveIndex = self.chip.GetSubstrateN(lam)
                , pol = self.pol
                , incidenceAngle = self.incidenceAngle
                , na = RefractiveIndex.vacuum
                , rt_units = RTUnits.ABS # solve in absolute units and convert later
                , backSideMatters = self.hasBackSide
                , backSideThickness = self.backSideThickness
            )
            op.meta['chip'] = self.curChipName
            op.meta['curLayer'] = self.curLayer
            op.InitTopLayers(1)
            self.cache['GetScan'] = op
        # update last layer thickness and calculate scan
        if len(op.thicknesses) > 0:
            op.thicknesses[-1] = self.chip.layers[-1].thickness
        op.UpdateTopLayers(False)
        scan = op.GetData(self.rt_data)
        # add gaussian noise
        if self.noiseTR > 0:
            scan += np.random.normal(0, self.noiseTR, len(scan))
        # add fluctuations in the spectrum level
        if self.levelFluct is not None:
            scan += self.levelFluct.value
        # adjust units after adding noise and fluctuations to ensute thay have same scale
        if self.rt_units == RTUnits.ABS:
            return scan
        elif self.rt_units == RTUnits.PERCENT:
            return scan * 100
        else:
            raise Exception("Unknown RT units")
        

    def SetFluctuations(self, shiftStd: np.float64, shiftTimeMean: np.float64, shiftTimeStd: np.float64):
        self.levelFluct = FluctuactionModel(0, shiftStd, shiftTimeMean, shiftTimeStd)
        self.logger.info("Fluctuations set", {
            'shiftStd': shiftStd,
            'shiftTimeMean': shiftTimeMean,
            'shiftTimeStd': shiftTimeStd
        })

    def GetVersionInfo(self) -> str:
        return str(self.versionMajor + self.versionMinor/10)
    
    def GetLogName(self) -> str:
        return self.logger.filename
    
    def GetReportHeader(self) ->List[str]:
        return ['OptiReOpt - On-Line Characterization and Reoptimization Software\n',
                'Virtual Deposition Process and Virtual Monitoring Device module\n',
                '            Version '  + self.GetVersionInfo() + ' \n',
                '\n']
    
    def GetReportGeneral(self) ->List[str]:
        return ['General information:\n',
                'Started: ' + self.creationDatetime.strftime("%Y-%m-%d at %H:%M:%S") +'\n',
                'Log file name: ' + self.GetLogName() +'\n',
                f'Length units:    {LightUnits.DEFAULT} \n',
                f'T/R units:       {RTUnits.DEFAULT} \n']
    
    def GetReportVDProcessConfig(self) ->List[str]:
        text =  ['Virtual Deposition Process configuration:\n']
        # chip list with parameters
        text += ['The number of witness chips = ' + str(len(self.name2chip)) +'\n\n']
        count = 0
        if len(self.name2chip)>0:
            for abbr, chip in self.name2chip.items():
                text += f'Chip #  {count+1} Thickness:   {chip.substrate.thickness} mm\n'
                text += f' Chip name: {chip} \n'
                text += f'{chip.substrate.material.about()}\n'
                count +=1
        # material Inhomogeneity
        text += ['Inhomogeneity for {} material = {:10.5f}\n'.format(abbr, 0.0) for abbr in self.abbr2material]
        # material deposition model
        text += ['Material {}: {}\n'.format(abbr, str(model)) for abbr, model in self.abbr2depModel.items()]               
        # material list with parameters
        text +='\n'
        if len(self.abbr2material)>0:
            for abbr, material in self.abbr2material.items():
                text += f'Material {abbr}, name: {material.airName} \n'
                text += f'{material.about()}\n'
                count +=1        

        return text

    def GetReportVMDeviceConfig(self) ->List[str]:
        return [f'Virtual Monitoring Device configuration:\n'
                f'Measurements type: {self.rt_data} \n',
                f'     Polarization: {self.pol.to_char()}\n'
                f'Angle of incidence = {self.incidenceAngle} deg\n',
                'Spectral photometry\n',
                f' Random Errors = {self.noiseTR} {RTUnits.DEFAULT}\n',
                f' Fluctuations: {self.levelFluct}\n',
                f' Calibration drifts: Type {self.corrMethod}, Rate = {self.calibrDriftRate} {RTUnits.DEFAULT}/1000 sec, Recalibration time = {self.recalibrTime} sec\n',
                'Spectral ellipsometry\n', 
                f' Random Errors: ErrPsi = {self.errPsi} deg, ErrDelta = {self.errPsi} deg \n']    


    def GetReport(self, fname: str):
        reportName = fname if fname else os.path.splitext(self.GetLogName())[0] + '.inp'
        try:
            with open(reportName, 'w') as file:
                file.write(''.join(self.GetReportHeader()))
                file.write('--------------------------------------------------------\n')            
                file.write(''.join(self.GetReportGeneral()))
                file.write('--------------------------------------------------------\n')
                file.write(''.join(self.GetReportVDProcessConfig()))
                file.write('--------------------------------------------------------\n')
                file.write(''.join(self.GetReportVMDeviceConfig()))
                self.logger.info("Report is created", {'filename': reportName})
        except Exception as e:
            self.logger.error(f"An error occurred while writing report to '{reportName}': {e}")
