import socket
import threading
import sys
import sqlite3

class clientobj():
    def __init__(self, header = 64, port = 3000, encoding = 'utf-8' ):
        if len(sys.argv) == 2:
            self._serverip = sys.argv[1]
        else:
            self._serverip = "172.17.0.1"
        print(self._serverip)
        self._header = header
        self._port = port
        self._encoding = encoding
        self._addr = (self._serverip, self._port)
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect(self._addr)
        self._DISCONNECT_MESSAGE = "kawudhvcjsfuhvslfroyivedfegeqsfvfggffgr"
        self._changegroup = "sjduyhgvkcsueyfvskeufjdghvskehdgsdfdvuehfg"
        self._downloadchat = "jytghdciyjhmgcgddikjhfgvkjjitgjdhfoewihigqer"
        self.messbuff = []
        self.connected = True
        self.printmess = True
        self.download = False
        self.num_mes_recv=0
        self.Cup = '\x1b[1A'
        self.eli = '\x1b[2K'
        self.name = "jsfhgvsikfhjdvsbfkfivhsbfolibkvjsbfvikh"

    def getserverip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        SERVER = s.getsockname()[0]
        s.close()
        return SERVER

    def startclient(self):
        print("Starting chat app, type :help and enter to get help regarding commands")
        username=input('[enter username]\n')
        self.sendmessage(username)
        thread = threading.Thread(target=self.recievemessage, args=())
        thread.start()
        print("[recieve thread started]")
        self.connected = True
        while self.connected:
            msg = input()
            self.printmess = False
            sys.stdout.write(self.Cup)
            sys.stdout.write(self.eli)
            self.printmess = True
            if msg == "logmeout":
                self.connected = False
                self.sendmessage(self._DISCONNECT_MESSAGE)
            elif msg == ":d":
                self.sendmessage(self._downloadchat)
                print("Enter filename to save to(with extension)")
                self.name = input() #input messing with sendmessage input
            elif msg == ":help":
                fn = open('info.txt','r')
                len = self.file_len('info.txt')
                self.num_mes_recv += len
                print(fn.read())
            else:
                self.sendmessage(msg)
        #stop threads

    def recievemessage(self):
        while self.connected:
            msg_length = self.client.recv(self._header).decode(self._encoding)
            self.num_mes_recv += 1
            if msg_length:
                msg_length = int(msg_length)
                msg = self.client.recv(msg_length).decode(self._encoding)
                if msg == self._changegroup:
                    self.delallmes()
                elif msg == self._downloadchat:
                    self.download = not self.download
                    self.downloadtofile(self._downloadchat)
                else:
                    if self.downloadtofile(msg):
                        pass
                    elif self.printmess == True:
                        print(r'{}'.format(msg))
                    else:
                        while self.printmess == False:
                            pass
                        print(r'{}'.format(msg))

    def downloadtofile(self, msg):
        if msg == self._downloadchat:
            if self.download:
                while self.name == "jsfhgvsikfhjdvsbfkfivhsbfolibkvjsbfvikh":
                    pass
                self.fp = open(f"{self.name}",'w')
            else:
                self.fp.close()
                print(f"File saved as {self.name}")
                self.num_mes_recv+=3
                #close file
        else:
            try:
                self.fp.write(msg)
            except:
                pass
            #addmess to file
            return self.download

    def delallmes(self):
        while self.num_mes_recv>0:
            self.printmess = False
            sys.stdout.write(self.Cup)
            sys.stdout.write(self.eli)
            self.printmess = True
            self.num_mes_recv -= 1
        print("[recieve string started]")

    def sendmessage(self,msg):
        message = msg.encode(self._encoding)
        msg_length = len(message)
        send_length = str(msg_length).encode(self._encoding)
        send_length += b' ' * (self._header - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def file_len(self,fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 2
    
c = clientobj()
c.startclient()     
