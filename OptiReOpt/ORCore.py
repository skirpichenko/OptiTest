from ORConstants import *
from typing import *
from scipy.interpolate import interp1d
from scipy.interpolate import CubicSpline
import numpy as np
from OREngine import *
import numpy.typing as npt
import re

##############################################################################
# Complex refractive index
class RefractiveIndex(object):
    vacuum = 1.0 + 0.0j
    air = 1.000293 + 0.0j
    def __init__(self
            , nType: MaterialNType
            , kType: MaterialKType
            , nInterMethod: InterMethod = InterMethod.SPLINE
            , kInterMethod: InterMethod = InterMethod.SPLINE
            , wavelength: Optional[npt.NDArray[np.float64]] = None
            , n: Optional[npt.NDArray[np.float64]] = None
            , k: Optional[npt.NDArray[np.float64]] = None
            , nFormulaCoef: Optional[npt.NDArray[np.float64]] = None
            , kFormulaCoef: Optional[npt.NDArray[np.float64]] = None
            , name: Optional[str] = None
            , comment: Optional[str] = None
        ):
        self.nType = nType # refractive formula or TABLE
        self.kType = kType # extinction formula or TABLE
        self.nInterMethod = nInterMethod  # linear or cubic
        self.kInterMethod = kInterMethod  # linear or cubic
        self.wavelength = wavelength
        self.n = n
        self.k = k
        self.nFormulaCoef = nFormulaCoef
        self.kFormulaCoef = kFormulaCoef
        self.name = name
        self.comment = comment

    def ApplyFormula(self
            , nType: MaterialNType, nFormulaCoef: Optional[npt.NDArray[np.float64]]
            , kType: MaterialKType, kFormulaCoef: Optional[npt.NDArray[np.float64]]
        ):
        if nType != MaterialNType.TABLE:
            if nFormulaCoef is None:
                raise Exception("nFormulaCoef must be not None for nType != TABLE")
            self.nType = nType
            self.nFormulaCoef = nFormulaCoef
            self.n = None
        if kType != MaterialKType.TABLE:
            if kFormulaCoef is None:
                raise Exception("kFormulaCoef must be not None for kType != TABLE")
            self.kType = kType
            self.kFormulaCoef = kFormulaCoef
            self.k = None

    def __str__(self):
        return f"{self.name} nType={self.nType.name},kType={self.kType.name}"
    def __repr__(self):
        return str(self)
        
    def get_n(self, lam: npt.NDArray[np.float64]):
        if self.nType == MaterialNType.TABLE:
            return self.n[0] * np.ones_like(lam) if len(self.n) == 1 else \
                self.__interpolate(self.wavelength, self.n, lam, method = self.nInterMethod)
        elif self.nType == MaterialNType.SELLMEIER1 and len(self.nFormulaCoef) == 3:
            lam = LightUnits(LightUnits.MKM).fromdef(lam)
            A = self.nFormulaCoef
            lam2 = lam ** 2
            n = A[0] + A[1] * lam2 / (lam2 - A[2])
            return n ** 0.5   
        elif self.nType == MaterialNType.SELLMEIER2 and len(self.nFormulaCoef) == 5:
            lam = LightUnits(LightUnits.MKM).fromdef(lam)
            A = self.nFormulaCoef
            lam2 = lam ** 2
            n = A[0] + A[1] * lam2 / (lam2 - A[2])
            n += A[3] * lam2 / (lam2 - A[4])
            return n ** 0.5    
        elif self.nType == MaterialNType.SELLMEIER2P and len(self.nFormulaCoef) == 4:
            lam = LightUnits(LightUnits.MKM).fromdef(lam)
            A = self.nFormulaCoef
            lam2 = lam ** 2
            n = A[0] + A[1] * lam2 / (lam2 - A[2])
            n += A[3] * lam2
            return n ** 0.5
        elif self.nType == MaterialNType.SELLMEIER3 and len(self.nFormulaCoef) == 7:
            # TODO: check why there is difference with old dll
            lam = LightUnits(LightUnits.MKM).fromdef(lam)
            A = self.nFormulaCoef
            lam2 = lam ** 2
            n = A[0] + A[1] * lam2 / (lam2 - A[2])
            n += A[3] * lam2 / (lam2 - A[4])
            n += A[5] * lam2 / (lam2 - A[6])
            return n ** 0.5
        elif self.nType == MaterialNType.CAUCHY and len(self.nFormulaCoef) == 3:
            lam = LightUnits(LightUnits.MKM).fromdef(lam)
            A = self.nFormulaCoef
            lam2 = lam ** 2
            lam4 = lam ** 4
            n = A[0] + A[1] / lam2 + A[2] / lam4
            return n        
        elif self.nType == MaterialNType.HARTMANN and len(self.nFormulaCoef) == 3:
            lam = LightUnits(LightUnits.MKM).fromdef(lam)
            A = self.nFormulaCoef
            n = A[0] + A[1] / (lam - A[2])
            return n               
        elif self.nType == MaterialNType.SCHOTTGLAS and len(self.nFormulaCoef) == 7:
            lam = LightUnits(LightUnits.MKM).fromdef(lam)
            A = self.nFormulaCoef
            lam2 = lam ** 2
            lam4 = lam ** 4
            lam6 = lam ** 6      
            lam8 = lam ** 8  
            #n = A[0] + A[1] * lam2 + A[2] / lam2 + A[3] / lam4 + A[4] / lam6 + A[5] / lam8 + A[6] * lam4
            n = A[0] + A[1] * lam2 + A[2] / lam2 + A[3] / lam4 + A[4] / lam6 + A[5] / lam8 + A[6] / lam4 # modified to fit old dll
            return n ** 0.5
        elif self.nType == MaterialNType.HARTMANN2 and len(self.nFormulaCoef) == 3:
            lam = LightUnits(LightUnits.MKM).fromdef(lam)
            A = self.nFormulaCoef
            # TODO: correction of formula is needed to have same results as in old DLL
            n = A[0] + A[1] / (lam - A[2])**2
            return n               
        elif self.nType == MaterialNType.NDRUDE and len(self.nFormulaCoef) == 3:
            lam = LightUnits(LightUnits.MKM).fromdef(lam)
            # n**2-k**2 = A0-A1*A2**2*lam**2/(lam**2+A2**2)
            # 2*n*k = A1*A2*lam**3/(lam**2+A2**2)
            A = self.nFormulaCoef
            X = A[0]-A[1]*A[2]**2*lam**2/(lam**2+A[2]**2)
            Y = A[1]*A[2]*lam**3/(lam**2+A[2]**2)
            n_squared = (X + np.sqrt(X**2 + Y**2)) / 2
            n = np.sqrt(n_squared)
            return n
        else:
            raise NotImplementedError
            
    def get_k(self, lam: npt.NDArray[np.float64]):
        ret_k = None
        if self.kType == MaterialKType.TABLE:
            ret_k = self.k[0] * np.ones_like(lam) if len(self.k) == 1 else \
                self.__interpolate(self.wavelength, self.k, lam, method = self.nInterMethod)
        elif self.kType == MaterialKType.NONABS:
            lam = LightUnits(LightUnits.MKM).fromdef(lam)
            ret_k = np.zeros_like(lam)
        elif self.kType == MaterialKType.NONDISP and len(self.kFormulaCoef) == 1:
            lam = LightUnits(LightUnits.MKM).fromdef(lam)
            B = self.kFormulaCoef
            ret_k = np.ones_like(lam) * B[0]
        elif self.kType == MaterialKType.KSELLMEIER and len(self.kFormulaCoef) == 3:
            B = self.kFormulaCoef
            n = self.get_n(lam)
            lam = LightUnits(LightUnits.MKM).fromdef(lam)
            lam3 = lam ** 3
            k = n * ( B[0] * lam + B[1] / lam + B[2] / lam3)
            ret_k = k ** (-1)
        elif self.kType == MaterialKType.EXPONENTIAL and len(self.kFormulaCoef) == 3:
            lam = LightUnits(LightUnits.MKM).fromdef(lam)
            B = self.kFormulaCoef
            ret_k = B[0] * np.exp(B[1] / lam + B[2] * lam)
        elif self.kType == MaterialKType.POLYNOMIAL and len(self.kFormulaCoef) == 4:
            lam = LightUnits(LightUnits.MKM).fromdef(lam)
            B = self.kFormulaCoef
            lam2 = lam ** 2
            lam3 = lam ** 3
            ret_k = B[0] + B[1] * lam + B[2] * lam2 + B[3] * lam3  
        elif self.kType == MaterialKType.KDRUDE and len(self.nFormulaCoef) == 3:
            lam = LightUnits(LightUnits.MKM).fromdef(lam)
            # n**2-k**2 = A0-A1*A2**2*lam**2/(lam**2+A2**2)
            # 2*n*k = A1*A2*lam**3/(lam**2+A2**2)
            A = self.nFormulaCoef
            X = A[0]-A[1]*A[2]**2*lam**2/(lam**2+A[2]**2)
            Y = A[1]*A[2]*lam**3/(lam**2+A[2]**2)
            n_squared = (X + np.sqrt(X**2 + Y**2)) / 2
            n = np.sqrt(n_squared)
            k = Y / (2 * np.sqrt(n_squared))
            ret_k = k
        else:
            raise NotImplementedError
        # NOTE: the imaginary part is negative in all calculations
        return -ret_k
            
    def __interpolate(self, x: npt.NDArray[np.float64], 
                            y: npt.NDArray[np.float64], 
                            lam: npt.NDArray[np.float64], 
                            method: InterMethod = InterMethod.DEFAULT):

        if method == InterMethod.LINEAR:
            f = interp1d(x, y, kind = 'linear', copy = False,
                        assume_sorted = True, fill_value = "extrapolate")
        elif method == InterMethod.SPLINE:
            f = CubicSpline(x, y, bc_type='natural', extrapolate=True)
        else:
            raise NotImplementedError
        return f(lam)

    @classmethod
    def FromFile(cls, fname: str):
        # TODO: compare with OptiLayer outputs
        wavelength = []
        N = []
        K = []
        name = ''
        comment = ''
        fileLightUnit = LightUnits.DEFAULT
        kRegexFormula = re.compile(
            r"(non-abs|non-disp|sellmeier|polynomial|exponential|drude)")
        nRegexFormula = re.compile(
            r"(sellmeier 1|sellmeier 2'|sellmeier 2|sellmeier 3|cauchy|hartmann 2|hartmann|schott glas|drude)")
        nCoefRegex = r"A\d+\s*=\s*([-+]?\d*\.?\d+(?:[Ee]?[-+]?\d+)?)"
        kCoefRegex = r"B\d+\s*=\s*([-+]?\d*\.?\d+(?:[Ee]?[-+]?\d+)?)"
        lUnitRegex = r"units: l:\s*(.*?)\s*,"
        nFormulaCoef = []
        kFormulaCoef = [] 
        with open(fname, 'r') as f:
            # skip header
            line = f.readline()
            while line and '#'.join(line.lower().split()) != 'wavelength#n#k':
                # layer material file
                if line.lower().startswith('layer material file:'):
                    name = line.split(':')[1].strip()
                # substrate material file
                if line.lower().startswith('substrate/incident/exit medium file:'):
                    name = line.split(':')[1].strip()
                if line.lower().startswith('comment:'):
                    comment = line.split(':')[1].strip()

                #parsing nType and interpolatio method
                if line.strip().lower().startswith('n given by'):
                    matchInterp = re.search(r'\((.*?)\)', line.lower())
                    if matchInterp:
                        substring = matchInterp.group(1)
                        str = substring.replace(
                            'interpolation', '').strip()
                        try:
                            nInterMethod = getattr(InterMethod, str.upper())
                        except AttributeError:
                            raise ValueError(f"No such interpolation method: {str.upper()}")
                    else:
                        nInterMethod = InterMethod.DEFAULT

                    nMatch = nRegexFormula.search(line.lower())
                    if nMatch:
                        substring = nMatch.group(1)
                        str = substring.replace(
                            "'", 'p').replace(" ", "").replace("-", "").strip()
                        if 'drude' in str:
                            nType = MaterialNType.NDRUDE
                        else:
                            try:
                                nType = getattr(MaterialNType, str.upper()) 
                            except AttributeError:
                                raise ValueError(f"No such formula type: {str.upper()}")
                    else:
                        nType = MaterialNType.DEFAULT

                if line.strip().lower().startswith('k given by'):
                    matchInterp = re.search(r'\((.*?)\)', line.lower())
                    if matchInterp:
                        substring = matchInterp.group(1)
                        str = substring.replace(
                            'interpolation', '').strip()
                        try:
                            kInterMethod = getattr(InterMethod, str.upper())
                        except AttributeError:
                            raise ValueError(f"No such interpolation method: {str.upper()}")
                    else:
                        kInterMethod = InterMethod.DEFAULT

                    kMatch = kRegexFormula.search(line.lower())
                    if kMatch:
                        substring = kMatch.group(1)
                        str = substring.replace(
                            "'", 'p').replace(" ", "").replace("-", "").strip()
                        if 'drude' in str:
                            kType = MaterialKType.KDRUDE
                        elif 'sellmeier' in str:
                            kType = MaterialKType.KSELLMEIER                        
                        else:
                            try:
                                kType = getattr(MaterialKType, str.upper()) 
                            except AttributeError:
                                raise ValueError(f"No such formula type: {str.upper()}")
                    else:
                        kType = MaterialKType.DEFAULT

                # parse coefficients
                nMatch = re.search(nCoefRegex, line)
                if nMatch:
                    nFormulaCoef.append(float(nMatch.group(1)))

                kMatch = re.search(kCoefRegex, line)
                if kMatch:
                    kFormulaCoef.append(float(kMatch.group(1)))

                # parse LUnits from file
                lUnitMatch = re.search(lUnitRegex, line.lower().strip())
                if lUnitMatch:
                    substring = lUnitMatch.group(1)
                    if substring == 'a':
                        fileLightUnit = LightUnits.ANGS
                    elif substring == 'um':
                        fileLightUnit = LightUnits.MKM
                    else:
                        try:
                            fileLightUnit = getattr(LightUnits, substring.upper()) 
                        except AttributeError:
                            raise ValueError(f"No such light unit type: {substring.upper()}")                                 

                line = f.readline()
            line = f.readline()
            while line:
                line = line.split()
                wavelength.append(LightUnits(fileLightUnit).todef(float(line[0])))
                N.append(float(line[1]))
                K.append(float(line[2]))   
                line = f.readline()       
        return RefractiveIndex(
            nType = nType,
            kType = kType,
            nInterMethod = nInterMethod,
            kInterMethod = kInterMethod,
            wavelength = np.array(wavelength, dtype=np.float64),
            n = np.array(N, dtype=np.float64),
            k = np.array(K, dtype=np.float64),
            nFormulaCoef = np.array(nFormulaCoef, dtype=np.float64),
            kFormulaCoef = np.array(kFormulaCoef, dtype=np.float64),
            name = name,
            comment = comment
        )
    
    @classmethod
    def FromXmlDict(cls, d: Dict[str, Any], name: Optional[str] = None):
        if 'row' not in d:
            raise Exception('No row data in XML material definition')
        row = d['row']
        if isinstance(row, dict):
            row = [row]
        wavelength = np.empty(len(row), dtype=np.float64)
        N = np.empty(len(row), dtype=np.float64)
        K = np.empty(len(row), dtype=np.float64)
        for i, r in enumerate(row):
            wavelength[i] = float(r['@wavelength-nm'])
            N[i] = float(r['@n'])
            K[i] = float(r['@k'])
        return RefractiveIndex(
            nType = MaterialNType.TABLE,
            kType = MaterialKType.TABLE,
            wavelength = wavelength,
            n = N,
            k = K,
            name = name
        )
    
    def about(self)->str:
        text = ''
        # refractive data information
        if self.nType!=MaterialNType.TABLE:
            text += f'Given as {self.nType} formula \n'
            text += 'Coefficients:\n  '
            coef_list = ['  {:0.5e}'.format(num) for num in self.nFormulaCoef]
            text += ''.join(coef_list)
            text +='\n'
        # extinction data information
        if self.kType!=MaterialKType.TABLE:
            text += f'Given as {self.kType} formula \n'
            text += 'Coefficients:\n  '
            coef_list = ['  {:0.5e}'.format(num) for num in self.kFormulaCoef]
            text += ''.join(coef_list)
            text +='\n'   
        if self.nType==MaterialNType.TABLE or self.kType==MaterialKType.TABLE:
            text += f'Dispersion table, {len(self.wavelength)} points\n'
            text += f'  Wavelength      Re(n)       Im(n)     Lin\n'            
            values_list = ['  {:10.5}  {:0.5e}  {:0.5e} \n'.format(w, n, k) for w,n,k in zip(self.wavelength, self.n, self.k)]
            text += ''.join(values_list)
        return text  

    def to_dict(self):
        excluded_variables = '_'  # Specify variables to exclude
        data = {}
        for key, value in self.__dict__.items():
            if excluded_variables not in key:
                if isinstance(value, np.ndarray):
                    data[key] = value.tolist()  # Convert NumPy array to list
                else:
                    data[key] = value
        return data

    @classmethod
    def from_dict(cls, data):
        converted_data = {}
        for key, value in data.items():
            if isinstance(value, list):
                converted_data[key] = np.array(value)  # Convert list to NumPy array
            else:
                converted_data[key] = value
        return cls(
            nType = MaterialNType(converted_data['nType']),
            kType = MaterialKType(converted_data['kType']),
            nInterMethod = InterMethod(converted_data['nInterMethod']),
            kInterMethod = InterMethod(converted_data['kInterMethod']),
            wavelength = np.array(converted_data['wavelength'], dtype=np.float64) if 'wavelength' in converted_data else None,
            n = np.array(converted_data['n'], dtype=np.float64) if 'n' in converted_data else None,
            k = np.array(converted_data['k'], dtype=np.float64) if 'k' in converted_data else None,
            nFormulaCoef = np.array(converted_data['nFormulaCoef'], dtype=np.float64) if 'nFormulaCoef' in converted_data else None,
            kFormulaCoef = np.array(converted_data['kFormulaCoef'], dtype=np.float64) if 'kFormulaCoef' in converted_data else None,
            name = converted_data.get('name'),
            comment = converted_data.get('comment'),
        )

