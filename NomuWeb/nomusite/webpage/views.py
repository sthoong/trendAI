from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def welcome(request):
    return render(request, "webpage/welcome.html", {
        'userId': "618586"
    })


def clientReport(request, id):
    print(request)
    return render(request, "webpage/client.html", {
        'clientId': id
    })


def sectorReport(request, id):
    return render(request, "webpage/sector.html", {
        'sectorId': id
    })


def marketReport(request, id):
    return render(request, "webpage/market.html", {
        'marketId': id
    })