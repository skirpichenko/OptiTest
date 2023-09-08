import numpy as np
import numpy.typing as npt
from ORConstants import *
import OREngineNB as engine
from typing import *
import ctypes
import gc

##############################################################################
class ORProps(object):
    def __init__(self
            , eff_na: np.complex128
            , eff_ns: np.complex128
            , M: Optional[npt.NDArray[np.complex128]] = None
            , D: Optional[npt.NDArray[np.complex128]] = None
        ):
        self._init(eff_na, eff_ns)
        if M is not None:
            self._update_t_tau(M)
        if D is not None:
            self._update_dt(D)
            self._update_dtau(D)
            self._update_dtau_(D)

    def Preallocate(self, nLamCount: int, nLayers: int, nTopLayers: int):
        self.nStartLayer = max(nLayers - nTopLayers, 0)
        # allocate memory for the optical properties when the only last nTopLayers are changing
        self._t = np.zeros(nLamCount, dtype=np.complex128)
        self._t_ = np.zeros(nLamCount, dtype=np.complex128)
        self._tau = np.zeros(nLamCount, dtype=np.complex128)
        self._tau_ = np.zeros(nLamCount, dtype=np.complex128)
        self._dt = np.zeros((nLayers - self.nStartLayer, nLamCount), dtype=np.complex128)
        self._dtau = np.zeros((nLayers - self.nStartLayer, nLamCount), dtype=np.complex128)
        self._dtau_ = np.zeros((nLayers - self.nStartLayer, nLamCount), dtype=np.complex128)

    def update_top_layers(self, M: npt.NDArray[np.complex128], D: npt.NDArray[np.complex128], nStartLayer:int):
        self._update_t_tau(M)
        self._update_dt(D, nStartLayer)
        self._update_dtau(D, nStartLayer)
        self._update_dtau_(D, nStartLayer)


    def _init(self, eff_na: np.complex128, eff_ns: np.complex128):
        self.eff_na = eff_na
        self.eff_ns = eff_ns
        self._t: Optional[npt.NDArray[np.complex128]] = None
        self._t_: Optional[npt.NDArray[np.complex128]] = None # t'
        self._tau: Optional[npt.NDArray[np.complex128]] = None
        self._tau_: Optional[npt.NDArray[np.complex128]] = None # tau'
        self._dt: Optional[npt.NDArray[np.complex128]] = None
        self._dtau: Optional[npt.NDArray[np.complex128]] = None
        self._dtau_: Optional[npt.NDArray[np.complex128]] = None # dtau'
        self.nStartLayer = 0

    @property
    def c_props(self) -> ctypes.POINTER(ctypes.POINTER(ctypes.c_double)):
        # returns ctypes double** array of optical properties
        # [0] = t, [1] = t', [2] = tau, [3] = tau', [4] = dt, [5] = dtau, [6] = dtau'
        nProps = 7
        c_props = (ctypes.POINTER(ctypes.c_double) * nProps)()
        c_props[0] = self._t.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        c_props[1] = self._t_.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        c_props[2] = self._tau.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        c_props[3] = self._tau_.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        c_props[4] = self._dt.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        c_props[5] = self._dtau.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        c_props[6] = self._dtau_.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        return c_props
    

    def _update_t_tau(self, M):
        denom = (self.eff_na * M[0,0,:] + self.eff_ns * M[1,1,:] + \
                 self.eff_na * self.eff_ns * M[0,1,:] + M[1,0,:])

        self._t = 2.0 * self.eff_na / denom
        self._t_ = 2.0 * self.eff_ns / denom
        self._tau = (self.eff_na * M[0,0,:] - self.eff_ns * M[1,1,:] + \
                    self.eff_na * self.eff_ns * M[0,1,:] - M[1,0,:]) / denom
        self._tau_ = (self.eff_ns * M[1,1,:] - self.eff_na * M[0,0,:] + \
                     self.eff_na * self.eff_ns * M[0,1,:] - M[1,0,:]) / denom


    def _update_dt(self, D, nStartLayer = 0):
        c = -1. * (self._t ** 2.) / (2. * self.eff_na)
        if nStartLayer == 0:
            self._dt = self.eff_na * D[:,0,0,:] + self.eff_ns * D[:,1,1,:] + \
                       self.eff_na * self.eff_ns * D[:,0,1,:] + D[:,1,0,:]
        else:
            self._dt[nStartLayer:] = self.eff_na * D[:,0,0,:] + self.eff_ns * D[:,1,1,:] + \
                                     self.eff_na * self.eff_ns * D[:,0,1,:] + D[:,1,0,:]
            # zero out the first nStartLayer elements as they become invalid
            self._dt[:nStartLayer] = 0.0
        self._dt *= c
        

    def _update_dtau(self, D, nStartLayer = 0):
        c = 0.5 * self._t / self.eff_na
        if nStartLayer == 0:
            self._dtau  = self.eff_na * (1. - self._tau) * D[:,0,0,:]
            self._dtau -= self.eff_ns * (1. + self._tau) * D[:,1,1,:]
            self._dtau += self.eff_na * self.eff_ns * (1. - self._tau) * D[:,0,1,:]
            self._dtau -= (1. + self._tau) * D[:,1,0,:]
        else:
            self._dtau[nStartLayer:]  = self.eff_na * (1. - self._tau) * D[:,0,0,:]
            self._dtau[nStartLayer:] -= self.eff_ns * (1. + self._tau) * D[:,1,1,:]
            self._dtau[nStartLayer:] += self.eff_na * self.eff_ns * (1. - self._tau) * D[:,0,1,:]
            self._dtau[nStartLayer:] -= (1. + self._tau) * D[:,1,0,:]
            # zero out the first nStartLayer elements as they become invalid
            self._dtau[:nStartLayer] = 0.0
        self._dtau *= c


    def _update_dtau_(self, D, nStartLayer = 0):
        c = 0.5 * self._t_ / self.eff_ns
        if nStartLayer == 0:
            self._dtau_  = self.eff_ns * (1. - self._tau_) * D[:,1,1,:]
            self._dtau_ -= self.eff_na * (1. + self._tau_) * D[:,0,0,:]
            self._dtau_ += self.eff_na * self.eff_ns * (1. - self._tau_) * D[:,0,1,:]
            self._dtau_ -= (1. + self._tau_) * D[:,1,0,:]
        else:
            self._dtau_[nStartLayer:]  = self.eff_ns * (1. - self._tau_) * D[:,1,1,:]
            self._dtau_[nStartLayer:] -= self.eff_na * (1. + self._tau_) * D[:,0,0,:]
            self._dtau_[nStartLayer:] += self.eff_na * self.eff_ns * (1. - self._tau_) * D[:,0,1,:]
            self._dtau_[nStartLayer:] -= (1. + self._tau_) * D[:,1,0,:]
            # zero out the first nStartLayer elements as they become invalid
            self._dtau_[:nStartLayer] = 0.0
        self._dtau_ *= c


    def _update_d_last_d(self, D):
        # update dt
        c = -1. * (self._t ** 2.) / (2. * self.eff_na)
        self._dt[-1,:] = self.eff_na * D[-1,0,0,:] + self.eff_ns * D[-1,1,1,:] + \
                         self.eff_na * self.eff_ns * D[-1,0,1,:] + D[-1,1,0,:]
        self._dt[-1,:] *= c
        # update dtau
        c = 0.5 * self._t / self.eff_na
        self._dtau[-1,:]  = self.eff_na * (1. - self._tau) * D[-1,0,0,:]
        self._dtau[-1,:] -= self.eff_ns * (1. + self._tau) * D[-1,1,1,:]
        self._dtau[-1,:] += self.eff_na * self.eff_ns * (1. - self._tau) * D[-1,0,1,:]
        self._dtau[-1,:] -= (1. + self._tau) * D[-1,1,0,:]
        self._dtau[-1,:] *= c
        # update dtau_
        c = 0.5 * self._t_ / self.eff_ns
        self._dtau_[-1,:]  = self.eff_ns * (1. - self._tau_) * D[-1,1,1,:]
        self._dtau_[-1,:] -= self.eff_na * (1. + self._tau_) * D[-1,0,0,:]
        self._dtau_[-1,:] += self.eff_na * self.eff_ns * (1. - self._tau_) * D[-1,0,1,:]
        self._dtau_[-1,:] -= (1. + self._tau_) * D[-1,1,0,:]
        self._dtau_[-1,:] *= c

    @property
    def t(self) -> npt.NDArray[np.complex128]:
        return self._t
    
    @property
    def t_(self) -> npt.NDArray[np.complex128]:
        return self._t_
    
    @property
    def tau(self) -> npt.NDArray[np.complex128]:
        return self._tau

    @property
    def tau_(self) -> npt.NDArray[np.complex128]:
        return self._tau_

    @property
    def dt(self) -> npt.NDArray[np.complex128]:
        return self._dt
    
    @property
    def dtau(self) -> npt.NDArray[np.complex128]:
        return self._dtau

    @property
    def dtau_(self) -> npt.NDArray[np.complex128]:
        return self._dtau_

    # derivatives indexed by layers
    def Get_dTE(self, ix) -> npt.NDArray[np.complex128]:
        return 2 * np.real(self.eff_ns) / np.real(self.eff_na) * np.real(np.conj(self._t) * self._dt[ix,:])

    def Get_dRE(self, ix) -> npt.NDArray[np.complex128]:
        return 2 * np.real(np.conj(self._tau) * self._dtau[ix,:])

    def Get_dBR(self, ix) -> npt.NDArray[np.complex128]:
        return 2 * np.real(np.conj(self._tau_) * self._dtau_[ix,:])

    # full derivatives
    @property
    def dTE(self):
        return 2 * np.real(self.eff_ns) / np.real(self.eff_na) * np.real(np.conj(self._t) * self._dt)
    
    @property
    def dRE(self):
        return 2 * np.real(np.conj(self._tau) * self._dtau)

    @property
    def dBR(self):
        return 2 * np.real(np.conj(self._tau_) * self._dtau_)
    
    @property
    def TE(self):
        return np.real(self.eff_ns) / np.real(self.eff_na) * (np.real(self._t) ** 2 + np.imag(self._t) ** 2)
    
    @property
    def RE(self):
        r, i = np.real(self._tau), np.imag(self._tau)
        return r*r + i*i
    
    @property
    def BR(self):
        return np.real(self._tau_) ** 2 + np.imag(self._tau_) ** 2

    def __getitem__(self, nLayer):
        return self

    @classmethod
    def EmptyChip(cls
            , ns: np.complex128
            , na: np.complex128
            , alpha: Union[np.float64, npt.NDArray[np.float64]]
            , pol: Polarization
        ):
        if pol == Polarization.S:
            eff_ns = (ns**2 - alpha**2)**0.5
            eff_na = (na**2 - alpha**2)**0.5 
        elif pol == Polarization.P:
            eff_ns = ns**2 / (ns**2 - alpha**2)**0.5
            eff_na = na**2 / (na**2 - alpha**2)**0.5
        elif pol == Polarization.A:
            eff_ns = ns
            eff_na = na
        else:
            raise ValueError(f"Unknown polarization {str(pol)}")
        M = np.zeros((2,2,1), dtype=np.complex128)
        M[0,0,0] = 1
        M[1,1,0] = 1
        return ORProps(
            eff_na = eff_na,
            eff_ns = eff_ns,
            M = M,
            D = np.zeros((1,2,2,1), dtype=np.complex128)
        )