##############################################################################
class Material(object):
    def __init__(self
            , abbr: str
            , vacuum: Optional[RefractiveIndex] = None
            , air: Optional[RefractiveIndex] = None
            , comment: str = ''
        ):
        self.abbr = abbr
        self.vacuum = vacuum
        self.air = air
        self.comment = comment

    @property
    def riAir(self) -> RefractiveIndex:
        return self.air if self.air is not None else self.vacuum
    @property
    def riVacuum(self) -> RefractiveIndex:
        return self.vacuum if self.vacuum is not None else self.air
    @property
    def airName(self) -> str:
        return self.air.name if self.air is not None else \
            ('' if self.vacuum is None else self.vacuum.name)
    @property
    def vacuumName(self) -> str:
        return self.vacuum.name if self.vacuum is not None else \
            ('' if self.air is None else self.air.name)
    @property
    def airComment(self) -> str:
        return self.air.comment if self.air is not None else \
            ('' if self.vacuum is None else self.vacuum.comment)
    @property
    def vacuumComment(self) -> str:
        return self.vacuum.comment if self.vacuum is not None else \
            ('' if self.air is None else self.air.comment)

    def GetRI(self, inVacuum: bool) -> RefractiveIndex:
        return self.vacuum if inVacuum else self.air
        
    def GetRefrativeIndex(self, 
            wavelength: npt.NDArray[np.float64],
            vacuum: bool = True
        ) -> npt.NDArray[np.complex128]:
        # try to get the refractive index for the given wavelength
        if vacuum:
            envir = self.air if self.vacuum is None else self.vacuum
        else:
            envir = self.vacuum if self.air is None else self.air
        if envir is None:
            raise Exception(f'No refractive index data for {"vacuum" if vacuum else "air"} in material {self.name}')
        return envir.get_n(wavelength) + 1j * envir.get_k(wavelength)

    def __str__(self) -> str:
        return f'Material(abbr={self.abbr}, comment={self.comment}, vacuum={self.vacuum}, air={self.air})'
    def __repr__(self) -> str:
        return str(self)

    def about(self) -> str:
        return self.vacuum.about() if self.vacuum is not None else \
            ('' if self.air is None else self.air.about())

    @classmethod
    def FromFile(cls, fname: str, abbr: str = '', isVacuum: bool = True):
        ri = RefractiveIndex.FromFile(fname)
        return Material(
            abbr = abbr,
            vacuum = ri if isVacuum else None,
            air = ri if not isVacuum else None
        )

    @classmethod
    def FromXmlDict(cls, d: Dict[str, Any], abbr: Optional[str] = None, isVacuum: bool = True):
        if abbr is None and 'name' not in d:
            raise Exception('Material name is not specified')
        abbr = abbr if abbr is not None else d['name']
        if 'refractive-index-table' not in d:
            raise Exception('Material refractive index table is not specified')
        else:
            ri = RefractiveIndex.FromXmlDict(d['refractive-index-table'], d['name'])
        return cls(
            abbr = abbr,
            comment = d.get('comment', ''),
            # handle air and vacuum based on isVacuum accoring to 'incident-medium' in XML
            air = ri if not isVacuum else None,
            vacuum = ri if isVacuum else None,
        )
    
    def to_dict(self):
        excluded_variables = '_'  # Specify variables to exclude
        data = {}
        for key, value in self.__dict__.items():
            if excluded_variables not in key:
                if isinstance(value, RefractiveIndex):
                    data[key] = value.to_dict()  # Convert RefractiveIndex to dict
                elif isinstance(value, Enum):
                    data[key] = str(value)
                else:
                    data[key] = value
        return data
    
    @classmethod
    def from_dict(cls, data):
        converted_data = {}
        for key, value in data.items():
            if key in ['vacuum', 'air'] and value is not None:
                converted_data[key] = RefractiveIndex.from_dict(value)  # Convert dict to RefractiveIndex
            if key in ['abbr', 'comment']:
                converted_data[key] = value
        return cls(**converted_data)
    
