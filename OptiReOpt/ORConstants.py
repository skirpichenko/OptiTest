from enum import IntEnum, Enum, auto
from typing import *


##############################################################################
# Calculation mode in the On-line characterization part of this dll.
# MODE_SEQUENTIAL means that only a thickness of the last layer will
#   be changed during characterization.
# MODE_TRIANGLE means that thicknesses of ALL deposited layers will
#   be changed at each on-line characterization step.
class CalculationMode(IntEnum):
    SEQUENTIAL = 1
    TRIANGLE = 2
    DEFAULT = TRIANGLE

    @property
    def depth(self) -> int:
        if self == CalculationMode.SEQUENTIAL:
            return 1
        elif self == CalculationMode.TRIANGLE:
            return 30
        else:
            raise Exception("Unknown CalculationMode")


# Input data types
class Polarization(IntEnum):
    S = 1  # s-polarization case
    P = 2  # p-polarization case
    A = 3  # average polarization case
    DEFAULT = A

    def to_char(self):
        if self == Polarization.S:
            return "S"
        elif self == Polarization.P:
            return "P"
        elif self == Polarization.A:
            return "A"
        else:
            raise Exception("Unknown polarization")


# Stream data types
class DataType(IntEnum):
    REFL = 1  # reflectance data measured in-situ
    TRANS = 2  # transmittance data measured in-situ
    BREFL = 3  # back reflectance data measured in-situ
    DEFAULT = TRANS

    def to_spechar(self, pol: Polarization):
        if self == DataType.REFL:
            if pol == Polarization.S:
                return SpectralCharacteristic.RS
            elif pol == Polarization.P:
                return SpectralCharacteristic.RP
            elif pol == Polarization.A:
                return SpectralCharacteristic.RA
            else:
                raise Exception("Unknown polarization")
        elif self == DataType.TRANS:
            if pol == Polarization.S:
                return SpectralCharacteristic.TS
            elif pol == Polarization.P:
                return SpectralCharacteristic.TP
            elif pol == Polarization.A:
                return SpectralCharacteristic.TA
            else:
                raise Exception("Unknown polarization")
        elif self == DataType.BREFL:
            if pol == Polarization.S:
                return SpectralCharacteristic.BRS
            elif pol == Polarization.P:
                return SpectralCharacteristic.BRP
            elif pol == Polarization.A:
                return SpectralCharacteristic.BRA
            else:
                raise Exception("Unknown polarization")
        else:
            raise Exception("Unknown DataType")

    def __str__(self) -> str:
        if self == DataType.REFL:
            return 'Reflectance'
        elif self == DataType.TRANS:
            return 'Transmittance'
        elif self == DataType.BREFL:
            return "Back Reflectance"
        else:
            raise Exception("Unknown DataType")


##############################################################################
# Input data correction modes (On-Line characterization mode only)
class InputDataCorrection(IntEnum):
    NONE = 0  # - correction disabled
    LAST_ONLY = 1  # - correction of the last scan only
    ALL_SCANS = 2  # - correction of all scans at each on-line step
    DEFAULT = ALL_SCANS


##############################################################################
#  Data correction types (On-Line characterization mode only)
#  Correction with the help of relative shift
#  or correction with the help of scale adjustment
class InputDataCorrectionMethod(IntEnum):
    SHIFT = 1  # relative shift corrections
    SCALE = 2  # scale adjustments
    DEFAULT = SCALE

    @classmethod
    def ClipScale(cls, scale: float) -> float:
        scale = max(0.85, scale)
        scale = min(1.15, scale)
        return scale

    def __str__(self):
        if self == InputDataCorrectionMethod.SHIFT:
            return "Shift"
        elif self == InputDataCorrectionMethod.SCALE:
            return "Scale"
        else:
            return f"{self.name}"


