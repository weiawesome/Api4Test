import datetime
from flask import *
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
    DataIn=DataIn[2:]
    result = DataIn.decode('utf-8')[:-1]
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
    OnewayReturn = input['OnewayReturn']
    StartTime = input['StartTime']
    BackStartTime = input['BackStartTime']
    Type = input['Type']
    Tickets = input['Tickets']
    Prefer = input['Prefer']

    ################################################
    # Set Data sent to Socket
    ################################################
    State = ''

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
        StationsBy = GetStationsBy(i['StationsBy'])
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
        if (State == 'False'):
            Price[i] *= 2

    ################################################
    # Set the Return Datas and to Json type
    ################################################
    RetrunDatas = {
        'Status':'False' if(len(Datas)==0 or (State=='False' and len(BackDatas)==0)) else 'True',
        'Price': Price,
        'Datas': Datas,
        'BackDatas': BackDatas
    }
    Json_Dump = json.dumps(RetrunDatas)

    return Json_Dump


@app.route('/GetEditDatas/', methods=['POST'])
def GetEditDatas_page():
    input = request.get_json()
    StartStation = input['StartStation']
    ArriveStation = input['ArriveStation']
    StartTime = input['StartTime']
    Type = input['Type']
    Tickets = input['Tickets']

    Command = {
        "CommandType": "GetTrains",
        "StartStation": StartStation,
        "ArriveStation": ArriveStation,
        "OneWayReturn": 'False',
        "StartDate": StartTime[0:10],
        "StartTime": StartTime[15:],
        "BackStartDate": '',
        "BackStartTime": '',
        "Type": Type,
        "Prefer": '無偏好'
    }
    Result = GetDataFromSocket(Command)
    sorted(Result['Datas'], key=TimeCmp)

    ################################################
    # Set the Datas
    ################################################
    Datas = []

    for i in Result['Datas']:
        StationsBy = GetStationsBy(i['StationsBy'])
        Datas.append(
            {
                'StartTime': i['StartTime'][:5],
                'ArriveTime': i['ArriveTime'][:5],
                'TotalTime': '',
                'Order': i['Order'],
                'StationsBy': StationsBy
            }
        )
    for i in Result['Datas']:
        StationsBy = GetStationsBy(i['StationsBy'])
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
        'Fees': []
    }
    Json_Dump = json.dumps(RetrunDatas)

    return Json_Dump


