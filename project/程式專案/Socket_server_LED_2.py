# -*- coding: utf-8 -*-

import socket
from _thread import *
import threading
import RPi.GPIO as GPIO
import time

# 指定GPIO接口
R,B,G=3,5,7

# 指定GPIO模式 
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# 設定GPIO接口
GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)
GPIO.output(3, 0)
GPIO.output(5, 0)
GPIO.output(7, 0)

# 指定協議
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 讓端口可以重複使用
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 绑定ip和端口
server.bind(('172.16.0.75', 8888))

# 監聽
server.listen(5)

def threaded(c, R, G, B):
    while True:
        # 從客戶端收資料
        data = c.recv(1024)
        if not data:
            print('Bye')

            break
 
        # 收到的資料
        data.decode("utf-8")
        VehiclesNum = int(data)
        print(VehiclesNum)
        
        # 依照資料亮燈
        if VehiclesNum > 9: #紅
            GPIO.output(3, 0) 
            GPIO.output(5, 1) 
            GPIO.output(7, 0)
            
        elif 5 < VehiclesNum <= 9: #紫
            GPIO.output(3, 0) 
            GPIO.output(5, 0) 
            GPIO.output(7, 1)
            
        elif 2 < VehiclesNum <= 5: #藍
            GPIO.output(3, 1) 
            GPIO.output(5, 0) 
            GPIO.output(7, 1)
            
        else:
        # 關燈
            GPIO.output(3, 1) 
            GPIO.output(5, 1) 
            GPIO.output(7, 1)
        time.sleep(0.1)
            
        data = "伺服器收到".encode("utf8") + data
        #data+= input("你好：").encode("utf8")
        # send back reversed string to client
        c.send(data)
    
while True:
    print("等待連接...")
    clientsocket, address = server.accept()
    print(address)
    # 等待消息
    print("連接成功")
    
    start_new_thread(threaded, (clientsocket, R, G, B))

# 關閉socket
clientsocket.close()
server.close()

# 停止GPIO
GPIO.output(3, 1) 
GPIO.output(5, 1) 
GPIO.output(7, 1)

# 清空GPIO
GPIO.cleanup()