##############################################################################
#  Presentation of wavelengths and physical thicknesses in mkm or nm
class LightUnits(IntEnum):
    MKM = 1
    NM = 2
    ANGS = 3  # Angstroms
    DEFAULT = NM

    # Convert from current units to nm
    def todef(self, val: float) -> float:
        if self.value == self.MKM:
            return val * 1000
        elif self.value == self.NM:
            return val
        elif self.value == self.ANGS:
            return val * 0.1
        else:
            raise ValueError("Unknown LightUnits")

    # Convert from nm to current units
    def fromdef(self, val: float) -> float:
        if self.value == self.MKM:
            return val / 1000
        elif self.value == self.NM:
            return val
        elif self.value == self.ANGS:
            return val * 10
        else:
            raise ValueError("Unknown LightUnits")

    def __str__(self):
        if self == LightUnits.MKM:
            return "μm"
        elif self == LightUnits.NM:
            return "nm"
        elif self == LightUnits.ANGS:
            return "Å"
        else:
            return ValueError("Unknown LightUnits")

##############################################################################
class SpectralUnits(IntEnum):
    MKM = 1  # Micrometre (μm)
    NM = auto()  # Nanometre
    ANGS = auto()  # Angstroms (Å)
    CM_1 = auto()  # Reciprocal wavelength (cm⁻¹)
    NCM = auto()  # Newton centimeter (2n/cm)
    KEV = auto()  # Kiloelectronvolt (keV)
    MKM_1 = auto()  # (μm⁻¹)
    THz = auto()  # Terahertz (THz)
    GHz = auto()  # Gigahertz (GHz)
    G_NUM = auto()  # (g-num)
    DEFAULT = ANGS

    def __str__(self):
        if self == SpectralUnits.MKM:
            return "μm"
        elif self == SpectralUnits.NM:
            return "nm"
        elif self == SpectralUnits.ANGS:
            return "Å"
        elif self == SpectralUnits.CM_1:
            return "cm⁻¹"
        elif self == SpectralUnits.NCM:
            return "2n/cm"
        elif self == SpectralUnits.KEV:
            return "keV"
        elif self == SpectralUnits.MKM_1:
            return "μm⁻¹"
        elif self == SpectralUnits.THz:
            return "THz"
        elif self == SpectralUnits.GHz:
            return "GHz"
        elif self == SpectralUnits.G_NUM:
            return "g-num"
        else:
            raise ValueError("Unknown SpectralUnits")



##############################################################################
#  Presentation of T/R data in absolute values of percents
class RTUnits(IntEnum):
    ABS = 1
    PERCENT = auto()
    DB = auto()
    OD = auto()
    DEFAULT = ABS

    def todef(self, val: float) -> float:
        if self.value == self.ABS:
            return val
        elif self.value == self.PERCENT:
            return val * 100
        else:
            raise ValueError("Unknown RTUnits")

    def fromdef(self, val: float) -> float:
        if self.value == self.ABS:
            return val
        elif self.value == self.PERCENT:
            return val / 100
        else:
            raise ValueError("Unknown RTUnits")

    def __str__(self):
        if self == RTUnits.ABS:
            return "0-1"
        elif self == RTUnits.PERCENT:
            return "%"
        elif self == RTUnits.DB:
            return "dB"
        elif self == RTUnits.OD:
            return "OD"
        else:
            raise ValueError("Unknown RTUnits")



##############################################################################
class SourceDetectorConeIntUnits(IntEnum):
    ABS = 1
    PERCENT = auto()
    DEFAULT = ABS

    def __str__(self):
        if self == SourceDetectorConeIntUnits.ABS:
            return "0-1"
        elif self == SourceDetectorConeIntUnits.PERCENT:
            return "%"
        else:
            raise ValueError("Unknown SourceDetectorConeIntUnits")



##############################################################################
class PsiDeltaUnits(IntEnum):
    PERCENT = 1
    RD = auto()
    DEFAULT = PERCENT

    def __str__(self):
        if self == PsiDeltaUnits.PERCENT:
            return "0-1"
        elif self == PsiDeltaUnits.RD:
            return "%"
        else:
            raise ValueError("Unknown PsiDeltaUnits")



