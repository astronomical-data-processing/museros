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
            fp, pathname, description = imp.find_module('_synthesisdeconvolver', [dirname(__file__)])
        except ImportError:
            import _synthesisdeconvolver
            return _synthesisdeconvolver
        if fp is not None:
            try:
                _mod = imp.load_module('_synthesisdeconvolver', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _synthesisdeconvolver = swig_import_helper()
    del swig_import_helper
else:
    import _synthesisdeconvolver
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


class synthesisdeconvolver(_object):
    """Proxy of C++ casac::synthesisdeconvolver class"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, synthesisdeconvolver, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, synthesisdeconvolver, name)
    __repr__ = _swig_repr
    def __init__(self): 
        """__init__(self) -> synthesisdeconvolver"""
        this = _synthesisdeconvolver.new_synthesisdeconvolver()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _synthesisdeconvolver.delete_synthesisdeconvolver
    __del__ = lambda self : None;
    def setupdeconvolution(self, *args, **kwargs):
        """
        setupdeconvolution(self, decpars=initialize_record("")) -> bool

        Summary
        	Set parameters to control minor cycle algorithms

        Description
        	


        Input Parameters:
        	decpars		 All parameters for deconvolution (minor cycle) 
        	
        --------------------------------------------------------------------------------
        	      
        """
        return _synthesisdeconvolver.synthesisdeconvolver_setupdeconvolution(self, *args, **kwargs)

    def initminorcycle(self):
        """
        initminorcycle(self) -> record *

        Summary
        	Find peak residual

        Description
        	

        --------------------------------------------------------------------------------
        	      
        """
        return _synthesisdeconvolver.synthesisdeconvolver_initminorcycle(self)

    def interactivegui(self, *args, **kwargs):
        """
        interactivegui(self, iterbotrecord=initialize_record("")) -> record *

        Summary
        	Run interactive GUI

        Description
        	


        Input Parameters:
        	iterbotrecord	 All parameters that control iterations 
        	
        --------------------------------------------------------------------------------
        	      
        """
        return _synthesisdeconvolver.synthesisdeconvolver_interactivegui(self, *args, **kwargs)

    def executeminorcycle(self, *args, **kwargs):
        """
        executeminorcycle(self, iterbotrecord=initialize_record("")) -> record *

        Summary
        	Run a minor cycle

        Description
        	


        Input Parameters:
        	iterbotrecord	 All parameters that control minor cycle 
        	
        --------------------------------------------------------------------------------
        	      
        """
        return _synthesisdeconvolver.synthesisdeconvolver_executeminorcycle(self, *args, **kwargs)

    def restore(self):
        """
        restore(self) -> bool

        Summary
        	Restore images

        Description
        	

        --------------------------------------------------------------------------------
        	      
        """
        return _synthesisdeconvolver.synthesisdeconvolver_restore(self)

    def done(self):
        """
        done(self) -> bool

        Summary
        	Close the tool

        Description
        	

        --------------------------------------------------------------------------------
        	      
        """
        return _synthesisdeconvolver.synthesisdeconvolver_done(self)

synthesisdeconvolver_swigregister = _synthesisdeconvolver.synthesisdeconvolver_swigregister
synthesisdeconvolver_swigregister(synthesisdeconvolver)

# This file is compatible with both classic and new-style classes.


