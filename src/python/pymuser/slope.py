import numpy as np
import heapq

def find_nearest_index(arr, value):
    """For a given value, the function finds the nearest value 
    in the array and returns its index."""
    arr = np.array(arr)
    index = (np.abs(arr - value)).argmin()
    return index


#the following two functions are taken from: 
#https://gist.github.com/1178136

def _datacheck_peakdetect(x_axis, y_axis):
    if x_axis is None:
        x_axis = range(len(y_axis))
    
    if len(y_axis) != len(x_axis):
        raise ValueError('Input vectors y_axis and x_axis must have same length')
    
    #needs to be a numpy array
    y_axis = np.array(y_axis)
    x_axis = np.array(x_axis)
    return x_axis, y_axis


def peakdetect(y_axis, x_axis=None, lookahead=300, delta=15, detectwidth = 40):
    """
    Converted from/based on a MATLAB script at: 
    http://billauer.co.il/peakdet.html
    
    function for detecting local maximas and minmias in a signal.
    Discovers peaks by searching for values which are surrounded by lower
    or larger values for maximas and minimas respectively
    
    keyword arguments:
    y_axis -- A list containg the signal over which to find peaks
    x_axis -- (optional) A x-axis whose values correspond to the y_axis list
        and is used in the return to specify the postion of the peaks. If
        omitted an index of the y_axis is used. (default: None)
    lookahead -- (optional) distance to look ahead from a peak candidate to
        determine if it is the actual peak (default: 200) 
        '(sample / period) / f' where '4 >= f >= 1.25' might be a good value
    delta -- (optional) this specifies a minimum difference between a peak and
        the following points, before a peak may be considered a peak. Useful
        to hinder the function from picking up false peaks towards to end of
        the signal. To work well delta should be set to delta >= RMSnoise * 5.
        (default: 0)
            delta function causes a 20% decrease in speed, when omitted
            Correctly used it can double the speed of the function
    
    return -- two lists [max_peaks, min_peaks] containing the positive and
        negative peaks respectively. Each cell of the lists contains a tupple
        of: (position, peak_value) 
        to get the average peak value do: np.mean(max_peaks, 0)[1] on the
        results to unpack one of the lists into x, y coordinates do: 
        x, y = zip(*tab)
    """
    max_peaks = []
    min_peaks = []
    dump = []   # Used to pop the first hit which almost always is false
    
    # check input data
    x_axis, y_axis = _datacheck_peakdetect(x_axis, y_axis)
    # store data length for later use
    length = len(y_axis)
    
    
    #perform some checks
    if lookahead < 1:
        raise ValueError, "Lookahead must be '1' or above in value"
    #NOTE: commented this to use the function with log(histogram)
    #if not (np.isscalar(delta) and delta >= 0):
    if not (np.isscalar(delta)):
        raise ValueError, "delta must be a positive number"
    
    #maxima and minima candidates are temporarily stored in
    #mx and mn respectively
    mn, mx = np.Inf, -np.Inf
    currentindex = 0

    delta = (y_axis.max()-y_axis.min())*0.03
    
    #Only detect peak if there is 'lookahead' amount of points after it
    for index, (x, y) in enumerate(zip(x_axis[:-lookahead], 
                                        y_axis[:-lookahead])):
        if y > mx:
            mx = y
            mxpos = x
        if y < mn:
            mn = y
            mnpos = x

        ####look for max####
        if y < mx-delta and mx != np.Inf:
            #Maxima peak candidate found
            #look ahead in signal to ensure that this is a peak and not jitter
            if y_axis[index:index+lookahead].max() < mx:
                max_peaks.append([mxpos, mx])
                dump.append(True)
                #set algorithm to only find minima now
                mx = np.Inf
                mn = np.Inf
                if index+lookahead >= length:
                    #end is within lookahead no more peaks can be found
                    break
                continue
            #else:  #slows shit down this does
            #    mx = ahead
            #    mxpos = x_axis[np.where(y_axis[index:index+lookahead]==mx)]
        
        ####look for min####
        if y > mn+delta and mn != -np.Inf:
            #Minima peak candidate found 
            #look ahead in signal to ensure that this is a peak and not jitter
            if y_axis[index:index+lookahead].min() > mn:
                min_peaks.append([mnpos, mn])
                dump.append(False)
                #set algorithm to only find maxima now
                mn = -np.Inf
                mx = -np.Inf
                if index+lookahead >= length:
                    #end is within lookahead no more peaks can be found
                    break
            #else:  #slows shit down this does
            #    mn = ahead
            #    mnpos = x_axis[np.where(y_axis[index:index+lookahead]==mn)]

    #Remove the false hit on the first value of the y_axis
    try:
        if dump[0]:
            max_peaks.pop(0)
        else:
            min_peaks.pop(0)
        del dump
    except IndexError:
        #no peaks were found, should the function return empty lists?
        pass
        
    return [max_peaks, min_peaks]


def check_peaks(x, y, lookahead=20, delta=0.00003):
    """
    A wrapper around peakdetect to pack the return values in a nicer format
    """
    _max, _min = peakdetect(y, x, lookahead, delta)
    x_peaks = [p[0] for p in _max] #heapq.nlargest(2,_max)]
    y_peaks = [p[1] for p in _max]
    y2_peaks = heapq.nlargest(2,y_peaks)
    x_valleys = [p[0] for p in _min]
    y_valleys = [p[1] for p in _min]
    _peaks = [x_peaks, y_peaks]

    _valleys = [x_valleys, y_valleys]
    #print {"peaks": _peaks, "valleys": _valleys}
    print y_peaks
    #print x_peaks[y_peaks.index(y2_peaks[0])],x_peaks[y_peaks.index(y2_peaks[1])]
    if len(y_peaks) <2:
        x2 = x_peaks[y_peaks.index(y2_peaks[0])]
        x1 = x2 * 0.8
    else:
        x1 = x_peaks[y_peaks.index(y2_peaks[0])]
        x2 = x_peaks[y_peaks.index(y2_peaks[1])]
    if x1 - x2 >0.:
        return x2, x1
    else:
        return x1,x2