##############################################################################
class GDUnits(IntEnum):
    PS = 1
    FS = auto()
    DEFAULT = PS

    def __str__(self):
        if self == GDUnits.PS:
            return "Ps"
        elif self == GDUnits.FS:
            return "Fs"
        else:
            raise ValueError("Unknown GDUnits")



##############################################################################
class GDDUnits(IntEnum):
    PSSQUARED = 1
    FSSQUARED = auto()
    DEFAULT = PSSQUARED

    def __str__(self):
        if self == GDDUnits.PSSQUARED:
            return "Ps²"
        elif self == GDDUnits.FSSQUARED:
            return "Fs²"
        else:
            raise ValueError("Unknown GDDUnits")



##############################################################################
# These flags are primarily for LoadTheoreticalDesign function
#  They indicate how input thicknesses are presented
class ThicknessUnits(IntEnum):
    PHYS = 1  # physical thicknesses
    OPT = 2  # optical thicknesses
    FWOT = 3  # Full-Wave Optical Thicknesses
    QWOT = 4  # Quarter-Wave Optical Thicknesses
    DEFAULT = PHYS

    def __str__(self):
        if self == ThicknessUnits.PHYS:
            return "Physical"
        elif self == ThicknessUnits.OPT:
            return "Optical"
        elif self == ThicknessUnits.FWOT:
            return "FWOT"
        elif self == ThicknessUnits.QWOT:
            return "QWOT"
        else:
            raise ValueError("Unknown ThicknessUnits")



##############################################################################
#  Values describing materials.
#  TABLE means that corresponding part of refractive index
#    (Re(n) or Im(n)) is given in table format.
#  Other constants correspond to different formulas

#  nType values (Re(n))
class MaterialNType(IntEnum):
    TABLE = 0
    SELLMEIER1 = 1
    SELLMEIER2 = 2
    SELLMEIER2P = 3
    SELLMEIER3 = 4
    CAUCHY = 5
    HARTMANN = 6
    SCHOTTGLAS = 7
    HARTMANN2 = 8
    NDRUDE = 9
    DEFAULT = TABLE

    @property
    def coefCount(self):
        if self == MaterialNType.TABLE:
            return 0
        elif self == MaterialNType.SELLMEIER1:
            return 3
        elif self == MaterialNType.SELLMEIER2:
            return 5
        elif self == MaterialNType.SELLMEIER2P:
            return 4
        elif self == MaterialNType.SELLMEIER3:
            return 7
        elif self == MaterialNType.CAUCHY:
            return 3
        elif self == MaterialNType.HARTMANN:
            return 3
        elif self == MaterialNType.SCHOTTGLAS:
            return 7
        elif self == MaterialNType.HARTMANN2:
            return 3
        elif self == MaterialNType.NDRUDE:
            return 3
        else:
            raise ValueError("Unknown MaterialNType")

    def __str__(self) -> str:
        if self == MaterialNType.TABLE:
            return 'Table'
        elif self == MaterialNType.SELLMEIER1:
            return "Sellmeier 1"
        elif self == MaterialNType.SELLMEIER2:
            return "Sellmeier 2"
        elif self == MaterialNType.SELLMEIER2P:
            return "Sellmeier 2'"
        elif self == MaterialNType.SELLMEIER3:
            return "Sellmeier 3"
        elif self == MaterialNType.CAUCHY:
            return 'Cauchy'
        elif self == MaterialNType.HARTMANN:
            return 'Hartmann'
        elif self == MaterialNType.SCHOTTGLAS:
            return 'Schottglass'
        elif self == MaterialNType.HARTMANN2:
            return 'Hartmann 2'
        elif self == MaterialNType.NDRUDE:
            return 'Drude'
        else:
            raise ValueError("Unknown MaterialNType")


