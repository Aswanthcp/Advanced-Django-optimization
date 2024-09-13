from django.shortcuts import render
from yahoo_fin.stock_info import *


def stockpicker(request):
    tickers = tickers_nifty50()
    print(tickers)
    return render(request, "app/stockpicker.html", context={"tracker_list": tickers})


def stocktracker(request):
    return render(request, "app/stocktracker.html")
