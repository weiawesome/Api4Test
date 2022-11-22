from flask import *
import random
import json
import socket
import struct

app = Flask(__name__)

HOST = '140.136.151.128'
PORT = 10001
def GetDataFromSocket(commands):
    print(commands)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    DataOut = json.dumps(commands)
    data = bytearray(DataOut, "utf8")
    size = len(data)
    s.sendall(struct.pack("!H", size))
    s.sendall(data)
    DataIn = s.recv(1024)
    while (DataIn.decode('unicode_escape')[-1] != '#'):
        buffer = s.recv(1024)
        DataIn += buffer
    result = DataIn.decode('unicode_escape')[2:-1]
    result = json.loads(result)
    print(result)
    s.close()
    return result


@app.route('/test/', methods=['POST'])
def test_page():
    input = request.get_json()
    start = input['StartStation']
    end = input['ArriveStation']
    oneway_return = input['OnewayReturn']
    gotime = input['StartTime']
    returntime = input['BackStartTime']
    traintype = input['Type']
    people = input['Tickets']
    prefer = input['Prefer']
    print(gotime[15:])
    print(oneway_return)
    state='False'
    if(oneway_return!='true'):
        state='True'
    j = {
        "CommandType": "GetTrains",
        "StartStation": start,
        "ArriveStation": end,
        "OneWayReturn": state,
        "StartDate": gotime[0:10],
        "StartTime": gotime[15:],
        "BackStartDate": returntime[0:10],
        "BackStartTime": returntime[15:],
        "Type": traintype,
        "Prefer": prefer
    }
    a=GetDataFromSocket(j)
    def cmp(item):
        return int(item["StartTime"][:2]) * 60 + int(item["StartTime"][3:5]) * 1
    sorted(a['Datas'],key=cmp)
    datas=[]
    backdatas=[]
    for i in a['Datas']:
        sb = i['StationsBy'].split(',')
        for j in range(len(sb)):
            if (sb[j] == '00:00:00'):
                sb[j] = ''
            else:
                sb[j] = sb[j][:5]
        datas.append({'StartTime': i['StartTime'][:5], 'ArriveTime': i['ArriveTime'][:5], 'TotalTime': '2時 06分', 'Order': i['Order'],
                      'StationsBy': sb})
    if(state=='False'):
        sorted(a['BackDatas'], key=cmp)
        for i in a['BackDatas']:
            sb = i['StationsBy'].split(',')
            for j in range(len(sb)):
                if (sb[j] == '00:00:00'):
                    sb[j] = ''
                else:
                    sb[j] = sb[j][:5]
            backdatas.append({'StartTime': i['StartTime'][:5], 'ArriveTime': i['ArriveTime'][:5], 'TotalTime': '2時 06分', 'Order': i['Order'],
                          'StationsBy': sb})
    price=(a['TicketPrice']).split(',')
    price[2],price[3],price[4]=price[1],price[1],int(price[0])*0.88
    people=people.split(',')
    for i in range(len(price)):
        price[i]=int(price[i])*int(people[i])
        if(state=='False'):
            price[i]*=2
    retrundata = {
        'Price': price,
        'Datas': datas,
        'BackDatas': backdatas
    }
    json_dump = json.dumps(retrundata)

    return json_dump


@app.route('/edit/', methods=['POST'])
def edit_page():
    input = request.get_json()
    start = input['StartStation']
    end = input['ArriveStation']
    gotime = input['StartTime']
    traintype = input['Type']
    people = input['Tickets']

    Fees = []
    price = []
    for i in (people.split(',')):
        price.append(int(i) * 100)
        Fees.append(int(i) * 10)

    num = random.randint(0, 100)
    datas = []
    for i in range(num):
        datas.append({'StartTime': '10:34', 'ArriveTime': '11:40', 'TotalTime': '1時 06分', 'Order': '616',
                      'StationsBy': ['21:30','21:41','21:50','22:05','22:17','','22:43','','','23:09','23:28','23:40']})
    num = random.randint(0, 100)
    retrundata = {
        'Price': price,
        'Datas': datas,
        'Fees': Fees
    }
    json_dump = json.dumps(retrundata)
    return json_dump