#  kType values (Im(n))
class MaterialKType(IntEnum):
    TABLE = 0
    NONABS = 1
    NONDISP = 2
    KSELLMEIER = 3
    EXPONENTIAL = 4
    POLYNOMIAL = 5
    KDRUDE = 6
    DEFAULT = TABLE

    @property
    def coefCount(self):
        if self == MaterialKType.TABLE:
            return 0
        elif self == MaterialKType.NONABS:
            return 0
        elif self == MaterialKType.NONDISP:
            return 1
        elif self == MaterialKType.KSELLMEIER:
            return 3
        elif self == MaterialKType.EXPONENTIAL:
            return 3
        elif self == MaterialKType.POLYNOMIAL:
            return 4
        elif self == MaterialKType.KDRUDE:
            return 3
        else:
            raise ValueError("Unknown MaterialKType")

    def __str__(self) -> str:
        if self == MaterialKType.TABLE:
            return 'Table'
        elif self == MaterialKType.NONABS:
            return 'Non-absorbing'
        elif self == MaterialKType.NONDISP:
            return ' Non-dispersive'
        elif self == MaterialKType.KSELLMEIER:
            return 'Sellmeier'
        elif self == MaterialKType.EXPONENTIAL:
            return ' Exponential'
        elif self == MaterialKType.POLYNOMIAL:
            return 'Polynomial'
        elif self == MaterialKType.KDRUDE:
            return 'Drude'
        else:
            raise ValueError("Unknown MaterialKType")

        # interpolation method for (Re(n)) and (Im(n)) tables


class InterMethod(IntEnum):
    LINEAR = 0
    SPLINE = 1
    DEFAULT = LINEAR


##############################################################################
# Flags used as OR_CheckOptimality return values
class OptState(IntEnum):
    OPTIMAL = 0
    NOT_OPTIMAL = 1
    DATA_NOT_LOADED = 2


##############################################################################
#  Values characterizing quality of OR_ProcessOnLineTRScan prediction
#  (see OR_ProcessOnLineTRScan description)
class PredQuality(IntEnum):
    GOOD = 1
    SATISFACTORY = 2
    BAD = 3
    DEFAULT = BAD


##############################################################################
#    Estimation of overall online characterization:
#    ( OR_GetOnLineState )
class ROState(IntEnum):
    INDIFFERENT = -1
    OK = 0
    WARNING = 1
    ERROR = 2
    DEFAULT = OK


##############################################################################
class OptiLayerMode(IntEnum):
    SPECTRAL = auto()
    ANGULAR = auto()
    DEFAULT = SPECTRAL

    def __str__(self) -> str:
        if self == OptiLayerMode.SPECTRAL:
            return "Spectral"
        elif self == OptiLayerMode.ANGULAR:
            return "Angular"
        else:
            raise ValueError("Unknown OptiLayerMode")



##############################################################################
#    Reoptimization methods, used in
#    OR_SetReoptimizationMethod 
class ReOptMode(IntEnum):
    MODIFIED_DLS = 1
    NEWTON = auto()
    QUASI_NEWTON_DLS = auto()
    SEQUENTIAL_QP = auto()
    CONJUGATE_GRADIENTS = auto()
    STEEPEST_DESCENT = auto()
    DEFAULT = MODIFIED_DLS

    def __str__(self) -> str:
        if self == ReOptMode.MODIFIED_DLS:
            return "Modified DLS"
        elif self == ReOptMode.NEWTON:
            return "Newton"
        elif self == ReOptMode.QUASI_NEWTON_DLS:
            return "Quasi-Newton DLS"
        elif self == ReOptMode.SEQUENTIAL_QP:
            return "Sequential QP"
        elif self == ReOptMode.CONJUGATE_GRADIENTS:
            return "Conjugate gradients"
        elif self == ReOptMode.STEEPEST_DESCENT:
            return "Steepest descent"
        else:
            raise ValueError("Unknown ReOptMode")



