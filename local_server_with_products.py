from flask import Flask, jsonify, request
from flask.ext.cors import CORS
from datetime import datetime
import sys
import json
import ast
from unidecode import unidecode
from flask.ext.cache import Cache

app = Flask(__name__)
CORS(app)
app.config['CACHE_TYPE'] = 'simple'
app.cache = Cache(app)

@app.route('/stateslived', methods=['GET'])
def get_stateslived():
    # f = open("stateslived.txt","r")
    f = open("states_lived_with_products.txt","r")
    contents = f.readlines()
    return_dict = {}
    result_data = []
    callback = request.args.get('callback')
    for c in contents:
        dict1 = {}
        states = c.split(",")[0]
        product_type = c.split(",")[1]
        revenue = c.split(",")[2]
        cloud = c.split(",")[3]
        visited = c.split(",")[4]
        dict1["state"] = states.strip("\n")
        dict1["product_type"] = product_type.strip("\n")
        dict1["revenue"] = revenue.strip("\n")
        dict1["cloud"] = cloud.strip("\n")
        dict1["visited"] = visited.strip("\n")
        result_data.append(dict1.copy())
    return_dict["data"] = result_data
    dynamics_crm = json.dumps(return_dict)
    return '{0}({1})'.format(callback, dynamics_crm)

@app.route('/citieslived', methods=['GET'])
def get_citieslived():
    f = open("cities_lived_with_products_original_data.txt","r")
    contents = f.readlines()
    return_dict = {}
    result_data = []
    result_data_updated = []
    new_dict1 = {}
    callback = request.args.get('callback')
    for c in contents:
        dict1 = {}
        years = c.split(",")[0]
        place = c.split(",")[1]
        product_type = c.split(",")[2]
        cloud = c.split(",")[3]
        revenue = c.split(",")[4]
        lat = c.split(",")[5]
        long = c.split(",")[6]
        dict1["years"] = years.strip("\n")
        dict1["place"] = place.strip("\n")
        dict1["product_type"] = product_type.strip("\n")
        dict1["revenue"] = revenue.strip("\n")
        dict1["cloud"] = cloud.strip("\n")
        dict1["lat"] = str(lat).strip("\n")
        dict1["lon"] = str(long).strip("\n")
        # unique_key = product_type.strip("\n") + "_" + cloud.strip("\n") + "_" + revenue.strip("\n") + "_" place.strip("\n")
        unique_key = product_type.strip("\n") + "_" + cloud.strip("\n") + "_" + revenue.strip("\n")
        if unique_key not in new_dict1.keys():
            new_dict1[unique_key] = 0
        new_dict1[unique_key] += int(years)
        result_data.append(dict1.copy())
    for i in result_data:
        for keys in new_dict1.keys():
            product_type = keys.split("_")[0]
            cloud = keys.split("_")[1]
            revenue = keys.split("_")[2]
            if ((i["product_type"] == product_type) and (i["cloud"]==cloud) and (i["revenue"]==revenue)):
                percentage = float(float(i["years"])/float(new_dict1[keys]))*100
                if int(percentage) < 1:
                    i["percentage"] = 1
                else:
                    i["percentage"] = percentage
                result_data_updated.append(i)
    return_dict["data"] = result_data_updated
    dynamics_crm = json.dumps(return_dict)
    return '{0}({1})'.format(callback, dynamics_crm)
# def get_citieslived():
    # # f = open("cities-lived.txt","r")
    # # f = open("cities-lived_with_products.txt","r")
    # f = open("cities_lived_with_products_original_data.txt","r")
    # # f = open("cities_lived_with_products_original_data_test.txt","r")
    # contents = f.readlines()
    # return_dict = {}
    # result_data = []
    # callback = request.args.get('callback')
    # for c in contents:
        # dict1 = {}
        # years = c.split(",")[0]
        # place = c.split(",")[1]
        # product_type = c.split(",")[2]
        # cloud = c.split(",")[3]
        # revenue = c.split(",")[4]
        # lat = c.split(",")[5]
        # long = c.split(",")[6]
        # dict1["years"] = years.strip("\n")
        # dict1["place"] = place.strip("\n")
        # dict1["product_type"] = product_type.strip("\n")
        # dict1["revenue"] = revenue.strip("\n")
        # dict1["cloud"] = cloud.strip("\n")
        # dict1["lat"] = str(lat).strip("\n")
        # dict1["lon"] = str(long).strip("\n")
        # result_data.append(dict1.copy())
    # return_dict["data"] = result_data
    # dynamics_crm = json.dumps(return_dict)
    # return '{0}({1})'.format(callback, dynamics_crm)

