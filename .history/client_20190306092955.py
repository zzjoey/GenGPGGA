# -*- coding: utf-8 -*-
#! /usr/bin/env python
#
# @Author: z.Joey
# @Date: 2019-03-04 08:28:46
# @Last Modified by:   z.Joey
# @Last Modified time: 2019-03-04 08:28:46


import time
import datetime
import random
import socket
import sqlite3
import threading

import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox as tkBox


'''
格式：$GPGGA,<1>,<2>,<3>,<4>,<5>,<6>,<7>,<8>,<9>,M,<10>,M,<11>,<12>*hh<CR><LF>
举例：$GPGGA,115542.000,3155.3446,N,11852.4283,E,1,03,4.4,32.6,M,5.4,M,,0000*5A
<1> UTC 时间，hhmmss（时分秒）格式
<2> 纬度ddmm.mmmm（度分）格式（前面的0 也将被传输）
<3> 纬度半球N（北半球）或S（南半球）
<4> 经度dddmm.mmmm（度分）格式（前面的0 也将被传输）
<5> 经度半球E（东经）或W（西经）
<6> GPS 状态：0=未定位，1=非差分定位，2=差分定位，6=正在估算
<7> 正在使用解算位置的卫星数量（00-12）（前面的0 也将被传输）
<8> HDOP水平精度因子（0.5-99.9）
<9> 海拔高度（-9999.9-99999.9）
<10> 地球椭球面相对大地水准面的高度
<11> 差分时间（从最近一次接收到差分信号开始的秒数，如果不是差分定位将为空）
<12> 差分站ID 号0000-1023（前面的0 也将被传输，如果不是差分定位将为空）
'''


def get_UTC():
    # 获取当前UTC时间，hhmmss.sss格式
    now_gm_time = time.strftime("%H%M%S", time.gmtime())
    ct = time.time()
    # zfill 前补全0
    millssec = str(int((ct - int(ct)) * 1000)).zfill(3)
    full_time = str(now_gm_time) + "." + millssec
    return full_time


def get_lati(input_lati):
    # 获取纬度，ddmm.mmmm（度分）格式
    # 0-90
    # 分0-60.0-9999

    lati = str(random.randrange(0, input_lati)).zfill(2)

    lati_min = str(random.randrange(0, 60)).zfill(2)
    lati_millimin = str(random.randrange(0, 9999)).zfill(4)
    full_lati = lati + lati_min + '.' + lati_millimin

    return full_lati


def get_latiHemi():
    # 获取纬度半球
    # 南/北 S/N
    hemis = ['N', 'S']
    lati_hemi = random.choice(hemis)
    return lati_hemi


def get_longi(input_longi):
    # 获取经度，ddmm.mmmm（度分）格式
    # 0-180
    # 分0-60.0-9999
    longi = str(random.randrange(0, input_longi)).zfill(3)
    longi_min = str(random.randrange(0, 60)).zfill(2)
    longi_millimin = str(random.randrange(0, 9999)).zfill(4)
    full_longi = longi + longi_min + '.' + longi_millimin
    return full_longi


def get_longiHemi():
    # 获取经度半球
    # 西/东 W/E
    hemis = ['W', 'E']
    longi_hemi = random.choice(hemis)
    return longi_hemi


def get_gpsStatus():
    # GPS 状态：0=未定位，1=非差分定位，2=差分定位，6=正在估算
    statuses = ['0', '1', '2', '6']
    gpsStatus = random.choice(statuses)
    return gpsStatus


def get_sateNum():
    # 获取卫星数量
    # 00-12随机数
    sate_num = str(random.randrange(0, 12)).zfill(2)
    return sate_num


def get_HDOP():
    # HDOP水平精度因子（0.5-99.9）
    hdop_int = random.randrange(5, 999)
    hdop_float = str(float(hdop_int/10))
    return hdop_float


def get_alti():
    # 海拔高度（-9999.9-99999.9）
    alti_int = random.randrange(-99999, 999999)
    alti_float = str(float(alti_int / 10))
    return alti_float


def get_diffTime(diff):
    # 差分时间（从最近一次接收到差分信号开始的秒数，如果不是差分定位将为空）
    if (diff != '2'):
        return ''
    else:
        time = str(random.randrange(0, 20))
        return time


def get_diffStationID(diff):
    # 差分站ID 号0000-1023（前面的0 也将被传输，如果不是差分定位将为空）
    if (diff != '2'):
        return '0000'
    else:
        stationID = str(random.randrange(0, 1023)).zfill(4)
        return stationID