##############################################################################
# Light Source types
class LightSource(IntEnum):
    CIE_A = 0
    CIE_B = 1
    CIE_C = 2
    CIE_D55 = 3
    CIE_D65 = 4
    CIE_D75 = 5
    ISO_9845_1 = 6
    Uniform = 7
    DEFAULT = CIE_A


##############################################################################
class SpectralCharacteristic(Enum):
    # Reflectance (for S-, P- and Average polarizations):
    RS = 'RS'
    RP = 'RP'
    RA = 'RA'
    # Back Reflectance (for S-, P- and Average polarizations):
    BRS = 'BRS'
    BRP = 'BRP'
    BRA = 'BRA'
    # Transmittance (for S-, P- and Average polarizations):
    TS = 'TS'
    TP = 'TP'
    TA = 'TA'
    # Absorptance (for S-, P- and Average polarizations):
    AS = 'AS'
    AP = 'AP'
    AA = 'AA'
    # Phase Shift on Reflection (for S- and P-polarizations):
    PRS = 'PRS'
    PRP = 'PRP'
    # Differential Phase Shift for Reflection (difference between phase shifts 
    # on reflection for S- and P-polarized waves):
    DPR = 'DPR'
    # Phase Shift on Transmission (for S- and P-polarization):
    PTS = 'PTS'
    PTP = 'PTP'
    # Differential Phase Shift for Transmission (difference between phase shifts on
    # transmission for S- and P-polarized waves):
    DPT = 'DPT'
    # Group delay and group delay dispersion on reflection: GDRS, GDRP, GDDRS, GDDRP
    GDRS = 'GDRS'
    GDRP = 'GDRP'
    GDTS = 'GDTS'
    GDTP = 'GDTP'
    # Group delay and group delay dispersion on transmission: GDTS, GDTP, GDDTS, GDDTP
    GDDRS = 'GDDRS'
    GDDRP = 'GDDRP'
    GDDTS = 'GDDTS'
    GDDTP = 'GDDTP'
    # User-Defined Target (UDT)
    UDT = 'UDT'

    @property
    def pol(self) -> Optional[Polarization]:
        if self in [SpectralCharacteristic.RS,
                    SpectralCharacteristic.TS,
                    SpectralCharacteristic.AS,
                    SpectralCharacteristic.PRS,
                    SpectralCharacteristic.PTS]:
            return Polarization.S
        elif self in [SpectralCharacteristic.RP,
                      SpectralCharacteristic.TP,
                      SpectralCharacteristic.AP,
                      SpectralCharacteristic.PRP,
                      SpectralCharacteristic.PTP]:
            return Polarization.P
        elif self in [SpectralCharacteristic.RA,
                      SpectralCharacteristic.TA,
                      SpectralCharacteristic.AA]:
            return Polarization.A
        else:
            return None

    @property
    def rt_data(self) -> Optional[DataType]:
        if self in [SpectralCharacteristic.RS,
                    SpectralCharacteristic.RP,
                    SpectralCharacteristic.RA]:
            return DataType.REFL
        elif self in [SpectralCharacteristic.TS,
                      SpectralCharacteristic.TP,
                      SpectralCharacteristic.TA]:
            return DataType.TRANS
        elif self in [SpectralCharacteristic.BRS,
                      SpectralCharacteristic.BRP,
                      SpectralCharacteristic.BRA]:
            return DataType.BREFL
        else:
            return None


##############################################################################
class ColorTargetChar(Enum):
    T = 'T'
    R = 'R'
    BR = 'BR'


class ColorQualifier(Enum):
    BLANK = ''
    A = 'A'
    B = 'B'
    C = 'C'  # The qualifier C correspond to anChor color, in this case target correspond to a difference between current color value and a similar color value for Anchor Color.
    R = 'R'  # The qualifier for so-called Range Color Target specified as convex polygons