##############################################################################
class Layer(object):
    def __init__(self
            , material: Material
            , thickness: np.float64
        ):
        self.material = material
        self.thickness = thickness # current thickness of the layer
        self.theoreticalThickness = thickness # thickness of the layer by design
        self.reoptThickness = thickness # thickness of the layer after re-optimization
        self.chipName: str = WitnessChip.DEFAULT_NAME
        self.corrFactor = 1.0 # ratio of the layer thickness in air to the layer thickness in vacuum
        # Degree of inhomogeneity must be expressed in relative units (not in percentage). 
        # Degree of inhomogeneity is defined as a (n_1-n_0)/n_ave, where n_1 is the layer refractive
        # index at the ambient boundary, n_0 is the layer refractive index at the substrate boundary,
        # n_ave is average value of layer refractive index. Typically degree of inhomogeneity 
        # is not significantly dependent on layer thickness. For this reason OptiReOpt considers 
        # degree of inhomogeneity as a value characterizing layer material.
        self.delta = 0.0 # degree of inhomogeneity
        
    def __str__(self):
        return f"{self.material.abbr} ph:{self.thickness}[{self.theoreticalThickness}]"
    def __repr__(self):
        return str(self)

    @property
    def abbr(self) -> str:
        return self.material.abbr
    
    def GetQWOT(self
            , refW: np.float64  # reference wavelength
            , angle: np.float64 # angle of incidence
            , ambient_n: np.float64 # refractive index of ambient medium
            , isVacuum: bool = True # which refractive index to use
        ) -> np.float64:
        raise NotImplementedError()
    
    def to_dict(self):
        excluded_variables = '_'  # Specify variables to exclude
        data = {}
        for key, value in self.__dict__.items():
            if excluded_variables not in key:
                if isinstance(value, Material):
                    data[key] = value.to_dict()  # Convert Material to dict
                else:
                    data[key] = value
        return data
    
    @classmethod
    def from_dict(cls, data):
        converted_data = {}
        for key, value in data.items():
            if key in ['material'] and value is not None:
                converted_data[key] = Material.from_dict(value)  # Convert dict to RefractiveIndex
            if key in ['thickness']:
                converted_data[key] = value
        return cls(**converted_data)

