# -*- coding: utf-8 -*-
#! /usr/bin/env python
#
# @Author: z.Joey
# @Date: 2019-03-04 10:48:05
# @Last Modified by:   z.Joey
# @Last Modified time: 2019-03-04 10:48:05


import time
import datetime
import random
import socket
import sqlite3
import threading
import socketserver
import sys

import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox as tkBox


class Node(object):
    # 结点
    def __init__(self, elem):
        self.elem = elem
        self.next = None  # 初始设置下一节点为空


class SingleLinkList(object):
    # 单链表

    def __init__(self, node=None):  # 使用一个默认参数，在传入头结点时则接收，在没有传入时，就默认头结点为空
        self.__head = node

    def is_empty(self):
        '''链表是否为空'''
        return self.__head == None

    def length(self):
        '''链表长度'''
        # cur游标，用来移动遍历节点
        cur = self.__head
        # count记录数量
        count = 0
        while cur != None:
            count += 1
        cur = cur.next
        return count

    def travel(self):
        '''遍历整个列表'''
        cur = self.__head
        while cur != None:
            print(cur.elem, end=' ')
            cur = cur.next
        print("\n")

    def add(self, item):
        '''链表头部添加元素'''
        node = Node(item)
        node.next = self.__head
        self.__head = node

    def append(self, item):
        '''链表尾部添加元素'''
        node = Node(item)
        # 由于特殊情况当链表为空时没有next，所以在前面要做个判断
        if self.is_empty():
            self.__head = node
        else:
            cur = self.__head
            while cur.next != None:
                cur = cur.next
            cur.next = node

    def insert(self, pos, item):
        '''指定位置添加元素'''
        if pos <= 0:
                # 如果pos位置在0或者以前，那么都当做头插法来做
            self.add(item)
        elif pos > self.length() - 1:
            # 如果pos位置比原链表长，那么都当做尾插法来做
            self.append(item)
        else:
            per = self.__head
            count = 0
            while count < pos - 1:
                count += 1
                per = per.next
            # 当循环退出后，pre指向pos-1位置
            node = Node(item)
            node.next = per.next
            per.next = node

    def remove(self, item):
        # '''删除节点'''
        cur = self.__head
        pre = None
        while cur != None:
            if cur.elem == item:
                # 先判断该节点是否是头结点
                if cur == self.__head:
                    self.__head = cur.next
                else:
                    pre.next = cur.next
                break
            else:
                pre = cur
                cur = cur.next

    def search(self, item):
        # '''查找节点是否存在'''
        cur = self.__head
        while not cur:
            if cur.elem == item:
                return True
        else:
            cur = cur.next
            return False


def get_localTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def parse(recv_data):
    parse_data = recv_data.split(",")
    rec_utcTime = time.strftime(
        '%H:%M:%S', time.localtime(float(parse_data[1])))
    rec_lati = parse_data[2]
    rec_longi = parse_data[4]

    return rec_utcTime, rec_lati, rec_longi


def store(rec_time, lati, longti, origin):
    local_time = get_localTime()

    db_conn = sqlite3.connect('gpsDB2.db')
    db_c = db_conn.cursor()
    # print("connect to sqlite")

    velocity = random.randrange(0, 100)

    db_c.execute(
        "INSERT INTO GPS (ID,rec_utcTime,longitude,latitude,velocity,time,origin) \
        VALUES (NULL,'%s','%s','%s','%s','%s','%s')" % (rec_time, longti, lati, velocity, local_time, origin))
    db_conn.commit()
    db_conn.close()
    # time.sleep(1)


class MyServer(socketserver.BaseRequestHandler):

    def handle(self):

        i = 0

        # 存入数据库
        conn = self.request
        rec_data = conn.recv(1024)
        rec_time, rec_lati, rec_longi = parse(str(rec_data))
        print(rec_data)
        print(str(rec_time)+"," + str(rec_lati)+"," + str(rec_longi))
        decode_data = bytes.decode(rec_data)
        store(rec_time, rec_lati, rec_longi, decode_data)

        # 存入链表
        link_message = str(i)+str(rec_time)+str(rec_lati)+str(rec_longi)
        store_list = SingleLinkList()
        store_list.append(link_message)

        # 序号
        i += 1

        conn.send('received'.encode(encoding='utf-8'))


def search():
    db_conn = sqlite3.connect('gpsDB2.db')
    db_c = db_conn.cursor()

    result = db_c.execute("select * from GPS")
    all_results = result.fetchall()
    db_conn.close()

    frame = tk.Frame()
    frame.pack()
    textarea = tk.Text(frame, width=80, height=35)
    frame.place(x=40, y=150)
    scrollbar = tk.Scrollbar(frame, orient='vertical')
    scrollbar.config(command=textarea.yview)
    scrollbar.pack(side='right', fill='y')  # 靠右摆放, fill整个纵向
    textarea.config(yscrollcommand=scrollbar.set)
    textarea.pack(side='left', fill='both', expand=1)
    textarea.config(state='normal')  # 开启允许编辑text
    textarea.delete(1.0, 'end')  # 删除所有之前的内容
    item1 = "From DB:"

    textarea.insert('end', item1)  # 插入到尾部, 就是app'end'的意思

    for i in range(len(all_results)):
        item2 = all_results[i]
        textarea.insert('end', "\n")
        textarea.insert('end', item2)

    textarea.config(state='disable')  # 关闭编辑text


def GUI():
    window = tk.Tk()
    window.title("GPS Fake Receiver")
    window.geometry('800x800')

    label1 = tk.Label(window, text="GPS模拟接收器",
                      font=tkFont.Font(size=20, weight=tkFont.BOLD))
    label1.pack()

    s1 = socketserver.ThreadingTCPServer(("127.0.0.1", 8008), MyServer)

    tk.Button(text='启动', width=20, height=2,
              command=lambda: start(s1)).place(x=100, y=50)

    tk.Button(text='查询', width=20, height=2, command=search).place(x=300, y=50)

    tk.Button(text='停止', width=20, height=2,
              command=lambda: stop(s1)).place(x=500, y=50)

    window.mainloop()


def listen(server):
    print("服务端正在监听...")
    server.serve_forever()


def start(server):
    thread2_start = threading.Thread(target=listen, args=(server,))
    thread2_start.start()


def stop(server):
    server.shutdown()
    exit()


if __name__ == '__main__':
    thread1_GUI = threading.Thread(target=GUI())
    thread1_GUI.start()
