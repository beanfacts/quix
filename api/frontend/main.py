
from flask import Flask, redirect, url_for, request, Response
import json
app = Flask(__name__)
#import mysql.connector
import secrets
import os
import time
from flaskext.mysql import MySQL
pin_user = {}

def import_server_config(fname="conf.json"):
    if os.path.isfile(fname):
        with open(fname, "r") as f:
            data = json.load(f)
            return data
    return None

db_data = import_server_config("quixdb.json")

app.config['MYSQL_DATABASE_HOST'] = db_data["host"]
app.config['MYSQL_DATABASE_USER'] = db_data["user"]
app.config['MYSQL_DATABASE_PASSWORD'] = db_data["password"]
app.config['MYSQL_DATABASE_PORT'] = int(db_data["port"])

mydb = MySQL(app)



def generateToken():
    return secrets.token_hex(16)

def generatePin():
    return secrets.token_hex(4)

def bytes_to_int(bytes):
    
    result = 0

    for b in bytes:
        result = result * 256 + int(b)

    return result
    
    """
    if bytes == '\x00':
        return 0
    elif bytes == '\x01':
        return 1"""

def findstatus(be_active,be_enabled):
    # print("xxx data")
    # print(be_active, be_enabled)
    # print("end data")
    be_active = bytes_to_int(be_active)
    be_enabled = bytes_to_int(be_enabled)
    if be_active == True and be_enabled == True:
        return 'ok'
    elif be_active == False and be_enabled == True:
        return 'unreachable'
    elif be_active == True and be_enabled == False:
        return 'standby'
    elif be_active == False and be_enabled == False:
        return 'stopped'
    else:
        return 'type of input error'

@app.route('/api/v1/client/auth',methods=["POST","GET"])
def authenticate():

    data = json.loads(request.data.decode("utf-8"))

    if len(data) == 0 or data == None:
        result = {
                "error_msg":"invalid_username_password"
            }
        return Response(json.dumps(result), status=401, mimetype='application/json')
    mycursor = mydb.get_db().cursor()
    mycursor.execute("SELECT id, username,passwd FROM quix.Users")
    myresult = mycursor.fetchall()
    token = generateToken()
    for info in myresult:
        #print(type(info), info[0])
        if info[1] == data['username'] and info[2] == data['password']:
            userID = info[0]
            print(info[0], info[1], info[2], type(token))
            mycursor = mydb.get_db().cursor()
            mycursor.execute("INSERT INTO quix.UserTokens (token,userID) VALUES (%s,%s);",(token,userID))
            mydb.get_db().commit()
            result = {
            "token": token,
            "valid": int(time.time()) + 86400}
            return result
    result = {
        "error_msg":"invalid_username_password"
    }
    return Response(json.dumps(result), status=401, mimetype='application/json')

@app.route('/api/v1/client/backends',methods=['GET'])
def getBacken():
    #print(request.headers, type(request.headers), dict(request.headers))
    header = dict(request.headers)
    if 'Authorization' not in header:
        result = {
            "error_msg":"no_authorization_provided"
        }
        return Response(json.dumps(result), status=400, mimetype='application/json')
    user_token = header['Authorization'].split(' ')[1]
    mycursor = mydb.get_db().cursor()
    mycursor.execute(f"SELECT  UserTokens.token, UserTokens.userID from quix.UserTokens where token='{user_token}'")
    token_array = mycursor.fetchall()
    if len(token_array) == 0 or token_array == None:
        result = {
                "error_msg":"invalid_token"
            }
        return Response(json.dumps(result), status=401, mimetype='application/json')
    

    request_id = request.args.get('id')
    userID = token_array[0][1]
    backendInfoArray = []
    valid_backendID = []
    AfterBackend = {}
    mycursor = mydb.get_db().cursor()
    mycursor.execute(f"SELECT Backend.id, Backend.friendly_name, Frontend.hostname, Backend.be_active, Backend.be_enabled, Frontend.location, private_ip FROM quix.Backend INNER JOIN quix.Users ON Backend.user_id = Users.id INNER JOIN quix.Frontend on Backend.frontend_id = Frontend.id WHERE Backend.id = {userID};")
    myresult_x = mycursor.fetchall()
    for info in myresult_x:
        print(' ss', myresult_x, info)
        valid_backendID.append(info[0])
        backendInfoArray.append( {
            "id": info[0],
            "name":     info[1],
            "uplink":   info[2],
            "status":   findstatus(info[3],info[4]),
            "location": info[5]
        })
        AfterBackend =  {
            "id": info[0],
            "name":     info[1],
            "uplink":   info[2],
            "status":   findstatus(info[3],info[4]),
            "location": info[5],
            "internal_ip": info[6],
            "rules":[]
        }
    if request_id == None or len(request_id) == 0:
        result = {'data':backendInfoArray}
        return json.dumps(result)
    elif request_id != None and len(request_id) > 0 and (int(request_id) in valid_backendID):
        backendRuleArray = []
        print(request_id)            
        mycursor = mydb.get_db().cursor()
        mycursor.execute(f"SELECT Backend.friendly_name, Frontend.hostname, Backend.be_active, Backend.be_enabled,location,private_ip,public_ip,protocol,ext_port,int_port  FROM quix.Forwarding INNER JOIN quix.Frontend on Forwarding.frontend_id = Frontend.id INNER JOIN quix.Backend on Forwarding.backend_id = Backend.id where backend_id = {request_id} order by quix.Forwarding.id DESC")
        myresult = mycursor.fetchall()
        if len(myresult) == 0 or myresult == None:
            msg = AfterBackend
            return msg
        for info in myresult:
            rule = {
                            "ext_ip":  info[6],
                            "proto":    info[7],
                            "eport":    info[8],
                            "iport":    info[9]
                        }
            backendRuleArray.append(rule)
        rule_result = {
                    "name": info[0],
                    "uplink": info[1],
                    "status": findstatus(info[2],info[3]),
                    "location": info[4],
                    "internal_ip": info[5],
                    "rules": backendRuleArray
                }
        return rule_result
    elif (int(request_id) not in valid_backendID) and request_id != None and len(request_id) > 0:
        print('valid ', type(valid_backendID[0]), 'requesid', type(request_id) )
        error_result = { "error_msg":"no_permission_for_id"}
        return Response(json.dumps(error_result), status=401, mimetype='application/json')

