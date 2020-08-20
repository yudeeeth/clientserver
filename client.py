import socket
import threading
import sys

class clientobj():
    def __init__(self, header = 64, port = 8080, encoding = 'utf-8' ):
        self._serverip = "192.168.0.101"
        print(self._serverip)
        self._header = header
        self._port = port
        self._encoding = encoding
        self._addr = (self._serverip, self._port)
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect(self._addr)
        self._DISCONNECT_MESSAGE = "kawudhvcjsfuhvslfroyivedfegeqsfvfggffgr"
        self._RECIEVEDSUCCESSFULLY = "sjduyhgvkcsueyfvskeufjdghvskehdgsdfdvuehfg"
        self.messbuff = []
        self.connected = True
        self.printmess = True

    # def __del__(self):
    #     if self.connected:
    #         self.sendmessage(self._DISCONNECT_MESSAGE)
    
    def getserverip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        SERVER = s.getsockname()[0]
        s.close()
        return SERVER

    def startclient(self):
        print("Starting chat app")
        username=input('[enter username]\n')
        self.sendmessage(username)
        thread = threading.Thread(target=self.recievemessage, args=())
        thread.start()
        print("[recieve thread started]")
        self.connected = True
        while self.connected:
            msg = input()
            self.printmess = False
            Cup = '\x1b[1A'
            eli = '\x1b[2K'
            sys.stdout.write(Cup)
            sys.stdout.write(eli)
            self.printmess = True
            if msg == "logmeout":
                self.connected = False
                self.sendmessage(self._DISCONNECT_MESSAGE)
            else:
                self.sendmessage(msg)
        #stop threads

    def recievemessage(self):
        while self.connected:
            msg_length = self.client.recv(self._header).decode(self._encoding)
            if msg_length:
                msg_length = int(msg_length)
                msg = self.client.recv(msg_length).decode(self._encoding)
                if ":" in msg:
                    if self.printmess == True:
                        print(msg)
                    else:
                        while self.printmess == False:
                            pass
                        print(msg)
                #else:
                #    self.messbuff.append(msg)
    
    def sendmessage(self,msg):
        message = msg.encode(self._encoding)
        msg_length = len(message)
        send_length = str(msg_length).encode(self._encoding)
        send_length += b' ' * (self._header - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
    
c = clientobj()
c.startclient()     
