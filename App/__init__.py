from flask import *
import random
import json
import socket
import struct

app = Flask(__name__)

HOST = '140.136.151.128'
PORT = 10001

def GetStationsBy(item):

    ################################################
    # Split the Data
    ################################################
    result = item.split(',')
    for i in range(len(result)):
        if (result[i] == '00:00:00'):
            result[i] = ''
        else:
            result[i] = result[i][:5]
    return result

def TimeCmp(item):
    return int(item["StartTime"][:2]) * 60 + int(item["StartTime"][3:5]) * 1

def GetDataFromSocket(commands):
    print(commands)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    DataOut = json.dumps(commands)
    data = bytearray(DataOut, "utf8")
    size = len(data)
    s.sendall(struct.pack("!H", size))
    s.sendall(data)
    print('Data sent!')
    DataIn = s.recv(1024)
    while (DataIn.decode('unicode_escape')[-1] != '#'):
        buffer = s.recv(1024)
        DataIn += buffer
    result = DataIn.decode('unicode_escape')[2:-1]
    result = json.loads(result)
    print('Data get!')
    print(result)
    s.close()
    return result


@app.route('/GetTrains/', methods=['POST'])
def GetTrains_page():

    ################################################
    # Get Input Datas
    ################################################
    input = request.get_json()
    StartStation = input['StartStation']
    ArriveStation = input['ArriveStation']
    OnewayReturn= input['OnewayReturn']
    StartTime = input['StartTime']
    BackStartTime = input['BackStartTime']
    Type = input['Type']
    Tickets = input['Tickets']
    Prefer = input['Prefer']

    ################################################
    # Set Data sent to Socket
    ################################################
    State=''
    
    if (OnewayReturn != 'true'):
        State = 'True'
    else:
        State = 'False'

    Command = {
        "CommandType": "GetTrains",
        "StartStation": StartStation,
        "ArriveStation": ArriveStation,
        "OneWayReturn": State,
        "StartDate": StartTime[0:10],
        "StartTime": StartTime[15:],
        "BackStartDate": BackStartTime[0:10],
        "BackStartTime": BackStartTime[15:],
        "Type": Type,
        "Prefer": Prefer
    }
    Result = GetDataFromSocket(Command)
    sorted(Result['Datas'], key=TimeCmp)

    ################################################
    # Set the Datas and BackDatas
    ################################################
    Datas = []
    BackDatas = []

    for i in Result['Datas']:
        StationsBy=GetStationsBy(i['StationsBy'])
        Datas.append(
            {
                'StartTime': i['StartTime'][:5], 
                'ArriveTime': i['ArriveTime'][:5], 
                'TotalTime': '',
                'Order': i['Order'],
                'StationsBy': StationsBy
            }
        )
        
    if (State == 'False'):
        sorted(Result['BackDatas'], key=TimeCmp)
        for i in Result['BackDatas']:
            StationsBy = GetStationsBy(i['StationsBy'])
            BackDatas.append(
                {
                    'StartTime': i['StartTime'][:5], 
                    'ArriveTime': i['ArriveTime'][:5], 
                    'TotalTime': '',
                    'Order': i['Order'],
                    'StationsBy': StationsBy
                }
            )

    ################################################
    # Set the Price
    ################################################
    Price = (Result['TicketPrice']).split(',')
    Price[2], Price[3], Price[4] = Price[1], Price[1], int(Price[0]) * 0.88
    Tickets = Tickets.split(',')
    for i in range(len(Tickets)):
        Price[i] = int(Price[i]) * int(Tickets[i])
        if (Tickets == 'False'):
            Price[i] *= 2

    ################################################
    # Set the Return Datas and to Json type
    ################################################
    RetrunDatas = {
        'Price': Price,
        'Datas': Datas,
        'BackDatas': BackDatas
    }
    Json_Dump = json.dumps(RetrunDatas)

    return Json_Dump


@app.route('/edit/', methods=['POST'])
def edit_page():
    input = request.get_json()
    StartStation = input['StartStation']
    ArriveStation = input['ArriveStation']
    StartTime = input['StartTime']
    Type = input['Type']
    Tickets = input['Tickets']

    Fees = []
    price = []
    for i in (Tickets.split(',')):
        price.append(int(i) * 100)
        Fees.append(int(i) * 10)

    num = random.randint(0, 100)
    datas = []
    for i in range(num):
        datas.append({'StartTime': '10:34', 'ArriveTime': '11:40', 'TotalTime': '1時 06分', 'Order': '616',
                      'StationsBy': ['21:30', '21:41', '21:50', '22:05', '22:17', '', '22:43', '', '', '23:09', '23:28',
                                     '23:40']})
    num = random.randint(0, 100)
    retrundata = {
        'Price': price,
        'Datas': datas,
        'Fees': Fees
    }
    Json_Dump = json.dumps(retrundata)
    return Json_Dump


