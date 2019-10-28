import os, sys

path = os.path.abspath(os.path.dirname(__file__))
if path.find('python') == -1:
    print("Cannot locate proper directory")
    exit(0)
path1 = path[0:path.find('python')+7]
sys.path.append(path1)

from taskinit import *
import traceback

if os.environ.get('MUSERGPU') == 'TRUE':
    from pymuser.muserclean import *
else:
    from pymuser.muserserialclean import *


def clean (
    inputfile=None,
    outdir = None,
    channel = None,
    weight= 'natural',
    mode = 'hogbom',
    automove = True,
    movera = 0.,
    movedec = 0.,
    plot = True,
    fits = False,
    correct = False,
    debug=None,
    ):

    try:
        #muserlog.origin('writeuvfits')
        # -----------------------------------------'
        # beginning of importmiriad implementation
        # -----------------------------------------
        #obsFileName = valid_date(start)

        if os.environ.get('MUSERGPU') == 'TRUE':
            clean = MuserClean()
            if mode=='hybrid':
                clean.hybrid_clean_with_fits(inputfile, outdir, channel, weight, mode, automove, movera, movedec, plot, fits, correct, debug)
            else:
                clean.clean_with_fits(inputfile, outdir, channel, weight, mode, automove, movera, movedec, plot, fits, correct, debug)
        else:
            clean = Clean()
            clean.serial_clean(inputfile, outdir, channel, weight, mode, automove, movera, movedec, plot, fits, correct, debug )


    except Exception, e:
        print traceback.format_exc()
    	muserlog.post("Failed to import muser file %s" % inputfile)
    return


