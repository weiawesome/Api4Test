from flask import *
import time,json
import datetime

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
    retrundata={
        'data':[
            {'gotime':'06:34','arrivetime':'08:40','totaltime':'2時 06分','orderof':'803','stations':['a','b','c']},
            {'gotime':'07:34','arrivetime':'09:40','totaltime':'2時 06分','orderof':'803','stations':['a','b','c']},
            {'gotime': '06:34', 'arrivetime': '08:40', 'totaltime': '2時 06分', 'orderof': '803', 'stations': ['a', 'b', 'c']},
            {'gotime': '07:34', 'arrivetime': '09:40', 'totaltime': '2時 06分', 'orderof': '803', 'stations': ['a', 'b', 'c']},
            {'gotime': '08:34', 'arrivetime': '10:40', 'totaltime': '2時 06分', 'orderof': '803', 'stations': ['a', 'b', 'c']},
            {'gotime': '08:34', 'arrivetime': '10:40', 'totaltime': '2時 06分', 'orderof': '803', 'stations': ['a', 'b', 'c']},
            {'gotime': '08:34', 'arrivetime': '10:40', 'totaltime': '2時 06分', 'orderof': '803', 'stations': ['a', 'b', 'c']},
            {'gotime': '08:34', 'arrivetime': '10:40', 'totaltime': '2時 06分', 'orderof': '803', 'stations': ['a', 'b', 'c']},
            {'gotime': '08:34', 'arrivetime': '10:40', 'totaltime': '2時 06分', 'orderof': '803', 'stations': ['a', 'b', 'c']},
            {'gotime': '08:34', 'arrivetime': '10:40', 'totaltime': '2時 06分', 'orderof': '803', 'stations': ['a', 'b', 'c']},
            {'gotime':'08:34','arrivetime':'10:40','totaltime':'2時 06分','orderof':'803','stations':['a','b','c']}
        ]}
    json_dump=json.dumps(retrundata)
    return json_dump

@app.route('/time/',methods=['GET'])
def time_page():
    t=datetime.datetime.today()
    YMD=str(t.year)+'/'+str(t.month)+'/'+str(t.day)
    HM=str(t.hour)+':'+str(t.minute)
    W=t.isoweekday()
    data_set={'YMD':YMD,'HM':HM,'W':W}
    json_dump=json.dumps(data_set)
    return json_dump
