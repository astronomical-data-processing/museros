import sys, os, datetime, time, math
from muserframe import *
#from muserenv import *
import numpy as np

logger = logging.getLogger('muser')


class MuserData(MuserFrame):
    def __init__(self, sub_array=1):

        super(MuserData, self).__init__(sub_array)

        self.if_time_setup = False
        self.if_file_opened = False
        self.integral_time = 0

        self.last_calibration_priority = -1
        self.last_date_time = MuserTime()
        self.last_sub_array = -1

        self.current_file_name = ''

        # self.start_date_time = MuserTime()
        # self.first_date_time = MuserTime()


    def set_data_date_time(self, year=0, month=0, day=0, hour=0, minute=0, second=0, millisecond=0, microsecond=0,
                           nanosecond=0):
        self.start_date_time = MuserTime(year, month, day, hour, minute, second, millisecond, microsecond, nanosecond)
        self.first_date_time = MuserTime(year, month, day, hour, minute, second, millisecond, microsecond, nanosecond)

        # set True to if_time_setup
        self.if_time_setup = True


    def set_priority(self, priority):
        self.calibration_priority = priority


    def search_first_file(self):
        '''
        search the first file of processing
        '''
        if self.open_data_file() == False:
            logger.error("Cannot open observational data.")
            return False

        # Read first frame and check the observational date and time
        if self.read_one_frame() == False:
            logger.error("Cannot read a frame.")
            return False

        if self.input_file_name != '' and self.start_date_time.year == 1970:  # Start!!!
            self.start_date_time = self.current_frame_time


        # The date and time in the first frame should be
        if self.current_frame_time.get_second() == 0 and (
                            self.current_frame_time.get_millisecond() * 1e3 + self.current_frame_time.get_microsecond() < 312500):
            return True

        if self.start_date_time.get_date_time() < self.current_frame_time.get_date_time():
            # previous 1 minute
            if self.debug:
                logger.debug("Change observational file.")
            if self.open_next_file(-1) == False:
                return False
            # Read first frame and check the observational date and time
            if self.read_one_frame() == False:
                self.in_file.close()
                return False
            if self.debug:
                logger.debug("Find data file: %s" % (os.path.basename(self.current_file_name)))
            return True
        else:
            logger.debug("Found observational data file: %s" % (os.path.basename(self.current_file_name)))
            return True

    def search_first_frame(self, specified_file = False):
        '''
        search first frame with proper date and time
        '''
        # Search first possible file

        if self.search_first_file() == False:
            logger.error("Cannot find a proper frame from the observational data.")
            return False

        frame_date_time = self.current_frame_time.get_date_time()
        if self.start_date_time.get_date_time() <  self.current_frame_time.get_date_time():
            t_offset = self.current_frame_time.get_date_time() - self.start_date_time.get_date_time()
        else:
            t_offset = self.start_date_time.get_date_time() - self.current_frame_time.get_date_time()

        if self.debug:
            logger.debug('Current frame time: %04d-%02d-%02d %02d:%02d:%02d %03d%03d%03d' % (
                self.current_frame_time.get_detail_time()))
        time_offset = t_offset.seconds * 1e6 + t_offset.microseconds

        skip_frame_number = int(time_offset / 3125) - 1
        if self.debug:
            logger.debug('Time interval %d, skip frames: %d' % (time_offset, skip_frame_number))

        if (skip_frame_number >= 2):
            self.skip_frames(skip_frame_number)

        # If can find, search first frame
        while True:
            if self.is_loop_mode == False:
                if self.start_date_time.get_date_time() <= self.current_frame_time.get_date_time():
                    break
            else:

                if specified_file == False:
                    if self.is_loop_mode == True and self.start_date_time.get_date_time() <= self.current_frame_time.get_date_time() and self.sub_band == 0 and self.polarization == 0:  # Find file in previous 1 minute
                        break

                    if self.is_loop_mode == False and self.start_date_time.get_date_time() <= self.current_frame_time.get_date_time():
                        break
                else:
                    if self.is_loop_mode == True and self.start_date_time.get_date_time() <= self.current_frame_time.get_date_time():  # Find file in previous 1 minute
                        break

            if self.read_one_frame() == False:
                self.in_file.close()
                return False
        if self.debug:
            logger.debug('Frame located.')
        return True

    def search_frame_realtime(self, specified_file = False):
        '''
        search first frame with proper date and time
        '''
        # Search first possible file

        if self.search_first_file() == False:
            logger.error("Cannot find a proper frame from the observational data.")
            return False

        frame_date_time = self.current_frame_time.get_date_time()
        if self.start_date_time.get_date_time() <  self.current_frame_time.get_date_time():
            t_offset = self.current_frame_time.get_date_time() - self.start_date_time.get_date_time()
        else:
            t_offset = self.start_date_time.get_date_time() - self.current_frame_time.get_date_time()

        #print "****",self.start_date_time.get_detail_time(), self.current_frame_time.get_detail_time()
        #print "####",self.start_date_time.get_date_time(),self.current_frame_time.get_date_time()
        # print "@@@@",t_offset

        #print self.start_date_time.get_date_time() , self.current_frame_time.get_date_time(),t_offset
        # Estimate the number of skip
        # print('current frame time: %04d-%02d-%02d %02d:%02d:%02d %03d%03d%03d' % (
        #     self.current_frame_time.get_detail_time()))
        if self.debug:
            logger.debug('Current frame time: %04d-%02d-%02d %02d:%02d:%02d %03d%03d%03d' % (
                self.current_frame_time.get_detail_time()))
        time_offset = t_offset.seconds * 1e6 + t_offset.microseconds

        skip_frame_number = int(time_offset / 3125) - 1
        if self.debug:
            logger.debug('Time interval %d, skip frames: %d' % (time_offset, skip_frame_number))

        if (skip_frame_number >= 2):
            self.skip_frames(skip_frame_number)

        # If can find, search first frame
        while True:
            if self.is_loop_mode == False:
                if self.start_date_time.get_date_time() <= self.current_frame_time.get_date_time():
                    break
            else:

                if specified_file == False:
                    if self.is_loop_mode == False and self.start_date_time.get_date_time() <= self.current_frame_time.get_date_time():
                        break
                else:
                    if self.is_loop_mode == True and self.start_date_time.get_date_time() <= self.current_frame_time.get_date_time():  # Find file in previous 1 minute
                        break

            if self.read_one_frame() == False:
                self.in_file.close()
                return False
        if self.debug:
            logger.debug('Frame located.')
        return True


    def check_next_file(self):
        '''
        Check file to determine whether the file should be changed
        '''
        offset = [100000, 204800]
        pos = self.in_file.tell()
        if ((pos // offset[self.sub_array - 1]) + 1) >= 19200:
            return True
        else:
            return False

    def open_raw_file(self, file_name):
        if not os.path.exists(file_name):
            logger.error("Cannot find file: %s " % (file_name))
            return False
        try:
            self.in_file = open(file_name, 'rb')
            self.in_file.seek(0, 0)
            self.if_read_first_frame_time = False
            self.current_file_name = file_name
            if self.debug:
                logger.debug("File opened: %s" % (os.path.basename(file_name)))
        except:
            #self.in_file.close()
            return False
        return True

    def close_raw_file(self):
        try:
            self.in_file.close()
        finally:
            None


    def open_data_file(self):
        if self.input_file_name == '':
            full_file_name = self.env.data_file(self.sub_array, self.first_date_time.year, self.first_date_time.month,
                                            self.first_date_time.day, self.first_date_time.hour,
                                            self.first_date_time.minute)

        else:
            full_file_name = self.input_file_name

        print "full_file_name:", full_file_name

        return self.open_raw_file(full_file_name)

    def open_muser_file(self, sub_array, year, month, day, hour, minute):
        self.set_array(sub_array)
        full_file_name = self.env.data_file(sub_array, year, month, day, hour, minute)
        return self.open_raw_file(full_file_name)


    def open_next_file(self, time_minute=1):

        self.first_date_time.set_with_date_time(
            self.first_date_time.get_date_time() + datetime.timedelta(minutes=time_minute))

        full_file_name = self.env.data_file(self.sub_array, self.first_date_time.year, self.first_date_time.month,
                                            self.first_date_time.day, self.first_date_time.hour,
                                            self.first_date_time.minute)
        return self.open_raw_file(full_file_name)

    def close_file(self):
        self.in_file.close()

    def load_calibration_data(self):

        # if self.last_calibration_priority == self.calibration_priority and self.last_date_time.day == self.start_date_time.day and self.last_date_time.month == self.start_date_time.month and self.last_date_time.year == self.start_date_time.year and self.last_sub_array == self.sub_array:
        #     return
        file_name = self.env.cal_file(self.sub_array, self.start_date_time.year, self.start_date_time.month, self.start_date_time.day, self.calibration_priority)
        self.last_date_time.copy(self.start_date_time)
        self.last_calibration_priority = self.calibration_priority
        if self.env.file_exist(file_name) == True:
            caldata = np.fromfile(file_name, dtype=complex)
            if self.is_loop_mode == True:
                if self.sub_array == 1:
                    self.cal = caldata.reshape(4, 2, self.antennas * (self.antennas - 1) // 2, 16)
                elif self.sub_array == 2:
                    self.cal = caldata.reshape(33, 2, self.antennas * (self.antennas - 1 ) // 2, 16)
            else:
                self.cal = caldata.reshape(self.antennas * (self.antennas - 1) // 2, 16)
            if self.debug:
                logger.debug("Load Calibrated data.")
        else:
            if self.debug:
                logger.error("Cannot find calibrated data.")

    def load_uvw_data(self, file_name):

        if self.env.file_exist(file_name) == True:
            self.uvw_data = np.fromfile(file_name, dtype=float) #.reshape(repaet_number*self.antennas * (self.antennas - 1) // 2, 3)
            if self.debug:
                logger.debug("Load UVW data.")
                #print self.cal
        else:
            if self.debug:
                logger.error("Cannot find UVW data.")


    def load_vis_data(self, file_name):

        if self.env.file_exist(file_name) == True:
            self.vis_data = np.fromfile(file_name, dtype=complex)
            # if self.sub_array == 1:
            #     self.vis = visdata.reshape(repaet_number*self.antennas * (self.antennas - 1) // 2, 16)
            # elif self.sub_array == 2:
            #     self.vis = visdata.reshape(repaet_number*self.antennas * (self.antennas - 1) // 2, 33)
            if self.debug:
                logger.debug("Load visibility data.")
                #print self.cal
        else:
            if self.debug:
                logger.error("Cannot find visibility data.")

    def load_date_file(self, file_name):

        if self.env.file_exist(file_name) == True:
            self.date = np.fromfile(file_name, dtype=float) #.reshape(3, repaet_number*self.antennas * (self.antennas - 1) // 2)
            # self.date1 = date[0]  # self.muser.obs_date_sum
            # self.date2 = date[1]  # self.muser.obs_time_sum
            # self.date3 = date[2]  # self.source

        if self.debug:
            logger.debug("Load date and position.")
        else:
            if self.debug:
                logger.error("Cannot find date and position.")

    def calibration(self):
        if self.debug:
            logger.debug("Satellite phase correction")

        if self.sub_array == 1:
            if self.obs_date == "2015-11-01": # Temp used
                print "2015-11-01"
                phase=[-3.0157,-2.7757,-2.8649,0.6462,1.8401,-0.7325,-2.1655,1.8243,1.8243,1.8243,1.8243,-0.5035,0.1383,-2.7669,1.8067,2.0335,-2.8008,-1.466,2.9967,-1.5397,1.0128,0.4667,-1.2595,1.3932,2.6025,-2.3351,2.145,-1.5066,1.0293,-1.7432,-1.5361,0.0217,-1.2084,-0.9153,2.6745,-2.1042,-0.3105,-3.0538,2.4344,0.2589,0.2471,3.0093,-1.495,2.7288,0.7909,3.0565,3.0565,3.0565,3.0565,2.5664,2.7845,0.288,-1.6055,-1.556,0.0351,1.4322,-0.3513,1.2078,-2.239,-2.8841,1.3048,-2.1556,-0.9622,0.4778,-0.7569,1.3243,-2.4111,0.7964,1.2482,3.018,1.714,1.8949,-0.9352,0.8531,2.4956,-0.285,-0.4261,0.1022,2.7844,-1.5592,2.4398,0.6549,2.2516,2.2516,2.2516,2.2516,2.3602,2.4797,0.1617,-1.9101,-1.9124,-0.2122,1.2105,-0.7452,0.9387,-2.3633,3.0681,1.1179,-2.4056,-1.1094,0.1899,-1.0318,1.1105,-2.646,0.5151,0.8578,2.8102,1.2963,1.5721,-1.1347,0.7336,2.3686,-0.5009,-0.4835,3.1267,-1.6615,1.925,0.6561,1.5965,1.5965,1.5965,1.5965,2.3017,3.0699,-0.0057,-1.8722,-1.4019,-0.1584,1.4975,-0.5823,1.0616,-2.5225,2.7865,1.4337,-2.036,-0.8933,0.2936,-1.5542,0.9577,-2.5795,0.5573,1.0665,2.6136,1.6438,1.7237,-0.9518,0.624,2.4119,-0.3967,-1.0796,1.2078,0.0036,-2.1879,-2.8585,-2.8585,-2.8585,-2.8585,-1.1711,-0.5568,-2.6376,1.1071,1.3173,-2.7735,-1.9631,2.6797,-2.1204,0.5531,0.3585,-2.2096,0.8878,2.1745,-2.7486,2.8796,-2.2857,0.8147,-2.1011,-2.0763,-0.2765,-1.7824,-1.4205,2.1966,-2.3604,-0.8817,2.4893,-2.8116,-2.4226,2.2537,-0.8702,-0.8702,-0.8702,-0.8702,-2.2856,-1.7224,1.662,-0.1107,0.2533,1.5522,-3.033,1.3104,3.0381,-0.868,-1.5331,3.1061,-0.4009,0.8493,2.2476,0.3575,2.8072,-0.8304,2.3727,2.9903,-1.8709,-3.0335,-2.8369,0.9276,2.371,-2.0512,1.3364,0.8162,-1.7626,-2.7906,-2.7906,-2.7906,-2.7906,-0.1371,-0.7387,-2.1328,1.9343,1.3017,-2.5177,-0.9541,2.9882,-1.5219,2.0872,0.4478,-2.1835,1.3066,2.9446,-2.2692,2.9412,-1.2042,1.4696,-1.918,-1.338,0.2148,-1.2586,-0.7985,2.8381,-1.6468,0.1806,-2.8924,-2.9401,-1.1087,-1.1087,-1.1087,-1.1087,1.5127,2.0524,-0.6379,-2.6265,-2.5069,-0.5749,0.6578,-1.1484,0.241,-2.7638,2.7453,0.6311,-2.8874,-1.62,-0.2595,-1.7559,0.5071,2.9436,-0.032,0.163,1.9703,0.7339,1.1638,-1.5306,0.0395,1.7005,-1.4037,-1.2314,0.0,0.0,0.0,2.1972,-2.6401,0.9654,3.0178,3.0337,3.0019,-0.3,-1.2747,-1.7224,-1.7218,-1.65,-2.9129,-2.4,2.0517,3.1361,2.8726,-2.3356,-1.589,1.9407,-2.6206,1.1446,1.1539,-1.0068,-2.2363,0.5307,-2.7919,-1.7488,-0.2112,0.0,0.0,2.1972,-2.6401,0.9654,3.0178,3.0337,3.0019,-0.3,-1.2747,-1.7224,-1.7218,-1.65,-2.9129,-2.4,2.0517,3.1361,2.8726,-2.3356,-1.589,1.9407,-2.6206,1.1446,1.1539,-1.0068,-2.2363,0.5307,-2.7919,-1.7488,-0.2112,0.0,2.1972,-2.6401,0.9654,3.0178,3.0337,3.0019,-0.3,-1.2747,-1.7224,-1.7218,-1.65,-2.9129,-2.4,2.0517,3.1361,2.8726,-2.3356,-1.589,1.9407,-2.6206,1.1446,1.1539,-1.0068,-2.2363,0.5307,-2.7919,-1.7488,-0.2112,2.1972,-2.6401,0.9654,3.0178,3.0337,3.0019,-0.3,-1.2747,-1.7224,-1.7218,-1.65,-2.9129,-2.4,2.0517,3.1361,2.8726,-2.3356,-1.589,1.9407,-2.6206,1.1446,1.1539,-1.0068,-2.2363,0.5307,-2.7919,-1.7488,-0.2112,0.889,-2.3093,2.1794,2.7116,-2.2211,-0.8221,-2.4743,-0.9501,1.6532,1.2015,-0.6729,1.748,3.0566,-2.0353,2.4677,-1.0896,1.6425,-1.1883,-0.9226,0.4153,-0.642,-0.3905,-3.0729,-1.5318,0.2839,-2.5593,2.5611,-2.4954,1.5539,1.7279,-2.579,-1.746,3.0867,-1.7773,0.7382,0.9964,-1.5567,1.4012,2.4211,-2.1823,-2.7327,-1.831,1.0335,-1.6935,-1.3798,0.1881,-1.2795,-1.0098,2.5751,-2.0215,-0.5272,2.8844,-1.757,-1.8793,-1.8658,-0.3608,1.1283,-0.8615,1.049,-2.3964,2.7857,1.4896,-2.6682,-1.0147,0.2923,-1.2932,1.197,-2.5618,0.3223,0.7424,2.5867,1.1862,1.6023,-0.9189,0.5819,2.5434,-0.5611,-0.9849,0.3353,1.8138,-3.0358,1.3551,2.6648,-0.934,-1.1924,3.0312,-0.2003,0.8375,2.009,0.7021,2.8673,-0.6719,2.6638,-3.1254,-1.6875,-2.8269,-2.8216,1.0793,2.5418,-1.925,1.5025,1.2794,1.8933,2.9041,1.3874,-3.0402,-1.0894,-1.1345,2.7608,-0.5038,0.6094,1.9349,0.8806,2.596,-0.7484,2.9667,3.0458,-1.9242,-2.9854,-2.973,0.7383,2.4497,-2.4284,1.0289,1.6865,1.2306,-0.4692,1.3112,-2.2065,-3.0076,1.2644,-2.4456,-0.9191,0.6117,-0.9049,1.1096,-2.4706,0.8636,1.2615,2.8081,1.2463,1.6246,-0.9898,0.8379,2.3589,-0.4826,-0.3071,-1.8297,-0.4304,2.4574,1.8979,0.0813,2.7761,-2.4584,-1.0394,-2.8204,-0.19,2.516,-0.6201,-0.1547,1.2848,0.2359,0.3388,-2.3579,-0.6158,1.1121,-1.7844,-2.2337,1.4075,-1.9548,-2.4813,1.6244,-1.7728,-0.5425,0.9327,-0.1535,1.6724,-1.9868,1.455,1.3606,-2.9363,2.0605,2.2882,-0.3377,1.2682,2.8191,0.0666,0.32,2.5887,2.1501,0.0925,2.9411,-2.3281,-0.8016,-1.7517,-0.0489,2.6356,0.0712,0.1743,2.1808,0.2262,0.6172,-2.0458,-0.4022,1.1515,-1.5402,-1.3092,-0.6014,-2.0816,0.0622,1.7863,-3.0009,0.4699,-2.6487,-0.3315,-3.0165,-2.6154,-1.0907,-2.2906,-1.8284,1.8077,2.9409,-1.239,1.9366,0.5805,-2.3648,0.8237,2.0732,-2.7168,2.4169,-1.9324,0.7231,-2.4106,-2.1052,-0.3867,-1.9197,-1.5752,2.3002,-2.5002,-0.8709,2.594,2.8477,3.1116,-2.1916,-0.9157,-1.6961,-0.3174,2.637,0.2198,0.0548,1.4916,0.2171,0.3607,-2.0415,-0.6293,1.0719,-1.5818,1.0437,1.4263,2.2977,1.4538,-3.1105,-0.0766,-3.086,-2.5896,-1.3403,-2.5303,-2.4983,1.5998,-3.1393,-1.8292,1.8421,1.9345,1.2492,0.0102,1.9131,-1.64,1.5038,1.8421,-2.5171,2.4714,2.7019,0.1135,1.8213,-2.9446,0.4916,0.2916,-1.0932,0.645,-2.8061,0.8336,0.7889,2.4399,0.8551,1.2892,-1.1771,0.3847,2.1016,-0.8144,-0.8597,2.3337,-1.3043,1.4654,2.009,-2.4369,2.6115,2.7916,0.3284,1.8116,-2.4584,0.6445,0.4768,2.8704,-0.3586,0.3944,1.604,0.3657,0.5977,-2.1067,-0.3774,1.3975,-1.475,-2.2476,-3.0633,-2.9249,-1.1268,-2.2794,-2.1224,1.5133,-2.9885,-1.4226,1.9583,1.9022,0.2737,1.8939,0.671,0.7979,-1.7533,-0.1881,1.428,-1.4076,-0.9419,1.6933,0.2842,0.5482,-1.8764,-0.2494,1.0603,-1.6491,-1.6461,-1.3645,-1.103,2.7609,-2.0356,-0.2136,3.1231,2.9666,0.1752,-2.5365,-0.6927,0.7652,-1.9546,-1.8845,-2.4163,-1.0859,0.7564,-2.0323,-2.3787,1.6074,-2.9891,0.3763,0.4854,1.7553,-1.1472,-1.3731,-2.8113,2.946,0.0727]
                for chan in range(0, self.sub_channels):
                    bl = 0
                    for antenna1 in range(0, self.antennas - 1):
                        for antenna2 in range(antenna1 + 1, self.antennas):
                            A = math.sqrt(
                                self.baseline_data[bl][chan].imag * self.baseline_data[bl][chan].imag +
                                self.baseline_data[bl][chan].real * self.baseline_data[bl][chan].real)
                            phai_sun = math.atan2(self.baseline_data[bl][chan].imag, self.baseline_data[bl][chan].real)
                            phai = phai_sun - phase[bl]
                            self.baseline_data[bl][chan] = complex(A * math.cos(phai), A * math.sin(phai))
                            bl = bl + 1
            else:
                for chan in range(0, self.sub_channels):
                    bl = 0
                    for antenna1 in range(0, self.antennas - 1):
                        for antenna2 in range(antenna1 + 1, self.antennas):
                            A = math.sqrt(
                                self.baseline_data[bl][chan].imag * self.baseline_data[bl][chan].imag +
                                self.baseline_data[bl][chan].real * self.baseline_data[bl][chan].real)
                            phai_sun = math.atan2(self.baseline_data[bl][chan].imag, self.baseline_data[bl][chan].real)
                            if self.is_loop_mode == True:
                                phai = phai_sun - math.atan2(
                                    self.cal[self.sub_band][self.polarization][bl][chan].imag,
                                    self.cal[self.sub_band][self.polarization][bl][chan].real)
                            else:
                                phai = phai_sun - math.atan2(self.cal[bl][chan].imag, self.cal[bl][chan].real)
                            self.baseline_data[bl][chan] = complex(A * math.cos(phai), A * math.sin(phai))
                            bl = bl + 1
        else:

            for chan in range(0, self.sub_channels):
                bl = 0
                for antenna1 in range(0, self.antennas - 1):
                    for antenna2 in range(antenna1 + 1, self.antennas):
                        A = math.sqrt(
                            self.baseline_data[bl][chan].imag * self.baseline_data[bl][chan].imag +
                            self.baseline_data[bl][chan].real * self.baseline_data[bl][chan].real)
                        phai_sun = math.atan2(self.baseline_data[bl][chan].imag, self.baseline_data[bl][chan].real)
                        if self.is_loop_mode == True:
                            phai = phai_sun - math.atan2(
                                    self.cal[self.sub_band][self.polarization][bl][chan].imag,
                                    self.cal[self.sub_band][self.polarization][bl][chan].real)
                        else:
                            phai = phai_sun - math.atan2(self.cal[bl][chan].imag, self.cal[bl][chan].real)
                        self.baseline_data[bl][chan] = complex(A * math.cos(phai), A * math.sin(phai))
                        bl = bl + 1