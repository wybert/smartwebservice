# -*- coding: utf-8 -*-
"""
Created on Mon Nov 03 14:50:23 2014

@author: wybert
"""
import SimpleHTTPServer
import SocketServer

##picture http server
ip="0.0.0.0"

pic_PORT = 8001
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer((ip, pic_PORT), Handler)
httpd.serve_forever()