##############################################################################
# When light passes through a thin film coating at a non-zero incident angle, 
# it experiences both physical thickness and optical thickness. The physical thickness is 
# the actual thickness of the film, while the optical thickness takes into account 
# the refractive index of the film material.
# The relationship between physical thickness (d) and optical thickness (Δ) is given by the formula:
# Δ = d × n
# where n is the refractive index of the film material.
#
# When the incident angle is non-zero, the effective optical thickness of the film is given by:
# Δ_eff = Δ/cos(θ)
# where θ is the angle of incidence.
#
# The effective optical thickness takes into account the change in path length that light experiences 
# when it enters the film at an angle. This formula is commonly used in the design and analysis 
# of thin film coatings in applications such as anti-reflection coatings and optical filters.

class Design(object):
    def __init__(self
            , comment: str = ''
            , matchAngle: Optional[np.float64] = None
            , controlW: Optional[np.float64] = None
            , matchMedium: Optional[np.float64] = None
            , layers: Optional[List[Layer]] = None
        ):
        self.comment = comment
        # match angle for calculations connecting QWOT and physical thickness
        # match refractive index of incidence medium. This value is also
        # using for calculations connecting QWOT and physical thickness.
        # It is significant only if MatchAngle > 0.0.
        self.matchAngle = np.float64(0 if matchAngle is None else matchAngle)
        self.matchMedium = np.float64(1 if matchMedium is None else matchMedium)
        # Control wavelength (in nm or mkm, depending on configuration)
        self.controlW = np.float64(600 if controlW is None else controlW)
        # content of the design 
        self.layers = [] if layers is None else layers 

    @property
    def isVacuum(self) -> bool:
        return self.matchMedium == 1.0
        
    @property
    def nLayers(self):
        return len(self.layers)
    
    def AddLayer(self, layer: Layer):
        self.layers.append(layer)
        
    def __str__(self):
        return f"'{''.join(l.abbr for l in self.layers)}'[{self.nLayers}],{self.comment}"
    def __repr__(self):
        return str(self)
    
    def GetRefractiveIndices(self, wavelength: npt.NDArray[np.float64], 
                             maxLayer = -1,
                             vacuum: bool = True) -> List[npt.NDArray[np.complex128]]:
        layers = self.layers if maxLayer < 0 else self.layers[:maxLayer]
        mat2ri = {} # cache
        ret = []
        for l in layers:
            if l.material.air is None and l.material.vacuum is None:
                return ret
            mat2ri.setdefault(l.material, l.material.GetRefrativeIndex(wavelength, vacuum))
            ret.append(mat2ri[l.material])
        return ret

    @property
    def theoretical_thicknesses(self) -> npt.NDArray[np.float64]:
        # returns a newly created array
        return np.array([l.theoreticalThickness for l in self.layers], dtype=np.float64)
    
    @property
    def ph_thicknesses(self) -> npt.NDArray[np.float64]:
        # returns a newly created array
        return np.array([l.thickness for l in self.layers], dtype=np.float64)

    @property
    def qwot_thicknesses(self) -> npt.NDArray[np.float64]:
        return np.array([]) if self.nLayers == 0 else self.ph_thicknesses / self.GetQWOT()
        
    def GetQWOT(self):
        if self.nLayers == 0:
            return np.array([]) 
        ret = []
        n0 = np.real(self.matchMedium)
        theta0 = np.radians(self.matchAngle)
        for ri in reversed(self.GetRefractiveIndices(np.array([self.controlW]), vacuum=self.isVacuum)):
            n1 = np.real(ri[0])
            theta1 = np.arcsin((n0 / n1) * np.sin(theta0))
            qwot = self.controlW / (4 * n1 * np.cos(theta1))
            ret.append(qwot)
            n0 = n1
            theta0 = theta1
        return np.array(ret[::-1], dtype=np.float64) 
    
    def updateLayers(self, materials: Dict[str, Material]):
        for l in self.layers:
            if l.material.abbr in materials:
                l.material = materials[l.material.abbr]


    @property
    def abbreviations(self) -> str:
        return ''.join([l.material.abbr for l in self.layers])
        
    @classmethod 
    def FromFile(cls, fname: str, materials: Dict[str, Material]):
        with open(fname, 'r') as f:
            controlW = None
            matchAngle = None
            matchMedium = None
            lUnitRegex = r"units: l: (.+)"
            fileLightUnit = LightUnits.DEFAULT
            # read header
            line = f.readline()
            while line:
                l = line.lower().replace(' ','').replace('\t','').replace('\n','')
                if l.startswith('#physicalth.opticalth.fwotqwotmatstatus'):
                    line = f.readline()
                    break
                elif l.startswith('controlwavelength'):
                    controlW = float(line.split('=')[1].split()[0])
                elif l.startswith('matchangle'):
                    matchAngle = float(line.split('=')[1].split()[0])
                elif l.startswith('matchmedium'):
                    matchMedium = float(line.split('=')[1].split()[0])
                # parse LUnits from file
                lUnitMatch = re.search(lUnitRegex, line.lower().strip())
                if lUnitMatch:
                    substring = lUnitMatch.group(1)
                    if substring == 'a':
                        fileLightUnit = LightUnits.ANGS
                    elif substring == 'um':
                        fileLightUnit = LightUnits.MKM
                    else:
                        try:
                            fileLightUnit = getattr(LightUnits, substring.upper()) 
                        except AttributeError:
                            raise ValueError(f"No such light unit type: {substring.upper()}")               
                line = f.readline()
            design = Design(
                comment = fname,
                controlW = LightUnits(fileLightUnit).todef(controlW),
                matchAngle = matchAngle,
                matchMedium = matchMedium
            )

            while line:
                line = line.split()
                p_thick = float(line[1])
                o_thick = float(line[2])
                abbr = line[5]
                layer = Layer(
                        material=Material(abbr=abbr, air=None, vacuum=None, comment=''), #materials[abbr],
                        thickness=LightUnits(fileLightUnit).todef(p_thick),
                    )
                if materials is not None:
                    if abbr in materials:
                        layer.material = materials[abbr]
                design.AddLayer(layer)
                line = f.readline()

            return design

    @classmethod
    def FromXmlDict(cls, d: Dict[str, Any], materials: Dict[str, Material]):
        design = Design(
            comment = "",
            controlW = d.get("@reference-wavelength-nm"),
            matchAngle = None,
            matchMedium = None
        )
        layers = d.get('layer', [])
        if isinstance(layers, dict):
            layers = [layers]
        for l in layers:
            if "material-name" not in l:
                raise Exception(f"Could not find 'material-name' in {l}")
            name = l["material-name"]
            for abbr, m in materials.items():
                if m.vacuumName == name:
                    break
            else:
                raise Exception(f"Could not find material with name '{name}'")
            if "thickness-nm" not in l:
                raise Exception(f"Could not find 'thickness-nm' in {l}")
            design.AddLayer(Layer(
                material = materials[abbr],
                thickness = l["thickness-nm"]
            ))
        return design
    
    def to_dict(self):
        excluded_variables = '_'  # Specify variables to exclude
        data = {}
        for key, value in self.__dict__.items():
            if excluded_variables not in key:
                if isinstance(value, List):
                    tmp = []
                    for item in value:
                        if isinstance(item, Layer):
                            tmp.append((item.material.abbr, item.thickness))
                        elif isinstance(item, str) or isinstance(item, Enum):
                            tmp.append(str(item))
                        else:
                            raise NotImplemented()
                    data[key] = tmp
                    #data[key] = [(item.material.abbr, item.thickness) for item in value]  # Convert Layer to dict
                else:
                    data[key] = value
        return data
    
    @classmethod
    def from_dict(cls, data, abbr2material: Dict[str, Any] = None):
        excluded_variables = '_'  # Specify variables to exclude
        converted_data = {}
        Layers= []
        if abbr2material is not None:
            _abbr2material = abbr2material.copy()
        else:
            _abbr2material = {}

        for key, value in data.items():
            if key in ['layers']:
                for item in value:
                    abbr, thickness = item
                    if len(_abbr2material.keys())>0 and abbr in _abbr2material.keys():
                        Layers.append(Layer(_abbr2material[abbr], thickness))
                    else:
                        _abbr2material[abbr] = Material(abbr=abbr, vacuum=None, air=None, comment='')
                        Layers.append(Layer(_abbr2material[abbr], thickness))

                converted_data[key] = Layers 
            else:
                if excluded_variables not in key:
                    converted_data[key] = value
        return cls(**converted_data), _abbr2material

