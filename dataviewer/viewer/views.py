# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from os import chdir, listdir, path
from datetime import datetime
from matplotlib import pyplot
import pandas as pd
import numpy as np
import cv2 as cv

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

def integral(data, step=1):
    toReturn = []
    for i in range(0, len(data) - 1):
        toReturn.append(float(data[i + 1] - data[i])/step)
    return toReturn

def index(request):
    chdir("/home/pi/pics")
    data = pd.read_csv("./data.csv",delimiter=",", header=0, engine='python')
    fileList = listdir("./")
    pngs = []
    for i in fileList:
        if i.endswith(".png"):
            pngs.append(i)
    newestFile = max(pngs, key=path.getctime)
    img = cv.imread(newestFile)
    chdir("/home/pi/dataviewer/dataviewer/viewer/static/viewer")
    startOfData = 7
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
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    selectedValue, thresholded = cv.threshold(img, 0, 1, cv.THRESH_OTSU)
    hist = cv.calcHist([img], [0], None, [256], [0, 256])
    pyplot.plot(hist, color="k")
    pyplot.xlabel("Pixel intensity")
    pyplot.ylabel("Pixel count")
    pyplot.title("Latest histogram")
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
    doi = data['Current White Pixels'][startOfData:len(data)].tolist()
    integration = integral(doi)
    sequence = countingSequence(len(doi))
    pyplot.plot(sequence, integration, color="red")
    pyplot.xlabel("Time (hours)")
    pyplot.ylabel("Pixel derivative")
    pyplot.title("Derivative of hourly pixel count")
    pyplot.savefig("./e.png")
    pyplot.cla()
    return render(request, 'viewer/index.html', {'time': str(datetime.now()), 'selectedValue': selectedValue})
