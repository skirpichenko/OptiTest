import numpy as np
from ctypes import *
import os

def LoadLibrary(fname):
    # __file__ contains the path of the current module
    current_module_path = __file__
    # You can get the full absolute path
    absolute_path = os.path.abspath(current_module_path)
    # You can also get the directory containing the current module
    current_directory = os.path.dirname(absolute_path)
    lib = cdll.LoadLibrary(current_directory + '\\' + fname)
    return lib


lib = LoadLibrary('OREngineCPP.dll')
lib.init(0)

def CheckLicense(key: c_wchar_p):
    return lib.check_license(key)

def calc_M(wavelength, D, lpp_N, lpp_eff_N, alpha, M):
    lib.calc_M(
        len(wavelength), # nLamCount 
        len(D), # nLayers
        wavelength.ctypes.data_as(c_void_p),
        D.ctypes.data_as(c_void_p),
        lpp_N,
        lpp_eff_N,
        c_double(alpha),
        M.ctypes.data_as(c_void_p),
    )

def forward(wavelength, D, N, eff_N, alpha, M, Mp):
    lib.forward(
        len(wavelength), # nLamCount 
        len(D), # nLayers
        wavelength.ctypes.data_as(c_void_p),
        D.ctypes.data_as(c_void_p),
        np.array(N).ctypes.data_as(c_void_p),
        np.array(eff_N).ctypes.data_as(c_void_p),
        c_double(alpha),
        M.ctypes.data_as(c_void_p),
        Mp.ctypes.data_as(c_void_p),
    )


def forward_backward(wavelength, D, N, eff_N, alpha, M, Mj, DMp, DMj, precalc = True):
    lib.forward_backward(
        len(wavelength), # nLamCount 
        len(D), # nLayers
        wavelength.ctypes.data_as(c_void_p),
        D.ctypes.data_as(c_void_p),
        np.array(N).ctypes.data_as(c_void_p),
        np.array(eff_N).ctypes.data_as(c_void_p),
        c_double(alpha),
        M.ctypes.data_as(c_void_p),
        Mj.ctypes.data_as(c_void_p),
        DMp.ctypes.data_as(c_void_p),
        DMj.ctypes.data_as(c_void_p),
        c_bool(precalc),
    )


def forward_backward_last_d(wavelength, D, N, eff_N, alpha, M, Mj, DMp, DMj):
    lib.forward_backward_last_d(
        len(wavelength), # nLamCount 
        len(D), # nLayers
        wavelength.ctypes.data_as(c_void_p),
        D.ctypes.data_as(c_void_p), 
        np.array(N).ctypes.data_as(c_void_p), 
        np.array(eff_N).ctypes.data_as(c_void_p), 
        c_double(alpha), 
        M.ctypes.data_as(c_void_p), 
        Mj.ctypes.data_as(c_void_p), 
        DMp.ctypes.data_as(c_void_p), 
        DMj.ctypes.data_as(c_void_p),
    )


def forward_last_d(wavelength, D, N, eff_N, alpha, M, Mp):
    lib.forward_last_d(
        len(wavelength), # nLamCount 
        len(D), # nLayers
        wavelength.ctypes.data_as(c_void_p),
        D.ctypes.data_as(c_void_p), 
        np.array(N).ctypes.data_as(c_void_p), 
        np.array(eff_N).ctypes.data_as(c_void_p), 
        c_double(alpha), 
        M.ctypes.data_as(c_void_p), 
        Mp.ctypes.data_as(c_void_p),
    )


def forward_backward_triag(wavelength, D, N, eff_N, alpha, M, Mj, Mn, Dj):
    lib.forward_backward_triag(
        len(wavelength), # nLamCount 
        len(D), # nLayers
        wavelength.ctypes.data_as(c_void_p),
        D.ctypes.data_as(c_void_p), 
        np.array(N).ctypes.data_as(c_void_p), 
        np.array(eff_N).ctypes.data_as(c_void_p), 
        c_double(alpha), 
        M.ctypes.data_as(c_void_p), 
        Mj.ctypes.data_as(c_void_p), 
        Mn.ctypes.data_as(c_void_p), 
        Dj.ctypes.data_as(c_void_p),
    )


def forward_backward_triag_top(wavelength, D, N, eff_N, alpha, Mj, Mn, Dj, nStartLayer):
    lib.forward_backward_triag_top(
        len(wavelength), # nLamCount 
        len(D), # nLayers
        wavelength.ctypes.data_as(c_void_p),
        D.ctypes.data_as(c_void_p), 
        np.array(N).ctypes.data_as(c_void_p), 
        np.array(eff_N).ctypes.data_as(c_void_p), 
        c_double(alpha), 
        Mj.ctypes.data_as(c_void_p), 
        Mn.ctypes.data_as(c_void_p), 
        Dj.ctypes.data_as(c_void_p), 
        c_int(nStartLayer),
    )


def forward_backward_triag_top_all(wavelength, D, N, eff_N, alpha, Mj, Mn, Dj, nStartLayer, 
                               eff_na, eff_ns, lpp_props):  
    lib.forward_backward_triag_top_all(
        len(wavelength), # nLamCount 
        len(D), # nLayers
        wavelength.ctypes.data_as(c_void_p),
        D.ctypes.data_as(c_void_p), 
        np.array(N).ctypes.data_as(c_void_p), 
        np.array(eff_N).ctypes.data_as(c_void_p), 
        c_double(alpha), 
        Mj.ctypes.data_as(c_void_p), 
        Mn.ctypes.data_as(c_void_p), 
        Dj.ctypes.data_as(c_void_p), 
        c_int(nStartLayer),
        np.array([eff_na]).ctypes.data_as(POINTER(c_double)), # pEff_na
        eff_ns.ctypes.data_as(c_void_p),
        lpp_props,
    )


def update_top_props(wavelength, D, lpp_N, lpp_eff_N, eff_na, eff_ns, alpha, Mp, 
                     nStartLayer, lpp_props, bCalcDerivatives = True):  
    lib.update_top_props(
        len(wavelength), # nLamCount 
        len(D), # nLayers
        wavelength.ctypes.data_as(c_void_p),
        D.ctypes.data_as(c_void_p), 
        lpp_N,
        lpp_eff_N, 
        np.array([eff_na]).ctypes.data_as(POINTER(c_double)), # pEff_na
        eff_ns.ctypes.data_as(c_void_p),
        c_double(alpha), 
        Mp.ctypes.data_as(c_void_p),
        nStartLayer,
        lpp_props,
        c_bool(bCalcDerivatives),
    )