def get_gpggsMessage():
    # 拼接GPGGA信息
    # 校验和随机生成
    head = "$GPGGA"
    comma = ','

    utc_time = get_UTC()
    lati = get_lati()
    lati_hemi = get_latiHemi()
    longi = get_longi()
    longi_hemi = get_longiHemi()
    gps_status = get_gpsStatus()
    sate_num = get_sateNum()
    hdop = get_HDOP()
    alti = get_alti()
    # 地球椭球面相对大地水准面的高度
    alti_diff = str(float(float(alti)+1))
    diff_time = get_diffTime(gps_status)
    diff_stationID = get_diffStationID(gps_status)
    # check_sum = str(hex(random.randrange(0, 255))[2:])

    gpggs_message = head+comma+utc_time+comma+lati+comma+lati_hemi+comma+longi+comma+longi_hemi+comma+gps_status+comma + \
        sate_num+comma+hdop+comma+alti+comma+"M"+comma+alti_diff+comma + \
        "M"+comma+diff_time+comma+diff_stationID+"*5A"+"\r"+"\n"

    return gpggs_message


def get_localTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def send_gpggsMessage():
    # 发送GPS信号并存入SQLite3

    while True:
        db_conn = sqlite3.connect('gpsDB.db')
        db_c = db_conn.cursor()
        # print("Open SQLite3 success")

        local_time = get_localTime()
        gpggs_message = get_gpggsMessage()

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 8008))

        send_message = gpggs_message.encode(encoding='utf-8')
        client.send(send_message)
        # print(send_message)
        rec_data = client.recv(512)
        # print(data)
        client.close()

        db_c.execute(
            "INSERT INTO GPS (ID,GPS,time) VALUES (NULL,'%s','%s')" % (gpggs_message, local_time))
        db_conn.commit()
        # print("Insert into SQLite3 Success")
        db_conn.close()
        time.sleep(0.5)


def get_threadSend():
    thread2_Send = threading.Thread(target=send_gpggsMessage())
    thread2_Send.start()