@app.route('/getlose/', methods=['POST'])
def getlose_page():
    input = request.get_json()
    ID=input['ID']
    BookID=input['BookID']

    retrundata = {
        'Status':'True',
        'StartStation':'左營',
        'ArriveStation':'板橋',
        'OnewayReturn':'True',
        'Type':'商務車廂',
        'Start':{
            'Date':'2022/10/13',
            'StartTime':'10:10',
            'ArriveTime':'12:00',
            'TotalTime':'1時5分',
            'Order':'987',
            'Seat':[['5車3A'],['3車4A','6車9A'],[],[],[]],
            'StationsBy':['21:30','21:41','21:50','22:05','22:17','','22:43','','','23:09','23:28','23:40']
        },
        'Arrive':{
            'Date': '2022/10/13',
            'StartTime':'13:00',
            'ArriveTime':'15:00',
            'TotalTime':'2時0分',
            'Order':'987',
            'Seat': [['5車3A'], ['3車4A', '6車9A'], [], [], []],
            'StationsBy': ['21:30','21:41','21:50','22:05','22:17','','22:43','','','23:09','23:28','23:40']
        },
        'Tickets':[1,2,0,0,0],
        'Prices':[100,200,0,0,0],
    }

    json_dump = json.dumps(retrundata)
    return json_dump

@app.route('/timetable/', methods=['POST'])
def timetable_page():
    input = request.get_json()
    StartStation = input['StartStation']
    ArriveStation = input['ArriveStation']
    StartTime = input['StartTime']

    j = {
        "CommandType": "GetTrains",
        "StartStation": StartStation,
        "ArriveStation": ArriveStation,
        "OneWayReturn": 'True',
        "StartDate": StartTime[0:10],
        "StartTime": StartTime[15:],
        "BackStartDate": StartTime[0:10],
        "BackStartTime": StartTime[15:],
        "Type": '標準車廂',
        "Prefer": '無偏好'
    }
    HOST = '140.136.151.128'
    PORT = 10001

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    outdata = json.dumps(j)
    print(outdata)
    data = bytearray(outdata, "utf8")
    size = len(data)
    s.sendall(struct.pack("!H", size))
    s.sendall(data)
    indata = s.recv(1024)
    while (indata.decode('unicode_escape')[-1] != '#'):
        a = s.recv(1024)
        indata += a
    print(indata)
    a = indata.decode('unicode_escape')[2:-1]
    a = json.loads(a)
    print(a)

    def cmp(item):
        return int(item["StartTime"][:2]) * 60 + int(item["StartTime"][3:5]) * 1

    sorted(a['Datas'], key=cmp)
    datas = []
    for i in a['Datas']:
        sb = i['StationsBy'].split(',')
        for j in range(len(sb)):
            if (sb[j] == '00:00:00'):
                sb[j] = ''
            else:
                sb[j] = sb[j][:5]
        datas.append({'StartTime': i['StartTime'][:5], 'ArriveTime': i['ArriveTime'][:5], 'TotalTime': '2時 06分',
                      'Order': i['Order'],
                      'StationsBy': sb})
    retrundata = {
        'data': datas,
    }
    json_dump = json.dumps(retrundata)
    return json_dump


@app.route('/pay/', methods=['POST'])
def pay_page():
    input = request.get_json()
    BookID = input['BookID']
    j = {
        "CommandType": "Pay",
        "BookID": BookID
    }
    HOST = '140.136.151.128'
    PORT = 10001

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    outdata = json.dumps(j)
    print(outdata)
    data = bytearray(outdata, "utf8")
    size = len(data)
    s.sendall(struct.pack("!H", size))
    s.sendall(data)
    indata = s.recv(1024)
    while (indata.decode('unicode_escape')[-1] != '#'):
        a = s.recv(1024)
        indata += a
    print(indata)
    a = indata.decode('unicode_escape')[2:-1]
    a = json.loads(a)
    print(a)
    data_set = {'Status': a['PayResult']}
    json_dump = json.dumps(data_set)
    return json_dump