##############################################################################
class ORPass(object):
    def __init__(self
            , wavelength: npt.NDArray[np.float64]
            , thicknesses: npt.NDArray[np.float64]
            , refractiveIndices: List[npt.NDArray[np.complex128]]
            , substrateRefractiveIndex: npt.NDArray[np.complex128]
            , na: np.complex128
            , incidenceAngle: np.float64
            , pol: Polarization
        ):
        self.wavelength = wavelength
        self.thicknesses = thicknesses
        self.refractiveIndices = refractiveIndices
        self.substrateRefractiveIndex = substrateRefractiveIndex
        self.na = na
        self.pol = pol
        self.incidenceAngle = incidenceAngle
        self._init_eff_values()
        self._init_calc_matrices()
        # layers
        self._layers: List[Optional[ORProps]] = [None] * (self.nLayers - 1)
        self._layers.append(ORProps(eff_na = self.eff_na, eff_ns = self.eff_ns))
        self.nStartLayer = 0


    @property
    def c_refractiveIndices(self) -> ctypes.POINTER(ctypes.POINTER(ctypes.c_double)):
        c_refractiveIndices = (ctypes.POINTER(ctypes.c_double) * len(self.refractiveIndices))()
        for i, x in enumerate(self.refractiveIndices):
            c_refractiveIndices[i] = x.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        return c_refractiveIndices
 

    @property
    def c_eff_N(self) -> ctypes.POINTER(ctypes.POINTER(ctypes.c_double)):
        c_eff_N = (ctypes.POINTER(ctypes.c_double) * len(self.eff_N))()
        for i, x in enumerate(self.eff_N):
            c_eff_N[i] = x.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        return c_eff_N
    

    def _init_eff_values(self):
        def get_eff_N(func):
            d = {}
            return [d.setdefault(id(ri), func(ri)) for ri in self.refractiveIndices]

        # efective na, ns, N
        self.alpha = np.real(self.na * np.sin(2. * np.pi * self.incidenceAngle / 360.0))
        self.eff_N = np.empty((len(self.thicknesses), len(self.wavelength)), dtype=np.complex128)
        if self.pol == Polarization.S:
            self.eff_ns = (self.substrateRefractiveIndex ** 2 - self.alpha ** 2) ** 0.5
            self.eff_na = (self.na ** 2 - self.alpha ** 2) ** 0.5
            self.eff_N = get_eff_N(lambda ri: (ri ** 2 - self.alpha ** 2) ** 0.5)
        elif self.pol == Polarization.P:
            self.eff_ns = self.substrateRefractiveIndex ** 2 / (self.substrateRefractiveIndex ** 2 - self.alpha ** 2) ** 0.5
            self.eff_na = self.na ** 2 / (self.na ** 2 - self.alpha ** 2) ** 0.5
            self.eff_N = get_eff_N(lambda ri: ri ** 2 / (ri ** 2 - self.alpha ** 2) ** 0.5)
        else:
            self.eff_ns = self.substrateRefractiveIndex
            self.eff_na = self.na
            self.eff_N = self.refractiveIndices


    def _init_calc_matrices(self):
        self.M: Optional[npt.NDArray[np.complex128]] = None  # np.complex128[:,:,:]
        self.Mp: Optional[npt.NDArray[np.complex128]] = None # np.complex128[:,:,:]
        self.Mj: Optional[npt.NDArray[np.complex128]] = None # np.complex128[:,:,:,:]
        self.DMj: Optional[npt.NDArray[np.complex128]] = None # np.complex128[:,:,:,:]
        # precomputed matrixes for the the case when only the last layer changes
        # DMp[:] = Inv(Mm) * DMj[:]  (DMj not multiplied by Mm)
        # DMp[m] = Mm-1...M1
        self.DMp: Optional[npt.NDArray[np.complex128]] = None # np.complex128[:,:,:,:]
        # triangular mode pre-computations
        # Mn = Mn*...*M1*M0
        self.Mn: Optional[npt.NDArray[np.complex128]] = None # np.complex128[:,:,:,:]
        self.Dj: Optional[npt.NDArray[np.complex128]] = None # np.complex128[:,:,:,:]

    def __str__(self):
        return f'Pass: wavelength={self.wavelength}, thicknesses={self.thicknesses}, refractiveIndices={self.refractiveIndices}, \
            substrateRefractiveIndex={self.substrateRefractiveIndex}, na={self.na}, pol={self.pol}, incidenceAngle={self.incidenceAngle}'
    def __repr__(self):
        return self.__str__()

    @property
    def nLayers(self):
        return len(self.thicknesses)

    def __getitem__(self, nLayer) -> ORProps:
        return self._layers[nLayer]
    
    def __len__(self) -> int:
        return len(self._layers)

    def InitTopLayers(self, nTopLayers: int):
        self.nStartLayer = max(0, self.nLayers - nTopLayers)
        for nLayer in range(self.nStartLayer, self.nLayers):
            self._layers[nLayer] = ORProps(eff_na = self.eff_na, eff_ns = self.eff_ns)
            self._layers[nLayer].Preallocate(
                nLamCount = len(self.wavelength),
                nLayers = nLayer + 1,
                nTopLayers = nLayer - self.nStartLayer + 1,
            )
        if self.nStartLayer > 0:
            self.CalcM(self.nStartLayer)
        else:
            self.M = np.empty((2, 2, len(self.wavelength)), dtype = np.complex128)
            self.M[0,0,:] = 1.0
            self.M[0,1,:] = 0.0
            self.M[1,0,:] = 0.0
            self.M[1,1,:] = 1.0


    def UpdateTopLayers(self, bCalcDerivatives: bool = True):
        lpp_props = (ctypes.POINTER(ctypes.POINTER(ctypes.c_double)) * (self.nLayers - self.nStartLayer + 1))()
        for n in range(self.nStartLayer, self.nLayers):
            lpp_props[n-self.nStartLayer] = self._layers[n].c_props

        engine.update_top_props(
            self.wavelength, 
            self.thicknesses,
            self.c_refractiveIndices,
            self.c_eff_N, 
            self.eff_na, 
            self.eff_ns, 
            self.alpha, 
            self.M,
            self.nStartLayer, 
            lpp_props,
            bCalcDerivatives,
        )

    def CalcM(self, nLayers: int = -1):
        self.M = np.empty((2, 2, len(self.wavelength)), dtype = np.complex128)
        if len(self.thicknesses[:nLayers]) > 0:
            engine.calc_M(
                self.wavelength,
                self.thicknesses[:nLayers],
                self.c_refractiveIndices,
                self.c_eff_N,
                self.alpha,
                self.M,
            )
        else:
            self.M[0,0,:] = 1.0
            self.M[0,1,:] = 0.0
            self.M[1,0,:] = 0.0
            self.M[1,1,:] = 1.0
    

    def Forward(self):
        self.M = np.empty((2, 2, len(self.wavelength)), dtype = np.complex128)
        self.Mp = np.empty((2, 2, len(self.wavelength)), dtype = np.complex128)
        engine.forward(
            self.wavelength,
            self.thicknesses,
            self.refractiveIndices,
            self.eff_N,
            self.alpha,
            self.M,
            self.Mp
        )
        self._layers[-1]._update_t_tau(self.M)


    def ForwardBackward(self, precalc: bool = False):
        self.M = np.empty((2, 2, len(self.wavelength)), dtype = np.complex128)
        self.Mj = np.empty((len(self.thicknesses), 2, 2, len(self.wavelength)), dtype = np.complex128)
        self.DMj = np.empty_like(self.Mj)
        if precalc:
            self.DMp = np.empty((len(self.thicknesses), 2, 2, len(self.wavelength)), dtype = np.complex128)
        engine.forward_backward(
            self.wavelength,
            self.thicknesses,
            self.refractiveIndices,
            self.eff_N,
            self.alpha,
            self.M,
            self.Mj,
            self.DMp,
            self.DMj,
            precalc
        )
        # TODO: lazy update
        self._layers[-1]._update_t_tau(self.M)
        self._layers[-1]._update_dt(self.DMj)
        self._layers[-1]._update_dtau(self.DMj)
        self._layers[-1]._update_dtau_(self.DMj)


    def ForwardBackwardLastD(self):
        if self.DMp is None:
            raise Exception('DMp is None. Make sure forward_backward_pass(result, True) is called previously.')
        engine.forward_backward_last_d(
            self.wavelength,
            self.thicknesses,
            self.refractiveIndices,
            self.eff_N,
            self.alpha,
            self.M,
            self.Mj,
            self.DMp,
            self.DMj
        )
        # TODO: lazy update
        self._layers[-1]._update_t_tau(self.M)
        self._layers[-1]._update_d_last_d(self.DMj)


    def ForwardLastD(self):
        if self.Mp is None:
            raise Exception("Mp matrix hasn't been calculated")
        engine.forward_last_d(
            self.wavelength,
            self.thicknesses,
            self.refractiveIndices,
            self.eff_N,
            self.alpha,
            self.M,
            self.Mp
        )
        self._layers[-1]._update_t_tau(self.M)


    def ForwardBackwardTriag(self, update = True):
        self.M = np.empty((2, 2, len(self.wavelength)), dtype = np.complex128)
        self.Mj = np.empty((len(self.thicknesses), 2, 2, len(self.wavelength)), dtype = np.complex128)
        self.Dj = np.empty_like(self.Mj)
        self.Mn = np.empty_like(self.Mj)
        engine.forward_backward_triag(
            self.wavelength,
            self.thicknesses,
            self.refractiveIndices,
            self.eff_N,
            self.alpha,
            self.M,
            self.Mj,
            self.Mn,
            self.Dj
        )
        if update:
            self._update_layers()


    def ForwardBackwardTriagTopOld(self, nStartLayer: int, update = True):
        if self.Mn is None or self.Dj is None or self.Mj is None:
            raise Exception("The ForwardBackwardTriag hasn't been ran.")
        engine.forward_backward_triag_top(
            self.wavelength,
            self.thicknesses,
            self.refractiveIndices,
            self.eff_N,
            self.alpha,
            self.Mj,
            self.Mn,
            self.Dj,
            nStartLayer
        )
        if update:
            self._update_top_layers(nStartLayer)

    def ForwardBackwardTriagTop(self, nStartLayer: int):
        if self.Mn is None or self.Dj is None or self.Mj is None:
            raise Exception("The ForwardBackwardTriag hasn't been ran.")

        nLayers = self.Mj.shape[0]
        lpp_props = (ctypes.POINTER(ctypes.POINTER(ctypes.c_double)) * (nLayers - nStartLayer + 1))()
        for n in range(nStartLayer, nLayers):
            lpp_props[n-nStartLayer] = self._layers[n].c_props

        engine.forward_backward_triag_top_all(
            self.wavelength,
            self.thicknesses,
            self.refractiveIndices,
            self.eff_N,
            self.alpha,
            self.Mj,
            self.Mn,
            self.Dj,
            nStartLayer,
            self.eff_na,
            self.eff_ns,
            lpp_props,
        )


    def _update_layers(self):
        Mj = self.Mj
        Mn = self.Mn
        Dj = self.Dj
        if Mj is None or Dj is None:
            raise RuntimeError("Pass.ForwardBackwardTriag() must be called first")
        nLayers = Mj.shape[0]
        self._layers = []
        gc.collect()
        DMj = np.copy(Dj)
        for n in range(nLayers):
            if n > 0:
                for j in range(n):
                    DMj[j,:,:,:] = np.einsum('ijw,jkw->ikw', Mj[n,:,:,:], DMj[j,:,:,:])
            self._layers.append(ORProps(
                eff_na = self.eff_na,
                eff_ns = self.eff_ns,
                M = Mn[n,:,:,:],
                D = DMj[:(n+1),:,:,:],
            ))


    def _update_top_layers(self, nStartLayer: int):
        Mj = self.Mj
        Mn = self.Mn
        Dj = self.Dj

        nLayers = Mj.shape[0]
        nLam = Mj.shape[3]
        if len(self._layers) != nLayers:
            raise Exception('Run _update_layers first')

        for n in range(nStartLayer, nLayers):
            DMj = np.empty((n-nStartLayer+1,2,2,nLam), dtype=np.complex128)
            DMj[-1,:,:,:] = Dj[n,:,:,:]
            if n > nStartLayer:
                DMj[:-1,:,:,:] = last_DMj
                for j in range(n - nStartLayer):
                    DMj[j,:,:,:] = np.einsum('ijw,jkw->ikw', Mj[n,:,:,:], DMj[j,:,:,:])
            last_DMj = DMj
            self._layers[n].update_top_layers(
                M = Mn[n,:,:,:], 
                D = DMj, 
                nStartLayer = nStartLayer
            )


    def _update_top_layers2(self, nStartLayer: int):
        Mj = self.Mj
        Mn = self.Mn
        Dj = self.Dj

        nLayers = Mj.shape[0]
        nLam = Mj.shape[3]
        if len(self._layers) != nLayers:
            raise Exception('Run _update_layers first')

        DMj = np.empty((nLayers-nStartLayer+1,2,2,nLam), dtype=np.complex128)
        for n in range(nStartLayer, nLayers):
            DMj[n-nStartLayer,:,:,:] = Dj[n,:,:,:]
            if n > nStartLayer:
                for j in range(n - nStartLayer):
                    DMj[j,:,:,:] = np.einsum('ijw,jkw->ikw', Mj[n,:,:,:], DMj[j,:,:,:])

            engine.lib.update_oprops(
                nLam,
                n, # nLayers
                Mn.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                DMj.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                np.array([self.eff_na]).ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                self.eff_ns.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                nStartLayer,
                self._layers[n].c_props,
            )


    def _update_top_layers3(self, nStartLayer: int):
        Mj = self.Mj
        Mn = self.Mn
        Dj = self.Dj

        nLayers = Mj.shape[0]
        nLam = Mj.shape[3]
        if len(self._layers) != nLayers:
            raise Exception('Run _update_layers first')

        lpp_props = (ctypes.POINTER(ctypes.POINTER(ctypes.c_double)) * (nLayers - nStartLayer + 1))()
        for n in range(nStartLayer, nLayers):
            lpp_props[n-nStartLayer] = self._layers[n].c_props

        engine.lib.update_top_layers(
            nLam,
            nLayers,
            Mj.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            Mn.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            Dj.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            np.array([self.eff_na]).ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            self.eff_ns.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            nStartLayer,
            lpp_props,
        )

    @property
    def t(self) -> npt.NDArray[np.complex128]:
        return self._layers[-1]._t
    
    @property
    def t_(self) -> npt.NDArray[np.complex128]:
        return self._layers[-1]._t_
    
    @property
    def tau(self) -> npt.NDArray[np.complex128]:
        return self._layers[-1]._tau

    @property
    def tau_(self) -> npt.NDArray[np.complex128]:
        return self._layers[-1]._tau_

    @property
    def dt(self) -> npt.NDArray[np.complex128]:
        return self._layers[-1]._dt
    
    @property
    def dtau(self) -> npt.NDArray[np.complex128]:
        return self._layers[-1]._dtau

    @property
    def dtau_(self) -> npt.NDArray[np.complex128]:
        return self._layers[-1]._dtau_

    # derivatives indexed by layers
    def Get_dTE(self, ix):
        return self._layers[-1].Get_dTE(ix)

    def Get_dRE(self, ix):
        return self._layers[-1].Get_dRE(ix)

    def Get_dBR(self, ix):
        return self._layers[-1].Get_dBR(ix)

    # full derivatives
    @property
    def dTE(self):
        return self._layers[-1].dTE
    
    @property
    def dRE(self):
        return self._layers[-1].dRE

    @property
    def dBR(self):
        return self._layers[-1].dBR
    
    @property
    def TE(self):
        return self._layers[-1].TE
    
    @property
    def RE(self):
        return self._layers[-1].RE
    
    @property
    def BR(self):
        return self._layers[-1].BR

