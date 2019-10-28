import os,sys,time,struct
import shutil
from muserenv import *

logger = logging.getLogger('muser')

class MuserTime(object):
    """
    class for system time obtained from digital receiver
    """

    def __init__(self, year=0, month=0, day=0, hour=0, minute=0, second=0, millisecond=0, microsecond=0, nanosecond=0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.millisecond = millisecond
        self.microsecond = microsecond
        self.nanosecond = nanosecond

        self.MJD_0 = 2400000.5
        self.MJD_JD2000 = 51544.5

def convert_time(stime):
    tmp = MuserTime()
    # print '%x' % stime
    tmp.nanosecond = (stime & 0x3f)
    if tmp.nanosecond >= 50:
        tmp.nanosecond = 0
    tmp.nanosecond *= 20
    stime >>= 6
    # read microsecond, 6-15
    tmp.microsecond = (stime & 0x3ff)
    stime >>= 10
    # read millisecond 16-25
    tmp.millisecond = (stime & 0x3ff)
    stime >>= 10
    # read second, 26-31
    tmp.second = (stime & 0x3f)
    stime >>= 6
    # read minute, 32-37
    tmp.minute = (stime & 0x3f)
    stime >>= 6
    # read hour, 38-42
    tmp.hour = (stime & 0x1f)
    stime >>= 5
    # read day
    tmp.day = (stime & 0x1f)
    stime >>= 5
    # read month, 48-51
    tmp.month = (stime & 0x0f)
    stime >>= 4
    # read year
    tmp.year = (stime & 0xfff) + 2000
    # print tmp
    return tmp

def search_frame_header(sub_array, in_file):
        # search the header of each frame which sent by digital receiver
        # per frame/3ms
        # in_file: the file handle of the raw file
        # return True : find a valid frame
        offset = [100000, 204800]
        pos = in_file.tell()

        if pos > 0:
            if pos % offset[sub_array -1] !=0:
                in_file.seek(((pos // offset[sub_array - 1]) + 1) * offset[sub_array - 1])
        in_file.seek(32, 1)

        return True

def scanrawdata(sub_array, path, debug):
    if os.path.exists(path):
        filenameList = os.listdir(path)
    else:
        if debug:
            logger.info("File Path not exist: %s" % path)
        return []
    print "File Number:", len(filenameList)

    for file in filenameList:
        file_name = path+'/'+file
        in_file = open(file_name, 'rb')
        in_file.seek(0, 0)

        if (search_frame_header(sub_array, in_file) == False):
            return False

        tmp = in_file.read(8)
        tmp_time = struct.unpack('Q', tmp)[0]

        current_frame_time = convert_time(tmp_time)
        fileNAME = ('%4d%02d%02d-%02d%02d') % (
            current_frame_time.year, current_frame_time.month, current_frame_time.day,
            current_frame_time.hour, current_frame_time.minute)
        obs_time = ('%4d-%02d-%02d %02d:%02d:%02d') % (
            current_frame_time.year, current_frame_time.month, current_frame_time.day,
            current_frame_time.hour, current_frame_time.minute, current_frame_time.second)
        in_file.close()
        print obs_time
        datadir = muserenv.data_dir(sub_array, current_frame_time.year, current_frame_time.month, current_frame_time.day, current_frame_time.hour, current_frame_time.minute)
        # # filepath = "/astrodata/archive/20151101/MUSER-1/dat"+'/'+fileNAME
        filepath = datadir +'/'+fileNAME
        if os.path.exists(datadir):
            if os.path.exists(filepath):
                os.remove(filepath)
            shutil.copyfile(file_name, filepath)
        else:
            os.makedirs(datadir)
            shutil.copyfile(file_name, filepath)

#
# if __name__ == '__main__':
#     scanrawdata("/astrodata/20160705_H")



