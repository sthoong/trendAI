import os

from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from django.contrib.staticfiles.storage import staticfiles_storage
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
def welcome(request):
    csvFile = staticfiles_storage.path(os.path.join(BASE_DIR, 'static/csv/client_welcome.csv'))
    clientData = loadCsv(csvFile)
    clientName = clientData.Client.to_list()
    clientNotional = clientData.Notional.to_list()
    clientShares = clientData.Shares.to_list()
    csvFile = staticfiles_storage.path(os.path.join(BASE_DIR, 'static/csv/market_welcome.csv'))
    marketData = loadCsv(csvFile)
    marketName = marketData.Market.to_list()
    marketNotional = marketData.Notional.to_list()
    marketShares = marketData.Shares.to_list()
    csvFile = staticfiles_storage.path(os.path.join(BASE_DIR, 'static/csv/sector_welcome.csv'))
    sectorData = loadCsv(csvFile)
    sectorName = sectorData.Sector.to_list()
    sectorNotional = sectorData.Notional.to_list()
    sectorShares = sectorData.Shares.to_list()
    return render(request, "webpage/welcome.html", {
        'userId': "618586",
        'clientName': clientName,
        'clientNotional': clientNotional,
        'clientShares': clientShares,
        'marketName': marketName,
        'marketNotional': marketNotional,
        'marketShares': marketShares,
        'sectorName': sectorName,
        'sectorNotional': sectorNotional,
        'sectorShares': sectorShares,
    })


def clientReport(request, id):

    csvFile = staticfiles_storage.path(os.path.join(BASE_DIR, 'static/csv/'+id+'_RecommendedItems.csv'))
    data = loadCsv(csvFile)
    sectorList = data.Sector.to_list()
    tickerList = data.Ticker.to_list()
    reportList = data.Title.to_list()
    ratingList = data.Rating.to_list()
    priceList = data.TP.to_list()

    similarClient = staticfiles_storage.path(os.path.join(BASE_DIR, 'static/csv/'+id+'_SimilarClientItems.csv'))
    data = loadCsv(similarClient)
    similarClientList = data.ClientName.to_list()
    similarTickerList = data.Ticker.to_list()
    similarReportList = data.Title.to_list()

    print(tickerList)
    return render(request, "webpage/client.html", {
        'clientId': id,
        'sectorList': sectorList,
        'tickerList': tickerList,
        'reportList': reportList,
        'ratingList': ratingList,
        'priceList': priceList,
        'similarClientList': similarClientList,
        'similarTickerList': similarTickerList,
        'similarReportList': similarReportList
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
def loadCsv(csvFile):
    return pd.read_csv(csvFile)