@app.route('/industries_mlb', methods=['GET'])
def get_industries_mlb():
    # f = open("cities-lived.txt","r")
    # f = open("cities-lived_with_products.txt","r")
    # f = open("industries_mlb_score.txt","r")
    f = open("industries_mlb_score_count.txt","r")
    contents = f.readlines()
    return_dict = {}
    result_data = []
    callback = request.args.get('callback')
    for c in contents:
        dict1 = {}
        industry = c.split(",")[0]
        product_type = c.split(",")[1]
        cloud = c.split(",")[2]
        revenue = c.split(",")[3]
        score = c.split(",")[4]
        counts = c.split(",")[5]
        dict1["industry"] = industry.strip("\n")
        dict1["product_type"] = product_type.strip("\n")
        dict1["revenue"] = revenue.strip("\n")
        dict1["cloud"] = cloud.strip("\n")
        # dict1["score"] = score.strip("\n")
        # dict1["counts"] = counts.strip("\n")
        dict1["score"] = round(float(score.strip("\n")),2)
        dict1["counts"] = float(counts.strip("\n"))
        result_data.append(dict1.copy())
    return_dict["data"] = result_data
    dynamics_crm = json.dumps(return_dict)
    return '{0}({1})'.format(callback, dynamics_crm)

@app.route('/industries_count_lb', methods=['GET'])
def get_industries_count_lb():
    # f = open("cities-lived.txt","r")
    # f = open("cities-lived_with_products.txt","r")
    # f = open("industries_mlb_score.txt","r")
    f = open("industries_mlb_score_count_mid_hig_low.txt","r")
    contents = f.readlines()
    return_dict = {}
    result_data = []
    callback = request.args.get('callback')
    for c in contents:
        #dict1 = {}
        dict1 = {"high": "","high_mid": "","mid":"","low": "","product_type": "","revenue": "","industry": "","score": "","counts": "","cloud": ""}
        industry = c.split(",")[0]
        product_type = c.split(",")[1]
        cloud = c.split(",")[2]
        revenue = c.split(",")[3]
        score = c.split(",")[4]
        counts = c.split(",")[5]
        low = c.split(",")[6]
        mid = c.split(",")[7]
        high_mid = c.split(",")[8]
        high = c.split(",")[9]
        dict1["high"] = round(float(high.strip("\n")),2)
        dict1["high_mid"] = round(float(high_mid.strip("\n")),2)
        dict1["mid"] = round(float(mid.strip("\n")),2)
        dict1["low"] = round(float(low.strip("\n")),2)
        dict1["industry"] = industry.strip("\n")
        dict1["product_type"] = product_type.strip("\n")
        dict1["revenue"] = revenue.strip("\n")
        dict1["cloud"] = cloud.strip("\n")
        # dict1["score"] = score.strip("\n")
        # dict1["counts"] = counts.strip("\n")
        dict1["score"] = round(float(score.strip("\n")),2)
        dict1["counts"] = float(counts.strip("\n"))
        # result_data.append(dict1.copy())
        result_data.append(dict1)
    return_dict["data"] = result_data
    dynamics_crm = json.dumps(return_dict)
    return '{0}({1})'.format(callback, dynamics_crm)

@app.route('/us_states', methods=['GET'])
def get_us_states():
    f = open("us-states.txt","r")
    contents = f.readlines()
    return_dict = {}
    result_data = []
    callback = request.args.get('callback')
    s = open('us-states.txt', 'r').read()
    whip = ast.literal_eval(s)
    result_data.append(whip)
    return_dict["data"] = result_data
    dynamics_crm = json.dumps(return_dict)
    return '{0}({1})'.format(callback, dynamics_crm)

# @app.route('/stateslived', methods=['GET'])
# def get_stateslived():
    # f = open("stateslived.txt","r")
    # contents = f.readlines()
    # return_dict = {}
    # result_data = []
    # callback = request.args.get('callback')
    # for c in contents:
        # dict1 = {}
        # states = c.split(",")[0]
        # visited = c.split(",")[0]
        # dict1["states"] = states
        # dict1["visited"] = visited
        # result_data.append(dict1.copy())
    # return_dict["data"] = result_data
    # dynamics_crm = json.dumps(return_dict)
    # return '{0}({1})'.format(callback, dynamics_crm)


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  response.cache_control.max_age = 300
  return response


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5005, debug=True)