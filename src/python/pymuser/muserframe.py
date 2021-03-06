from muserdelay import *
from muserbase import *
import numpy as np
import datetime

logger = logging.getLogger('muser')

angle = 180 / math.pi
pi = math.pi


class MuserFrame(MuserBase):
    def __init__(self, sub_array=1):
        super(MuserFrame, self).__init__()
        # public member
        self.real_sub_array = 0
        self.frame_number = 8
        self.sub_channels = 0
        self.channels = 0
        self.antennas = 0
        self.dr_output_antennas = 0
        self.polarization = 0
        self.freqid = 1

        self.groups = 0
        self.fre_rows = 0
        self.source_rows = 0

        # observe parameters
        self.obs_date = ''
        self.obs_time = ''

        # for data integral
        self.obs_date_sum = 0.
        self.obs_date_sum0 = 0.
        self.obs_time_sum = 0.
        self.ra_sum = 0.
        self.dec_sum = 0.
        self.pbs_target = ""
        self.obs_target = ""

        self.if_bandwidth = 25000000

        self.baseline = []

        self.channel_group = 0
        self.current_frame_time = MuserTime()
        self.current_frame_utc_time = MuserTime()
        self.first_frame_time = MuserTime()

        self.frequency = 1600000000
        self.current_frame_header = MuserFrameHeader()
        self.if_read_first_frame_time = False
        self.set_array(sub_array)

        self.read_number =0

    def set_array(self, sub_array):
        '''
        switch between muser-i and muser-ii
        sub_array: 1:muser-i/2:muser-ii
        '''

        muser_para = {0: (16, 40, 44, 4, 2), 1: (16, 60, 64, 33, 2)}

        self.sub_array = sub_array
        if self.sub_array not in [1, 2]:
            return False

        self.sub_channels, self.antennas, self.dr_output_antennas, self.frame_number, self.polarization_number = \
            muser_para[
                self.sub_array - 1]
        if self.debug:
            logger.debug('Array: muser-%d: antennas:%d, frame: %d, polarization:%d' % (self.sub_array,
                                                                                       self.antennas, self.frame_number,
                                                                                       self.polarization_number))

        self.uvws_sum = np.ndarray(shape=((self.antennas * (self.antennas - 1) / 2), 3), dtype=float)

        self.baseline_data = np.ndarray(
            shape=(self.antennas * (self.antennas - 1) / 2, self.sub_channels),
            dtype=complex)
        self.baseline_data_flag = np.ndarray(
            shape=(self.antennas * (self.antennas - 1) / 2, self.sub_channels),
            dtype=int)

        self.position_data = np.ndarray(shape=(self.sub_channels, self.dr_output_antennas, self.dr_output_antennas),
                                        dtype=float)
        self.correlation_data = np.ndarray(shape=(self.sub_channels, self.dr_output_antennas, self.dr_output_antennas),
                                           dtype=float)
        self.auto_correlation_data = np.ndarray(shape=(self.sub_channels, self.dr_output_antennas), dtype=float)

        self.par_delay = np.ndarray(shape=(self.dr_output_antennas), dtype=float)

        self.delay = np.ndarray(shape=(self.dr_output_antennas), dtype=float)

        self.delay_compensation = MuserDelay()

        self.env.antenna_loaded = False

    def search_frame_header_with_byte(self):
        # search the header of each frame which sent by digital receiver
        # per frame/3ms
        # in_file: the file handle of the raw file
        # return True : find a valid frame

        while True:
            bb = self.in_file.read(1)
            if not bb:
                break
            beginner = struct.unpack('b', bb)[0]
            # print '%2x ' % beginner

            if beginner == 0x55:
                for i in range(0, 27):
                    bb = self.in_file.read(1)
                    if not bb: break
                    second = struct.unpack('b', bb)[0]
                    # print ('%d %2x ') % (i,second)
                    if second != 0x55:
                        break
                if i == 26:
                    self.in_file.seek(4, 1)
                    return True
        return False

    def search_frame_header(self):
        # search the header of each frame which sent by digital receiver
        # per frame/3ms
        # in_file: the file handle of the raw file
        # return True : find a valid frame
        offset = [100000, 204800]
        pos = self.in_file.tell()
        if pos > 0:
            if pos % offset[self.sub_array -1] !=0:
                self.in_file.seek(((pos // offset[self.sub_array - 1]) + 1) * offset[self.sub_array - 1])
        self.in_file.seek(32, 1)
        if self.debug:
            logger.debug('Frame header searched - %d ', (pos))

        return True

    def seek_frame_header(self):
        # search the header of each frame which sent by digital receiver
        # per frame/3ms
        # in_file: the file handle of the raw file
        # return True : find a valid frame
        offset = [100000, 204800]
        pos = self.in_file.tell()
        if pos > 0:
            self.in_file.seek((pos // offset[self.sub_array - 1]) * offset[self.sub_array - 1])
        self.in_file.seek(32, 1)
        return True

    def skip_frames(self, number_of_frames):
        offset = [100000, 204800]
        pos = self.in_file.tell()
        if pos > 0 and ( pos % offset[self.sub_array - 1] !=0):
            self.in_file.seek((pos // offset[self.sub_array - 1]) * offset[self.sub_array - 1])

        self.in_file.seek(offset[self.sub_array - 1] * number_of_frames, 1)
        if self.debug:
            logger.debug('Skip %d frames' % (number_of_frames))
        return True

    def read_one_frame(self, search = True):
        if search == True:
            if (self.search_frame_header() == False):
                if self.debug: logger.error('Cannot find a correct header information.')
                return False
        if search == False:
            self.in_file.seek(32, 1)
        tmp = self.in_file.read(8)
        tmp_time = struct.unpack('Q', tmp)[0]

        self.current_frame_time = self.convert_time(tmp_time)
        # if self.Debug:
        if self.debug:
            logger.debug("Read frame date and time: %s " % self.current_frame_time.get_string())

        self.current_frame_date_time = self.current_frame_time.get_date_time()  # self.get_frame_datetime()
        if self.if_read_first_frame_time == False:
            self.first_frame_time.copy(self.current_frame_time)
            self.if_read_first_frame_time = True

        obs_time = ('%4d-%02d-%02d %02d:%02d:%02d') % (
            self.current_frame_time.year, self.current_frame_time.month, self.current_frame_time.day,
            self.current_frame_time.hour, self.current_frame_time.minute, self.current_frame_time.second)

        # self.current_frame_time.millisecond*1e3+self.current_frame_time.microsecond)

        # the date and time are beijing time of china, utc = cst - 8
        # utc = cst - 8
        self.current_frame_utc_time.copy(self.current_frame_time)
        self.current_frame_utc_time.set_with_date_time(
            self.current_frame_utc_time.get_date_time() + datetime.timedelta(hours=-8))

        # print "observaton time(utc):", date

        self.obs_date = ('%4d-%02d-%02d') % (
            self.current_frame_utc_time.year, self.current_frame_utc_time.month, self.current_frame_utc_time.day)
        self.obs_time = ('%02d:%02d:%02d.%03d%03d%03d') % (
            self.current_frame_utc_time.hour, self.current_frame_utc_time.minute, self.current_frame_utc_time.second,
            self.current_frame_utc_time.millisecond, self.current_frame_utc_time.microsecond,
            self.current_frame_utc_time.nanosecond)

        if (self.current_frame_utc_time.year < 2015):
            self.version = False
        else:
            self.version = True

        # read out parameters
        self.current_frame_header.frequency_switch = struct.unpack('I', self.in_file.read(4))[0]
        self.in_file.seek(128, 1)
        self.current_frame_header.bandwidth = struct.unpack('I', self.in_file.read(4))[0]
        self.current_frame_header.quantization_level = struct.unpack('I', self.in_file.read(4))[0]
        self.current_frame_header.delay_switch = struct.unpack('I', self.in_file.read(4))[0]
        self.current_frame_header.strip_switch = struct.unpack('I', self.in_file.read(4))[0]
        self.current_frame_header.sub_band_switch = struct.unpack('I', self.in_file.read(4))[0]
        self.if_bandwidth = self.IF_BANDWIDTH[self.current_frame_header.bandwidth]

        if self.version == True:
            if (self.current_frame_header.sub_band_switch & 0xffff) == 0x3333:  # Polarization
                self.polarization = 0
            else:
                self.polarization = 1
        else:
            self.polarization = (self.read_number % 2)
            self.read_number = self.read_number +1
        self.sub_band_switch = self.current_frame_header.sub_band_switch >> 16  # Sub_band frequency
        self.is_loop_mode = False

        if self.sub_array == 1:
            # We have to support two types of files
            if self.version==False:
                if self.sub_band_switch in [ 0x3333, 0x7777, 0xbbbb, 0xcccc]:
                    self.channel_group = self.NON_LOOP_MODE_LOW[self.sub_band_switch][0]
                    self.frequency = self.NON_LOOP_MODE_LOW[self.sub_band_switch][1]
                    self.freqid = self.NON_LOOP_MODE_LOW[self.sub_band_switch][2]

                    self.numrows = 1
                    self.groups = 60*1000/25*8*(self.antennas * (self.antennas - 1) // 2)
                    self.source_rows = 60*1000/25*8/2

                else:
                    self.is_loop_mode = True

                    self.numrows =4
                    self.groups = 60*1000/25*8*(self.antennas * (self.antennas - 1) // 2)/2
                    self.source_rows = 60*1000/25*8

                    # In loop mode, we should read another two bytes in absolute offset: 99264
                    # We have read 192 bytes. So, we shoudl foward 99264-192  bytes
                    # 0000,5555,AAAA,FFFF 0.4-0.8GHZ 0.8~1.2GHz 1.2~1.6GHz 1.6~2.0GHz
                    self.in_file.seek(99264 - 192, 1)
                    self.sub_band_switch = struct.unpack('H', self.in_file.read(2))[0]
                    if self.sub_band_switch == 0x0000:
                        self.channel_group = 0
                        self.frequency = 400000000
                        self.freqid = 1
                    elif self.sub_band_switch == 0x5555:
                        self.channel_group = 16
                        self.frequency = 800000000
                        self.freqid = 2
                    elif self.sub_band_switch == 0xaaaa:
                        self.channel_group = 32
                        self.frequency = 1200000000
                        self.freqid = 3
                    elif self.sub_band_switch == 0xffff:
                        self.channel_group = 48
                        self.frequency = 1600000000
                        self.freqid = 4
                    self.in_file.seek(-(99264 - 192 + 2), 1)
            else:
                if self.NON_LOOP_MODE_LOW.has_key(self.sub_band_switch):
                    self.channel_group = self.NON_LOOP_MODE_LOW[self.sub_band_switch][0]
                    self.frequency = self.NON_LOOP_MODE_LOW[self.sub_band_switch][1]
                    self.freqid = self.NON_LOOP_MODE_LOW[self.sub_band_switch][2]
                else:
                    self.is_loop_mode = True
                    # in loop mode, we should read another two bytes in absolute offset: 99264
                    # we have read 192 bytes. so, we shoudl foward 99264-192  bytes
                    # 0000,5555,aaaa,ffff 0.4-0.8ghz 0.8~1.2ghz 1.2~1.6ghz 1.6~2.0ghz
                    self.in_file.seek(16, 1)  # todo:
                    self.current_frame_header.sub_band_switch = struct.unpack('B', self.in_file.read(1))[0]
                    # print "self.current_frame_header.sub_band_switch", self.current_frame_header.sub_band_switch
                    self.polarization = self.LOOP_MODE_LOW[self.current_frame_header.sub_band_switch][0]
                    self.channel_group = self.LOOP_MODE_LOW[self.current_frame_header.sub_band_switch][1]
                    self.frequency = self.LOOP_MODE_LOW[self.current_frame_header.sub_band_switch][2]
                    self.freqid = self.LOOP_MODE_LOW[self.current_frame_header.sub_band_switch][3]
                    # print "freqid:", self.freqid
                    self.in_file.seek(-17, 1)
                self.sub_band = self.channel_group // 16

        elif self.sub_array == 2:
            if self.NON_LOOP_MODE_HIGH.has_key(self.sub_band_switch):  # Sub_band frequency
                if not self.NON_LOOP_MODE_HIGH.has_key(self.sub_band_switch):
                        self.sub_band_switch = 0
                self.channel_group = self.NON_LOOP_MODE_HIGH[self.sub_band_switch][0]
                self.frequency = self.NON_LOOP_MODE_HIGH[self.sub_band_switch][1]
                self.freqid = self.NON_LOOP_MODE_HIGH[self.sub_band_switch][2]
            else:
                self.is_loop_mode = True
                self.in_file.seek(4, 1)
                self.current_frame_header.sub_band_switch = struct.unpack('H', self.in_file.read(2))[0]
                self.polarization = self.LOOP_MODE_HIGH[self.current_frame_header.sub_band_switch][0]
                self.channel_group = self.LOOP_MODE_HIGH[self.current_frame_header.sub_band_switch][1]
                self.frequency = self.LOOP_MODE_HIGH[self.current_frame_header.sub_band_switch][2]
                self.freqid = 1
                self.in_file.seek(-6, 1)

        self.sub_band = self.channel_group // 16

        if self.version==True:
            obs_target = struct.unpack('H', self.in_file.read(2))[0]  # calibration source
            if obs_target == 0x0000:
                self.obs_target = "sun"
            elif obs_target == 0x0101:
                self.obs_target = "satellite"
            elif obs_target == 0x0202:
                self.obs_target = "swan"
            else:
                self.obs_target = "other"

            tag = struct.unpack('H', self.in_file.read(2))[0]

            if tag == 0x0000:  # high array or low array
                self.real_sub_array = 1
            elif tag == 0x4e4e:
                self.real_sub_array = 2
            if self.sub_array == 1:
                self.in_file.seek(-4, 1)
        else:
            self.obs_target = "sun"
            self.real_sub_array = self.sub_array

        if self.debug:
            logger.debug(
                'Read header info - time: %04d-%02d-%02d %02d:%02d:%02d %03d%03d%03d - array:%d band:%d polization:%d frequence:%d' % (
                    self.current_frame_time.year, self.current_frame_time.month, self.current_frame_time.day,
                    self.current_frame_time.hour, self.current_frame_time.minute, self.current_frame_time.second,
                    self.current_frame_time.millisecond, self.current_frame_time.microsecond,
                    self.current_frame_time.nanosecond, self.real_sub_array, self.sub_band, self.polarization,
                    self.frequency))

    def read_data(self):
        if self.sub_array == 1:
            if self.debug:
                logger.debug('Read data current pos %d' % self.in_file.tell())
            self.in_file.seek(2752, 1)

            for channel in range(0, self.sub_channels, 2):
                bl = 0
                for antenna1 in range(0, self.dr_output_antennas - 1):
                    for antenna2 in range(antenna1 + 1, self.dr_output_antennas):
                        # if bl==0:
                        #     print self.in_file.tell()
                        buff = self.in_file.read(12)
                        # if ((antenna1 ==0) and (antenna2 ==1)):
                        #     print repr(buff)
                        c1, c2 = self.convert_cross_correlation(buff)
                        # self.baseline_data[self.polarization][antenna1][antenna2][channel] = c1
                        if (antenna1 < self.antennas - 1 and antenna2 < self.antennas):
                            self.baseline_data[bl][channel] = c1
                            self.baseline_data_flag[bl][channel] = True

                            self.baseline_data[bl][channel + 1] = c2
                            self.baseline_data_flag[bl][channel + 1] = True
                            # if channel==8:
                            #     a = ('%3d%5d%5d  %20.5f %20.5f\n')%(channel, antenna1, antenna2, self.baseline_data[bl][channel].real,self.baseline_data[bl][channel].imag)
                            #     b = ('%3d%5d%5d  %20.5f %20.5f\n')%(channel+1, antenna1, antenna2, self.baseline_data[bl][channel+1].real,self.baseline_data[bl][channel+1].imag)
                            #
                            #     print a
                            #     file1.writelines(a)
                            #     file1.writelines(b)

                            bl = bl + 1

                    #print csrh.par_Delay
                # file1.close()

                self.in_file.seek(40, 1)

                for antenna in range(0, self.dr_output_antennas, 4):

                    buff1 = self.in_file.read(8)
                    r1, r2 = self.convert_auto_correlation(buff1)
                    self.auto_correlation_data[channel][antenna] = r1
                    self.auto_correlation_data[channel + 1][antenna] = r2

                    buff1 = self.in_file.read(8)
                    r1, r2 = self.convert_auto_correlation(buff1)
                    self.auto_correlation_data[channel][antenna + 1] = r1
                    self.auto_correlation_data[channel + 1][antenna + 1] = r2

                    buff1 = self.in_file.read(8)
                    r1, r2 = self.convert_auto_correlation(buff1)
                    self.auto_correlation_data[channel][antenna + 2] = r1
                    self.auto_correlation_data[channel + 1][antenna + 2] = r2

                    buff1 = self.in_file.read(8)
                    r1, r2 = self.convert_auto_correlation(buff1)
                    self.auto_correlation_data[channel][antenna + 3] = r1
                    self.auto_correlation_data[channel + 1][antenna + 3] = r2

                    self.in_file.seek(32, 1)
                    # if channel==4 and antenna ==0:
                    #       print self.auto_correlation_data[channel][antenna]

                    if channel == self.sub_channels - 2 :
                        self.in_file.seek(-24, 1)
                        buff = self.in_file.read(16)
                        (self.par_delay[antenna], self.par_delay[antenna + 1], self.par_delay[antenna + 2],
                         self.par_delay[antenna + 3]) = self.convert_time_offset(buff)[:]
                        self.in_file.seek(8, 1)

                # print self.auto_correlation_data
                self.in_file.seek(32, 1)

        elif self.sub_array == 2:
            self.in_file.seek(1692, 1) # 1690 reserve and 2bytes frequency code
            visbility = np.ndarray(shape=(self.dr_output_antennas * (self.dr_output_antennas - 1) / 2),
                                   dtype=complex)
            for channel in range(0, self.sub_channels): # read data of all antennas in one channel
                for bl_len in range(0, self.dr_output_antennas * (self.dr_output_antennas - 1) / 2, 2):
                    buff = self.in_file.read(12)
                    c1, c2 = self.convert_cross_correlation(buff)
                    visbility[bl_len] = c2
                    visbility[bl_len + 1] = c1

                bl1, bl2 = 0, 0
                for antenna1 in range(0, self.antennas-1):
                    for antenna2 in range(antenna1 + 1, self.dr_output_antennas):
                        if antenna2 < self.antennas:
                            self.baseline_data[bl1][channel] = visbility[bl2]  # write data to baseline_data
                            self.baseline_data_flag[bl1][channel] = True
                            bl1 += 1
                        bl2 += 1

                newch = channel % 2
                for antenna in range(0, 8):
                    buff1 = self.in_file.read(8)
                    r1, r2 = self.convert_auto_correlation(buff1)
                    self.auto_correlation_data[0 + channel - newch][0 + antenna * 8 + newch * 4] = r1
                    self.auto_correlation_data[1 + channel - newch][0 + antenna * 8 + newch * 4] = r2

                    buff1 = self.in_file.read(8)
                    r1, r2 = self.convert_auto_correlation(buff1)
                    self.auto_correlation_data[0 + channel - newch][1 + antenna * 8 + newch * 4] = r1
                    self.auto_correlation_data[1 + channel - newch][1 + antenna * 8 + newch * 4] = r2

                    buff1 = self.in_file.read(8)
                    r1, r2 = self.convert_auto_correlation(buff1)
                    self.auto_correlation_data[0 + channel - newch][2 + antenna * 8 + newch * 4] = r1
                    self.auto_correlation_data[1 + channel - newch][2 + antenna * 8 + newch * 4] = r2

                    buff1 = self.in_file.read(8)
                    r1, r2 = self.convert_auto_correlation(buff1)
                    self.auto_correlation_data[0 + channel - newch][3 + antenna * 8 + newch * 4] = r1
                    self.auto_correlation_data[1 + channel - newch][3 + antenna * 8 + newch * 4] = r2

                    self.in_file.seek(32, 1)
                    if channel == 14 or channel == 15:
                        self.in_file.seek(-24, 1)
                        buff = self.in_file.read(16)
                        (self.par_delay[0 + antenna * 8 + newch * 4], self.par_delay[1 + antenna * 8 + newch * 4],
                         self.par_delay[2 + antenna * 8 + newch * 4],
                         self.par_delay[3 + antenna * 8 + newch * 4]) = self.convert_time_offset_high(buff)[:]

                        self.in_file.seek(8, 1)
                self.in_file.seek(72, 1)

        if self.debug:
            logger.debug("Read visibility  and auto correlation data.")
        return True

    def read_one_file(self): # data in the same channe: 780*2400
        if self.search_first_frame() == False:
            logger.error("Cannot find observational data.")
            return str(False), []
        self.seek_frame_header()


    def delay_process(self, planet):
        # print "delay processing..."
        parameter = 0.
        delay = np.ndarray(shape=(self.dr_output_antennas), dtype=float)

        if self.sub_array == 1:  # muser-1
            if planet == 'sun':
                parameter = 12.5
            elif planet == 'satellite':
                parameter = 2.5
            delayns = self.delay_compensation.get_delay_value(self.sub_array, self.current_frame_time.get_short_string())
            delay = self.par_delay*(10**9) - delayns
        else: # muser-2
            parameter = 12.5
            delay = self.par_delay

        for channel in range(0, self.sub_channels):
            bl = 0
            for antenna1 in range(0, self.antennas - 1):  #SubChannelsLow = 16
                for antenna2 in range(antenna1 + 1, self.antennas):
                    tg = delay[antenna2] - delay[antenna1]
                    tg0 = int(delay[antenna2]) - int(delay[antenna1])
                    if self.sub_array == 1:
                        Frf = (self.frequency*1e-6 + channel * 25 + parameter) / 1000.0
                        Fif = (channel * 25 + parameter + 50.0) / 1000.0
                        phai = 2 * pi * (Frf * tg - Fif * tg0)
                        self.baseline_data[bl][channel] = complex(
                            self.baseline_data[bl][channel].real * math.cos(phai) +
                            self.baseline_data[bl][channel].imag * math.sin(phai),
                            self.baseline_data[bl][channel].imag * math.cos(phai) -
                            self.baseline_data[bl][channel].real * math.sin(phai))
                    else:
                        Frf = (self.frequency*1e-6 + (15- channel) * 25 + parameter) / 1000.0
                        Fif = (channel * 25 + parameter + 50.0) / 1000.0  # local frequency(GHz)
                        phai = 2 * pi * (-Frf * tg - Fif * tg0)
                        # phai = 2 * pi * Fif * tg0 + 2 * pi * Frf * (tg - tg0)
                        self.baseline_data[bl][channel] = complex(
                            self.baseline_data[bl][channel].real * math.cos(phai) +
                            self.baseline_data[bl][channel].imag * math.sin(phai),
                            self.baseline_data[bl][channel].imag*(-1) * math.cos(phai) +
                            self.baseline_data[bl][channel].real * math.sin(phai))
                    bl = bl + 1

        if self.debug:
            logger.debug("Delay Process and fringe stopping... Done.")