@app.route('/FindLose/', methods=['POST'])
def FindLose_page():
    input = request.get_json()
    ID = input['ID']
    BookID = input['BookID']

    Command = {
        "CommandType": "FindLose",
        "ID": ID,
        "BookID": BookID
    }
    Result = GetDataFromSocket(Command)
    if (Result['OnewayReturn']=='NoData'):
        RetrunData = {
            'Status': 'False',
        }
    elif Result['OnewayReturn'] == 'False':
        try:
            Seat1=str((Result['Data1'][0]['Seat1']).replace('cabin', '車')).split(',')
        except:
            Seat1=[]
        try:
            Seat2=str((Result['Data1'][0]['Seat2']).replace('cabin', '車')).split(',')
        except:
            Seat2=[]
        try:
            Seat3=str((Result['Data1'][0]['Seat3']).replace('cabin', '車')).split(',')
        except:
            Seat3=[]
        try:
            Seat4=str((Result['Data1'][0]['Seat4']).replace('cabin', '車')).split(',')
        except:
            Seat4=[]
        try:
            Seat5=str((Result['Data1'][0]['Seat5']).replace('cabin', '車')).split(',')
        except:
            Seat5=[]
        ts = str(Result['Tickets']).split(',')
        ps = str(Result['Prices']).split(',')
        for i in range(len(ts)):
            ts[i] = int(ts[i])
        for i in range(len(ps)):
            ps[i] = int(ps[i])
        RetrunData = {
            'Status': Result['Status'],
            'StartStation': Result['Data1'][0]['StartStation'],
            'ArriveStation': Result['Data1'][0]['ArriveStation'],
            'OnewayReturn': Result['OnewayReturn'],
            'Type': Result['Type'],
            'Start': {
                'Date': str(Result['Data1'][0]['Date'][:10]).replace('-', '/'),
                'StartTime': Result['Data1'][0]['StartTime'][:5],
                'ArriveTime': Result['Data1'][0]['ArriveTime'][:5],
                'TotalTime': '',
                'Order': Result['Data1'][0]['Order'],
                'Seat': [Seat1,Seat2,Seat3,Seat4,Seat5],
                'StationsBy': GetStationsBy(Result['Data1'][0]['StationsBy'])
            },
            'Arrive': {},
            'Tickets': ts,
            'Prices': ps,
        }
    else:
        try:
            Seat1=str((Result['Data1'][0]['Seat1']).replace('cabin', '車')).split(',')
        except:
            Seat1=[]
        try:
            Seat2=str((Result['Data1'][0]['Seat2']).replace('cabin', '車')).split(',')
        except:
            Seat2=[]
        try:
            Seat3=str((Result['Data1'][0]['Seat3']).replace('cabin', '車')).split(',')
        except:
            Seat3=[]
        try:
            Seat4=str((Result['Data1'][0]['Seat4']).replace('cabin', '車')).split(',')
        except:
            Seat4=[]
        try:
            Seat5=str((Result['Data1'][0]['Seat5']).replace('cabin', '車')).split(',')
        except:
            Seat5=[]
        try:
            BackSeat1=str((Result['Data2'][0]['Seat1']).replace('cabin', '車')).split(',')
        except:
            BackSeat1=[]
        try:
            BackSeat2=str((Result['Data2'][0]['Seat2']).replace('cabin', '車')).split(',')
        except:
            BackSeat2=[]
        try:
            BackSeat3=str((Result['Data2'][0]['Seat3']).replace('cabin', '車')).split(',')
        except:
            BackSeat3=[]
        try:
            BackSeat4=str((Result['Data2'][0]['Seat4']).replace('cabin', '車')).split(',')
        except:
            BackSeat4=[]
        try:
            BackSeat5=str((Result['Data2'][0]['Seat5']).replace('cabin', '車')).split(',')
        except:
            BackSeat5=[]
        TimeOfD1=datetime.datetime.strptime(str(Result['Data1'][0]['Date'][:10])+'-'+Result['Data1'][0]['StartTime'], "%Y-%m-%d-%H:%M:%S")
        TimeOfD2 = datetime.datetime.strptime(str(Result['Data2'][0]['Date'][:10]) + '-' + Result['Data2'][0]['StartTime'], "%Y-%m-%d-%H:%M:%S")
        if(TimeOfD1>TimeOfD2):
            State=False
        else:
            State=True
        ts = str(Result['Tickets']).split(',')
        ps = str(Result['Prices']).split(',')
        for i in range(len(ts)):
            ts[i] = int(ts[i])
        for i in range(len(ps)):
            ps[i] = int(ps[i])
        Data1={
                'Date': str(Result['Data1'][0]['Date'][:10]).replace('-', '/'),
                'StartTime': Result['Data1'][0]['StartTime'][:5],
                'ArriveTime': Result['Data1'][0]['ArriveTime'][:5],
                'TotalTime': '',
                'Order': Result['Data1'][0]['Order'],
                'Seat': [Seat1, Seat2, Seat3, Seat4, Seat5],
                'StationsBy': GetStationsBy(Result['Data1'][0]['StationsBy'])
            }
        Data2={
                'Date': str(Result['Data2'][0]['Date'][:10]).replace('-', '/'),
                'StartTime': Result['Data2'][0]['StartTime'][:5],
                'ArriveTime': Result['Data2'][0]['ArriveTime'][:5],
                'TotalTime': '',
                'Order': Result['Data2'][0]['Order'],
                'Seat': [BackSeat1, BackSeat2, BackSeat3, BackSeat4, BackSeat5],
                'StationsBy': GetStationsBy(Result['Data2'][0]['StationsBy'])
            }
        RetrunData = {
            'Status': Result['Status'],
            'StartStation': Result['Data1'][0]['StartStation'] if State else Result['Data1'][0]['ArriveStation'],
            'ArriveStation': Result['Data1'][0]['ArriveStation'] if State else Result['Data1'][0]['StartStation'],
            'OnewayReturn': Result['OnewayReturn'],
            'Type': Result['Type'],
            'Start': Data1 if State else Data2,
            'Arrive': Data2 if State else Data1,
            'Tickets': ts,
            'Prices': ps,
        }
    Json_Dump = json.dumps(RetrunData)
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
        StationsBy = GetStationsBy(i['StationsBy'])
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


@app.route('/Pay/', methods=['POST'])
def Pay_page():
    input = request.get_json()
    BookID = input['BookID']
    Command = {
        "CommandType": "Pay",
        "BookID": BookID
    }

    Result = GetDataFromSocket(Command)
    data_set = {'Status': Result['PayResult']}
    Json_Dump = json.dumps(data_set)
    return Json_Dump


