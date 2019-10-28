#
# This file was generated using xslt from its XML file
#
# Copyright 2014, Associated Universities Inc., Washington DC
#
import sys
import os
import string
import time
import inspect
import gc
import numpy
from odict import odict
from types import *
from task_importraw import importraw
from taskinit import *
import traceback
import globalpy


class importraw_cli_:
    __name__ = "importraw"
    rkey = None
    i_am_a_muserpy_task = None
    # The existence of the i_am_a_muserpy_task attribute allows help()
    # (and other) to treat muserpy tasks as a special case.

    def __init__(self) :
       self.__bases__ = (importraw_cli_,)
       self.__doc__ = self.__call__.__doc__

       self.parameters={'subarray':None, 'filepath':None, 'debug':None}


    def result(self, key=None):
	    #### and add any that have completed...
	    return None


    def __call__(self, subarray=None,  filepath=None, debug=None):

        """Get data information from MUSER data file

	Detailed Description:

        Get data information from MUSER data file
	optional time range and interator

	Arguments :
	    subarray:  Subarray ID of subarray (1-low, 2-high)
	       Deafult Value:

		filepath:	Path of raw data file to be processed.
		   Default Value:

		debug

	Returns: void

        importraw(subarray=1, filepath='/home/20151101', debug=1)

        """

        if not hasattr(self, "__globals__") or self.__globals__ == None :
               self.__globals__=sys._getframe(len(inspect.stack())-1).f_globals
        #muserc = self.__globals__['muserc']
        muserlog = self.__globals__['muserlog']
        #muserlog = muserc.muserc.logsink()
        self.__globals__['__last_task'] = 'importraw'
        self.__globals__['taskname'] = 'importraw'
        ###
        self.__globals__['update_params'](func=self.__globals__['taskname'],printtext=False,ipython_globals=self.__globals__)
        ###
        ###
        #Handle globals or user over-ride of arguments
        #
        if type(self.__call__.func_defaults) is NoneType:
            function_signature_defaults={}
        else:
            function_signature_defaults=dict(zip(self.__call__.func_code.co_varnames[1:],self.__call__.func_defaults))
        useLocalDefaults = False

        for item in function_signature_defaults.iteritems():
            key,val = item
            keyVal = eval(key)
            if (keyVal == None):
                #user hasn't set it - use global/default
                pass
            else:
                #user has set it - use over-ride
                if (key != 'self') :
                    useLocalDefaults = True

        myparams = {}
        if useLocalDefaults :
           for item in function_signature_defaults.iteritems():
               key,val = item
               keyVal = eval(key)
               exec('myparams[key] = keyVal')
               self.parameters[key] = keyVal
               if (keyVal == None):
                   exec('myparams[key] = '+ key + ' = self.itsdefault(key)')
                   keyVal = eval(key)
                   if(type(keyVal) == dict) :
                      if len(keyVal) > 0 :
                         exec('myparams[key] = ' + key + ' = keyVal[len(keyVal)-1][\'value\']')
                      else :
                         exec('myparams[key] = ' + key + ' = {}')
        else :
            print ''
            myparams['subarray'] = subarray = self.parameters['subarray']
            myparams['filepath'] = inputfile = self.parameters['filepath']
            myparams['debug'] = debug = self.parameters['debug']

        result = None

