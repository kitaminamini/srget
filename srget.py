#!/usr/bin/env python

import socket as sock
import sys
from urlparse import urlparse


def makeRequest(command, path, host, port):
    NewLine = "\r\n"
    return (command + " {o} HTTP/1.1" + NewLine + "Host: {s}" + NewLine + NewLine).format(o=path, s=host + ":" + port)


def mysend(sock, msg):
    totalsent = 0
    while totalsent < len(msg):
        sent = sock.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent

def checkCode(headerlst):
    if (headerLst[0][9]=="2"):
        return 2
    elif (headerLst[0][9]=="3"):
        return 3
    elif (headerLst[0][9]=="4"):
        return 4
    elif (headerLst[0][9]=="5"):
        return 5
    else:
        return -1


def myreceive(msgsize, sock):
    chunks = []
    bytes_recd = 0
    while bytes_recd < msgsize:
        chunk = sock.recv(min(msgsize - bytes_recd, 2048))
        if chunk == '':
            raise RuntimeError("socket connection broken")
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    return ''.join(chunks)

def isHeader(string):
    return "\r\n\r\n" in string

def extractFromHeader(headerlst, httpstatus):
    if (httpStatus==2):
        for w in headerLst:
            if "Content-Length" in w:
                contentLen = w[16:]
                return contentLen
    elif (httpStatus==3):
        for w in headerLst:
            if "Location:" in w:
                location = w[10:]
                return location
    return "-1"

httpStatus=0
filename = ""
url = ""
location = ""
prev_data = ""
contentLen = ""

if len(sys.argv) == 4 and sys.argv[1] == "-o":
    filename = sys.argv[2]
    u = sys.argv[3]
    URL = urlparse(u)
    path = URL.path
    host = URL.hostname
    # print "host: "+host
    if (URL.port == None):
        port = 80
    else:
        port = URL.port
    # print "port: " + str(port)
    if URL.scheme == "http":
        clientSock = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        clientSock.connect((host, port))
        header = ""
        getRequest = makeRequest("GET", path, host, str(port))
        mysend(clientSock, getRequest)
        # print long(contentLen)
        while True:
            data_received = clientSock.recv(1024)
            if isHeader(data_received)==True or isHeader(prev_data[len(prev_data)-3:]+data_received[0:3])==True:
                header = header + data_received
                allHead,Body=header.split("\r\n\r\n")
                headerLst = allHead.split("\r\n")
                httpStatus=checkCode(headerLst)
                if (httpStatus==2):
                    contentLen=extractFromHeader(headerLst, httpStatus)
                    # print "content len: " + str(contentLen)
                    Body=Body+myreceive(long(contentLen)-len(Body),clientSock)
                    # print len(Body)
                    clientSock.close()
                    break
                elif (httpStatus==3):
                    location=extractFromHeader(headerLst, httpStatus)
                    clientSock.close()
                    break
                else:
                    clientSock.close()
                    break
            else:
                header = header + data_received
                prev_data=data_received
            # if len(data_received) == 0:
            #     clientSock.close()
            #     break
        if httpStatus==4:
            print "Client Error: incorrect syntax"
            sys.exit()
        elif httpStatus==5:
            print "Server Error: server failed to fulfill an apparently valid request"
            sys.exit()
        elif httpStatus==-1:
            print "Unknown Error: close socket connection"
            sys.exit()
        elif httpStatus==3:
            print "Redirection"
            sys.exit()
        else:
            downloaded = open(filename, 'wb')
            downloaded.write(Body)


else:
    print "Can't proceed, killing self [invalid input parameters]"
    sys.exit()
