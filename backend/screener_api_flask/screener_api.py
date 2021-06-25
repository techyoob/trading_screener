


# Commemt 



import talib
import pandas as pd
from flask import Flask, jsonify, make_response, request
from pymongo import MongoClient
from io import StringIO
from datetime import datetime
import requests
import json

import os
from dotenv import load_dotenv
load_dotenv()


from cors_controller import CorsController
from stock_watch_route import StockRequest
from strategies_route import StrategyRequest
from alerts_route import AlertRequest
from manager_route import ManagerRequest


app = Flask(__name__)



response_404 = {
    "status":404,
    "results":[]
}

response_200 = {
    "status":200,
    "results":""
}




@app.route('/', methods=['OPTIONS', 'GET'])
def home():
    cors=CorsController()
    if request.method == 'OPTIONS': 
        return cors.preflight()
    elif request.method == 'GET':
        return cors.response_control({"code": "success"})




@app.route('/api/v1/alert', methods=['OPTIONS', 'GET'])
def api_alert():
    cors=CorsController()
    if request.method == 'OPTIONS':
        return cors.preflight()
    elif request.method == 'GET':
        handler=AlertRequest(request.args)
        reply = handler.getRequest()
        return cors.response_control(reply)




@app.route('/api/v1/stock', methods=['OPTIONS', 'GET'])
def api_stock():
    cors=CorsController()
    if request.method == 'OPTIONS':
        return cors.preflight()
    elif request.method == 'GET':
        handler=StockRequest(request.args)
        reply = handler.getRequest()
        return cors.response_control(reply)




@app.route('/api/v1/screener', methods=['OPTIONS', 'GET'])
def api_screener():
    cors=CorsController()
    if request.method == 'OPTIONS':
        return cors.preflight()
    elif request.method == 'GET':
        handler=StrategyRequest(request.args)
        reply = handler.getRequest()
        return cors.response_control(reply)




@app.route('/api/v1/manager', methods=['OPTIONS', 'GET'])
def api_manager():
    cors=CorsController()
    if request.method == 'OPTIONS':
        return cors.preflight()
    elif request.method == 'GET':
        handler=ManagerRequest(request.args)
        reply = handler.getRequest()
        return cors.response_control(reply)









@app.route('/api/v1/ticker_info', methods=['OPTIONS', 'GET'])
def api_ticker_info():
    cors=CorsController()
    if request.method == 'OPTIONS':
        return cors.preflight()

    elif request.method == 'GET':
        try:
            ticker = request.args.get('ticker')

            if(ticker is None or len(ticker) < 1):
                raise Exception('ticker is None or len(ticker) < 1')

            apiKey = os.getenv("FMG_KEY")
            url = os.getenv("FMG_URL")

            stockInfoReply = requests.get(url+"quote/"+ticker+"?apikey="+apiKey)
            stockInfo = json.loads(stockInfoReply.text)[0]

            results = {
                "ticker":ticker,
                "name":stockInfo['name'],
                "price":stockInfo['price'],
                "change":stockInfo['change'],
                "change percentage":stockInfo['changesPercentage'],
                "volume":stockInfo['volume'],
                "market cap":stockInfo['marketCap'],
                "day range":"$%s - $%s" %(stockInfo['dayLow'], stockInfo['dayHigh']),
                "open":stockInfo['open']
            }

            reply = {
                "status":200,
                "results":results
            }

            return cors.response_control(reply)

        except Exception as e:
            # print('Error processing ticker with symbol ', symbol , "  and reason is ", e)
            print('Error processing ticker with symbol ', ticker )
            return cors.response_control(response_404)

def shortBigNumber(number):
    numberLength = len(str(number))
    return str(int(number/pow(10,12)))+"."+str(int(number/pow(10,10))%100)+"T" if numberLength > 12 else str(int(number/pow(10,9)))+"."+str(int(number/pow(10,7))%100)+"B" if numberLength > 9 else str(int(number/pow(10,6)))+"."+str(int(number/pow(10,4))%100)+"M" if numberLength > 6 else number


