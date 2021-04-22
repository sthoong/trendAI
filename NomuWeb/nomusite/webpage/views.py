import os

from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from django.contrib.staticfiles.storage import staticfiles_storage
from pathlib import Path


# Create your views here.
def welcome(request):
    return render(request, "webpage/welcome.html", {
        'userId': "618586"
    })


def clientReport(request, id):
    print(request)
    BASE_DIR = Path(__file__).resolve().parent.parent
    csvFile = staticfiles_storage.path(os.path.join(BASE_DIR, 'static/csv/'+id+'.csv'))
    data = loadCsv(csvFile, colName=["Sector","Ticker","Title","Rating","TP"])
    sectorList = data.Sector.to_list()
    tickerList = data.Ticker.to_list()
    reportList = data.Title.to_list()
    ratingList = data.Rating.to_list()
    priceList = data.TP.to_list()

    print(tickerList)
    return render(request, "webpage/client.html", {
        'clientId': id,
        'sectorList': sectorList,
        'tickerList': tickerList,
        'reportList': reportList,
        'ratingList': ratingList,
        'priceList': priceList
    })


def sectorReport(request, id):
    return render(request, "webpage/sector.html", {
        'sectorId': id
    })


def marketReport(request, id):
    return render(request, "webpage/market.html", {
        'marketId': id
    })


# Internal Utilities functions
def loadCsv(csvFile, colName):
    return pd.read_csv(csvFile)