####################################################################################################
class BroadBandScan(object):
    DEFAULT_TOL = 0.01
    def __init__(self
            , wavelength: npt.NDArray[np.float64]
            , values: npt.NDArray[np.float64]
            , rt_data: DataType = DataType.DEFAULT
            , tols: Optional[np.float64] = None
        ):
        if len(wavelength) != len(values):
            raise Exception(f"Length of wavelength and values must be the same")
        if tols is not None and len(wavelength) != len(tols):
            raise Exception(f"Length of wavelength and tols must be the same")
        self.wavelength = wavelength
        self.values = values
        self.tols = self.DEFAULT_TOL * np.ones_like(wavelength) if tols is None else tols
        self.rt_data = rt_data

    def __len__(self):
        return len(self.wavelength)
    
    def GetValues(self
            , wavelength: npt.NDArray[np.float64]
            , method: InterMethod = InterMethod.DEFAULT
        ) -> npt.NDArray[np.float64]:

        if method == InterMethod.LINEAR:
            f = interp1d(self.wavelength, self.values, kind = "linear", copy = False,
                        assume_sorted = True, fill_value = "extrapolate")
        elif method == InterMethod.SPLINE:
            f = CubicSpline(self.wavelength, self.values, bc_type='natural', extrapolate=True)
        else:
            raise NotImplementedError
        return f(wavelength)


class Measurement(BroadBandScan):
    def __init__(self
            , wavelength: npt.NDArray[np.float64]
            , values: npt.NDArray[np.float64]
            , nLayers: int
            , incidenceAngle: float
            , pol: Polarization
            , rt_data: DataType
            , tols: Optional[np.float64] = None
        ):
        super().__init__(wavelength, values, tols)
        self.nLayers = nLayers
        self.incidenceAngle = incidenceAngle
        self.pol = pol
        self.rt_data = rt_data
        
####################################################################################################
class Coating(object):
    ABBREVIATIONS = "ABCDEFGIJKMNOPQRSTUVWXYZ123456789abcdefghijklmnopqrstuvwxyz" # without L,H,0
    class Provider(NamedTuple):
        name: str
        software_name: str
        software_version: str
        @classmethod
        def FromXmlDict(cls, d: Dict[str, Any]):
            return cls(
                name = d.get('name', ''),
                software_name = d.get('software-name', ''),
                software_version = d.get('software-version', '')
            )
        def ToXmlDict(self):
            return {
                'name': self.name,
                'software-name': self.software_name,
                'software-version': self.software_version
            }
        
    def __init__(self):
        self.provider = Coating.Provider.FromXmlDict({})
        self.abbr2material: Dict[str, Material] = {}
        self.design: Optional[Design] = None
        self.substrate: Optional[Layer] = None
        self.na: np.complex128 = RefractiveIndex.vacuum
        self.hasBackside = False

    @property
    def vacuumName2material(self) -> Dict[str, Material]:
        return {m.vacuumName: m for m in self.abbr2material.values()}

    @classmethod
    def FromXmlDict(cls, d: Dict[str, Any]):
        coating = cls()
        coating.provider = Coating.Provider.FromXmlDict(d.get('provider', {}))
        # read materials
        if 'materials' in d and 'material' in d['materials']:
            materials = d['materials']['material']
            # if only one material, it will be a dict, not a list
            if isinstance(materials, dict):
                materials = [materials]
            materials = materials[:len(cls.ABBREVIATIONS)]
            for m, abbr in zip(materials, cls.ABBREVIATIONS):
                if 'name' not in m:
                    raise Exception('Material name is not specified')
                isVacuum = False if m['name'] in d.get('incident-medium','') else True
                coating.abbr2material[abbr] = Material.FromXmlDict(m, abbr, isVacuum)
        # read design
        if 'layers' in d and 'layer' in d['layers']:
            coating.design = Design.FromXmlDict(d['layers'], coating.abbr2material)
        # read substrate
        if 'substrate' in d:
            substrate_mat = coating.vacuumName2material.get(d['substrate'])
            if substrate_mat is None:
                raise Exception(f"Could not find substrate with name '{d['substrate']}'")
            if 'substrate-thickness-mm' not in d:
                raise Exception(f"Could not find 'substrate-thickness-mm' in {d}")
            coating.substrate = Layer(substrate_mat, float(d['substrate-thickness-mm']))
        if 'incident-medium' in d:
            incident_mat = coating.vacuumName2material[d['incident-medium']]
            if incident_mat is None:
                raise Exception(f"Could not find incident medium with name '{d['incident-medium']}'")
            coating.na = incident_mat.GetRefrativeIndex(np.array([500]))[0]
        # rear-surface-reflects
        if 'rear-surface-reflects' in d:
            coating.hasBackside = d['rear-surface-reflects'].lower() == 'true'

        # apdate abbreviations
        if coating.design is not None:
            if len(coating.design.layers) > 0:
                del coating.abbr2material[coating.design.layers[0].abbr] # remove previous abbr  
                coating.design.layers[0].material.abbr = 'L'
                coating.abbr2material['L'] = coating.design.layers[0].material
            if len(coating.design.layers) > 1:
                del coating.abbr2material[coating.design.layers[1].abbr] # remove previous abbr
                coating.design.layers[1].material.abbr = 'H'
                coating.abbr2material['H'] = coating.design.layers[1].material
        if coating.substrate is not None:
            del coating.abbr2material[coating.substrate.abbr] # remove previous abbreviation
            coating.substrate.material.abbr = '0'
            coating.abbr2material['0'] = coating.substrate.material
        return coating

