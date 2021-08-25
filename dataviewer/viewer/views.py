# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from os import chdir
from datetime import datetime
from matplotlib import pyplot
import pandas as pd
import numpy as np

def rollingAverage(n, data):
    return np.convolve(data, np.ones(n), 'valid')/n

def dailyAverage(data):
    toReturn = []
    iterations = int(len(data)/24)
    for i in range(iterations):
        toReturn.append(np.mean(data[i * 24:(i + 1) * 24 - 1]))
    return toReturn

def countingSequence(n):
    toReturn = []
    for i in range(n):
        toReturn.append(i + 1)
    return toReturn

# Create your views here.

def index(request):
    chdir("/home/pi/pics")
    data = pd.read_csv("./data.csv",delimiter=", ", header=0, engine='python')
    chdir("/home/pi/dataviewer/dataviewer/viewer/static/viewer")
    startOfData = 60
    pyplot.plot(countingSequence(len(data[startOfData:len(data)])), data['Daily RGR'][startOfData:len(data)], color='red')
    pyplot.xlabel("Time (hours)")
    pyplot.ylabel("Daily RGR (New pixels per old pixel per day)")
    pyplot.title("RGR for the past 24 hours, recorded hourly")
    pyplot.savefig("./a.png")
    pyplot.cla()
    rolling3Hourly = rollingAverage(3, data['Daily RGR'][startOfData:len(data)])
    pyplot.plot(rolling3Hourly, color='red')
    pyplot.xlabel("Time (hours)")
    pyplot.ylabel("Daily RGR (New pixels per old pixel per day)")
    pyplot.title("RGR for the past 24 hours, recorded hourly, 3-point rolling average")
    pyplot.savefig("./b.png")
    pyplot.cla()
    highNumber = 10
    rollingHigh = rollingAverage(highNumber, data['Daily RGR'][startOfData:len(data)])
    pyplot.plot(rollingHigh, color='red')
    pyplot.xlabel("Time (hours)")
    pyplot.ylabel("Daily RGR (New pixels per old pixel per day)")
    pyplot.title("RGR for the past 24 hours, recorded hourly, " + str(highNumber) + "-point rolling average")
    pyplot.savefig("./c.png")
    pyplot.cla()
    daily = dailyAverage(data['Daily RGR'][startOfData:len(data)])
    sequence = countingSequence(len(daily))
    pyplot.scatter(sequence, daily)
    pyplot.xlabel("Time (days)")
    pyplot.ylabel("Daily RGR (New pixels per old pixel per day)")
    pyplot.title("RGR for the past 24 hours, recorded every hour, averaged every 24 hours")
    pyplot.savefig("./d.png")
    pyplot.cla()
    return render(request, 'viewer/index.html', {'time': str(datetime.now())})
    return HttpResponse("<img src='./static/viewer/a.png'>")