@app.route('/api/v1/ticker_history', methods=['OPTIONS', 'GET'])
def api_ticker_history():
    cors=CorsController()
    if request.method == 'OPTIONS':
        return cors.preflight()
    elif request.method == 'GET':
        try:
            results = []

            symbol = request.args.get('ticker')            
            if(symbol is None or len(symbol) < 1):
                raise Exception('symbol is None or len(symbol) < 1')
            
            
            period = request.args.get('p')            
            if(period is None):
                raise Exception('period is None or len(symbol) < 1')


            apiKey = os.getenv("FMG_KEY")
            url = os.getenv("FMG_URL")

            if(period=="1D"):
                historical5minReply = requests.get(url+"historical-chart/5min/"+symbol+"?apikey="+apiKey)

                if historical5minReply.status_code == 200:
                    results = json.loads(historical5minReply.content)[:78]
                    results.reverse()

            if(period=="5D"):
                historical5minReply = requests.get(url+"historical-chart/1hour/"+symbol+"?apikey="+apiKey)

                if historical5minReply.status_code == 200:
                    results = json.loads(historical5minReply.content)[:33]
                    results.reverse()


            reply = {
                "status":200,
                "results":results
            }

            return cors.response_control(reply)

        except Exception as e:
            # print('Error processing ticker with symbol ', symbol , "  and reason is ", e)
            print('Error processing ticker with symbol ', symbol)
            return cors.response_control(response_404)


@app.route('/api/v1/screener_header', methods=['OPTIONS', 'GET'])
def api_screener_header():
    cors=CorsController()
    if request.method == 'OPTIONS':
        return cors.preflight()
    elif request.method == 'GET':
        def aggregateHeaderTicker(ticker):

            historicalHourReply = requests.get(url+"historical-chart/1hour/"+ticker['ticker']+"?apikey="+apiKey)

            if historicalHourReply.status_code == 200:
                historicalHourData = json.loads(historicalHourReply.content)
                tickerChartData=[]
                for item in historicalHourData[:5]:
                    tickerChartData.append({
                        "date":item['date'],
                        "price":item['open']
                    })
                    
                return {
                    "symbol":ticker['ticker'],
                    "name":ticker['companyName'],
                    "price":ticker['price'],
                    "changes":ticker['changesPercentage'],
                    "chartData":tickerChartData
                }

            return {}
        try:
 
            apiKey = os.getenv("FMG_KEY")
            url = os.getenv("FMG_URL")

            activesReply = requests.get(url+"actives/"+"?apikey="+apiKey)
            headerTickersData = json.loads(activesReply.text)

            results = []
            for tickerItem in headerTickersData[:7]:
                historicalHourReply = requests.get(url+"historical-chart/1hour/"+tickerItem['ticker']+"?apikey="+apiKey)

                if historicalHourReply.status_code == 200:
                    historicalHourData = json.loads(historicalHourReply.content)
                    tickerChartData=[]
                    for item in historicalHourData[:5]:
                        tickerChartData.append({
                            "date":item['date'],
                            "price":item['open']
                        })

                results.append({
                    "symbol":tickerItem['ticker'],
                    "name":tickerItem['companyName'],
                    "price":tickerItem['price'],
                    "changes":tickerItem['changesPercentage'],
                    "chartData":tickerChartData
                })


            reply = {
                "status":200,
                "results":results
            }

            return cors.response_control(reply)

        except Exception as e:
            # print('Error processing ticker with symbol ', symbol , "  and reason is ", e)
            print('Error processing ticker with symbol ' )
            return cors.response_control(response_404)













if __name__ == "__main__":

    # import logging
    # logging.basicConfig(filename='screener_flask_api.log', format='%(asctime)s  [ %(levelname)s ]  %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    app.run(host='0.0.0.0')