####################################################################################################
class WitnessChip(object):
    DEFAULT_NAME = '0'

    def __init__(self, substrate: Material, thickness: np.float64):
        if thickness <= 0:
            raise ValueError('Thickness must be positive')
        self.substrate = Layer(substrate, thickness)
        self.layers: List[Layer] = []
        self.measurements: List[Tuple[int, BroadBandScan]] = [] # (layer index, measurement)
        self.op: Optional[OptiProps] = None
        self.local2global = {} # local layer index -> global layer index, both are zero-based

    @property
    def thicknesses(self) -> npt.NDArray[np.float64]:
        return np.array([layer.thickness for layer in self.layers], dtype=np.float64)

    @property
    def theoreticalThicknesses(self) -> npt.NDArray[np.float64]:
        return np.array([layer.theoreticalThickness for layer in self.layers], dtype=np.float64)

    @property
    def nLayers(self) -> int:
        return len(self.layers)

    def Reset(self):
        self.layers = []
        self.op = None
        self.local2global = {}

    def AddLayer(self, layer: Layer, nGlobalLayer: int):
        self.layers.append(layer)
        self.local2global[self.nLayers - 1] = nGlobalLayer

    def nMeasurements(self) -> int:
        return len(self.measurements)
    
    def GetLayersN(self, wavelength: npt.NDArray[np.float64]) -> List[npt.NDArray[np.complex128]]:
        return [layer.material.GetRefrativeIndex(wavelength, True) for layer in self.layers]

    def GetSubstrateN(self, wavelength: npt.NDArray[np.float64]) -> npt.NDArray[np.complex128]:
        return self.substrate.material.GetRefrativeIndex(wavelength, True)

    # layer index is zero-based
    def AddMeasurement(self, measurement: BroadBandScan, nLayer: int):
        self.measurements.append((nLayer, measurement))

    def GetCommonWavelength(self) -> Optional[npt.NDArray[np.float64]]:
        if len(self.measurements) == 0:
            return None
        wavelength = self.measurements[0][1].wavelength
        for _, m in self.measurements:
            wavelength = np.union1d(wavelength, m.wavelength)
        return np.sort(wavelength)

    def UpdateOptiProps(self
            , pol: Polarization
            , incidenceAngle: np.float64
            , na: np.float64
            , rt_units: RTUnits
            , backSideMatters: bool
            , backSideThickness: np.float64
            , thicknesses: Optional[npt.NDArray[np.float64]] = None
        ):
        wavelength = self.GetCommonWavelength()
        if wavelength is None:
            raise Exception('No common wavelength')
        self.op = OptiProps(
            thicknesses = self.thicknesses if thicknesses is None else thicknesses,
            wavelength = wavelength,
            refractiveIndices = self.GetLayersN(wavelength),
            substrateRefractiveIndex = self.GetSubstrateN(wavelength),
            pol = pol,
            incidenceAngle = incidenceAngle,
            na = na,
            rt_units = rt_units,
            backSideMatters = backSideMatters,
            backSideThickness = backSideThickness,
        )

    def GetLoss(self, scale: np.float64 = 1.) -> npt.NDArray[np.float64]:
        if self.op is None:
            raise Exception('OptiProps is not initialized')
        loss = 0.0
        effMeasurements = 0
        for nLayer, m in self.measurements:
            if nLayer >= self.nLayers:
                continue
            effMeasurements += 1
            diff = self.op.GetData(rt_data = m.rt_data, nLayer = nLayer) - scale * m.values
            loss += np.mean(diff * diff)
        effMeasurements = max(effMeasurements, 1)
        return loss / effMeasurements

    def GetGrad(self, scale: np.float64 = 1.) -> npt.NDArray[np.float64]:
        if self.op is None:
            raise Exception('OptiProps is not initialized')
        grad = np.zeros(self.nLayers, dtype=np.float64)
        dScale = 0.0
        effMeasurements = 0
        for nLayer, m in self.measurements:
            if nLayer >= self.nLayers:
                continue
            effMeasurements += 1
            diff = self.op.GetData(rt_data = m.rt_data, nLayer = nLayer) - scale * m.values
            grad[:(nLayer+1)] += np.mean(2 * diff * self.op.GetGrad(rt_data = m.rt_data, nLayer = nLayer), axis=1)
            dScale -= np.mean(2 * diff * m.values)
        effMeasurements = max(effMeasurements, 1)
        return dScale / effMeasurements, grad / effMeasurements
    

    def __str__(self)->str:
        return self.substrate.material.vacuumName

####################################################################################################
# TODO: think about Holt-Winters filter
class DepositionHistory(object):
    # 15
    MAX_HIST = 12 # number of past observations to use in the fit
    MIN_OBSERVATIONS = 4 # at least 4 observations are needed to make a good fit
    def __init__(self, t_start: np.float64 = 0):
        self.observations = [] # (time, thickness)
        self.t_start = t_start
        
    def AddObservation(self, tsec: np.float64, thickness: np.float64):
        self.observations.append((tsec - self.t_start, thickness))
        
    def LeastSquare(self):
        if len(self.observations) < 1:
            return 0, 1
        nPast = min(len(self.observations), self.MAX_HIST)
        A = np.empty((nPast, 2), dtype=np.float64)
        b = np.empty((nPast, 1), dtype=np.float64)
        A[:,0] = 0.
        for n, (tsec, thick) in enumerate(self.observations[-nPast:]):
            A[n,1] = tsec
            b[n,0] = thick
        x, residuals, rank, singular_values = np.linalg.lstsq(A, b, rcond=-1)
        # Calculate the predicted values
        y_pred = A @ x
        residuals = b - y_pred
        # Compute the total sum of squares (TSS)
        y_mean = np.mean(b)
        TSS = np.sum((b - y_mean) ** 2)
        # Compute the residual sum of squares (RSS)
        RSS = np.sum((b - y_pred) ** 2)
        # Calculate R-squared
        r_squared = -1 if TSS == 0 else 1 - (RSS / TSS)
        return x, residuals, r_squared, y_pred
            
    def GetDepositionRate(self) -> np.float64:
        x, residuals, r_squared, y_pred = self.LeastSquare()
        y_pred = y_pred.flatten()[-1]
        v_dep = max(0, x[1][0])
        # estimate quality
        if r_squared < 0.3 or len(self.observations) < self.MIN_OBSERVATIONS:
            return v_dep, PredQuality.BAD, y_pred
        # normalize residuals
        residuals -= np.mean(residuals)
        st = np.std(residuals)
        # remove outliers
        residuals[residuals > 3*st] = 3*st
        residuals[residuals < -3*st] = -3*st
        # normalize again
        residuals -= np.mean(residuals)
        st = np.std(residuals)
        if st == 0:
            # TODO: does this make sense?
            return v_dep, PredQuality.GOOD, y_pred
        residuals /= st
        residual = abs(residuals[-1])
        if residual > 2:
            return v_dep, PredQuality.BAD, y_pred
        if residual > 1.2 or r_squared < 0.7:
            return v_dep, PredQuality.SATISFACTORY, y_pred
        return v_dep, PredQuality.GOOD, y_pred


