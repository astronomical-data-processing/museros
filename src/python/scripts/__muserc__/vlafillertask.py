# This file was automatically generated by SWIG (http://www.swig.org).
# Version 2.0.10
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.



from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_vlafillertask', [dirname(__file__)])
        except ImportError:
            import _vlafillertask
            return _vlafillertask
        if fp is not None:
            try:
                _mod = imp.load_module('_vlafillertask', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _vlafillertask = swig_import_helper()
    del swig_import_helper
else:
    import _vlafillertask
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


class vlafillertask(_object):
    """Proxy of C++ casac::vlafillertask class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, vlafillertask, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, vlafillertask, name)
    __repr__ = _swig_repr
    def __init__(self): 
        """__init__(self) -> vlafillertask"""
        this = _vlafillertask.new_vlafillertask()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _vlafillertask.delete_vlafillertask
    __del__ = lambda self : None;
    def fill(self, *args, **kwargs):
        """
        fill(self, msname, inputfile, project=string(""), start=string("1970/1/1/00:00:00"), stop=string("2199/1/1/23:59:59"), 
            centerfreq=string("1.0e18Hz"), bandwidth=string("2.0e18Hz"), 
            bandname=string("*"), source=string(""), subarray=0, qualifier=-65536, 
            calcode=string("#"), overwrite=False, freqtol=initialize_variant("0.0"), 
            applytsys=True, keepautocorr=False, antnamescheme=string("new"), useday=1, 
            keepblanks=False, evlabands=True)

        Summary
        	Perform fill operations

        Description
        	

        Input Parameters:
        	msname		 name of output ms 
        	inputfile	 name of vla archive 
        	project		 name of project to extract, defaults to all projects in input 
        	start		 start time to extract 1970/1/1/00:00:00 
        	stop		 end time of extracted data 2199/1/1/23:59:59 
        	centerfreq	 frequency of data to extract (used along with bandwidth param) 1.0e18Hz 
        	bandwidth	 data around centerfreq to get out 2.0e18Hz 
        	bandname	 name of band to extract 4 P L C X U K Q * 
        	source		 name of source 
        	subarray	 subarray - 0 means all subarrays 0 
        	qualifier	 qualifier for source -65536 
        	calcode		 Calibrator code, 1 character only * \# 
        	overwrite	 overwrite or append false 
        	freqtol		 Frequency tolerance, the default tolerance for frequency is set to be 6 times of the channel width. You may have to tweak the tolerance depending on the dataset, just depends. 0.0 
        	applytsys	 scale data and weights by Tsys info true 
        	keepautocorr	 Fill autocorrelations along with cross correlation data. If False data that have same ANTENNA1 and ANTENNA2 are ignored false 
        	antnamescheme	 If 'new', VLA antenna name is prepended by EVLA or VLA to distinguish between the refurbished and non-refubished antennas. 'old' will just put the VLA antenna identifier as is in the NAME column of the ANTENNA table. old new 
        	useday		 This option is only available at the AOC in Socorro! When filling at the AOC, select the online day file to use \< 0 means any previous day up to 14 0 means from the start of the current day \> 0 means starting now 1 
        	keepblanks	 Scans with blank (empty) source names (i.e. tipping scans) will be filled. The default is to not fill. false 
        	evlabands	 Use the EVLA frequencies and bandwith tolerances when specifying band codes or wavelengths. true 
        	
        Example:
        	
        --------------------------------------------------------------------------------
        	      
        """
        return _vlafillertask.vlafillertask_fill(self, *args, **kwargs)

vlafillertask_swigregister = _vlafillertask.vlafillertask_swigregister
vlafillertask_swigregister(vlafillertask)

# This file is compatible with both classic and new-style classes.


