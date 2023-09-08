from typing import *
from cffi import FFI
import numpy as np
from ctypes import *
import traceback
import gc
import datetime
import OREngineNB

ffi = FFI()

class Instance(object):
    BUFFER_SIZE: int = 2048
    _last_handle: int = 0

    versionMinor = 1
    versionMajor = 0
    version = "1.0"

    def __init__(self):
        self.last_error: str = ''
        Instance._last_handle += 1
        self._hinstance = self._last_handle
        # burrers to return to C++ without the risk to be garbage collected
        self._char_buf = ffi.new('char[]', self.BUFFER_SIZE)
        self._wchar_buf = ffi.new('wchar_t[]', self.BUFFER_SIZE)
        self._stop_immidiately = False
        self.creationDatetime = datetime.datetime.now()
    @property
    def id(self) -> int:
        return self._hinstance

    # Returns the state of the object to be pickled.
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_char_buf'] 
        del state['_wchar_buf']
        return state
    # Sets the state of the object after being unpickled.
    def __setstate__(self, state):
        self.__dict__.update(state)
        self._char_buf = ffi.new('char[]', self.BUFFER_SIZE)
        self._wchar_buf = ffi.new('wchar_t[]', self.BUFFER_SIZE)

    def GetLastErrorC(self, err: str = None) -> c_char_p:
        err = self.last_error if err is None else err
        chars2copy = min(len(err), self.BUFFER_SIZE-1)
        ffi.memmove(self._char_buf, err.encode('ascii'), chars2copy)
        # Add the null terminator manually
        ffi.memmove(ffi.addressof(self._char_buf, chars2copy), b'\x00', 1)
        return self._char_buf
    
    def GetLastErrorW(self, err: str = None) -> c_wchar_p:
        err = self.last_error if err is None else err
        chars2copy = min(len(err), self.BUFFER_SIZE-1)
        ffi.memmove(self._wchar_buf, err.encode('utf-16-le'), chars2copy*2)
        # Add the null terminator manually
        ffi.memmove(ffi.addressof(self._wchar_buf, chars2copy*2), b'\x00\x00', 2)
        return self._wchar_buf

    def Stop(self):
        self._stop_immidiately = True


class ORContext:
    _instances: Dict[int, Instance] = {}
    _base_folder: Optional[str] = None
    _has_license: bool = False
    _no_handle_err_c = ffi.new('char[]', b"An instance with a given handle doesn't exist.")
    _no_handle_err_w = ffi.new('wchar_t[]', "An instance with a given handle doesn't exist.")

    @classmethod
    def Init(cls, base_folder: str):
        cls._base_folder = base_folder
        # check if the license is valid
        try:
            with open(f"{base_folder}/License/license.json", 'r', encoding='utf-8') as f:
                lic = f.read()
                cls._has_license = OREngineNB.CheckLicense(ffi.new('wchar_t[]', lic))
        except:
            cls._has_license = False
    
    @classmethod
    def AttachInstance(cls, instance: Instance) -> int:
        if instance.id in cls._instances:
            raise ValueError(f"An instance with handle #{instance.id} already exists.")
        cls._instances[instance.id] = instance
        return instance.id

    @classmethod
    def StopAllInstances(cls):
        for instance in cls._instances.values():
            instance._stop_immidiately = True

    @classmethod
    def DetachInstance(cls, instance: Instance) -> bool:
        if instance.id in cls._instances:
            del cls._instances[instance.id]
            gc.collect()
            return True
        return False
    
    @classmethod
    def GetLastError(cls, handle: int) -> str:
        if handle in cls._instances:
            return cls._instances[handle].last_error
        else:
            return f"An instance with a given handle doesn't exist."

    @classmethod
    def GetLastErrorC(cls, handle: int) -> c_char_p:
        if handle in cls._instances:
            return cls._instances[handle].GetLastErrorC()
        else:
            return cls._no_handle_err_c
        
    @classmethod
    def GetLastErrorW(cls, handle: int) -> c_wchar_p:
        if handle in cls._instances:
            return cls._instances[handle].GetLastErrorW()
        else:
            return cls._no_handle_err_w
    
    def __init__(self, handle: int, func_name: str = ''):
        self._handle = handle
        self._func_name = func_name
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            if self._handle in self._instances:
                # TODO: log exception
                s = ''.join(traceback.format_exception(exc_type, exc_val, exc_tb))
                # print (''.join(traceback.format_exception(exc_type, exc_val, exc_tb)))
                # self._instances[self._handle].last_error = f"{self._func_name}: {exc_type.__name__} {exc_val}"
                self._instances[self._handle].last_error = f"{self._func_name}: {s}"
            return True

    def __call__(self):
        return self.instance

    @property
    def instance(self):
        if self._handle not in self._instances:
            raise ValueError(f"An instance with handle #{self._handle} doesn't exist.")
        return self._instances[self._handle]

