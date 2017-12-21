#!/usr/bin/env python
import eventlet
import json
eventlet.monkey_patch()
from threading import Lock
from flask import Flask, render_template, session, request
from flask import make_response
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import random
import threading
from threading import Event
from flask import Flask, Response

from flask_sse import sse
from flask import Flask, Response
from threading import Thread
from threading import Timer
from multiprocessing import Process
import asyncio

import time

masterSem = threading.Semaphore()
tempSem = threading.Semaphore(0)
lock = Event()

pixelCache = None


locked = False #checks to see if control is currently locked to timer

# thread control object
def timerFunction():
    count = 0
    global masterSem
    while True:
        time.sleep(15)
        masterSem.acquire()
        global pixelArray
        global pixelCache
        arr = []
        for x in range(0, 39999):
            color = max(pixelArray[x].colors, key=pixelArray[x].colors.get)
            pixelColor = {'c':color}
            arr.append(pixelColor)
        data = {'pixels': arr, 'timestamp': time.time()}
        pixelCache = json.dumps(data)
        masterSem.release()
        print('Updated Cache')


#
# def background_thread():
#     count = 0
#     while True:
#         socketio.sleep(5)
#         count += 1
#         socketio.emit('my_response', {'data': 'server is doing this', 'count':count}, namespace = '/test')

#creating pixel class
class Pixel:
    def __init__(self):
        self.colors = { "W":0, "R":0,  "O":0, "Y":0, "G":0, "B":0,"I":0,"V":0,"Bl":0 }
    def incrementColor(self, color):
        self.colors[color] += 1

#creating array of 40,000 Pixel objects
pixelArray = []
for x in range(0, 39999):
    newPixel = Pixel()
    pixelArray.append(newPixel)

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)


timerThread = socketio.start_background_task(target=timerFunction)



thread = None

@app.route('/')
def index():
    return render_template('index.html', async_mode = socketio.async_mode)

@app.route('/demo')
def demo():
    return render_template('demo.html', async_mode = socketio.async_mode)

@app.route("/stream")
def stream():
    lock.wait()
    return Response("data: 'kill'\n\n", mimetype="text/event-stream")


@app.route("/kill/se3313")
def killGrace():
    lock.set()
    # thread = socketio.start_background_task(target=killAfterWait)
    killAfterWait()
    return "ok"
    #kill itself here

def killAfterWait():
    time.sleep(5)
    print("in kill")
    global socketio
    socketio.stop()
    return'server shutting down..'


@app.route('/images/<path>')
def sendImage(path):
    return app.send_static_file("images/" + path)

@app.route('/imageData.js')
def sendImageData():
    return app.send_static_file("imageData.js")

@app.route('/pixels')
def send_pixels():
    global pixelCache
    global masterSem
    global pixelArray
    res = {}
    masterSem.acquire()
    if (pixelCache == None):
        arr = []
        for x in range(0, 39999):
            color = max(pixelArray[x].colors, key=pixelArray[x].colors.get)
            pixelColor = {'c':color}
            arr.append(pixelColor)
        data = {'pixels': arr, 'timestamp': time.time()}
        res = json.dumps(data)
        pixelCache = res
        masterSem.release()
        print('Created Cache')
    else:
        res = pixelCache
        masterSem.release()
        print('Read From Cache')
    return res

@app.route('/pixelRequest/<int:pixelNumber>/<requestedColor>', methods = ["POST"])
def pixel_request(pixelNumber, requestedColor):
    global masterSem
    masterSem.acquire()
    global pixelArray
    pixelArray[pixelNumber].incrementColor(requestedColor)
    masterSem.release()
    return("color %s for pixel % requested" % (requestedColor, pixelNumber))

@app.route('/pixelPicture', methods = ["POST"])
def pixel_picture():
    global pixelArray
    pic = json.loads(request.data)
    print(pic)
    global masterSem
    masterSem.acquire()
    for x in range(0,39999):

        if(pic["pixels"][x]["c"] != ""):
            pixelArray[x].incrementColor(pic["pixels"][x]["c"])
    masterSem.release()
    return "OK"

if __name__ == '__main__':

    socketio.run(app, debug=True)

