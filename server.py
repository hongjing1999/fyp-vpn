import threading

from flask import Flask, request, json, send_from_directory, abort

import google_api
import readConfig
import command
import os


app = Flask(__name__)
workingDirectory = "/root/"

queue = []
deleteQueue = []
uploadFileQueue = []

@app.route('/create-user', methods=['POST'])
def create_user():
    global queue
    username = request.json["username"]
    queue.append(username)
    response = app.response_class(
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/delete-user', methods=['POST'])
def delete_user():
    global deleteQueue
    username = request.json["username"]
    deleteQueue.append(username)
    response = app.response_class(
        status=200,
        mimetype='application/json'
    )
    return response


# @app.route('/delete-user', methods=['POST'])
# def delete_user():
#     username = request.json["username"]
#     users, filetext, startIndex, endIndex = readConfig.get_user_list()
#     newUsers = readConfig.del_user(users, username)
#     readConfig.write_file(newUsers, filetext, startIndex, endIndex)
#     response = app.response_class(
#         status=200,
#         mimetype='application/json'
#     )
#     command.run_command()
#     os.remove(f"{workingDirectory}algo/configs/178.128.102.222/wireguard/{username}.conf")
#     os.remove(f"{workingDirectory}algo/configs/178.128.102.222/wireguard/{username}.png")
#     os.remove(f"{workingDirectory}algo/configs/178.128.102.222/wireguard/apple/ios/{username}.mobileconfig")
#     os.remove(f"{workingDirectory}algo/configs/178.128.102.222/wireguard/apple/macos/{username}.mobileconfig")
#     return response

def execute(username):
    print(username)
    users, filetext, startIndex, endIndex = readConfig.get_user_list()
    print(users)
    try:
        newUsers = readConfig.add_user(users, username)
        readConfig.write_file(newUsers, filetext, startIndex, endIndex)
    except Exception:
        print("Drone Exists")
        # google_api.uploadFile(username + ".conf")
    else:
        return username

def executeDelete(username):
    print(username)
    users, filetext, startIndex, endIndex = readConfig.get_user_list()
    print(users)
    newUsers = readConfig.del_user(users, username)
    readConfig.write_file(newUsers, filetext, startIndex, endIndex)


def queueing():
    global queue
    global deleteQueue
    global uploadFileQueue
    while True:
        change = False
        while len(queue) > 0:
            username = execute(queue.pop(0))
            uploadFileQueue.append(username)
            change = True
        while len(deleteQueue) > 0:
            executeDelete(deleteQueue.pop(0))
            change = True
        if change:
            command.run_command()
            while len(uploadFileQueue) > 0:
                google_api.uploadFile(uploadFileQueue.pop(0) + ".conf")




if __name__ == '__main__':
    queueThread = threading.Thread(target=queueing)
    queueThread.start()
    app.run(host="157.245.94.152", port="5000", debug=True)