@app.route('/Use/', methods=['POST'])
def Use_page():
    input = request.get_json()
    BookID = input['BookID']
    OnewayReturn = input['OnewayReturn']
    Order = input['Order']
    Seat = input['Seat']
    ArriveOrder = input['ArriveOrder']
    ArriveSeat = input['ArriveSeat']
    Seat = str(Seat).replace('車', 'cabin')
    ArriveSeat = str(ArriveSeat).replace('車', 'cabin')
    Command = {
        "CommandType": "Use",
        "BookID": BookID,
        "Order": Order,
        "Seat": Seat
    }
    Result = GetDataFromSocket(Command)
    if (OnewayReturn != 'true'):
        data_set = {'Status': Result['UseResult'], 'Out': 'True'}
    else:
        if (Result['UseResult'] == 'True'):
            data_set = {'Status': Result['UseResult'], 'Out': 'False'}
        else:
            Command = {
                "CommandType": "Use",
                "BookID": BookID,
                "Order": ArriveOrder,
                "Seat": ArriveSeat
            }
            Result = GetDataFromSocket(Command)
            data_set = {'Status': Result['UseResult'], 'Out': 'True'}
    Json_Dump = json.dumps(data_set)
    return Json_Dump


@app.route('/CheckID/', methods=['POST'])
def CheckID_page():
    input = request.get_json()
    Name = input['Name']
    Gender = input['Gender']
    ID = input['ID']
    Phone = input['Phone']
    Email = input['Email']

    Command = {
        "CommandType": "CheckID",
        "ID": ID,
        "Phone": Phone,
        "Email": Email
    }
    Result = GetDataFromSocket(Command)
    data_set = {'Status': Result['Status']}
    Json_Dump = json.dumps(data_set)
    return Json_Dump


@app.route('/FindCode/', methods=['POST'])
def FindCode_page():
    input = request.get_json()
    StartStation = input['StartStation']
    ArriveStation = input['ArriveStation']
    StartTime = input['StartTime']
    Order = input['Order']
    ID = input['ID']
    Command = {
        "CommandType": "FindCode",
        "StartStation": StartStation,
        "ArriveStation": ArriveStation,
        "StartDate": StartTime,
        "Order": Order,
        "ID": ID
    }
    Result = GetDataFromSocket(Command)
    Datas = []
    for i in Result['Datas']:
        Datas.append({'Code': i['Code'], 'State': i['PayResult']})
    data_set = {'Status': Result['Status'], 'Datas': Datas}
    Json_Dump = json.dumps(data_set)
    return Json_Dump


