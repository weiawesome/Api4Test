from flask import *
import time,json
import datetime
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.mime.image import MIMEImage
from pathlib import Path

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
    price=[]
    for i in people:
        price.append(100*int(i))
    num=random.randint(0, 100)
    datas=[]
    for i in range(num):
        datas.append({'gotime':'06:34','arrivetime':'08:40','totaltime':'2時 06分','orderof':'803','stations':['a','b','c']});
    num=random.randint(0, 100)
    backdatas=[]
    for i in range(num):
        backdatas.append({'gotime':'06:34','arrivetime':'08:40','totaltime':'2時 06分','orderof':'803','stations':['a','b','c']});
    retrundata = {
        'price':price,
        'data': datas,
        'backdata':backdatas
        }
    json_dump=json.dumps(retrundata)
    return json_dump

@app.route('/pay/',methods=['POST'])
def pay_page():
    input=request.get_json()
    BookID=input['BookID']
    data_set = {'Status': 'True'}
    json_dump = json.dumps(data_set)
    return json_dump

@app.route('/use/',methods=['POST'])
def use_page():
    input=request.get_json()
    BookID=input['BookID']
    data_set = {'Status': 'True'}
    json_dump = json.dumps(data_set)
    return json_dump

@app.route('/checkID/',methods=['POST'])
def check_page():
    input=request.get_json()
    Name=input['Name']
    Gender = input['Gender']
    ID = input['ID']
    Phone=input['Phone']
    Email=input['Email']
    data_set = {'Status': 'True'}
    json_dump = json.dumps(data_set)
    return json_dump

@app.route('/book/',methods=['POST'])
def book_page():
    input = request.get_json()
    Name=input['Name']
    Email=input['Email']
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
    Type=input['Type']

    Tickets=int(Tickets)
    seat=[]
    n = [ '1', '2', '3', '4', '5', '6', '7', '8', '9']
    t=['A','B','C','D','E']
    v = ['1', '2', '3', '4', '5', '6', '7', '8', '9','10','11','12','13']
    print(Tickets)
    for i in range(Tickets):
        s=''
        s=random.choice(n)+'車'+'-'+random.choice(v)+random.choice(t)
        seat.append(s)
        
    #產生八碼編號
    n=['0','1','2','3','4','5','6','7','8','9']
    result=''
    for i in range(8):
        result+=random.choice(n)
    data_set = {'Status':'True','Result':result,'Seat':seat}
    json_dump = json.dumps(data_set)

    # content = MIMEMultipart()  # 建立MIMEMultipart物件
    # content["subject"] = "訂票成功通知(wei-HSR)"  # 郵件標題
    # content["from"] = "open891013@gmail.com"  # 寄件者
    # content["to"] = (Email)  # 收件者
    # print(Email)

    # name = Name
    # day = StartDate
    # start = StartStation
    # end = ArriveStation
    # text = '親愛的顧客您好!\n\n' \
    #        '{} 剛才系統已收到您\n預定於 {} \n從{}前往{}的高鐵車票!\n\n' \
    #        '目前已幫您完成訂票的手續\n' \
    #        '您的訂位編號是 {}\n\n'\
    #        'wei-wei-HSR公司祝您順心~\n\n'.format(name, day, start, end,result)
    #
    # content.attach(MIMEText(text))  # 郵件內容
    # content.attach(MIMEImage(Path("i.jpg").read_bytes()))  # 郵件圖片內容
    #
    # with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
    #     try:
    #         smtp.ehlo()  # 驗證SMTP伺服器
    #         smtp.starttls()  # 建立加密傳輸
    #         smtp.login("open891013@gmail.com", "frjweeccmqbpvviy")  # 登入寄件者gmail
    #         smtp.send_message(content)  # 寄送郵件
    #         print("成功傳送")
    #     except Exception as e:
    #         print("Error message: ", e)

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
