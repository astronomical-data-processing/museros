
from pymuser.muserscanraw import *


def importraw(
    sub_array=None,
    filepath=None,
    debug=None
    ):
    try:
        scanrawdata(sub_array, filepath, debug)
    except Exception, e:
        print traceback.format_exc()
    	# muserlog.post("Failed to import muser file %s" % inputfile)
    return
