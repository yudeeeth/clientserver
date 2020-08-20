import socket
import threading
import sqlite3

class serverobj():
    def __init__(self, header = 64, port = 8080, encoding = 'utf-8' ):
        #self._serverip = socket.gethostbyname(socket.gethostname())
        self._serverip = self.getserverip()
        self._header = header
        self._port = port
        self._encoding = encoding
        self._addr = (self._serverip, self._port)
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind(self._addr)
        self._DISCONNECT_MESSAGE = "kawudhvcjsfuhvslfroyivedfegeqsfvfggffgr"
        self._RECIEVEDSUCCESSFULLY = "sjduyhgvkcsueyfvskeufjdghvskehdgsdfdvuehfg"
        self.currentserialnumber = int(self.getcurser())
        self.stop_command = "puter stop"

    def __del__(self):
        self.addtodata("[server]","Server killed")
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute('DELETE FROM chats WHERE user="[server]"')
        conn.close()

    def getserverip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        SERVER = s.getsockname()[0]
        s.close()
        return SERVER

    def startserver(self):
        print(f"[Server ip:{self._serverip} listening at port:{self._port}]")
        self.server.listen()
        self.conn_list = []
        start = True
        while start:
            conn, addr = self.server.accept()
            msg_length = conn.recv(self._header).decode(self._encoding)
            username='buffer'
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self._encoding)
                username = msg
                if username == self.stop_command:
                    start = False
            threadhandlecli = threading.Thread(target= self.HandleClient,args=(conn, addr,username))
            threadhandlecli.start()
            self.conn_list.append( conn  )
            print(f"Active connections {threading.activeCount()-1}")

    def HandleClient(self,conn,addr,username):
        print(f"[New Connection {addr}{username}]")
        connected = True
        while connected:
            msg_length = conn.recv(self._header).decode(self._encoding)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self._encoding)
                if msg == self._DISCONNECT_MESSAGE:
                    self.messagesend(conn,"Disconnected from server")
                    connected = False
                    self.conn_list.remove( conn  )
                    print(f"[Connection severed {username}]")
                    print(f"Active connections {threading.activeCount() - 2}")
                else:
                    print(f"[{username}]: {msg}")
                    self.addtodata(username,msg)
                #self.messagesend(conn , self._RECIEVEDSUCCESSFULLY) 

    def update_all(self):
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute("SELECT user from chats ORDER BY serial DESC LIMIT 1")
        u = c.fetchone()
        c.execute("SELECT msg from chats ORDER BY serial DESC LIMIT 1")
        m = c.fetchone()
        for i in self.conn_list:
            try:
                self.messagesend(i, f"{u[0]}:{m[0]}")
            except:
                pass

    def messagesend(self,conn,msg):
        message = msg.encode(self._encoding)
        msg_length = len(message)
        send_length = str(msg_length).encode(self._encoding)
        send_length += b' ' * (self._header - len(send_length))
        conn.send(send_length)
        conn.send(message)

    def getcurser(self):
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute("SELECT serial from chats ORDER BY serial DESC LIMIT 1")
        s = c.fetchone()
        
        if s:
            integ = int(s[0])
            print(f"current serial number : {integ + 1}")
            return integ+1
        else:
            print(f"current serial number : {1}")
            return 1
        conn.close()
    
    def addtodata(self,addr,msg):
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute("INSERT INTO chats VALUES (?,?,?)",(self.currentserialnumber,str(addr),msg))
        conn.commit()
        self.update_all()
        self.currentserialnumber += 1
        conn.close()

s = serverobj()
s.startserver()