@app.route('/use/', methods=['POST'])
def use_page():
    input = request.get_json()
    BookID = input['BookID']
    Order=input['Order']
    Seat=input['Seat']
    Seat=str(Seat).replace('車','cabin')
    j={
        "CommandType": "Use",
        "BookID": BookID,
        "Order": Order,
        "Seat": Seat
    }
    a=GetDataFromSocket(j)
    data_set = {'Status': a['UseResult'],'Out':'True'}
    json_dump = json.dumps(data_set)
    return json_dump


@app.route('/checkID/', methods=['POST'])
def check_page():
    input = request.get_json()
    Name = input['Name']
    Gender = input['Gender']
    ID = input['ID']
    Phone = input['Phone']
    Email = input['Email']
    HOST = '140.136.151.128'
    PORT = 10001

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    j ={
      "CommandType": "CheckID",
      "ID": ID,
      "Phone": Phone,
      "Email": Email
    }


    outdata = json.dumps(j)
    print(outdata)
    data = bytearray(outdata, "utf8")
    size = len(data)
    s.sendall(struct.pack("!H", size))
    s.sendall(data)
    print('has do it')
    indata = s.recv(1024)
    print(type(indata))
    a=indata.decode('unicode_escape')[2:-1]
    a=json.loads(a)
    print(a)
    data_set = {'Status': a['Status']}
    json_dump = json.dumps(data_set)
    s.close()
    return json_dump

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
        datas.append({'Code':'12345678','State':'False','DeadLine':'False'})
    num = random.randint(1, 5)
    for i in range(num):
        datas.append({'Code':'12345678','State':'True','DeadLine':'False'})
    data_set = {'Status': 'True','Datas':datas}
    json_dump = json.dumps(data_set)
    return json_dump

@app.route('/book/', methods=['POST'])
def book_page():
    input = request.get_json()
    Name = input['Name']
    ID=input['ID']
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
    Prefer=input['Prefer']

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

    a=GetDataFromSocket(j)
    seats=[]
    backseats=[]
    seat1=a['GoSeat1'].split(',')
    seat2 = a['GoSeat2'].split(',')
    seat3 = a['GoSeat3'].split(',')
    seat4 = a['GoSeat4'].split(',')
    seat5 = a['GoSeat5'].split(',')
    for i in range(len(seat1)):
        seat1[i]=seat1[i].replace('cabin','車')
    for i in range(len(seat2)):
        seat2[i]=seat2[i].replace('cabin','車')
    for i in range(len(seat3)):
        seat3[i]=seat3[i].replace('cabin','車')
    for i in range(len(seat4)):
        seat4[i]=seat4[i].replace('cabin','車')
    for i in range(len(seat5)):
        seat5[i]=seat5[i].replace('cabin','車')
    seats = [seat1, seat2, seat3, seat4,seat5]
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
        backseats = [backseat1, backseat2, backseat3, backseat4,backseat5]


    status='True'
    if(a['RecordID']=='NoSeat'):
        status='False'
    data_set = {'Status': status, 'Result': a['RecordID'], 'Seat':seats, 'BackSeat': backseats}
    json_dump = json.dumps(data_set)

    return json_dump


@app.route('/editnow/', methods=['POST'])
def editnow_page():
    input = request.get_json()
    BookID=input['BookID']
    StartDate = input['StartDate']
    BackDate = input['BackDate']
    Order = input['Order']
    BackOrder = input['BackOrder']
    StartTime = input['StartTime']
    ArriveTime = input['ArriveTime']
    BackStartTime = input['BackStartTime']
    BackArriveTime = input['BackArriveTime']
    Tickets=input['Tickets']

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
    json_dump = json.dumps(data_set)

    return json_dump

@app.route('/refundnow/', methods=['POST'])
def refundnow_page():
    input = request.get_json()
    BookID=input['BookID']

    data_set = {'Status': 'True'}
    json_dump = json.dumps(data_set)

    return json_dump

