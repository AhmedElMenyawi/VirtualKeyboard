import os
import time

import numpy as np
import scipy.signal

import numpy
import statistics
import pickle

from scipy.signal import butter, lfilter
from pylab import *

import pywt

def Normalize(Signal):
    Values = Signal
    minr = -1
    maxr = 1
    result = 0
    NewValues = []
    Values = np.array(Values)
    ValuesMin = min(Values)
    ValuesMax = max(Values)
    for i in range(0, len(Values)):
        result = ((Values[i] - ValuesMin) / float(ValuesMax - ValuesMin)) + minr
        NewValues.append(result)
    return NewValues


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def butter_highpass(cutoff, fs, order=2):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a


def butter_highpass_filter(data, cutoff, fs, order=2):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = scipy.signal.filtfilt(b, a, data)  # filtfilt
    return y


def Filter_Signal(MySignal):
    return butter_highpass_filter(butter_lowpass_filter(MySignal, 20, 176, 5), 0.05, 176, 2)


def Calculate_Mean(signal):
    return statistics.mean(signal)


def Decimate_Signal(Filtered_Signal):
    # return scipy.signal.resample(Filtered_Signal[:250],5)
    return scipy.signal.decimate(Filtered_Signal[:250], 5)


def Concatenate_Signal_Channels(horizontal_signal, vertical_signal):  # Meno_Checked
    return (horizontal_signal + vertical_signal)


def ProcessSignal(Signal):
    Signal = list(numpy.array(Signal) - Calculate_Mean(Signal))
    Signal = list(Filter_Signal(Signal))
    Signal = list(Decimate_Signal(Signal))
    Signal = Normalize(Signal)
    return Signal


def ExtractFeatures(Signal):
    A3, D2, D1 = pywt.wavedec(Signal, 'db1', level=2)
    WaveletFeat = []
    size = len(A3) + len(D2) + len(D1)
    for value in A3:
        WaveletFeat.append(value)
    for value in D2:
        WaveletFeat.append(value)
    for value in D1:
        WaveletFeat.append(value)
    return WaveletFeat


def Classify(Label):
    if Label == 0:
        return "Down"
    elif Label == 1:
        return "Blink"
    elif Label == 2:
        return "Right"
    elif Label == 3:
        return "Left"
    elif Label == 4:
        return "Up"