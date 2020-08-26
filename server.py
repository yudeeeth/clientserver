import socket
import threading
import sqlite3

class serverobj():
    def __init__(self, header = 64, port = 3000, encoding = 'utf-8' ):
        #self._serverip = socket.gethostbyname(socket.gethostname())
        self._serverip = self.getserverip()
        self._header = header
        self._port = port
        self._encoding = encoding
        self._addr = (self._serverip, self._port)
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind(self._addr)
        self._DISCONNECT_MESSAGE = "kawudhvcjsfuhvslfroyivedfegeqsfvfggffgr"
        self._changegroup = "sjduyhgvkcsueyfvskeufjdghvskehdgsdfdvuehfg"
        self._downloadchat = "jytghdciyjhmgcgddikjhfgvkjjitgjdhfoewihigqer"
        self.currentserialnumber = int(self.getcurser())
        self.stop_command = "puter stop"

    #destructor which does nothin coz its almost never called or something
    def __del__(self):
        self.addtodata("[server]","Server killed",'h')
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute("DELETE FROM chats WHERE user LIKE '%server%'")
        conn.commit()
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
                group = self.assigngrp(username)
                if username == self.stop_command:
                    start = False
            threadhandlecli = threading.Thread(target= self.HandleClient,args=(conn, addr,username,group))
            threadhandlecli.start()
            self.conn_list.append( [ conn , username , group ] )
            print(f"Active connections {threading.activeCount()-1}")

    def HandleClient(self,conn,addr,username,group):
        print(f"[New Connection {addr}{username}]")
        connected = True
        self.sendbulk(conn,username,group)
        while connected:
            msg_length = conn.recv(self._header).decode(self._encoding)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self._encoding)
                if msg == self._DISCONNECT_MESSAGE:
                    self.messagesend(conn,"Disconnected from server")
                    connected = False
                    for i in range(len(self.conn_list)):
                        if self.conn_list[i][1] == username:
                            del self.conn_list[i]
                    print(f"[Connection severed {username}]")
                    print(f"Active connections {threading.activeCount() - 2}")
                elif self.command(msg,username,group):
                    group = self.changegrp(msg,group,username)
                    self.findgrpnhange(username,group)
                    #send change group command to client
                    self.messagesend(conn,"sjduyhgvkcsueyfvskeufjdghvskehdgsdfdvuehfg")
                    #message to delete all recv messages
                    self.sendbulk(conn,username,group)
                    #self.addtodata(username,msg,group)
                elif msg == self._downloadchat:
                    self.messagesend(conn,self._downloadchat)
                    self.prepquerynsend(username,group,conn)
                elif username=="Chiefcommander" and group !="h":
                    self.messagesend(conn,'Chiefcommander can NOT send messages to troops direcctly. Sendng message to troop leaders without changing group...')
                    self.addtodata(username,msg,'h')
                else:
                    print(r"[{}@{}]: {}".format(username,group,msg))
                    self.addtodata(username,msg,group)
                #self.messagesend(conn , self._RECIEVEDSUCCESSFULLY) 

    def prepquerynsend(self, username, group, conn):
        con = sqlite3.connect('messages.db')
        c = con.cursor()
        c.execute(f"SELECT user,grp,date, time, msg from chats where date > (select date('now','-7 day')) and grp like '%{group}%' order by serial")
        var = c.fetchall()
        for row in var:
            self.messagesend(conn,f"[{row[2]} {row[3]}]{row[0]}:{row[4]}\n")
        self.messagesend(conn,self._downloadchat)

    def findgrpnhange(self,username, group):
        for i in self.conn_list:
            if i[1]==username:
                i[2]=group

    def update_all(self,group):
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute(f"SELECT user,msg,time from chats where grp like '%{group}%' ORDER BY serial DESC LIMIT 1")
        u = c.fetchone()
        #c.execute("SELECT msg from chats ORDER BY serial DESC LIMIT 1")
        #m = c.fetchone()
        for i in self.conn_list:
            try:
                if i[2]==group:
                    if i[1]==u[0]:
                        self.messagesend(i[0], f"[{u[2]}]{u[0]}(me):{u[1]}")
                    else:
                        self.messagesend(i[0], f"[{u[2]}]{u[0]}:{u[1]}")

            except:
                pass
    def sendbulk(self,conn,user,group):
        #configure to senf only group group messages
        conns = sqlite3.connect('messages.db')
        c=conns.cursor()
        c.execute(f"SELECT user,msg,time from (SELECT * from chats where grp like '%{group}%'ORDER BY serial DESC LIMIT 30) ORDER BY serial ASC")
        msg_list=c.fetchall()
        for row in msg_list:
            if user==row[0]:
                self.messagesend(conn,f"[{row[2]}]{row[0]}(me):{row[1]}")
            else:
                self.messagesend(conn,f"[{row[2]}]{row[0]}:{row[1]}")

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
    
    def addtodata(self,user,msg,group):
        #implement group stuff
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute("INSERT INTO chats VALUES (?,?,?,?,?,?)",(self.currentserialnumber,group,str(user),msg,self.gettime(),self.getdate()))
        conn.commit()
        self.update_all(group)
        self.currentserialnumber += 1
        conn.close()

    def getdate(self):
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute("select date('now')")
        time = c.fetchone()
        return time[0]

    def gettime(self):
        conn = sqlite3.connect('messages.db')
        c = conn.cursor()
        c.execute("select time('now')")
        time = c.fetchone()
        return time[0]

    def assigngrp(self,username):
        lis = ['ArmyGeneral','NavyMarshal','AirForceChief','Chiefcommander','yudeeeth','puter stop']
        if username in lis:
            return 'h'
        elif "Army" in username:
            return 'r'
        elif 'Navy' in username:
            return 'n'
        elif 'AirForce' in username:
            return 'a'
    def command(self, msg, username,group):
        lis = ['ArmyGeneral','NavyMarshal','AirForceChief','yudeeeth','puter stop']
        lis2 = [':H',':R',':N',':A',':h',':r',':n',':a']
        if username in lis:
            if msg == ":t":
                return True
            else:
                return False
        elif username == "Chiefcommander":
            if msg in lis2:
                return True
            else:
                return False
        return False

    def changegrp(self,msg,group,username):
        dic = {
                'ArmyGeneral':'r',
                'NavyMarshal':'n',
                'AirForceChief':'a'
                }
        if msg == ":t":
            if group == 'H' or group == 'h':
                return dic[username]
            else:
                return 'h'
        else:
            return msg[1].lower()



s = serverobj()
s.startserver()
