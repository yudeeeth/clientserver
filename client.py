import socket
import threading

class clientobj():
    def __init__(self, header = 64, port = 8080, encoding = 'utf-8' ):
        self._serverip = "127.0.1.1"
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

    def __del__(self):
        if self.connected:
            self.sendmessage(self._DISCONNECT_MESSAGE)

    def startclient(self):
        print("Starting chat app")
        thread = threading.Thread(target=self.recievemessage, args=())
        thread.start()
        print("[recieve thread started]")
        self.connected = True
        while self.connected:
            msg = input()
            if msg == "logmeout":
                self.sendmessage(self._DISCONNECT_MESSAGE)
                self.connected = False
            else:
                self.sendmessage(msg)



    def recievemessage(self):
        while self.connected:
            msg_length = self.client.recv(self._header).decode(self._encoding)
            if msg_length:
                msg_length = int(msg_length)
                msg = self.client.recv(msg_length).decode(self._encoding)
                if ":" in msg:
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


            