#
#    The following is work around to avoid a bug with current python translation
#
        mytmp = {}
        mytmp['subarray'] = subarray
        mytmp['filepath'] = filepath
        mytmp['debug'] = debug

        muserlog.origin('importraw')
        try :
            saveinputs = self.__globals__['saveinputs']

            tname = 'importraw'
            spaces = ' ' * (18 - len(tname))


            result = importraw(subarray, filepath, debug)
            # muserlog.post('##### End Task: ' + tname + '  ' + spaces + ' #####'+
            #              '\n##########################################')
        except Exception, instance:
            if (self.__globals__.has_key('__rethrow_muser_exceptions') and self.__globals__[
                '__rethrow_muser_exceptions']):
                raise
            else:
                print '**** Error **** ', instance
                tname = 'integrationuvfits'
                muserlog.post('An error occurred running task ' + tname + '.', 'ERROR')
                pass

        gc.collect()
        return result

    def paramgui(self, useGlobals=True, ipython_globals=None):
        """
        Opens a parameter GUI for this task.  If useGlobals is true, then any relevant global parameter settings are used.
        """
        import paramgui
        if not hasattr(self, "__globals__") or self.__globals__ == None :
               self.__globals__=sys._getframe(len(inspect.stack())-1).f_globals

        if useGlobals:
    	    if ipython_globals == None:
                myf=self.__globals__
            else:
                myf=ipython_globals

            paramgui.setGlobals(myf)
        else:
            paramgui.setGlobals({})

        paramgui.runTask('importraw', myf['_ip'])
        paramgui.setGlobals({})

#
#
#
    def defaults(self, param=None, ipython_globals=None, paramvalue=None, subparam=None):
        if not hasattr(self, "__globals__") or self.__globals__ == None :
               self.__globals__=sys._getframe(len(inspect.stack())-1).f_globals
        if ipython_globals == None:
            myf=self.__globals__
        else:
            myf=ipython_globals
        a = odict()
        a['subarray'] = 1
        a['filepath']  = ''
        a['debug']  = globalpy.muser_global_debug



### This function sets the default values but also will return the list of
### parameters or the default value of a given parameter
        if(param == None):
                myf['__set_default_parameters'](a)
        elif(param == 'paramkeys'):
                return a.keys()
        else:
            if(paramvalue==None and subparam==None):
               if(a.has_key(param)):
                  return a[param]
               else:
                  return self.itsdefault(param)
            else:
               retval=a[param]
               if(type(a[param])==dict):
                  for k in range(len(a[param])):
                     valornotval='value'
                     if(a[param][k].has_key('notvalue')):
                        valornotval='notvalue'
                     if((a[param][k][valornotval])==paramvalue):
                        retval=a[param][k].copy()
                        retval.pop(valornotval)
                        if(subparam != None):
                           if(retval.has_key(subparam)):
                              retval=retval[subparam]
                           else:
                              retval=self.itsdefault(subparam)
                     else:
                         retval=self.itsdefault(subparam)
               return retval


#
#
    def check_params(self, param=None, value=None, ipython_globals=None):
      if ipython_globals == None:
          myf=self.__globals__
      else:
          myf=ipython_globals
#      print 'param:', param, 'value:', value
      try :
         if str(type(value)) != "<type 'instance'>" :
            value0 = value
            value = myf['cu'].expandparam(param, value)
            matchtype = False
            if(type(value) == numpy.ndarray):
               if(type(value) == type(value0)):
                  myf[param] = value.tolist()
               else:
                  #print 'value:', value, 'value0:', value0
                  #print 'type(value):', type(value), 'type(value0):', type(value0)
                  myf[param] = value0
                  if type(value0) != list :
                     matchtype = True
            else :
               myf[param] = value
            value = myf['cu'].verifyparam({param:value})
            if matchtype:
               value = False
      except Exception, instance:
         #ignore the exception and just return it unchecked
         myf[param] = value
      return value
#
#
    def description(self, key='importraw', subkey=None):
        desc={'importraw': 'Copy MUSER observational data to specified directory',
              'subarray':'Muser subarray 1 or 2',
               'filepath': 'path of input MUSER raw data',
               'debug': 'Display increasingly verbose debug messages',

              }

#
# Set subfields defaults if needed
#

        if(desc.has_key(key)) :
           return desc[key]

    def itsdefault(self, paramname) :
        a = {}
        a['subarray'] = 1
        a['filepath']  = ''
        a['debug']  = globalpy.muser_global_debug

        if a.has_key(paramname) :
            return a[paramname]

importraw_cli = importraw_cli_()