def GUI():
    window = tk.Tk()
    window.title("GPS Fake Simulator")
    window.geometry('800x400')

    v1_lati_N = tk.StringVar()
    v2_lati_S = tk.StringVar()
    v3_longi_W = tk.StringVar()
    v4_longi_E = tk.StringVar()
    v5_alti_P = tk.StringVar()
    v6_alti_N = tk.StringVar()

    label1 = tk.Label(window, text="GPS模拟发生器（假的！）",
                      font=tkFont.Font(size=20, weight=tkFont.BOLD))
    label1.pack()

    # 纬度范围输入
    tk.Label(window, text="纬度 °N").place(x=250, y=100)
    tk.Entry(window, textvariable=v1_lati_N).place(x=350, y=100)
    tk.Label(window, text="纬度 °S").place(x=250, y=150)
    tk.Entry(window, textvariable=v2_lati_S).place(x=350, y=150)

    # 经度范围输入
    tk.Label(window, text="经度 °W").place(x=50, y=200)
    tk.Entry(window, textvariable=v3_longi_W).place(x=150, y=200)
    tk.Label(window, text="180°W / 0°").place(x=350, y=200)
    tk.Entry(window, textvariable=v4_longi_E).place(x=470, y=200)
    tk.Label(window, text="经度 °E").place(x=670, y=200)

    # 高度范围输入
    tk.Label(window, text="海拔高度 -/m").place(x=50, y=250)
    tk.Entry(window, textvariable=v5_alti_P).place(x=200, y=250)
    tk.Label(window, text=" 0 m").place(x=400, y=250)
    tk.Entry(window, textvariable=v6_alti_N).place(x=450, y=250)
    tk.Label(window, text="海拔高度 +/m").place(x=650, y=250)

    def check_input():
        # 检查并填充参数
        # 检查纬度范围，边界检测，情况判断，充分随机
        v1_latiN_input = v1_lati_N.get()
        v2_latiS_input = v2_lati_S.get()
        try:
            v1_latiN_input_int = int(v1_lati_N.get())
            v2_latiS_input_int = int(v2_lati_S.get())
        except ValueError:
            v1_latiN_input_int = 90
            v2_latiS_input_int = 90

        if ((v1_lati_N.get() == '') & (v2_lati_S.get() == '')):
            final_lati = get_lati(90)
            final_latiHemi = get_latiHemi()
        elif ((v1_lati_N.get() != '') & (v2_lati_S.get() == '')):
            if int(v1_latiN_input) not in range(0, 91):
                tkBox.showwarning("Latitude Error", "纬度范围为 0 ~ 90")
            else:
                try:
                    v1_latiN_input_int = int(v1_latiN_input)
                    final_lati = get_lati(v1_latiN_input_int)
                except ValueError:
                    final_latiHemi = 'S'
                    final_lati = get_lati(90)
                else:
                    final_latiHemi = 'N'

        elif((v1_lati_N.get() == '') & (v2_lati_S.get() != '')):
            if v2_latiS_input_int not in range(0, 91):
                tkBox.showwarning("Latitude Error", "纬度范围为 0 ~ 90")
            else:
                try:
                    v2_latiS_input_int = int(v2_latiS_input)
                    final_lati = get_lati(v2_latiS_input_int)
                final_latiHemi = 'S'
                except ValueError:
                    final_latiHemi = 'S'
                    final_lati = get_lati(90)
                else:
                    final_latiHemi = 'N'
                 
                

        else:
            if v1_latiN_input_int not in range(0, 91):
                tkBox.showwarning("Latitude Error", "纬度范围为 0 ~ 90")
            elif v2_latiS_input_int not in range(0, 91):
                tkBox.showwarning("Latitude Error", "纬度范围为 0 ~ 90")
            else:
                try:
                    temp_lati1 = random.randrange(0, v1_latiN_input_int)
                    temp_lati2 = random.randrange(0, v2_latiS_input_int)
                except ValueError:
                    tkBox.showwarning("Value Error", "值错误！请重新输入")
                temp_latiHemi1 = 'N'
                temp_latiHemi2 = 'S'
                temp_latis = [temp_lati1, temp_lati2]
                final_lati = random.choice(temp_latis)
                if (final_lati == temp_lati1):
                    final_latiHemi = 'N'
                else:
                    final_latiHemi = 'S'

        # 检查经度范围，边界检测，情况判断，充分随机
        v3_longiW_input = v3_longi_W.get()
        v4_longiE_input = v4_longi_E.get()

        try:
            v3_longiW_input_int = int(v3_longi_W.get())
            v4_longiE_input_int = int(v4_longi_E.get())
        except ValueError:
            v3_longiW_input_int = 180
            v4_longiE_input_int = 180

        if ((v3_longi_W.get() == '') & (v4_longi_E.get() == '')):
            final_longi = get_longi(180)
            final_longiHemi = get_longiHemi()
        elif ((v3_longi_W.get() != '') & (v4_longi_E.get() == '')):
            if int(v3_longiW_input) not in range(0, 181):
                tkBox.showwarning("Longitude Error", "经度范围为 0 ~ 180")
            else:
                v3_longiW_input_int = int(v3_longiW_input)
                final_longi = get_longi(v3_longiW_input_int)
                final_longiHemi = 'W'
        elif ((v3_longi_W.get() == '') & (v4_longi_E.get() != '')):
            # print(v4_longiE_input_int)
            if int(v4_longi_E.get()) not in range(0, 181):
                tkBox.showwarning("Longitude Error", "经度范围为 0 ~ 180")
            else:
                v4_longiE_input_int = int(v4_longi_E.get())
                final_longi = get_longi(v4_longiE_input_int)
                final_longiHemi = 'E'

        else:
            if v3_longiW_input_int not in range(0, 181):
                tkBox.showwarning("Longitude Error", "经度范围为 0 ~ 180")
            elif v4_longiE_input_int not in range(0, 181):
                tkBox.showwarning("Longitude Error", "经度范围为 0 ~ 180")
            else:
                try:
                    temp_longi1 = random.randrange(0, v3_longiW_input_int)
                    temp_longi2 = random.randrange(0, v4_longiE_input_int)
                except ValueError:
                    tkBox.showwarning("Value Error", "值错误！请重新输入")
                temp_longiHemi1 = 'W'

                temp_longiHemi2 = 'E'
                temp_longis = [temp_longi1, temp_longi2]
                final_longi = random.choice(temp_longis)
                if (final_longi == temp_longi1):
                    final_longiHemi = 'W'
                else:
                    final_longiHemi = 'E'
        if (v1_latiN_input_int not in range(0, 91)
        or v2_latiS_input_int not in range(0, 91)
        or v3_longiW_input_int not in range(0, 181)
        or v4_longiE_input_int not in range(0,181)):
            tkBox.showwarning("Value Error", "输入值错误！请检查：经度范围0~180，纬度范围0~90")
        else:
            print(str(final_lati)+final_latiHemi)
            print(str(final_longi) + final_longiHemi)
            
    # 开始按钮
    tk.Button(text='发射', width=40, height=2,
              command=check_input).place(x=200, y=300)

    window.mainloop()


if __name__ == '__main__':
    thread1_GUI = threading.Thread(target=GUI())
    thread1_GUI.start()
