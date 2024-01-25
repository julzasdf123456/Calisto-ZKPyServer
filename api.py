from flask import Flask, jsonify, request
from datetime import datetime
from zk import ZK, const

conn = None

app = Flask(__name__)

# TEST CONNECTION TO API
@app.route('/test-connect', methods=['GET'])
def test():
    data = {"message": "Hello, this is your REST API!"}
    return jsonify(data)

# GET USERS
@app.route('/get-users', methods=['GET'])
def get_users() :
    ipaddress = request.args.get('Ip')
    zk = ZK(ipaddress, port=4370, timeout=360, password=0, force_udp=False, ommit_ping=False)
    try:
        # connect to device
        conn = zk.connect()
        # disable device, this method ensures no activity on the device while the process is run
        conn.disable_device()
        # another commands will be here!

        # Example: Get All Users
        userList = []
        users = conn.get_users()

        for user in users :
            data = {
                "uid" : user.uid,
                "userid" : user.user_id,
                "name" : user.name,
                "role" : user.privilege,
                "password" : user.password,
                "cardno" : user.card,
            }

            userList.append(data)
        # Test Voice: Say Thank You
        # conn.test_voice()
        # re-enable device after all commands already executed
        conn.enable_device()
        return jsonify(userList)
    except Exception as e:
        print ("Process terminate : {}".format(e))
        return jsonify([])
    finally:
        if conn:
            conn.disconnect()

# GET ATTENDANCE DATA
@app.route('/get-attendance', methods=['GET'])
def get_attendace() :
    ipaddress = request.args.get('Ip')
    zk = ZK(ipaddress, port=4370, timeout=360, password=0, force_udp=False, ommit_ping=False)
    try:
        # connect to device
        conn = zk.connect()
        # disable device, this method ensures no activity on the device while the process is run
        conn.disable_device()
        # another commands will be here!

        # Example: Get All Users
        # users = conn.get_users()
        # for user in users:
        #     privilege = 'User'
        #     if user.privilege == const.USER_ADMIN:
        #         privilege = 'Admin'
        #     print ('+ UID #{}'.format(user.uid))
        #     print ('  Name       : {}'.format(user.name))
        #     print ('  Privilege  : {}'.format(privilege))
        #     print ('  Password   : {}'.format(user.password))
        #     print ('  Group ID   : {}'.format(user.group_id))
        #     print ('  User  ID   : {}'.format(user.user_id))

        # GET ATTENDANCE
        attList = []
        attendances = conn.get_attendance()

        for att in attendances :
            data = {
                "uid" : att.uid,
                "id" : att.user_id,
                "state" : att.status,
                "timestamp" : att.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "type" : att.punch
            }

            attList.append(data)
        # Test Voice: Say Thank You
        # conn.test_voice()
        # re-enable device after all commands already executed
        conn.enable_device()
        return jsonify(attList)
    except Exception as e:
        print ("Process terminate : {}".format(e))
        return jsonify([])
    finally:
        if conn:
            conn.disconnect()


if __name__ == '__main__':
    app.run(host='192.168.12.200', port=5000, debug=True)