@app.route('/getlose/', methods=['POST'])
def getlose_page():
    input = request.get_json()
    ID = input['ID']
    BookID = input['BookID']

    retrundata = {
        'Status': 'True',
        'StartStation': '左營',
        'ArriveStation': '板橋',
        'OnewayReturn': 'True',
        'Type': '商務車廂',
        'Start': {
            'Date': '2022/10/13',
            'StartTime': '10:10',
            'ArriveTime': '12:00',
            'TotalTime': '1時5分',
            'Order': '987',
            'Seat': [['5車3A'], ['3車4A', '6車9A'], [], [], []],
            'StationsBy': ['21:30', '21:41', '21:50', '22:05', '22:17', '', '22:43', '', '', '23:09', '23:28', '23:40']
        },
        'Arrive': {
            'Date': '2022/10/13',
            'StartTime': '13:00',
            'ArriveTime': '15:00',
            'TotalTime': '2時0分',
            'Order': '987',
            'Seat': [['5車3A'], ['3車4A', '6車9A'], [], [], []],
            'StationsBy': ['21:30', '21:41', '21:50', '22:05', '22:17', '', '22:43', '', '', '23:09', '23:28', '23:40']
        },
        'Tickets': [1, 2, 0, 0, 0],
        'Prices': [100, 200, 0, 0, 0],
    }

    Json_Dump = json.dumps(retrundata)
    return Json_Dump


@app.route('/TimeTable/', methods=['POST'])
def TimeTable_page():

    ################################################
    # Get Input Datas
    ################################################
    input = request.get_json()
    StartStation = input['StartStation']
    ArriveStation = input['ArriveStation']
    StartTime = input['StartTime']

    ################################################
    # Set Data sent to Socket
    ################################################
    Command = {
        "CommandType": "GetTrains",
        "StartStation": StartStation,
        "ArriveStation": ArriveStation,
        "OneWayReturn": 'True',
        "StartDate": StartTime[0:10],
        "StartTime": '00:00',
        "BackStartDate": StartTime[0:10],
        "BackStartTime": '00:00',
        "Type": '標準車廂',
        "Prefer": '無偏好'
    }
    Result = GetDataFromSocket(Command)
    sorted(Result['Datas'], key=TimeCmp)

    ################################################
    # Set the Datas
    ################################################
    Datas = []

    for i in Result['Datas']:
        StationsBy=GetStationsBy(i['StationsBy'])
        Datas.append(
            {
                'StartTime': i['StartTime'][:5],
                'ArriveTime': i['ArriveTime'][:5],
                'TotalTime': '',
                'Order': i['Order'],
                'StationsBy': StationsBy
            }
        )

    ################################################
    # Set the Return Datas and to Json type
    ################################################
    RetrunDatas = {
        'Datas': Datas,
    }
    Json_Dump = json.dumps(RetrunDatas)

    return Json_Dump


@app.route('/pay/', methods=['POST'])
def pay_page():
    input = request.get_json()
    BookID = input['BookID']
    j = {
        "CommandType": "Pay",
        "BookID": BookID
    }

    a = GetDataFromSocket(j)
    data_set = {'Status': a['PayResult']}
    Json_Dump = json.dumps(data_set)
    return Json_Dump


@app.route('/use/', methods=['POST'])
def use_page():
    input = request.get_json()
    BookID = input['BookID']
    Order = input['Order']
    Seat = input['Seat']
    Seat = str(Seat).replace('車', 'cabin')
    j = {
        "CommandType": "Use",
        "BookID": BookID,
        "Order": Order,
        "Seat": Seat
    }
    a = GetDataFromSocket(j)
    data_set = {'Status': a['UseResult'], 'Out': 'True'}
    Json_Dump = json.dumps(data_set)
    return Json_Dump


@app.route('/checkID/', methods=['POST'])
def check_page():
    input = request.get_json()
    Name = input['Name']
    Gender = input['Gender']
    ID = input['ID']
    Phone = input['Phone']
    Email = input['Email']

    j = {
        "CommandType": "CheckID",
        "ID": ID,
        "Phone": Phone,
        "Email": Email
    }
    a = GetDataFromSocket(j)
    data_set = {'Status': a['Status']}
    Json_Dump = json.dumps(data_set)
    return Json_Dump


@app.route('/findnow/', methods=['POST'])
def findnow_page():
    input = request.get_json()
    StartStation = input['StartStation']
    ArriveStation = input['ArriveStation']
    StartTime = input['StartTime']
    Order = input['Order']
    ID = input['ID']
    num = random.randint(1, 5)
    datas = []
    for i in range(num):
        datas.append({'Code': '12345678', 'State': 'False', 'DeadLine': 'False'})
    num = random.randint(1, 5)
    for i in range(num):
        datas.append({'Code': '12345678', 'State': 'True', 'DeadLine': 'False'})
    data_set = {'Status': 'True', 'Datas': datas}
    Json_Dump = json.dumps(data_set)
    return Json_Dump