def get_peaks(x, y, peak_amp_thresh=0.00005,
              valley_thresh=0.00003, intervals=None, lookahead=20,
              avg_interval=100):
    """
    This function expects SMOOTHED histogram. If you run it on a raw histogram,
    there is a high chance that it returns no peaks.
    method can be interval/slope/hybrid.
        The interval-based method simply steps through the whole histogram
        and pick up the local maxima in each interval, from which irrelevant
        peaks are filtered out by looking at the proportion of points on
        either side of the detected peak in each interval, and by applying
        peal_amp_thresh and valley_thresh bounds.

        Slope approach uses, of course slope information, to find peaks,
        which are then filtered by applying peal_amp_thresh and
        valley_thresh bounds.

        Hybrid approach combines the peaks obtained using slope method and
        interval-based approach. It retains the peaks/valleys from slope method
        if there should be a peak around the same region from each of the methods.

    peak_amp_thresh is the minimum amplitude/height that a peak should have
    in a normalized smoothed histogram, to be qualified as a peak.
    valley_thresh is viceversa for valleys!
    If the method is interval/hybrid, then the intervals argument must be passed
    and it should be an instance of Intervals class.
    If the method is slope/hybrid, then the lookahead and avg_window
    arguments should be changed based on the application.
    They have some default values though.
    The method stores peaks in peaks in the following format:
    {"peaks":[[peak positions], [peak amplitudes]],
    "valleys": [[valley positions], [valley amplitudes]]}
    """

    peaks = {}
    slope_peaks = {}
    #Oh dear future me, please don't get confused with a lot of mess around
    # indices around here. All indices (eg: left_index etc) refer to indices
    # of x or y (of histogram).

    #step 1: get the peaks
    return check_peaks(x, y, lookahead=lookahead,
                         delta=valley_thresh)

    #step 2: find left and right valley points for each peak
    #peak_data = result["peaks"]
    #valley_data = result["valleys"]

    #return peak_data, valley_data

    for i in xrange(len(peak_data[0])):
        nearest_index = find_nearest_index(valley_data[0],
                                                 peak_data[0][i])
        if valley_data[0][nearest_index] < peak_data[0][i]:
            left_index = find_nearest_index(
                x, valley_data[0][nearest_index])
            if len(valley_data[0][nearest_index + 1:]) == 0:
                right_index = find_nearest_index(
                    x, peak_data[0][i] + avg_interval / 2)
            else:
                offset = nearest_index + 1
                nearest_index = offset + find_nearest_index(
                    valley_data[0][offset:], peak_data[0][i])
                right_index = find_nearest_index(
                    x, valley_data[0][nearest_index])
        else:
            right_index = find_nearest_index(
                x, valley_data[0][nearest_index])
            if len(valley_data[0][:nearest_index]) == 0:
                left_index = find_nearest_index(
                    x, peak_data[0][i] - avg_interval / 2)
            else:
                nearest_index = find_nearest_index(
                    valley_data[0][:nearest_index], peak_data[0][i])
                left_index = find_nearest_index(
                    x, valley_data[0][nearest_index])

        pos = find_nearest_index(x, peak_data[0][i])
        slope_peaks[pos] = [peak_data[1][i], left_index, right_index]

    peaks = slope_peaks

    # Finally, filter the peaks and retain eligible peaks, also get
    # their valley points.

    # check 1: peak_amp_thresh
    for pos in peaks.keys():
        # pos is an index in x/y. DOES NOT refer to a cent value.
        if peaks[pos][0] < peak_amp_thresh:
            peaks.pop(pos)

    # check 2, 3: valley_thresh, proportion of size of left and right lobes
    valleys = {}
    for pos in peaks.keys():
        # remember that peaks[pos][1] is left_index and
        # peaks[pos][2] is the right_index
        left_lobe = y[peaks[pos][1]:pos]
        right_lobe = y[pos:peaks[pos][2]]
        if len(left_lobe) == 0 or len(right_lobe) == 0:
            peaks.pop(pos)
            continue
        if len(left_lobe) / len(right_lobe) < 0.15 or len(right_lobe) / len(left_lobe) < 0.15:
            peaks.pop(pos)
            continue
        left_valley_pos = np.argmin(left_lobe)
        right_valley_pos = np.argmin(right_lobe)
        if (abs(left_lobe[left_valley_pos] - y[pos]) < valley_thresh and
            abs(right_lobe[right_valley_pos] - y[pos]) < valley_thresh):
            peaks.pop(pos)
        else:
            valleys[peaks[pos][1] + left_valley_pos] = left_lobe[left_valley_pos]
            valleys[pos + right_valley_pos] = right_lobe[right_valley_pos]

    if len(peaks) > 0:
        peak_amps = np.array(peaks.values())
        peak_amps = peak_amps[:, 0]
        # hello again future me, it is given that you'll pause here
        # wondering why the heck we index x with peaks.keys() and
        # valleys.keys(). Just recall that pos refers to indices and
        # not value corresponding to the histogram bin. If i is pos,
        # x[i] is the bin value. Tada!!
        peaks = {'peaks': [x[peaks.keys()], peak_amps], 'valleys': [x[valleys.keys()], valleys.values()]}
    else:
        peaks = {'peaks': [[], []], 'valleys': [[], []]}