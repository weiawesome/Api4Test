from flask import *
import time,json
import datetime
import random

app=Flask(__name__)
chiness_weeksate=['零','一','二','三','四','五','六','日']
# @app.route('/',methods=['GET'])
# def home_page():
#     data_set={'Page':'Home','Messege':'Sucess loaded the home page','Timestamp':time.time()}
#     json_dump=json.dumps(data_set)
#     return json_dump

@app.route('/user/',methods=['GET'])
def request_page():
    user_query=str(request.args.get('user'))
    # print(user_query)
    data_set={'Page':'Request','Messege':f'Sucess got the request for {user_query}','Timestamp':time.time()}
    json_dump=json.dumps(data_set)
    return json_dump

@app.route('/test/',methods=['POST'])
def test_page():
    input=request.get_json()
    start=input['start']
    end=input['end']
    oneway_return=input['oneway_return']
    gotime=input['gotime']
    returntime=input['returntime']
    traintype=input['traintype']
    people=input['people']
    prefer=input['prefer']
    data=[start,end,oneway_return,gotime,returntime,traintype,people,prefer]
    num=random.randint(0, 100)
    datas=[]
    for i in range(num):
        datas.append({'gotime':'06:34','arrivetime':'08:40','totaltime':'2時 06分','orderof':'803','stations':['a','b','c']});
    num=random.randint(0, 100)
    backdatas=[]
    for i in range(num):
        backdatas.append({'gotime':'06:34','arrivetime':'08:40','totaltime':'2時 06分','orderof':'803','stations':['a','b','c']});
    # retrundata = {
    #     'data': [
    #         {'gotime': '06:34', 'arrivetime': '08:40', 'totaltime': '2時 06分', 'orderof': '803',
    #          'stations': ['a', 'b', 'c']},
    #         {'gotime': '07:34', 'arrivetime': '09:40', 'totaltime': '2時 06分', 'orderof': '803',
    #          'stations': ['a', 'b', 'c']},
    #         {'gotime': '06:34', 'arrivetime': '08:40', 'totaltime': '2時 06分', 'orderof': '803',
    #          'stations': ['a', 'b', 'c']},
    #         {'gotime': '07:34', 'arrivetime': '09:40', 'totaltime': '2時 06分', 'orderof': '803',
    #          'stations': ['a', 'b', 'c']},
    #         {'gotime': '08:34', 'arrivetime': '10:40', 'totaltime': '2時 06分', 'orderof': '803',
    #          'stations': ['a', 'b', 'c']},
    #         {'gotime': '08:34', 'arrivetime': '10:40', 'totaltime': '2時 06分', 'orderof': '803',
    #          'stations': ['a', 'b', 'c']},
    #         {'gotime': '08:34', 'arrivetime': '10:40', 'totaltime': '2時 06分', 'orderof': '803',
    #          'stations': ['a', 'b', 'c']},
    #         {'gotime': '08:34', 'arrivetime': '10:40', 'totaltime': '2時 06分', 'orderof': '803',
    #          'stations': ['a', 'b', 'c']},
    #         {'gotime': '08:34', 'arrivetime': '10:40', 'totaltime': '2時 06分', 'orderof': '803',
    #          'stations': ['a', 'b', 'c']},
    #         {'gotime': '08:34', 'arrivetime': '10:40', 'totaltime': '2時 06分', 'orderof': '803',
    #          'stations': ['a', 'b', 'c']},
    #         {'gotime': '08:34', 'arrivetime': '10:40', 'totaltime': '2時 06分', 'orderof': '803',
    #          'stations': ['a', 'b', 'c']}
    #     ]}
    retrundata = {
        'tickets':[1,1,1,1,1],
        'price':[100,200,300,400,500],
        'data': datas,
        'backdata':backdatas
        }
    json_dump=json.dumps(retrundata)
    return json_dump

@app.route('/pay/',methods=['POST'])
def pay_page():
    input=request.get_json()
    BookID=input['BookID']
    data_set = {'Status': True}
    json_dump = json.dumps(data_set)
    return json_dump

@app.route('/book/',methods=['POST'])
def book_page():
    input = request.get_json()
    StartDate=input['StartDate']
    BackDate=input['BackDate']
    Tickets=input['Tickets']
    Order=input['Order']
    BackOrder=input['BackOrder']
    StartStation=input['StartStation']
    ArriveStation=input['ArriveStation']
    StartTime=input['StartTime']
    ArriveTime=input['ArriveTime']
    BackStartTime=input['BackStartTime']
    BackArriveTime=input['BackArriveTime']

    #產生八碼編號
    n=['0','1','2','3','4','5','6','7','8','9']
    result=''
    for i in range(8):
        result+=random.choice(n)
    data_set = {'Status':'True','Result':{result}}
    json_dump = json.dumps(data_set)

    return  json_dump


@app.route('/time/',methods=['GET'])
def time_page():
    t=datetime.datetime.today()
    YMD=str(t.year)+'/'+str(t.month)+'/'+str(t.day)
    HM=str(t.hour)+':'+str(t.minute)
    W=t.isoweekday()
    data_set={'YMD':YMD,'HM':HM,'W':W}
    json_dump=json.dumps(data_set)
    return json_dump
