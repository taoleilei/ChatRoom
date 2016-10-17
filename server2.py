#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2016-10-12 17:20:54
# @Author  : taoleilei (1214360171@qq.com)
# @Link    : ${link}
# @Version : $Id$

import selectors
import socket
 
sel = selectors.DefaultSelector()
CONNECTION_LIST = []

def broadcast_data(conn, message):
    # 循环监听列表，将该客户端（sock）发的消息（message）转发给除过服务器和他自己以外的其他客户端。
    for socket in CONNECTION_LIST:
        if socket != sock and socket != conn:
            try:
                socket.send(message)
            except:
                socket.close()
                CONNECTION_LIST.remove(socket)

def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    CONNECTION_LIST.append(conn)
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)
 
def read(conn, mask):
    data = conn.recv(1024)  # Should be ready
    if data:
        broadcast_data(conn, data)
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()
 
sock = socket.socket()
sock.bind(('localhost', 5000))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)
 
while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
