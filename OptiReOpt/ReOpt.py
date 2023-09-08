from ORConstants import *
from ORCore import *
from typing import *
import numpy as np
import numpy.typing as npt
import ORLogging
import os
from typing import NamedTuple
from ORContext import Instance, ORCache
import xmltodict
import datetime 
import gc

from scipy.optimize import least_squares, minimize
import time

##############################################################################
class ReOptConfig:
    def __init__(self):
        self.l_units = LightUnits.DEFAULT
        self.rt_units = RTUnits.DEFAULT
        self.th_units = ThicknessUnits.DEFAULT
        self.rt_data = DataType.DEFAULT
        self.calcMode = CalculationMode.DEFAULT
        self.dataCorr = InputDataCorrection.DEFAULT
        self.dataCorrType = InputDataCorrectionMethod.DEFAULT
        
    def __str__(self):
        prop2name = lambda prop: getattr(prop, 'name', str(prop))
        props = [p for p in dir(self) if not p.startswith('_')]
        props = ','.join([f'{p}={prop2name(getattr(self, p))}' for p in props])
        return f"{self.__class__.__name__}({props})"
    def __repr__(self):
        return str(self) 

####################################################################################################    
class ReOpt(Instance):   

    def __init__(self, logFileName: str, multiProc: bool):
        super().__init__()
        self.multiProc = multiProc
        self._nCores = max(os.cpu_count(), 1) if multiProc else 1
        self.logger = ORLogging.get_logger(f"reopt{self.id}", logFileName)
        self.config = ReOptConfig()
        self.abbr2material: Dict[str, Material] = {}
        self.material2deprate: Dict[str, float] = {}
        self.design: Optional[Design] = None
        # substrate effects
        self.onlineBackside = True
        self.onlineBacksideThickness = np.float64(1.0)
        self.reoptBackside = True
        self.reoptBacksideThickness = np.float64(1.0)
        # The angle of incidence and polarization of the light source
        self._incidenceAngle = np.float64(0.0) # normal incidence case
        self.pol: Polarization = Polarization.DEFAULT   
        self.na = RefractiveIndex.vacuum
        # witnesses chips
        self.name2chip: Dict[str, WitnessChip] = {}
        # online wavelength range
        self.lamMin: Optional[np.float64] = None
        self.lamMax: Optional[np.float64] = None
        self.wavelength: Optional[npt.NDArray[np.float64]] = None
        # monitoring parameters
        self.nScanWindow = 0
        self.nAverWindow = 0
        # Reoptimization
        self.target: Optional[Target] = None
        self.thicknessThreshold = np.float64(0.05) # replace criteria
        self.meritThreshold = np.float64(0.15) # replace criteria
        # system members
        self.cache = {}
        self._scaleFactor = 1.0
        self._scalShift = 0.0
        # logging
        self.logger.info("ReOpt instance created", {
            'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'id': self.id,
            'logFileName': logFileName,
            'multiProc': multiProc
        })

    # Returns the state of the object to be pickled.
    def __getstate__(self):
        state = super().__getstate__().copy()
        state['_log_file_name'] = self.logger.handlers[0].baseFilename
        del state['logger']
        return state
    # Sets the state of the object after being unpickled.
    def __setstate__(self, state):
        super().__setstate__(state)
        self.__dict__.update(state)
        self.logger = ORLogging.get_logger(f"reopt{self.id}", state['_log_file_name'])
        
    @property
    def scaleFactor(self):
        return self._scaleFactor
    @scaleFactor.setter
    def scaleFactor(self, value: np.float64):
        self._scaleFactor = InputDataCorrectionMethod.ClipScale(value)

    def GetChip(self, name: str = WitnessChip.DEFAULT_NAME) -> WitnessChip:
        if name in self.name2chip:
            return self.name2chip[name]
        if name == WitnessChip.DEFAULT_NAME and name in self.abbr2material:
            chip = WitnessChip(
                substrate = self.abbr2material[name],
                thickness = self.onlineBacksideThickness
            )
            self.name2chip[name] = chip
            return chip
        raise ValueError(f"Chip {name} not found.")

    def __str__(self):
        prop2name = lambda prop: getattr(prop, 'name', str(prop))
        with np.printoptions(precision=3, suppress=True, edgeitems=1):
            props = [p for p in dir(self.__class__) if isinstance(getattr(self.__class__,p),property) and 
                    str(p) != '_numba_type_']
            props = ','.join([f'{p}={prop2name(getattr(self, p))}' for p in props])
            return f"{self.__class__.__name__}({props})"

    def __repr__(self):
        return str(self) 

    def __del__(self):
        # TODO: flush logs etc.
        pass

    @property
    def incidenceAngle(self):
        return self._incidenceAngle
    
    @incidenceAngle.setter
    def incidenceAngle(self, angle: np.float64):
        if angle < 0 or angle > 90:
            raise ValueError("Incidence angle must be in range from 0 to 90 degrees.")
        self._incidenceAngle = angle

    @property
    def NProcessors(self):
        return self._nCores
    
    @NProcessors.setter
    def NProcessors(self, NProc: np.int64):
        if NProc <= 0 or NProc > 64:
            raise ValueError("NProc must be in range from 1 to 64")
        self._nCores = NProc

    @property
    def nLayers(self):
        return self.design.nLayers if self.design is not None else 0
    
    def GetDepositionRate(self, nLayer: np.float64):
        MIN_DEP_RATE = 0.1
        return self.material2deprate.get(self.design.layers[nLayer].material, MIN_DEP_RATE)


    def SetWavelengthGrid(self, wavelength: npt.NDArray[np.float64]):
        if self.lamMax is not None:
            wavelength = wavelength[wavelength <= self.lamMax]
        if self.lamMin is not None:
            wavelength = wavelength[wavelength >= self.lamMin]
        if len(wavelength) == 0:
            raise ValueError("Wavelength grid is empty.")
        self.wavelength = wavelength
        self.logger.info(f"Wavelength grid set to:", {
            'wavelength': str(wavelength),
        })

    def ImportODXFile(self, fname: str):
        # Read the XML file
        with open(fname, "r", encoding="utf-8") as file:
            xml_data = file.read()
            # Parse the XML data and convert it to a dictionary
            xml_dict = xmltodict.parse(xml_data)
            # parse the dictionary
            coating = Coating.FromXmlDict(xml_dict['thin-film-coating'])
            self.logger.info(f"Coating {coating.provider} imported from {fname}.", {
                'coating': str(coating),
                'design': str(coating.design),
                'materials': str(coating.abbr2material)
            })
            # create design
            if self.design is not None:
                self.logger.warning("Design already exists. It will be replaced.")
            self.design = coating.design
            # create materials
            for abbr, mat in coating.abbr2material.items():
                if abbr in self.abbr2material:
                    self.logger.warning(f"Material {abbr} already exists. It will be replaced.")
                self.abbr2material[abbr] = mat
            # create substrate

    def LoadMaterialFile(self, abbr: str, fname: str, inVacuum: bool = True):
        ri = RefractiveIndex.FromFile(fname)
        self.LoadMaterial(abbr, ri, inVacuum)

    def LoadMaterialTable(self
            , abbr: str
            , name: Optional[str]
            , wavelength: npt.NDArray[np.float64]
            , n: npt.NDArray[np.float64]
            , k: npt.NDArray[np.float64]
            , inVacuum: bool = True
        ):
        ri = RefractiveIndex(
            nType = MaterialNType.TABLE,
            kType = MaterialKType.TABLE,
            wavelength = wavelength,
            n = n,
            k = k,
            name = name
        )
        self.LoadMaterial(abbr, ri, inVacuum)

    def LoadMaterialFormula(self
            , abbr: str
            , name: Optional[str]
            , nType: MaterialNType, nFormulaCoef: npt.NDArray[np.float64]
            , kType: MaterialKType, kFormulaCoef: npt.NDArray[np.float64]
            , inVacuum: bool = True
        ):
        if abbr in self.abbr2material and self.abbr2material[abbr].GetRI(inVacuum) is not None:
            self.abbr2material[abbr].GetRI(inVacuum).ApplyFormula(
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
            self.LoadMaterial(abbr, ri, inVacuum)

    def LoadMaterial(self
            , abbr: str
            , ri: RefractiveIndex
            , inVacuum: bool = True
        ):
        if len(abbr) != 1:
            raise ValueError(f"Material abbreviation has to be a single character string; given {abbr}")
        if abbr not in self.abbr2material:
            mat = Material(abbr, vacuum = ri) if inVacuum else Material(abbr, air = ri)
            self.abbr2material[abbr] = mat
        else:
            mat = self.abbr2material[abbr]
            if inVacuum:
                if mat.vacuum != None:
                    self.logger.warning("Loaded material will be replaced.", {'Abbr': abbr})
                mat.vacuum = ri
            else:
                if mat.air != None:
                    self.logger.warning("Loaded material will be replaced.", {'Abbr': abbr})
                mat.air = ri
        # the design has been changed, so we need to erase the cache
        self.cache = {}
        
    def LoadTheoreticalDesignFile(self, fname: str) -> np.int64:
        design = Design.FromFile(fname, self.abbr2material)
        if self.design is not None:
            log_data = {'new_fname': fname, 'current_design': str(self.design), 'new_design': str(design)}
            self.logger.warning("The loaded designs is to be overwritten.", log_data)
        self.design = Design.FromFile(fname, self.abbr2material)
        # the design has been changed, so we need to erase the cache
        self.cache = {}
        return self.design.nLayers

    def LoadTheoreticalDesign(self
            , controlW: np.float64, matchAngle: np.float64, matchMedium: np.float64, nLayers: np.int64
            , thicknesses: npt.NDArray[np.float64], abbreviations: str, comment: Optional[str] = ''
        ):
        # self.logger.info("Loading design from the given parameters.", {'nLayers': nLayers, 'thicknesses': thicknesses, 'abbreviations': abbreviations})
        if self.design is not None:
            log_data = {'current_design': str(self.design)}
            self.logger.warning("The loaded design is to be overwritten.", log_data)
        if len(thicknesses) != nLayers:
            raise ValueError("Number of layers does not match the number of thicknesses.")
        if len(abbreviations) != nLayers:
            raise ValueError("Number of layers does not match the number of abbreviations.")
        # TDOD: convert units !!!!!!!!!!!!!!
        self.design = Design(
            comment = comment,
            controlW = controlW,
            matchAngle = matchAngle,
            matchMedium = matchMedium
        )
        # make sure all the materials are loaded
        for abbr, thick in zip(abbreviations, thicknesses):
            if abbr not in self.abbr2material:
                raise ValueError(f"Material {abbr} is not loaded.")
            layer = Layer(self.abbr2material[abbr], thick)
            self.design.AddLayer(layer)
        # the design has been changed, so we need to erase the cache
        self.cache = {}
        return self.design.nLayers

    def LoadChipFile(self, chipName: str, chipThickness: np.float64, fname: str):
        if chipName in self.name2chip:
            self.logger.warning("Loaded chip will be replaced.", {'chipName': chipName, 'fname': fname})
        material = Material.FromFile(fname)
        self.name2chip[chipName] = WitnessChip(material, chipThickness)
        self.logger.info("Chip loaded", {'chipName': chipName, 'chipThickness': chipThickness, 'fname': fname})
        # the design has been changed, so we need to erase the cache
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

    def LoadChipFormula(self, chipName: str, chipThickness: np.float64
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

    def LoadDepositionStrategy(self, strategy: List[str]):
        if set(strategy) > set(self.name2chip.keys()):
            diff = list(set(strategy) > set(self.name2chip.keys()))
            raise ValueError(f"The deposition strategy contains unknown chip names {' '.join(diff)}")
        if self.design is None:
            raise ValueError("No design is loaded.")
        # clean up the chips
        for chip in self.name2chip.values():
            chip.Reset()
        # the design has been changed, so we need to erase the cache
        self.cache = {}

    def RemoveAllChips(self):
        self.name2chip = {}
        if self.design is not None:
            for layer in self.design.layers:
                layer.chipName = None
        self.logger.info("All chips removed")
        # the design has been changed, so we need to erase the cache
        self.cache = {}

    def GetSubstrateRI(self, wavelength: npt.NDArray[np.float64]) -> npt.NDArray[np.complex128]:
        if '0' in self.abbr2material:
            return self.abbr2material['0'].GetRefrativeIndex(wavelength)
        else:
            return np.ones_like(wavelength, dtype=np.complex128)
        
    def LoadTarget(self, fname: Optional[str] = None):
        if self.target is not None:
            self.logger.warning("Loaded target will be replaced.", {'fname': fname})
        if fname is None:
            # auto-generate the target
            if self.design is None:
                raise ValueError("No design is loaded.")
            if self.wavelength is None:
                raise ValueError("No wavelength is loaded.")
            self.target = Target(name = 'AUTO', comment = 'Auto-generated target based on the design.')
            values = self.GetOnLineValues(
                  wavelength = self.wavelength
                , lastLayer = self.design.nLayers
                , lastLayerFraction = 1.0
                , incidenceAngle = self.incidenceAngle
                , pol = self.pol
                , rt_data = self.config.rt_data
            )
            self.target.AddPage(TargetPage(
                  angle = self.incidenceAngle
                , wavelength = self.wavelength
                , spechar = self.config.rt_data.to_spechar(self.pol)
                , values = values
            ))
        else:
            self.target = Target.FromFile(fname)
            self.logger.info("Target loaded", {'fname': fname})

    def AddTargetPage(self, name: str, page: TargetPage):
        if self.target is None:
            self.target = Target(name = name, comment = '')
        self.target.AddPage(page)
        self.logger.info("Target page added", {'page': page})

    def GetOnLineValues(self, 
            wavelength: npt.NDArray[np.float64], 
            lastLayer: np.int64, 
            lastLayerFraction: np.float64,
            incidenceAngle: Optional[np.float64] = None,
            pol: Optional[Polarization] = None,
            rt_data: Optional[DataType] = None
        ) -> npt.NDArray[np.float64]:
        if self.design is None:
            raise ValueError("A theoretical design must be loaded.")
        if lastLayer < 1 or lastLayer > self.design.nLayers:
            raise ValueError("The 'lastLayer' parameter must be between 1 and the number of layers.")

        if lastLayerFraction < 0:
            if lastLayerFraction != -1 and lastLayerFraction != -2:
                raise ValueError("The 'lastLayerFraction' parameter must be between 0 and 1, or -1 or -2.")
            # TODO: find out the difference between -1 and -2
            thicknesses = self.design.ph_thicknesses[:lastLayer]
        else:
            # use ticknesses determinned during the last characterization
            thicknesses = self.design.ph_thicknesses[:lastLayer]
            thicknesses[-1] *= lastLayerFraction

        if 'GetOnLineValues' in self.cache \
                and np.array_equal(self.cache['GetOnLineValues'].wavelength, wavelength) \
                and self.cache['GetOnLineValues'].nLayers == lastLayer \
                and np.array_equal(self.cache['GetOnLineValues'].thicknesses[:-1], thicknesses[:-1]) \
                and self.cache['GetOnLineValues'].incidenceAngle == incidenceAngle \
                and self.cache['GetOnLineValues'].pol == pol:
            op = self.cache['GetOnLineValues']
        else:
            op = OptiProps(
                thicknesses = thicknesses
                , wavelength = wavelength
                , refractiveIndices = self.design.GetRefractiveIndices(wavelength, lastLayer)
                , substrateRefractiveIndex = self.GetSubstrateRI(wavelength)
                , pol = self.pol if pol is None else pol
                , incidenceAngle = self.incidenceAngle if incidenceAngle is None else incidenceAngle
                , na = self.na
                , rt_units = self.config.rt_units
                , backSideMatters = self.onlineBackside
                , backSideThickness = self.onlineBacksideThickness
            )
            # op.Forward()
            op.InitTopLayers(1)
            self.cache['GetOnLineValues'] = op
            # clean up memory
            th = gc.get_threshold()
            gc.set_threshold(0, 0, 0)
            gc.collect()
            gc.set_threshold(*th)

        # update last layer thickness and calculate scan
        op.thicknesses[-1] = thicknesses[-1]
        # op.ForwardLastD()
        op.UpdateTopLayers(False)
        return op.GetData(self.config.rt_data if rt_data is None else rt_data)


    class ProcessOnLineTRScanReturn(NamedTuple):
        d_currGeo: np.float64
        d_currQWOT: np.float64
        v_dep: np.float64
        quality: PredQuality
        dt_switch: np.float64
        f_avg: np.float64
        def __str__(self):
            s = [
                f"d_currGeo={self.d_currGeo:0.3f}",
                f"d_currQWOT={self.d_currQWOT:0.3f}",
                f"v_dep={self.v_dep:0.3f}",
                str(self.quality),
                f"dt_switch={self.dt_switch:0.2f}",
                f"f_avg={self.f_avg:0.3f}"
            ]
            return f"({', '.join(s)})"
        def __repr__(self):
            return self.__str__()


    def ProcessOnLineTRScan(self
            , tm: np.float64
            , lastLayer: np.int64
            , lam: npt.NDArray[np.float64]
            , val: npt.NDArray[np.float64]
            , tol: Optional[npt.NDArray[np.float64]] = None
            , verbose: bool = False
        ) -> ProcessOnLineTRScanReturn:
        if self.design is None:
            raise ValueError("A theoretical design must be loaded before calling 'ProcessOnLineTRScan'.")
        if tm < 0.0:
            raise ValueError("The 'tm' parameter must be greater than or equal to zero.")
        if lastLayer < 1 or lastLayer > self.design.nLayers:
            raise ValueError("The 'lastLayer' parameter must be between 1 and the number of layers.")
        if len(lam) < 1:
            raise ValueError("The 'nLam' parameter must be greater than zero.")

        spectrum = val.astype(np.float64)
        wavelength = lam.astype(np.float64)
        design_thicknesses = self.design.ph_thicknesses
        thicknesses = design_thicknesses[:lastLayer]
        tsec = tm # time.time()

        if 'ProcessOnLineTRScan' in self.cache \
                and np.array_equal(self.cache['ProcessOnLineTRScan'].wavelength, wavelength) \
                and self.cache['ProcessOnLineTRScan'].nLayers == lastLayer \
                and np.array_equal(self.cache['ProcessOnLineTRScan'].thicknesses[:-1], thicknesses[:-1]) \
                and self.cache['ProcessOnLineTRScan'].incidenceAngle == self.incidenceAngle \
                and self.cache['ProcessOnLineTRScan'].pol == self.pol:
            op = self.cache['ProcessOnLineTRScan']
        else:
            op = OptiProps(
                thicknesses = thicknesses,
                wavelength = wavelength,
                refractiveIndices = self.design.GetRefractiveIndices(wavelength, lastLayer),
                substrateRefractiveIndex = self.GetSubstrateRI(wavelength),
                pol = self.pol,
                incidenceAngle = self.incidenceAngle,
                na = self.na,
                rt_units = self.config.rt_units,
                backSideMatters = self.onlineBackside,
                backSideThickness = self.onlineBacksideThickness,
            )
            # precalculate the forward pass
            op.InitTopLayers(1)
            op.meta['dep_history'] = DepositionHistory(tsec)
            self.cache['ProcessOnLineTRScan'] = op
            # clean up memory
            th = gc.get_threshold()
            gc.set_threshold(0,0,0)
            gc.collect()
            gc.set_threshold(*th)
        
        def residuals(D: npt.NDArray[np.float64]):
            if self._stop_immidiately:
                return np.zeros((len(wavelength), 1), dtype=np.float64)
            # relu thickness
            D[0] = max(D[0], 0.1)
            op.thicknesses[-1] = D[0]
            # update for the last layer changes only
            # op.ForwardBackwardLastD()
            op.UpdateTopLayers()
            return (op.GetData(self.config.rt_data) - self.scaleFactor*spectrum)
        
        def jacobian(D: npt.NDArray[np.float64]):
            res = np.empty((len(wavelength), 1), dtype=np.float64)
            if self._stop_immidiately:
                return res
            res[:,0] = op.GetGrad(self.config.rt_data, nLayer = -1, ix = -1)
            return res

        # initial thockness estimate
        minThickness = self.GetDepositionRate(lastLayer-1) * tsec

        # TODO: ask AVT about the initial guess if the thickness is high
        D_init = op.meta.setdefault('D_init', np.array([minThickness], dtype=np.float64))
        # update the initial guess based on dep rate and time elapsed
        if op.meta.get('quality', PredQuality.BAD) != PredQuality.BAD:
            dt = tsec - op.meta['tsec']
            # SK: this seems to worsen things
            D_init[0] += op.meta['v_dep'] * dt
            
        # avoid zero thickness
        D_init[0] = max(D_init[0], minThickness)

        t = -time.time()
        res = least_squares(
            fun = residuals, 
            x0 = D_init,
            jac = jacobian,
            method = 'lm',  
            gtol = 1e-10,
            ftol = 1e-10, #np.finfo(np.float64).eps,
            xtol = 1e-10, #np.finfo(np.float64).eps,
            max_nfev = 40,
            verbose = 0
        )
        t += time.time()

        # update the initial guess for the next call
        D_init[:] = res.x
        # update the deposition history
        op.meta['dep_history'].AddObservation(tsec, res.x[0])
        # calculate the deposition rate
        v_dep, quality, d_currGeo = op.meta['dep_history'].GetDepositionRate()
        d_currGeo = min(d_currGeo, res.x[0])
        # save velocity and quality to use in the next call
        op.meta['v_dep'] = v_dep
        op.meta['quality'] = quality
        op.meta['tsec'] = tsec
        op.meta['f_av'] = 100*100*np.mean(np.power(res['fun'], 2)) # ** 0.5
        op.meta['thickness'] = max(op.meta.get('thickness', 0), d_currGeo)
        # make determined thickness monotonically increasing
        d_currGeo = op.meta['thickness']
        # calculate time to switch
        dt_switch = ((design_thicknesses[lastLayer-1] - d_currGeo) / v_dep) if v_dep > 0 else 100.
        d_currQWOT = 0
        # convert units
        d_currGeo = self.config.l_units.fromdef(d_currGeo)
        v_dep = self.config.l_units.fromdef(v_dep)

        if verbose:
            self.logger.info("ProcessOnLineTRScan", {
                'exec_time': t,
                'd_currGeo': d_currGeo,
                'res.x': res.x,
                'd_currQWOT': d_currQWOT,
                'v_dep': v_dep,
                'quality': quality,
                'dt_switch': dt_switch,
                'minThickness': minThickness,
            })

        return self.ProcessOnLineTRScanReturn(
            d_currGeo = d_currGeo, 
            d_currQWOT = d_currQWOT,
            v_dep = v_dep,
            quality = quality,
            dt_switch = dt_switch,
            f_avg = op.meta['f_av'],
        )
        

    # layer index is 1-based
    def AddMeasurement(self, nLayer: int, scan: BroadBandScan):
        if self.design is None:
            raise ValueError("A theoretical design must be loaded before calling 'AddMeasurement'.")
        if nLayer < 1 or nLayer > self.design.nLayers:
            raise ValueError("The 'nLayer' parameter must be between 1 and the number of layers.")

        chipName = self.design.layers[nLayer-1].chipName
        chip = self.GetChip(chipName)
        chip.AddMeasurement(scan, nLayer-1)
        self.logger.info("AddMeasurement", {
            'chipName': chipName,
            'nLayer': nLayer,
            'scan.wavelength': scan.wavelength,
            'scan.values': scan.values,
        })

    class CharacterizationResult(NamedTuple):
        phThicknesses: npt.NDArray[np.float64]
        qwotThicknesses: npt.NDArray[np.float64]
        method: CalculationMode
        f_avg: np.float64
        @property
        def nLayers(self):
            return len(self.phThicknesses)
        def __str__(self):
            s = [
                f"phThicknesses={str(self.phThicknesses)}",
                f"qwotThicknesses={str(self.qwotThicknesses)}"
            ]
            return f"({', '.join(s)})"
        def __repr__(self):
            return self.__str__()


    def SolveOnLine(self, nLayer: int) -> CharacterizationResult:
        if self.design is None:
            raise ValueError("A theoretical design must be loaded before calling 'SolveOnLine'.")
        if nLayer < 1 or nLayer > self.design.nLayers:
            raise ValueError("The 'nLayer' parameter must be between 1 and the number of layers.")

        nTopLayers = max(self.config.calcMode.depth, int(nLayer*0.3))
        nStartLayer = max(0, nLayer - nTopLayers)
        D_init = np.empty(nLayer - nStartLayer, dtype=np.float64)

        for n in range(nStartLayer, nLayer):
            D_init[n - nStartLayer] = self.design.layers[n].thickness * 0.5 + 0.5 * self.design.layers[n].theoreticalThickness

        self.logger.info("Thicknesses before optimization", {
            'nLayer': nLayer,
            'nStartLayer': nStartLayer,
            'D_init': D_init,
        })
        # should we do characterization of the whole stack or just the last chip?
        chip = self.GetChip(self.design.layers[nLayer - 1].chipName)
        chip.Reset()
        for n in range(nLayer):
            chip.AddLayer(self.design.layers[n], n)
        chip.UpdateOptiProps(
            pol = self.pol,
            incidenceAngle = self.incidenceAngle,
            na = self.na,
            rt_units = self.config.rt_units,
            backSideMatters = self.onlineBackside,
            backSideThickness = self.onlineBacksideThickness,
        )
#        # apply initial thicknesses
#        for ixChip, ixGlobal in chip.local2global.items():
#            if ixGlobal >= nStartLayer:
#                chip.op.thicknesses[ixChip] = D_init[ixGlobal - nStartLayer]

        global t_triag
        t_triag = 0

        def merit(D: npt.NDArray[np.float64]) -> np.float64:
            if self._stop_immidiately:
                return 0
            global t_triag
            # relu thickness
            D[D < 3] = 3
            chip.op.thicknesses[nStartLayer:] = D
            # print ('merit', op.thicknesses)
            if hasattr(merit, 'initialized') and nStartLayer > 0:
                # calculate derivatives only for the the last nTopLayers
                chip.op.UpdateTopLayers()
            else:
                merit.initialized = True
                # calculate optical properties of all preceeding layers
                chip.op.InitTopLayers(nTopLayers)
                chip.op.UpdateTopLayers()
            # calculate loss function
            t_triag -= time.time()
            nMeasurements = 0
            scale = self.scaleFactor
            loss = 0
            for l, m in chip.measurements:
                if l >= nStartLayer and l < nLayer:
                    nMeasurements += 1
                    diff = chip.op.GetRawData(rt_data = m.rt_data, nLayer = l) - scale * m.values
                    loss += np.mean(diff * diff)
            loss /= nMeasurements
            t_triag += time.time()
            return loss
        
        def gradient(D: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
            global t_triag
            grad = np.zeros_like(D)
            if self._stop_immidiately:
                return grad
            scale = self.scaleFactor
            t_triag -= time.time()
            nMeasurements = 0
            for l, m in chip.measurements:
                if l >= nStartLayer and l < nLayer:
                    nMeasurements += 1
                    diff = chip.op.GetRawData(rt_data = m.rt_data, nLayer = l) - scale * m.values
                    l_grad = chip.op.GetRawGrad(
                        rt_data = m.rt_data, 
                        nLayer = l,
                        ix = slice(None),
                        # ix = slice(nStartLayer, None)
                    )
                    #l_grad = l_grad[nStartLayer:]
                    grad[:(l-nStartLayer+1)] += 2 * np.mean(diff * l_grad, axis=1)
            grad /= nMeasurements
            t_triag += time.time()
            return grad

        t = -time.time()
        res = minimize(merit, D_init, 
                    method='L-BFGS-B',  
                    options={
                        'maxiter': 150,
                        'ftol': 4e-18,
                        'gtol': 4e-14,
                    },
                    jac = gradient,
                    tol = np.finfo(np.float64).eps
        )
        t += time.time()

        # write obtained thicknesses back to the design
        for n in range(nStartLayer, nLayer):
            self.design.layers[n].thickness = res.x[n - nStartLayer]

        self.logger.info("Optimization finished.", {
            'nLayer': nLayer,
            't_triag': t_triag,
            't_total': t,
            'nfev': res.nfev,
            'nStartLayer': nStartLayer,
            'success': res.success,
        })

        # clean up memory
        self.cache = {}
        chip.op = None
        del merit
        del gradient
        gc_thresh = gc.get_threshold()
        gc.set_threshold(0,0,0)
        gc.collect()
        gc.set_threshold(*gc_thresh)

        return self.CharacterizationResult(
            phThicknesses = self.design.ph_thicknesses,
            qwotThicknesses = np.zeros(nLayer, dtype=np.float64),
            method = self.config.calcMode,
            f_avg = np.mean(np.abs(res['fun'])),
        )


    class ReoptimizationResult(NamedTuple):
        deltaMerit: np.float64
        nextThickness: np.float64
        nextQWOT: np.float64
        def __str__(self):
            return "dM=%.4f,nextTh=%.3f,nextQWOT=%.3f" % (self.deltaMerit, self.nextThickness, self.nextQWOT)
        def __repr__(self):
            return str(self)

    def SolveReopt(self, doneLayers: int) -> ReoptimizationResult:
        if self.design is None:
            raise ValueError("A theoretical design must be loaded before calling 'SolveReopt'.")
        if doneLayers >= self.design.nLayers:
            raise ValueError("All layers are already done.")
        if self.target is None:
            raise ValueError("A target must be loaded before calling 'SolveReopt'.")
        
        D_init = np.empty(self.design.nLayers - doneLayers, dtype=np.float64)
        for n in range(len(D_init)):
            D_init[n] = self.design.layers[n+doneLayers].thickness
        ops = []
        thicknesses = self.design.ph_thicknesses
        
        for page in self.target.pages:
            if page.spechar.rt_data is None:
                continue
            if page.spechar.pol is None:
                continue
            op = OptiProps(
                  thicknesses = thicknesses
                , wavelength = page.wavelength
                , refractiveIndices = self.design.GetRefractiveIndices(page.wavelength)
                , substrateRefractiveIndex = self.GetSubstrateRI(page.wavelength)
                , pol = page.spechar.pol
                , incidenceAngle = page.incidenceAngle
                , na = RefractiveIndex.vacuum
                , rt_units = self.config.rt_units
                , backSideMatters = self.reoptBackside
                , backSideThickness = self.reoptBacksideThickness
            )
            op.meta['page'] = page
            ops.append(op)
        if len(ops) == 0:
            raise ValueError("No valid target pages were specified.")
        
        def merit(D: npt.NDArray[np.float64]) -> np.float64:
            # relu thickness
            D[D < 1] = 1.0
            # apply thicknesses
            thicknesses[doneLayers:] = D[:] 
            # calculate loss function
            loss = 0.0
            for op in ops:
                op.ForwardBackward()
                loss += np.mean((op.GetData(op.meta['page'].spechar.rt_data) - op.meta['page'].values)**2)
            return loss / len(ops)
        
        loss = lambda D: merit(D) ** 0.5
        
        def gradient(D: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
            grad = np.zeros_like(D)
            for op in ops:
                diff = op.GetData(op.meta['page'].spechar.rt_data) - op.meta['page'].values
                grad += 2 * np.mean(op.GetGrad(op.meta['page'].spechar.rt_data) * diff, axis=1)[doneLayers:]
            return grad / len(ops)
        
        t = -time.time()
        res = minimize(
            merit, D_init
            , method='L-BFGS-B'
            , options = {
                'maxiter': 600
                , 'ftol': 1e-10
                , 'gtol': 1e-10
            }
            , jac = gradient
            , tol = 1e-10
        )
        t += time.time()
        # write obtained thicknesses to the design
        for n in range(len(res.x)):
            self.design.layers[n+doneLayers].reoptThickness = res.x[n]

        return self.ReoptimizationResult(
              deltaMerit = loss(D_init) - loss(res.x)
            , nextThickness = res.x[0]
            , nextQWOT = res.x[0] / self.design.GetQWOT()[doneLayers]
        )
    
    def IsNewDesignRecommended(self) -> bool:
        # TODO: implement
        return True


    def AcceptReoptimizedDesign(self, doneLayers: int):
        if doneLayers >= self.design.nLayers:
            raise ValueError("Invalid number of done layers.")
        for n in range(doneLayers, self.design.nLayers):
            self.design.layers[n].thickness = self.design.layers[n].reoptThickness

        self.logger.info("Accepting reoptimized design.", {
              'doneLayers': doneLayers
            , 'newThicknesses': self.design.ph_thicknesses
        })


    def ReplaceThicknesses(self, layerStart: int, layerEnd: int, thicknesses: npt.NDArray[np.float64]):
        if layerStart < 0 or layerStart >= self.design.nLayers:
            raise ValueError("Invalid layerStart.")
        if layerEnd < 0 or layerEnd >= self.design.nLayers:
            raise ValueError("Invalid layerEnd.")

        for i in range(layerStart, layerEnd+1):
            self.design.layers[i].thickness = thicknesses[i]
            self.design.layers[i].theoreticalThickness = thicknesses[i]