####################################################################################################
class OptiProps(object):
    def __init__(self
            , thicknesses: npt.NDArray[np.float64]
            , wavelength: npt.NDArray[np.float64]
            , refractiveIndices: List[npt.NDArray[np.complex128]]
            , substrateRefractiveIndex: npt.NDArray[np.complex128]
            , pol: Polarization = Polarization.A
            , incidenceAngle: np.float64 = 0.0
            , na: np.complex128 = np.complex128(1 + 0j)
            , rt_units: RTUnits = RTUnits.DEFAULT
            , backSideMatters = False
            , backSideThickness: np.float64 = 1.0 # in mm
            , lineMask: Optional[npt.NDArray[np.float64]] = None
        ):
        # TODO: replace with parameter
        if lineMask is None:
            # Pascal triangle of 7 elements
            lineMask = np.array([1, 6, 15, 20, 15, 6, 1], dtype=np.float64)

        if lineMask is not None and len(lineMask) % 2 == 0:
            raise Exception("lineMask has to have an odd number of elements")
        if len(thicknesses) != len(refractiveIndices):
            raise Exception("The size of refractive index data doesn't match layer thicknesses.") 
        # normalize lineMask to sum to 1 and flip (check np.covolve why)
        self.lineMask = (lineMask / np.sum(lineMask))[::-1] if lineMask is not None else None
        self.thicknesses = thicknesses
        self.wavelength = wavelength
        self.refractiveIndices = refractiveIndices
        self.substrateRefractiveIndex = substrateRefractiveIndex
        self.pol = pol
        self.incidenceAngle = np.float64(incidenceAngle)
        self.na = np.complex128(na)
        self.rt_units = rt_units
        self.meta: Dict[str, Any] = {} # for user to store any data
        self.backSideMatters = backSideMatters
        self.backSideThickness = backSideThickness
        # front side optical properties (p,s or p and s cases)
        self.ps: Optional[ORPass] = None
        self.ps_p: Optional[ORPass] = None
        # back side optical properties (p,s or p and s cases)
        self.bps: Optional[ORPass] = None
        self.bps_p: Optional[ORPass] = None
        # ash to adjust for a non zero extinsion of the back side
        self.ash: Optional[npt.NDArray[np.float64]] = None
        # Initialize numba objects
        self._init_nb_objects()


    # Returns the state of the object to be pickled.
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['assembly']
        del state['light']
        del state['ps']
        del state['ps_p']
        del state['bps']
        del state['bps_p']
        return state
    # Sets the state of the object after being unpickled.
    def __setstate__(self, state):
        self.__dict__.update(state)
        self._init_nb_objects()

    def _convolve_with_normalization(self
            , x: npt.NDArray[np.float64]
            , w: npt.NDArray[np.float64]
        ) -> npt.NDArray[np.float64]:
        # Regular convolution
        y = np.convolve(x, w, mode='same')
        # Normalization for the beginning and end of the vector
        filter_size = len(w)
        half_filter_size = filter_size // 2
        for i in range(half_filter_size):
            y[i] /= np.sum(w[:half_filter_size + i + 1])
            y[-(i+1)] /= np.sum(w[half_filter_size - i:])
        return y

    def _apply_line_mask(self, x: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        if self.lineMask is None:
            return x
        if len(x.shape) == 1:
            return self._convolve_with_normalization(x, self.lineMask)
        else:
            # iterate over the first dimension
            for i in range(x.shape[0]):
                x[i,:] = self._convolve_with_normalization(x[i,:], self.lineMask)
            return x

    def _init_nb_objects(self):
        # Snell's law
        alpha = self.na * np.sin(2. * np.pi * self.incidenceAngle / 360.0)
        if self.backSideMatters:
            # print (self.substrateRefractiveIndex)
            x = np.imag((self.substrateRefractiveIndex ** 2 - alpha ** 2) ** 0.5)
            # print (x)
            x *= 4 * np.pi * self.backSideThickness * 1e6 # in nm
            # print (x)
            x /= self.wavelength
            # print (x)
            self.ash = np.exp(x)
            # print (f"ash = {self.ash}")

        if self.onePass:
            if len(self.thicknesses) > 0:
                self.ps = ORPass(
                    wavelength = self.wavelength,
                    thicknesses = self.thicknesses,
                    refractiveIndices = self.refractiveIndices,
                    substrateRefractiveIndex = self.substrateRefractiveIndex,
                    na = self.na,
                    incidenceAngle = self.incidenceAngle,
                    pol = self.pol
                )
            else:
                self.ps = ORProps.EmptyChip(
                      ns = self.substrateRefractiveIndex
                    , na = self.na
                    , alpha = alpha
                    , pol = self.pol
                )
            if self.backSideMatters:
                # TODO: implement back side coating case
                self.bps = ORProps.EmptyChip(
                          ns = self.na
                        , na = self.substrateRefractiveIndex
                        , alpha = alpha
                        , pol = self.pol
                    )
        else:
            if len(self.thicknesses) > 0:
                self.ps = ORPass(
                    wavelength = self.wavelength,
                    thicknesses = self.thicknesses,
                    refractiveIndices = self.refractiveIndices,
                    substrateRefractiveIndex = self.substrateRefractiveIndex,
                    na = self.na,
                    incidenceAngle = self.incidenceAngle,
                    pol = Polarization.S
                )
                self.ps_p = ORPass(
                    wavelength = self.wavelength,
                    thicknesses = self.thicknesses,
                    refractiveIndices = self.refractiveIndices,
                    substrateRefractiveIndex = self.substrateRefractiveIndex,
                    na = self.na,
                    incidenceAngle = self.incidenceAngle,
                    pol = Polarization.P
                )
            else:
                self.ps = ORProps.EmptyChip(
                      ns = self.substrateRefractiveIndex
                    , na = self.na
                    , alpha = alpha
                    , pol = Polarization.S
                )
                self.ps_p = ORProps.EmptyChip(
                      ns = self.substrateRefractiveIndex
                    , na = self.na
                    , alpha = alpha
                    , pol =  Polarization.P
                )
            if self.backSideMatters:
                # TODO: implement back side coating case
                self.bps = ORProps.EmptyChip(
                      ns = self.na
                    , na = self.substrateRefractiveIndex
                    , alpha = alpha
                    , pol = Polarization.S
                )
                self.bps_p = ORProps.EmptyChip(
                      ns = self.na
                    , na = self.substrateRefractiveIndex
                    , alpha = alpha
                    , pol =  Polarization.P
                )

    def __str__(self):
        s = [
            f"th: {self.thicknesses}",
            f"lam: {self.wavelength}",
            f"ri: {self.refractiveIndices}",
            f"sri: {self.substrateRefractiveIndex}",
            f"pol: {self.pol}",
            f"angle: {self.incidenceAngle}",
            f"na: {self.na}",
            f"rt_units: {self.rt_units}",
            f"ps: {self.ps}",
            f"ps_p: {self.ps_p}",
            f"backSide: {self.backSideMatters}",
        ]
        return ','.join(s)
    
    @property
    def nLayers(self) -> int:
        return len(self.thicknesses)

    @property
    def onePass(self) -> bool:
        return self.incidenceAngle == 0.0 or self.pol != Polarization.A

    @property
    def TE(self) -> npt.NDArray[np.float64]:
        return self.GetTE(-1)
    
    def GetTE(self, nLayer: int) -> npt.NDArray[np.float64]:
        if self.backSideMatters:
            formula = lambda T1,T2,R1,R2_: T1 * T2 * self.ash / (1 - R1 * R2_ * self.ash * self.ash)
            if self.onePass:
                return formula(self.bps.TE, self.ps[nLayer].TE, self.bps.RE, self.ps[nLayer].BR)
            else:
                return 0.5 * formula(self.bps.TE, self.ps[nLayer].TE, self.bps.RE, self.ps[nLayer].BR) + \
                       0.5 * formula(self.bps_p.TE, self.ps_p[nLayer].TE, self.bps_p.RE, self.ps_p[nLayer].BR)
        else:
            return self.ps[nLayer].TE if self.onePass else  0.5 * (self.ps[nLayer].TE + self.ps_p[nLayer].TE)

    @property
    def RE(self) -> npt.NDArray[np.float64]:
        return self.GetRE(-1)

    def GetRE(self, nLayer: int) -> npt.NDArray[np.float64]:
        if self.backSideMatters:
            def formula(R1, R2, T2, R2_):
                aa = self.ash * self.ash
                return R2 + R1 * T2 * T2 * aa / (1 - R1 * R2_ * aa)
            if self.onePass:
                return formula(self.bps.RE, self.ps[nLayer].RE, self.ps[nLayer].TE, self.ps[nLayer].BR)
            else:
                return 0.5 * formula(self.bps.RE, self.ps[nLayer].RE, self.ps[nLayer].TE, self.ps[nLayer].BR) + \
                       0.5 * formula(self.bps_p.RE, self.ps_p[nLayer].RE, self.ps_p[nLayer].TE, self.ps_p[nLayer].BR)
        else:
            return self.ps[nLayer].RE if self.onePass else 0.5 * (self.ps[nLayer].RE + self.ps_p[nLayer].RE)

    @property
    def BR(self) -> npt.NDArray[np.float64]:
        return self.GetBR(-1)

    def GetBR(self, nLayer: int) -> npt.NDArray[np.float64]:
        if self.backSideMatters:
            def formula(R1,R1_,R2_,T1):
                aa = self.ash * self.ash
                return R1_ + R2_ * T1 * T1 * aa / (1 - R1 * R2_ * aa)
            if self.onePass:
                return formula(self.bps.RE, self.bps.BR, self.ps[nLayer].BR, self.bps.TE)
            else:
                return 0.5 * formula(self.bps.RE, self.bps.BR, self.ps[nLayer].BR, self.bps.TE) + \
                       0.5 * formula(self.bps_p.RE, self.bps_p.BR, self.ps_p[nLayer].BR, self.bps_p.TE)
        else:
            return self.ps[nLayer].BR if self.onePass else 0.5 * (self.ps[nLayer].BR + self.ps_p[nLayer].BR)

    @property
    def dTE(self) -> npt.NDArray[np.float64]:
        return self.GetdTE(-1)

    # slice(None) is equivalent to ':'
    def GetdTE(self, nLayer: int, ix = slice(None)) -> npt.NDArray[np.float64]:
        if self.backSideMatters:
            def formula(T1, T2, R1, R2_, dT2, dR2_):
                a = self.ash
                aa = self.ash * self.ash
                denom = 1. - R1 * R2_ * aa
                return a * T1 * (dT2 * denom + R1 * dR2_ * aa * T2) / (denom * denom)
            if self.onePass:
                return formula(self.bps.TE, self.ps[nLayer].TE, self.bps.RE, self.ps[nLayer].BR, 
                               self.ps[nLayer].Get_dTE(ix), self.ps[nLayer].Get_dBR(ix))
            else:
                return 0.5 * formula(self.bps.TE, self.ps[nLayer].TE, self.bps.RE, self.ps[nLayer].BR, 
                                     self.ps[nLayer].Get_dTE(ix), self.ps[nLayer].Get_dBR(ix)) + \
                       0.5 * formula(self.bps_p.TE, self.ps_p[nLayer].TE, self.bps_p.RE, self.ps_p[nLayer].BR,
                                     self.ps_p[nLayer].Get_dTE(ix), self.ps_p[nLayer].Get_dBR(ix))
        else:
            return self.ps[nLayer].Get_dTE(ix) if self.onePass else  \
                   0.5 * (self.ps[nLayer].Get_dTE(ix) + self.ps_p[nLayer].Get_dTE(ix))

    def GetdRE(self, nLayer: int, ix = slice(None)) -> npt.NDArray[np.float64]:
        # RE = R2 + R1 * T2 * T2 * aa / (1 - R1 * R2_ * aa)
        if self.backSideMatters:
            def formula(R1, T2, R2_, dR2, dT2, dR2_):
                aa = self.ash * self.ash
                denom = 1. - R1 * R2_ * aa

                return dR2 + aa * T2 * R1 * (2 * dT2 * denom + R1 * dR2_ * T2 * aa) / (denom * denom)
            
            if self.onePass:
                return formula(
                    R1 = self.bps.RE, 
                    T2 = self.ps[nLayer].TE, 
                    R2_ = self.ps[nLayer].BR, 
                    dR2 = self.ps[nLayer].Get_dRE(ix),
                    dT2 = self.ps[nLayer].Get_dTE(ix),
                    dR2_ = self.ps[nLayer].Get_dBR(ix),
                )
            else:
                return 0.5 * formula(self.bps.RE, self.ps[nLayer].TE, self.ps[nLayer].BR, 
                                     self.ps[nLayer].Get_dRE(ix), self.ps[nLayer].Get_dTE(ix), self.ps[nLayer].Get_dBR(ix)) + \
                       0.5 * formula(self.bps_p.RE, self.ps_p[nLayer].TE, self.ps_p[nLayer].BR,
                                     self.ps_p[nLayer].Get_dRE(ix), self.ps_p[nLayer].Get_dTE(ix), self.ps_p[nLayer].Get_dBR(ix))
        else:
            return self.ps[nLayer].Get_dRE(ix) if self.onePass else  \
                   0.5 * (self.ps[nLayer].Get_dRE(ix) + self.ps_p[nLayer].Get_dRE(ix))

    def GetdBR(self, nLayer: int, ix = slice(None)) -> npt.NDArray[np.float64]:
        if self.backSideMatters:
            def formula(R1, T1, R2_, dR2_):
                aa = self.ash * self.ash
                denom = 1. - R1 * R2_ * aa
                return aa * dR2_ * T1 * T1 * (denom + R1 * aa * R2_) / (denom * denom)
            
            if self.onePass:
                return formula(
                    R1 = self.bps.RE, 
                    T1 = self.bps.TE, 
                    R2_ = self.ps[nLayer].BR, 
                    dR2_ = self.ps[nLayer].Get_dBR(ix),
                )
            else:
                return 0.5 * formula(self.bps.RE, self.bps.TE, self.ps[nLayer].BR, 
                                     self.ps[nLayer].Get_dBR(ix)) + \
                       0.5 * formula(self.bps_p.RE, self.bps_p.TE, self.ps_p[nLayer].BR,
                                     self.ps_p[nLayer].Get_dBR(ix))
        else:
            return self.ps[nLayer].Get_dBR(ix) if self.onePass else  \
                   0.5 * (self.ps[nLayer].Get_dBR(ix) + self.ps_p[nLayer].Get_dBR(ix))


    @property
    def dRE(self) -> npt.NDArray[np.float64]:
        return self.GetdRE(-1)

    @property
    def dBR(self) -> npt.NDArray[np.float64]:
        return self.GetdBR(-1)

    def InitTopLayers(self, nTopLayers: int):
        if self.nLayers > 0:
            self.ps.InitTopLayers(nTopLayers)
            if not self.onePass:
                self.ps_p.InitTopLayers(nTopLayers)

    def UpdateTopLayers(self, bCalcDerivatives: bool = True):
        if self.nLayers > 0:
            self.ps.UpdateTopLayers(bCalcDerivatives)
            if not self.onePass:
                self.ps_p.UpdateTopLayers(bCalcDerivatives)

    def CalcM(self):
        if self.nLayers > 0:
            self.ps.CalcM()
            if not self.onePass:
                self.ps_p.CalcM()

    def Forward(self):
        if self.nLayers > 0:
            self.ps.Forward()
            if not self.onePass:
                self.ps_p.Forward()

    def ForwardLastD(self):
        if self.nLayers > 0:
            self.ps.ForwardLastD()
            if not self.onePass:
                self.ps_p.ForwardLastD()

    def ForwardBackward(self, precalc = True):
        if self.nLayers > 0:
            self.ps.ForwardBackward(precalc)
            if not self.onePass:
                self.ps_p.ForwardBackward(precalc)

    def ForwardBackwardLastD(self):
        if self.nLayers > 0:
            self.ps.ForwardBackwardLastD()
            if not self.onePass:
                self.ps_p.ForwardBackwardLastD()

    def ForwardBackwardTriag(self):
        if self.nLayers > 0:
            self.ps.ForwardBackwardTriag()
            if not self.onePass:
                self.ps_p.ForwardBackwardTriag()

    def ForwardBackwardTriagTop(self, nStartLayer: int):
        if self.nLayers > 0:
            self.ps.ForwardBackwardTriagTop(nStartLayer)
            if not self.onePass:
                self.ps_p.ForwardBackwardTriagTop(nStartLayer)

    @property
    def dLastTE(self):
        return self.ps.dLastTE if self.onePass else 0.5 * (self.ps.dLastTE + self.ps_p.dLastTE)

    def GetRawData(self, rt_data: DataType, nLayer: int = -1) -> npt.NDArray[np.float64]:
        if rt_data == DataType.REFL:
            ret = self.GetRE(nLayer)
        elif rt_data == DataType.TRANS:
            ret = self.GetTE(nLayer)
        elif rt_data == DataType.BREFL:
            ret = self.GetBR(nLayer)
        else:
            raise NotImplementedError(f"Data type {rt_data} is not implemented")
        return self._apply_line_mask(ret)
        
    # get optical property at a specific layer, -1 for the last layer
    def GetData(self, rt_data: DataType, nLayer: int = -1) -> npt.NDArray[np.float64]:
        data = self.GetRawData(rt_data, nLayer)
        # convert to user units
        if self.rt_units == RTUnits.ABS:
            return data
        elif self.rt_units == RTUnits.PERCENT:
            return 100 * data
        else:
            raise NotImplementedError(f"RT units {self.rt_units} is not implemented")

    def GetRawGrad(self, rt_data: DataType, nLayer: int = -1, ix = slice(None)) -> npt.NDArray[np.float64]:
        # ix = -1 if bLast else slice(None)
        if rt_data == DataType.REFL:
            ret = self.GetdRE(nLayer, ix)
        elif rt_data == DataType.TRANS:
            ret = self.GetdTE(nLayer, ix)
        elif rt_data == DataType.BREFL:
            ret = self.GetdBR(nLayer, ix)
        else:
            raise NotImplementedError(f"Data type {rt_data} is not implemented")
        return self._apply_line_mask(ret)

    def GetGrad(self, rt_data: DataType, nLayer: int = -1, ix = slice(None)) -> npt.NDArray[np.float64]:
        data = self.GetRawGrad(rt_data, nLayer, ix)
        # convert to user units
        if self.rt_units == RTUnits.ABS:
            return data
        elif self.rt_units == RTUnits.PERCENT:
            return 100 * data
        else:
            raise NotImplementedError(f"RT units {self.rt_units} is not implemented")