@app.route('/book/', methods=['POST'])
def book_page():
    input = request.get_json()
    Name = input['Name']
    ID = input['ID']
    Email = input['Email']
    StartDate = input['StartDate']
    BackDate = input['BackDate']
    Tickets = input['Tickets']
    Order = input['Order']
    BackOrder = input['BackOrder']
    StartStation = input['StartStation']
    ArriveStation = input['ArriveStation']
    StartTime = input['StartTime']
    ArriveTime = input['ArriveTime']
    BackStartTime = input['BackStartTime']
    BackArriveTime = input['BackArriveTime']
    Type = input['Type']
    Prefer = input['Prefer']

    if (BackOrder == 'None'):
        state = 'True'
        j = {
            "CommandType": "Book",
            "ID": ID,
            "OneWayReturn": state,
            "StartDate": StartDate[0:10],
            "StartStation": StartStation,
            "ArriveStation": ArriveStation,
            "Tickets": Tickets,
            "Order": Order,
            "Type": Type,
            "Prefer": Prefer
        }
    else:
        state = 'False'
        j = {
            "CommandType": "Book",
            "ID": ID,
            "OneWayReturn": state,
            "StartDate": StartDate[0:10],
            "BackDate": BackDate[0:10],
            "StartStation": StartStation,
            "ArriveStation": ArriveStation,
            "Tickets": Tickets,
            "Order": Order,
            "BackOrder": BackOrder,
            "Type": Type,
            "Prefer": Prefer
        }

    a = GetDataFromSocket(j)
    seats = []
    backseats = []
    seat1 = a['GoSeat1'].split(',')
    seat2 = a['GoSeat2'].split(',')
    seat3 = a['GoSeat3'].split(',')
    seat4 = a['GoSeat4'].split(',')
    seat5 = a['GoSeat5'].split(',')
    for i in range(len(seat1)):
        seat1[i] = seat1[i].replace('cabin', '車')
    for i in range(len(seat2)):
        seat2[i] = seat2[i].replace('cabin', '車')
    for i in range(len(seat3)):
        seat3[i] = seat3[i].replace('cabin', '車')
    for i in range(len(seat4)):
        seat4[i] = seat4[i].replace('cabin', '車')
    for i in range(len(seat5)):
        seat5[i] = seat5[i].replace('cabin', '車')
    seats = [seat1, seat2, seat3, seat4, seat5]
    if (BackOrder != 'None'):
        backseat1 = a['BackSeat1'].split(',')
        backseat2 = a['BackSeat2'].split(',')
        backseat3 = a['BackSeat3'].split(',')
        backseat4 = a['BackSeat4'].split(',')
        backseat5 = a['BackSeat5'].split(',')
        for i in range(len(backseat1)):
            backseat1[i] = backseat1[i].replace('cabin', '車')
        for i in range(len(backseat2)):
            backseat2[i] = backseat2[i].replace('cabin', '車')
        for i in range(len(backseat3)):
            backseat3[i] = backseat3[i].replace('cabin', '車')
        for i in range(len(backseat4)):
            backseat4[i] = backseat4[i].replace('cabin', '車')
        for i in range(len(backseat5)):
            backseat5[i] = backseat5[i].replace('cabin', '車')
        backseats = [backseat1, backseat2, backseat3, backseat4, backseat5]

    status = 'True'
    if (a['RecordID'] == 'NoSeat'):
        status = 'False'
    data_set = {'Status': status, 'Result': a['RecordID'], 'Seat': seats, 'BackSeat': backseats}
    Json_Dump = json.dumps(data_set)

    return Json_Dump


@app.route('/editnow/', methods=['POST'])
def editnow_page():
    input = request.get_json()
    BookID = input['BookID']
    StartDate = input['StartDate']
    BackDate = input['BackDate']
    Order = input['Order']
    BackOrder = input['BackOrder']
    StartTime = input['StartTime']
    ArriveTime = input['ArriveTime']
    BackStartTime = input['BackStartTime']
    BackArriveTime = input['BackArriveTime']
    Tickets = input['Tickets']

    seat = []
    backseat = []
    n = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    t = ['A', 'B', 'C', 'D', 'E']
    v = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
    for i in Tickets.split(','):
        tmp = []
        for j in range(int(i)):
            s = ''
            s = random.choice(n) + '車' + '-' + random.choice(v) + random.choice(t)
            tmp.append(s)
        seat.append(tmp)
    if (BackOrder != 'None'):
        for i in Tickets.split(','):
            tmp = []
            for j in range(int(i)):
                s = ''
                s = random.choice(n) + '車' + '-' + random.choice(v) + random.choice(t)
                tmp.append(s)
            backseat.append(tmp)

    data_set = {'Status': 'True', 'Seat': seat, 'BackSeat': backseat}
    Json_Dump = json.dumps(data_set)

    return Json_Dump


@app.route('/refundnow/', methods=['POST'])
def refundnow_page():
    input = request.get_json()
    BookID = input['BookID']
    j = {
        "CommandType": "Refund",
        "BookID": BookID
    }
    a = GetDataFromSocket(j)
    data_set = {'Status': a['RefundResult']}
    Json_Dump = json.dumps(data_set)

    return Json_Dump