####################################################################################################
class TargetColumn(object):
    DEF_TOLERANCE = 0.01 # 1%
    def __init__(self
            , spechar: SpectralCharacteristic
            , values: npt.NDArray[np.float64]
            , floatingConstant: Optional[FloatingConstant] = None
            , values2: Optional[npt.NDArray[np.float64]] = None
            , tolerances: Optional[npt.NDArray[np.float64]] = None
            , qualifiers: Optional[List[TargetQualifier]] = None
        ):
        self.spechar = spechar
        self.values = values
        self.floatingConstant = FloatingConstant.NONE if floatingConstant is None else floatingConstant
        # values2 is for the RANGE qualifier to define upper limits
        if values2 is None:
             self.values2 = np.copy(values)
        elif len(values2) != len(values):
            raise Exception(f"Length of values and values2 must be the same, got {len(values)} and {len(values2)}")
        else:
            self.values2 = values2
        # set tolerances
        if tolerances is None:
            self.tolerances = self.DEF_TOLERANCE * np.ones_like(values)
        elif len(tolerances) != len(values):
            raise Exception(f"Length of tolerances and values must be the same, got {len(tolerances)} and {len(values)}")
        else:
            self.tolerances = tolerances
        # set qualifier
        if qualifiers is None:
            self._qualifiers = np.ones_like(values, dtype=np.int64) * TargetQualifier.DEFAULT
        elif len(qualifiers) != len(values):
            raise Exception(f"Length of qualifier and values must be the same, got {len(qualifiers)} and {len(values)}")
        else:
            self._qualifiers = np.array(qualifiers, dtype=np.int64)

    @property
    def qualifiers(self) -> List[TargetQualifier]:
        return [TargetQualifier(q) for q in self._qualifiers]
    
    def __str__(self) -> str:
        return f"{self.spechar.name} {self.values}"
    def __repr__(self) -> str:
        return str(self)
    
    def get_qualifier(self, index: int) -> TargetQualifier:
        return TargetQualifier(self._qualifiers[index])

    def set_qualifier(self, index: int, qualifier: TargetQualifier):
        self._qualifiers[index] = qualifier.value


####################################################################################################
class TargetPage(object): #angle, wavelength, spechar, values, tolerance, qualifier
    def __init__(self
            , angle: np.float64
            , wavelength: npt.NDArray[np.float64]
            , spechar: SpectralCharacteristic
            , values: npt.NDArray[np.float64]
            , tolerance: Optional[npt.NDArray[np.float64]] = None
            , qualifier: Optional[List[TargetQualifier]] = None
        ):
        self.angle = angle
        self.wavelength = wavelength
        self.columns: List[TargetColumn] = []
        self.AddColumn(TargetColumn(spechar, values, tolerances=tolerance, qualifiers=qualifier))

    @property
    def spechar(self) -> SpectralCharacteristic:
        return self.columns[0].spechar
    
    @property
    def values(self) -> npt.NDArray[np.float64]:
        return self.columns[0].values
    
    @property
    def tolerance(self) -> npt.NDArray[np.float64]:
        return self.columns[0].tolerances
    
    @property
    def qualifier(self) -> List[TargetQualifier]:
        return self.columns[0].qualifiers
    
    def AddColumn(self, col: TargetColumn) -> int:
        # check if the column is already present
        for c in self.columns:
            if c.spechar == col.spechar:
                raise Exception(f"Column with spectral characteristic {col.spechar.name} already exists")
        # check if the column is compatible with the existing ones
        if len(self.wavelength) != len(col):
            raise Exception(f"Length of wavelength and values must be the same, got {len(self.wavelength)} and {len(col)}")
        self.columns.append(col)
        return len(self.columns) - 1

    @property
    def incidenceAngle(self):
        return self.angle
    
    def __str__(self) -> str:
        return f"{self.spechar.name} {self.angle} {self.wavelength} {self.values}"
    def __repr__(self) -> str:
        return str(self)
    
    def to_dict(self):
        excluded_variables = '_'  # Specify variables to exclude
        data = {}
        for key, value in self.__dict__.items():
            if excluded_variables not in key:
                if isinstance(value, List):
                    tmp = []
                    for item in value:
                        if isinstance(item, Enum):
                            tmp.append(str(item.value))
                    data[key] = tmp
                elif isinstance(value, np.ndarray):
                    data[key] = value.tolist()  # Convert NumPy array to list
                elif isinstance(value, Enum):
                    data[key] = str(value.value)
                else:
                    data[key] = value
        return data
    
    @classmethod
    def from_dict(cls, data):
        converted_data = {}
        for key, value in data.items():
            if isinstance(value, list):
                converted_data[key] = np.array(value)  # Convert list to NumPy array
            else:
                converted_data[key] = value
        return cls(
            angle = converted_data['angle'] if 'angle' in converted_data else 0.0,
            spechar = SpectralCharacteristic(converted_data['spechar']),
            wavelength = np.array(converted_data['wavelength'], dtype=np.float64) if 'wavelength' in converted_data else np.array([], dtype=np.float64),
            values = np.array(converted_data['values'], dtype=np.float64) if 'values' in converted_data else np.array([], dtype=np.float64),
            tolerance = np.array(converted_data['tolerance'], dtype=np.float64) if 'tolerance' in converted_data else None,
            qualifier = [TargetQualifier(val) for val in converted_data['qualifier']] if 'qualifier' in converted_data else []
        )