# decorator
def reopt_handler(func):
    def wrapper(handle: int, *args, **kwargs) -> bool:
        with ORContext(handle, func.__name__) as ctx:
            reopt = ctx()
            if reopt.__class__.__name__ != 'ReOpt':
                ctx.last_error = f"{func.__name__}: The given handle doesn't point to a ReOpt instance."
                return False
#            # log this call
#            params = {}
#            for n, name in enumerate(func.__code__.co_varnames[1:func.__code__.co_argcount]):
#                params[name] = args[n] if n < len(args) else kwargs[name]
#            reopt.logger.info(func.__name__, params)
            # execute function
            func(reopt, *args, **kwargs)
            return True
        return False
    wrapper.__name__ = func.__name__
    return wrapper    

# decorator
def vdp_handler(func):
    def wrapper(handle: int, *args, **kwargs) -> bool:
        with ORContext(handle, func.__name__) as ctx:
            vdp = ctx()
            if vdp.__class__.__name__ != 'VDP':
                ctx.last_error = f"{func.__name__}: The given handle doesn't point to a VDP instance."
                return False
            # execute function
            func(vdp, *args, **kwargs)
            return True
        return False
    wrapper.__name__ = func.__name__
    return wrapper

####################################################################################################
class ORCache(object):
    def __init__(self, cahceSize: int = 5):
        self._cacheSize = cahceSize
        self._cache: Dict[int, object] = {}

    def __getitem__(self, key: Dict) -> object:
        _hash = self.hash(key) if isinstance(key, dict) else key
        return self._cache.get(_hash)
    
    def hash(self, key: Dict) -> int:
        _hash = 0
        for k, v in key.items():
            _hash += hash(k)
            if isinstance(v, np.ndarray):
                _hash += hash(v.tobytes())
            else:
                _hash += hash(v)
        return _hash

    # starting from Python 3.7, the insertion order of items in dictionaries 
    # is guaranteed to be preserved. 
    # https://stackoverflow.com/questions/39980323/are-dictionaries-ordered-in-python-3-6
    def __setitem__(self, key, value: object):
        _hash = self.hash(key) if isinstance(key, dict) else key
        if _hash in self._cache:
            return
        if len(self._cache) >= self._cacheSize:
            # Remove the first item
            first_key = next(iter(self._cache))
            self._cache.pop(first_key)

        self._cache[_hash] = value

    def Erase(self):
        self._cache.clear()

    def __contains__(self, key: Dict) -> bool:
        _hash = self.hash(key) if isinstance(key, dict) else key
        return _hash in self._cache

###################################################################################################
if __file__ == '__main__':
    from ReOpt import ReOpt
        
    @reopt_handler
    def test(reopt: ReOpt):
        print (reopt)
        raise ValueError('Test error')
        
    reopt = ReOpt('test.log', 1)
    hOR = ORContext.AttachInstance(reopt)
    print (test(hOR))
    print (ORContext.GetLastError(hOR))