@app.route('/Book/', methods=['POST'])
def Book_page():
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
        State = 'True'
        Command = {
            "CommandType": "Book",
            "ID": ID,
            "OneWayReturn": State,
            "StartDate": StartDate[0:10],
            "StartStation": StartStation,
            "ArriveStation": ArriveStation,
            "Tickets": Tickets,
            "Order": Order,
            "Type": Type,
            "Prefer": Prefer
        }
    else:
        State = 'False'
        Command = {
            "CommandType": "Book",
            "ID": ID,
            "OneWayReturn": State,
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

    Result = GetDataFromSocket(Command)
    Seats = []
    BackSeats = []
    Seat1 = Result['GoSeat1'].split(',')
    Seat2 = Result['GoSeat2'].split(',')
    Seat3 = Result['GoSeat3'].split(',')
    Seat4 = Result['GoSeat4'].split(',')
    Seat5 = Result['GoSeat5'].split(',')
    for i in range(len(Seat1)):
        Seat1[i] = Seat1[i].replace('cabin', '車')
    for i in range(len(Seat2)):
        Seat2[i] = Seat2[i].replace('cabin', '車')
    for i in range(len(Seat3)):
        Seat3[i] = Seat3[i].replace('cabin', '車')
    for i in range(len(Seat4)):
        Seat4[i] = Seat4[i].replace('cabin', '車')
    for i in range(len(Seat5)):
        Seat5[i] = Seat5[i].replace('cabin', '車')
    Seats = [Seat1, Seat2, Seat3, Seat4, Seat5]
    if (BackOrder != 'None'):
        BackSeat1 = Result['BackSeat1'].split(',')
        BackSeat2 = Result['BackSeat2'].split(',')
        BackSeat3 = Result['BackSeat3'].split(',')
        BackSeat4 = Result['BackSeat4'].split(',')
        BackSeat5 = Result['BackSeat5'].split(',')
        for i in range(len(BackSeat1)):
            BackSeat1[i] = BackSeat1[i].replace('cabin', '車')
        for i in range(len(BackSeat2)):
            BackSeat2[i] = BackSeat2[i].replace('cabin', '車')
        for i in range(len(BackSeat3)):
            BackSeat3[i] = BackSeat3[i].replace('cabin', '車')
        for i in range(len(BackSeat4)):
            BackSeat4[i] = BackSeat4[i].replace('cabin', '車')
        for i in range(len(BackSeat5)):
            BackSeat5[i] = BackSeat5[i].replace('cabin', '車')
        BackSeats = [BackSeat1, BackSeat2, BackSeat3, BackSeat4, BackSeat5]

    Status=''
    if (Result['RecordID'] == 'NoSeat'):
        Status = 'False'
    else:
        Status = 'True'
    data_set = {'Status': Status, 'BookID': Result['RecordID'], 'Seat': Seats, 'BackSeat': BackSeats}
    Json_Dump = json.dumps(data_set)

    return Json_Dump


@app.route('/Edit/', methods=['POST'])
def Edit_page():
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

    Command = {
        "CommandType": "Edit",
        "BookID": BookID,
        "OneWayReturn": "False" if BackOrder == 'None' else 'True',
        "StartDate": StartDate[:10],
        "BackDate": "" if BackOrder == 'None' else BackDate[:10],
        "Order": Order,
        "BackOrder": BackOrder
    }

    Result = GetDataFromSocket(Command)

    Seats = []
    BackSeats = []
    Seat1 = Result['GoSeat1'].split(',')
    Seat2 = Result['GoSeat2'].split(',')
    Seat3 = Result['GoSeat3'].split(',')
    Seat4 = Result['GoSeat4'].split(',')
    Seat5 = Result['GoSeat5'].split(',')
    for i in range(len(Seat1)):
        Seat1[i] = Seat1[i].replace('cabin', '車')
    for i in range(len(Seat2)):
        Seat2[i] = Seat2[i].replace('cabin', '車')
    for i in range(len(Seat3)):
        Seat3[i] = Seat3[i].replace('cabin', '車')
    for i in range(len(Seat4)):
        Seat4[i] = Seat4[i].replace('cabin', '車')
    for i in range(len(Seat5)):
        Seat5[i] = Seat5[i].replace('cabin', '車')
    Seats = [Seat1, Seat2, Seat3, Seat4, Seat5]
    if (BackOrder != 'None'):
        BackSeat1 = Result['BackSeat1'].split(',')
        BackSeat2 = Result['BackSeat2'].split(',')
        BackSeat3 = Result['BackSeat3'].split(',')
        BackSeat4 = Result['BackSeat4'].split(',')
        BackSeat5 = Result['BackSeat5'].split(',')
        for i in range(len(BackSeat1)):
            BackSeat1[i] = BackSeat1[i].replace('cabin', '車')
        for i in range(len(BackSeat2)):
            BackSeat2[i] = BackSeat2[i].replace('cabin', '車')
        for i in range(len(BackSeat3)):
            BackSeat3[i] = BackSeat3[i].replace('cabin', '車')
        for i in range(len(BackSeat4)):
            BackSeat4[i] = BackSeat4[i].replace('cabin', '車')
        for i in range(len(BackSeat5)):
            BackSeat5[i] = BackSeat5[i].replace('cabin', '車')
        BackSeats = [BackSeat1, BackSeat2, BackSeat3, BackSeat4, BackSeat5]

    data_set = {'Status': Result['Status'], 'Seat': Seats, 'BackSeat': BackSeats}
    Json_Dump = json.dumps(data_set)

    return Json_Dump


@app.route('/Refund/', methods=['POST'])
def Refund_page():
    input = request.get_json()
    BookID = input['BookID']
    Order=input['Order']
    Seat=input['Seat']
    Command = {
        "CommandType": "Refund",
        "BookID": BookID,
        "Order":Order,
        "Seat":Seat
    }
    Result = GetDataFromSocket(Command)
    data_set = {'Status': Result['RefundResult']}
    Json_Dump = json.dumps(data_set)

    return Json_Dump

@app.route('/Take/', methods=['POST'])
def Take_page():
    input = request.get_json()
    BookID = input['BookID']
    Datas=input['Datas']
    Results=[]
    for i in Datas:
        Command = {
            "CommandType": "Take",
            "BookID":BookID,
            "Order": i[0],
            "Seat": i[1]
        }
        Results.append(GetDataFromSocket(Command))
    for i in Results:
        if(i['TakeResult']=='False'):
            data_set = {'Status': i['TakeResult']}
            break
        else:
            data_set = {'Status': i['TakeResult']}
    
    Json_Dump = json.dumps(data_set)

    return Json_Dump

@app.route('/HasTake/', methods=['POST'])
def HasTake_page():
    input = request.get_json()
    BookID = input['BookID']
    Datas = input['Datas']
    Results = []
    for i in Datas:
        Command = {
            "CommandType": "HasTake",
            "BookID": BookID,
            "Order": i[0],
            "Seat": i[1]
        }
        Results.append(GetDataFromSocket(Command))
    for i in Results:
        if (i['TakeResult'] == 'False'):
            data_set = {'Status': i['TakeResult']}
            break
        else:
            data_set = {'Status': i['TakeResult']}
    Json_Dump = json.dumps(data_set)

    return Json_Dump