class ColorSpace(Enum):
    CHROMATICITIES = 'CHROMATICITIES'
    TRISTIMULUS = 'TRISTIMULUS'
    CIE_YUV_1960 = 'CIE_YUV_1960'
    CIE_YUV_1976 = 'CIE_YUV_1976'
    CIE_LUV = 'CIE_LUV'
    CIE_LAB = 'CIE_LAB'
    HUNTER_LAB = 'HUNTER_LAB'
    CIE_H_LC = 'CIE_H_LC'
    CIE_CHSUV = 'CIE_CHSUV'


class ColorType(Enum):
    X = 'x'
    Y = 'y'
    Z = 'z'
    LU = 'LU'
    LY = 'LY'
    V = 'V'
    U = 'U'
    VSTAR = 'v*'
    USTAR = 'u*'
    LSTAR = 'L*'
    LH = 'LH'
    AH = 'AH'
    BH = 'BH'
    ASTAR = 'a*'
    BSTAR = 'b*'
    CSTAR = 'C*'
    H_UV = 'h_(uv)'
    SUV = 's(uv)'
    H_AB = 'H_(ab)'
    L = 'L'
    CSTARAB = 'C*(ab)'
    VPRIM = 'VPRIM'
    UPRIM = 'UPRIM'

    @classmethod
    def is_valid(cls, space, value):
        if space.value == ColorSpace.CHROMATICITIES:
            return value in [cls.X.value, cls.Y.value, cls.Z.value, cls.LU.value]
        if space.value == ColorSpace.TRISTIMULUS:
            return value in [cls.X.value, cls.Y.value, cls.Z.value]
        if space.value == ColorSpace.CIE_YUV_1960:
            return value in [cls.U.value, cls.V.value, cls.Y.value]
        if space.value == ColorSpace.CIE_YUV_1976:
            return value in [cls.UPRIM.value, cls.VPRIM.value, cls.Y.value]
        if space.value == ColorSpace.CIE_LUV:
            return value in [cls.USTAR.value, cls.VSTAR.value, cls.LSTAR.value]
        if space.value == ColorSpace.CIE_LAB:
            return value in [cls.ASTAR.value, cls.BSTAR.value, cls.LSTAR.value]
        if space.value == ColorSpace.HUNTER_LAB:
            return value in [cls.AH.value, cls.BH.value, cls.LH.value]
        if space.value == ColorSpace.CIE_H_LC:
            return value in [cls.H_AB.value, cls.LSTAR.value, cls.CSTARAB.value]
        if space.value == ColorSpace.CIE_CHSUV:
            return value in [cls.H_UV.value, cls.SUV.value, cls.CSTAR.value]


##############################################################################
class FloatingConstant(Enum):
    NONE = 'None'
    C1 = 'C1'
    C1_C2W = 'C1 + C2 * ω'
    C1_C2W_C3W2 = 'C1 + C2*ω + C3 * ω²'
    DEFAULT = NONE

    def __str__(self) -> str:
        return self.name


class TargetQualifier(IntEnum):
    NONE = 0
    ABOVE = 1
    BELOW = 2
    RANGE = 3
    A = ABOVE
    B = BELOW
    R = RANGE
    DEFAULT = NONE

    def __str__(self) -> str:
        if self == TargetQualifier.NONE:
            return ''
        elif self == TargetQualifier.ABOVE:
            return 'A'
        elif self == TargetQualifier.BELOW:
            return 'B'
        elif self == TargetQualifier.RANGE:
            return 'R'
        else:
            raise ValueError("Unknown TargetQualifier")
        
    @classmethod
    def from_char(cls, char: str) -> 'TargetQualifier':
        if char == '':
            return TargetQualifier.NONE
        elif char.upper() == 'A':
            return TargetQualifier.ABOVE
        elif char.upper() == 'B':
            return TargetQualifier.BELOW
        elif char.upper() == 'R':
            return TargetQualifier.RANGE
        else:
            raise ValueError(f"Cannot convert '{char}' to TargetQualifier")