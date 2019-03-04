# -*- coding: utf-8 -*-
#! /usr/bin/env python
#
# @Author: z.Joey
# @Date: 2019-03-04 10:48:05
# @Last Modified by:   z.Joey
# @Last Modified time: 2019-03-04 10:48:05

import socketserver


class MyServer(socketserver.BaseRequestHandler):

    def handle(self):
        conn = self.request
        rec_data = conn.recv(1024)
        print(rec_data)
        conn.send('received')


if __name__=='__main__':
    s1 = socketserver.ThreadingTCPServer(("127.0.0.1", 8008), MyServer)
    print("Server Listening...")
    s1.serve_forever()