@app.route('/api/v1/client/backends/modify',methods=['PATCH'])
def backendModify():
    #print(request.headers, type(request.headers), dict(request.headers))
    header = dict(request.headers)
    if 'Authorization' not in header:
        result = {
            "error_msg":"no_authorization_provided"
        }
        return Response(json.dumps(result), status=400, mimetype='application/json')
    user_token = header['Authorization'].split(' ')[1]
    mycursor = mydb.get_db().cursor()
    mycursor.execute(f"SELECT  UserTokens.token, UserTokens.userID from quix.UserTokens where token='{user_token}'")
    token_array = mycursor.fetchall()
    if len(token_array) == 0 or token_array == None:
        result = {
                "error_msg":"invalid_token"
            }
        return Response(json.dumps(result), status=401, mimetype='application/json')
    

    request_id = request.args.get('id')
    userID = token_array[0][1]
    valid_backendID = []
    mycursor = mydb.get_db().cursor()
    mycursor.execute(f"SELECT Backend.id FROM quix.Backend INNER JOIN quix.Users ON Backend.user_id = Users.id INNER JOIN quix.Frontend on Backend.frontend_id = Frontend.id WHERE Backend.id = {userID};")
    myresult = mycursor.fetchall()
    for info in myresult:
        print('valid info', info[0])
        valid_backendID.append(info[0])
    if request_id == None or len(request_id) == 0:
        result = {'err_message':'no_information_provided'}
        return Response(json.dumps(result), status=404, mimetype='application/json')
    elif request_id != None and len(request_id) > 0 and (int(request_id) in valid_backendID):
        mycursor = mydb.get_db().cursor()
        mycursor.execute(f"SELECT token,userID from quix.UserTokens where UserTokens.token = '{user_token}';")
        backendID = mycursor.fetchall()
        temp = request.data.decode("utf-8")
        if temp == None or len(temp) == 0:
            error_msg = {"err_msg":"no_json_provided"}
            return Response(json.dumps(error_msg), status=404, mimetype='application/json')
        print('temp is ', temp)
        temp = json.loads(temp)
        list_of_command = temp['cmd']
        if len(list_of_command) != 0:
            for operation in list_of_command:
                action = operation['op']
                data = operation['data']
                if action == "modify_kv":      
                    if 'name' in data:
                        mycursor = mydb.get_db().cursor()
                        if data['name'] == None:
                            mycursor.execute(f"UPDATE quix.Backend SET friendly_name = Null where Backend.id = '{request_id}' ;")
                            mydb.get_db().commit()
                        else:
                            mycursor.execute(f"UPDATE quix.Backend SET friendly_name = '{data['name']}' where Backend.id = '{request_id}' ;")
                            mydb.get_db().commit()  
                    print('modify')
                    if 'location' in data:
                        mycursor = mydb.get_db().cursor()
                        if data['location'] == None:                
                            mycursor.execute(f"UPDATE quix.Frontend INNER JOIN quix.Backend on Backend.frontend_id = Frontend.id SET location = Null where Backend.id = '{request_id}' ;")
                            mydb.get_db().commit()
                        else:
                            mycursor.execute(f"UPDATE quix.Frontend INNER JOIN quix.Backend on Backend.frontend_id = Frontend.id SET location = '{data['location']}' where Backend.id = '{request_id}' ;")
                            mydb.get_db().commit()
                elif action == "delete_rule":
                    mycursor = mydb.get_db().cursor()
                    mycursor.execute(f"DELETE quix.Forwarding FROM quix.Forwarding INNER JOIN quix.Addresses on Forwarding.frontend_id = Addresses.frontendID WHERE Forwarding.protocol = '{data['proto']}' AND Forwarding.ext_port = '{data['eport']}' AND Forwarding.int_port='{data['iport']}' AND Addresses.ip='{data['ext_ip']}' AND Forwarding.backend_id= '{request_id}'")
                    mydb.get_db().commit()
                    print('delete rule')
                elif action == "create_rule":
                    mycursor = mydb.get_db().cursor()
                    mycursor.execute(f"SELECT * FROM quix.Addresses where ip = '{data['ext_ip']}';")
                    list_of_externalIP = mycursor.fetchall()
                    frontend_id = list_of_externalIP[0][1]
                    print(list_of_externalIP , frontend_id)
                    if len(list_of_externalIP) != 0 and list_of_externalIP != None:
                        mycursor = mydb.get_db().cursor()
                        mycursor.execute(f"Select * from quix.Forwarding INNER JOIN quix.Addresses on Addresses.frontendID = Forwarding.frontend_id WHERE Forwarding.protocol = '{data['proto']}' AND Forwarding.ext_port = '{data['eport']}' AND Forwarding.int_port='{data['iport']}' AND Addresses.ip='{data['ext_ip']}' AND Forwarding.backend_id= '{request_id}';")
                        checkResult = mycursor.fetchall()
                        if len(checkResult) == 0 and checkResult != None:
                            mycursor.execute(f"INSERT INTO quix.Forwarding(protocol,frontend_id,ext_port,int_port,backend_id) VALUES('{data['proto']}','{frontend_id}','{data['eport']}','{data['iport']}', '{request_id}');")    
                            mydb.get_db().commit()
                            print('create rule success')
                        else:
                            message = {"err_message":'rule_already_existed'}
                            return Response(json.dumps(message), status=409, mimetype='application/json')
                    else:
                        message = {'err_message':'not_valid_rules'}
                        return Response(json.dumps(message), status=404, mimetype='application/json')

                elif action == "modify_rule":
                    mycursor = mydb.get_db().cursor()
                    mycursor.execute(f"Select * from quix.Forwarding INNER JOIN quix.Addresses on Forwarding.frontend_id = Addresses.frontendID WHERE Forwarding.protocol = '{data['from']['proto']}' AND Forwarding.ext_port = '{data['from']['eport']}' AND Forwarding.int_port='{data['from']['iport']}' AND Addresses.ip='{data['from']['ext_ip']}' AND Forwarding.backend_id= '{request_id}';")
                    checkResult = mycursor.fetchall()
                    if len(checkResult) != 0 and checkResult != None:
                        mycursor = mydb.get_db().cursor()
                        mycursor.execute(f"UPDATE quix.Forwarding INNER JOIN quix.Addresses on Forwarding.frontend_id = Addresses.frontendID SET protocol = '{data['to']['proto']}', ext_port='{data['to']['eport']}', int_port='{data['to']['iport']}' WHERE Forwarding.protocol = '{data['from']['proto']}' AND Forwarding.ext_port = '{data['from']['eport']}' AND Forwarding.int_port='{data['from']['iport']}' AND Addresses.ip='{data['from']['ext_ip']}' AND Forwarding.backend_id= '{request_id}' ")
                        mydb.get_db().commit()
                    else:
                        message = {'err_message':'forwarding_not_found'}
                        return Response(json.dumps(message), status=404, mimetype='application/json')
            result = {'operation_name':'update', 'status':'success'}
            return Response(json.dumps(result), status=200, mimetype='application/json')
    elif (int(request_id) not in valid_backendID) and request_id != None and len(request_id) > 0:
        print('valid ', type(valid_backendID[0]), 'requesid', type(request_id) )
        error_result = { "error_msg":"no_permission_for_id"}
        return Response(json.dumps(error_result), status=401, mimetype='application/json')
        


@app.route('/api/v1/client/pin',methods=['GET'])   
def tokenGenerate():
    request_id = request.args.get('type')
    header = dict(request.headers)
    user_token = header['Authorization'].split(' ')[1]
    if request_id == 'token':
        pin = generatePin()
        mycursor = mydb.get_db().cursor()
        mycursor.execute(f"SELECT token,userID from quix.UserTokens where UserTokens.token = '{user_token}';")
        userID = mycursor.fetchall()
        if len(userID) != 0 and userID != None:
            print('userID', userID)
            pin_user[pin] = userID[0][1]
            result = {
            "pin":      pin,
            "valid":    int(time.time()) + 180
        } 
            return result
        else:
            result = {
                "error_msg":"invalid_token"
            }
            return Response(json.dumps(result), status=401, mimetype='application/json')


#b579264844ff2d16

if __name__ == '__main__':
   app.run(debug = True,host="0.0.0.0")