class Target(object):
    def __init__(self
            , name: str
            , comment: str
            , pages: Optional[List[TargetPage]] = None
            , weight: np.float64 = 1.0
        ):
        self.name = name
        self.comment = comment
        self.pages = [] if pages is None else pages
        self.weight = weight

    def __str__(self) -> str:
        return "\n".join([str(p) for p in self.pages])
    def __repr__(self) -> str:
        return str(self)

    def AddPage(self, page: TargetPage):
        self.pages.append(page)

    @classmethod
    def FromFile(cls, fname: str):
        # TODO: units control
        # TODO: support of multiple columns for values in different pages
        name = ''
        comment = ''
        angle = 0.0
        spechar = SpectralCharacteristic.AA
        wavelength = 0.0
        values = []
        tolerance = []
        qualifier = []
        pagesN = 0
        # parsing number of pages and total number of points
        with open(fname, 'r') as f:
            line = f.readline()
            while line:
                # data points
                if line.lower().startswith('target data:'):
                    pointsN = line.split(':')[1].strip().replace('points','')
                    pointsN = int(pointsN)
                # pages count
                if line.lower().startswith('page #'):
                    pagesN = pagesN + 1
                # TODO: Support Floating Constant Targets
                if line.strip().lower().startswith('floating constant targets:'):
                    raise NotImplementedError(f"Floating Constant Targets are not supported: {fname}")
                line = f.readline()

        #reading target data
        with open(fname, 'r') as f:
            line = f.readline()
            while line and 'page' not in line.lower():
                if line.startswith('#physicalth.opticalth.fwotqwotmatstatus'):
                    line = f.readline()
                    break
                # tager name
                if line.lower().startswith('target data file:'):
                    name = line.split(':')[1].strip()
                # comment text
                if line.lower().startswith('comment:'):
                    comment = line.split(':')[1].strip()
                line = f.readline()

                
            target = Target(name, comment)

            cur_page = 0
            while line and cur_page<pagesN:

                wavelength = [] 
                spechar = []
                values = []
                qualifier = []
                tolerance = []

                if line.strip() == '':
                    line = f.readline()
                    continue

                cur_page = cur_page+1
                cur_point = 0
                spechar_list = []
                while line and cur_point < pointsN//pagesN:
                    if line.lower().strip().startswith('# wavelength'):
                        #remove multiple spaces
                        text = " ".join(line.lower().split())
                        labels = text.split(' ')
                        page_data = text.split('q')
                        pageinpageN = len(page_data)-1
                        # TODO: multiple targets in single page  
                        if pageinpageN > 1:
                            raise NotImplementedError(f"Multiple targets in single page are not supported: {fname}")
                        
                        spechar_list.append(labels[2])                                                
                    elif '=' in line.lower():
                            # angle text
                            angle = float(line.split('=')[1].strip())

                    else:
                        #text = " ".join(line.lower().split())                   
                        cur_point = cur_point+1
                        index1 = 15
                        try:
                            wavelength.append(float(line[5:15].replace(',','')))

                            values.append(float(line[index1:index1+10].replace(',','')))
                            tolerance.append(float(line[index1+10:index1+19].replace(',','')))
                            try:
                                qual = line[index1+20:index1+21]
                                qualifier.append(TargetQualifier.from_char(qual))
                            except:
                                qualifier.append(TargetQualifier.DEFAULT)                                
                        except AttributeError:
                            raise ValueError(f"Data is corrupted: {fname}")      
                    line = f.readline()  
                # TODO: Support TargetQualifier.R  
                if TargetQualifier.R in qualifier:
                    raise NotImplementedError(f"TargetQualifier R is supported: {fname}")

                target.AddPage(TargetPage(angle,
                                           np.array(wavelength, np.float64), 
                                           SpectralCharacteristic(spechar_list[0].upper()), 
                                           np.array(values), 
                                           np.array(tolerance), 
                                           qualifier))

            return target
        
    def to_dict(self):
        excluded_variables = '_'  # Specify variables to exclude
        data = {}
        for key, value in self.__dict__.items():
            if excluded_variables not in key:
                if isinstance(value, List):
                    tmp = []
                    for item in value:
                        if isinstance(item, TargetPage):
                            tmp.append(item.to_dict())
                        else:
                            raise NotImplemented()
                    if len(tmp) == 0:
                        tmp = None
                    data[key] = tmp
                else:
                    data[key] = value
        return data
    
    @classmethod
    def from_dict(cls, data):
        excluded_variables = '_'  # Specify variables to exclude
        converted_data = {}

        for key, value in data.items():
            if key in ['pages']:
                pages= []
                for item in value:
                    pages.append(TargetPage.from_dict(item))
                converted_data[key] = pages 
            elif excluded_variables not in key:
                converted_data[key] = value
            else:
                raise NotImplemented()

        return cls(
            name = converted_data['name'] if 'name' in converted_data else "",
            comment = converted_data['comment'] if 'comment' in converted_data else "",
            pages = converted_data['pages'] if 'pages' in converted_data else None,
            weight = converted_data['weight'] if 'weight' in converted_data else 1.0
        )

####################################################################################################
    
class ColorTarget(object):
    def __init__(self
            , name: str
            , comment: str
            , space: ColorSpace
            , angles: List[np.float64]
            , ctypes: List[ColorType]
            , ctargets: List[ColorTargetChar]
            , cqualifiers: List[ColorQualifier]
            , cpolarizations: List[Polarization]
            , values: List[np.float64]
            , tolerances: List[np.float64]  
            , weight: np.float64 = 1.0        
        ):
        self.name = name
        self.comment = comment
        self.cspace = space
        self.angles = angles
        self.ctypes = ctypes
        self.ctargets = ctargets
        self.cqualifiers = cqualifiers
        self.cpolarizations = cpolarizations
        self.values = values
        self.tolerances = tolerances
        self.weight = weight


    @classmethod
    def FromFile(cls, fname: str):
        # init arrays
        angles = []
        types = []
        ctargets =[]
        cqualifiers = []
        cpolarizations =[]
        values =[]
        tolerances = []
        #reading color target data
        with open(fname, 'r') as f:
            line = f.readline()
            while line:
                if line.strip().lower().replace(' ','').startswith('#angle'):
                    break
                # tager name
                if line.lower().startswith('color target function file:'):
                    name = line.split(':')[1].strip()
                # comment text
                if line.lower().startswith('comment:'):
                    comment = line.split(':')[1].strip()
                # color space text
                if line.lower().startswith('color space:'):
                    spacetext = line.split(':')[1].strip().replace('\'','').replace(' ','_').replace('*','').replace('\u00B0','_').replace('(','').replace(')','')
                    try:
                        space = getattr(ColorSpace, spacetext.upper()) 
                    except AttributeError:
                        raise ValueError(f"No such color space type: {spacetext.upper()}")                  

                line = f.readline()

            while line:     
                line = f.readline()           
                line = line.replace('\'','prim').replace('*','star').replace('(','').replace(')','').replace('\u00B0','_').replace('R-','br')
                # Split the line into separate fields based on whitespace
                fields = line.strip().split()
                if len(fields)==0:
                    continue
                try:
                    # Extract the values for each field and append them to the corresponding array
                    if len(fields)>7:
                        cqualifiers.append(getattr(ColorQualifier, fields[7].upper()) )
                    else:
                        cqualifiers.append(ColorQualifier.BLANK)
                    # TODO: implementation of ColorQualifier.R
                    if ColorQualifier.R in cqualifiers:
                        raise NotImplementedError(f"ColorQualifier R is supported: {fname}")

                    angles.append(float(fields[1]))
                    types.append(getattr(ColorType, fields[2].upper()) )
                    ctargets.append(getattr(ColorTargetChar, fields[3].upper()) )
                    cpolarizations.append(getattr(Polarization, fields[4].upper()) )
                    values.append(float(fields[5]))
                    tolerances.append(float(fields[6]))

                except AttributeError:
                    raise ValueError(f"Data corrupted in color target file: {fname}")                       

            for type in types:
                if ColorType.is_valid(space, type):
                    raise ValueError(f"Color type do not correspond to color space: {space}")  

        return ColorTarget(name, comment, space, angles, types, ctargets, cqualifiers, cpolarizations, values, tolerances)
