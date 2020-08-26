import socket
import threading
import sys
import sqlite3
import getpass

class clientobj():
    def __init__(self, header = 64, port = 3000, encoding = 'utf-8' ):
        #setup variables for connection
        if len(sys.argv) == 2:
            self._serverip = sys.argv[1]
        else:
            self._serverip = "172.17.0.1"
        print(self._serverip)
        self._header = header
        self._port = port
        self._encoding = encoding
        self._addr = (self._serverip, self._port)
        #connecting
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect(self._addr)
        #special messages
        self._DISCONNECT_MESSAGE = "kawudhvcjsfuhvslfroyivedfegeqsfvfggffgr"
        self._changegroup = "sjduyhgvkcsueyfvskeufjdghvskehdgsdfdvuehfg"
        self._downloadchat = "jytghdciyjhmgcgddikjhfgvkjjitgjdhfoewihigqer"
        #control bools
        self.connected = True
        self.printmess = True
        self.download = False
        #variable to keep track of number of lines to erase
        self.num_mes_recv=0
        #hex codes
        self.Cup = '\x1b[1A'
        self.eli = '\x1b[2K'
        self.name = "jsfhgvsikfhjdvsbfkfivhsbfolibkvjsbfvikh"


    #starts the connection
    def startclient(self):
        print("Starting chat app, type :help and enter to get help regarding commands")
        userlist = ['Chiefcommander','ArmyGeneral','NavyMarshal', 'AirForceChief','puter stop']
        #checks if username is allowed
        if getpass.getuser() in userlist:
            username = getpass.getuser()
            #code to get usename using getpass
        elif self.otheruser(getpass.getuser()):
            username = getpass.getuser()
        else:
            username=input('[enter username(because you werent part of predefined users)]\n')
            while not self.otheruser(username) and username not in userlist: 
                username=input('[enter username(because you werent part of predefined users)]\n')
            #asks username if no match found
        #first message to be sent is the username(in my custom protocol)
        self.sendmessage(username)
        thread = threading.Thread(target=self.recievemessage, args=())
        thread.start()
        print("[recieve thread started]")
        self.connected = True
        while self.connected:
            msg = input()
            #to delete the previous message that was typed
            self.printmess = False
            #the printmess is to hold off printing new messages when deleting prev messages
            #hex codes for doing the same
            sys.stdout.write(self.Cup)
            sys.stdout.write(self.eli)
            self.printmess = True
            if msg == "logmeout":
                #client setup for logginh out
                self.connected = False
                self.sendmessage(self._DISCONNECT_MESSAGE)
            elif msg == ":d":
                #client setup for download 
                self.sendmessage(self._downloadchat)
                print("Enter filename to save to(with extension)")
                self.name = input() #input messing with sendmessage input
            elif msg == ":help":
                #setuo for help
                fn = open('info.txt','r')
                len = self.file_len('info.txt')
                self.num_mes_recv += len
                print(fn.read())
            else:
                self.sendmessage(msg)
        #stop threads

    #checks if username valid
    def otheruser(self,name):
        flag=False
        for i in range(50):
            if name in [f"Army{i+1}",f"AirForce{i+1}",f"Navy{i+1}"]:
                flag = True
        return flag

    #thread fucntion to recieve messages
    def recievemessage(self):
        while self.connected:
            msg_length = self.client.recv(self._header).decode(self._encoding)
            self.num_mes_recv += 1
            if msg_length:
                msg_length = int(msg_length)
                msg = self.client.recv(msg_length).decode(self._encoding)
                #checking if message is a command to change group
                if msg == self._changegroup:
                    self.delallmes()
                    #checking if message to download chat
                elif msg == self._downloadchat:
                    self.download = not self.download
                    #opens file when arg is self._downloadchat
                    self.downloadtofile(self._downloadchat)
                else:
                    #if normal message prints when printmess is set(to prevent unnecessary deletions)
                    if self.downloadtofile(msg):
                        pass
                    elif self.printmess == True:
                        print(r'{}'.format(msg))
                    else:
                        while self.printmess == False:
                            pass
                        print(r'{}'.format(msg))

    def downloadtofile(self, msg):
        #open and close files and write to file, when downloading
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
        #delete the number of lines above as mentioned by self.num_mes_recv
        while self.num_mes_recv>0:
            self.printmess = False
            sys.stdout.write(self.Cup)
            sys.stdout.write(self.eli)
            self.printmess = True
            self.num_mes_recv -= 1
        print("[recieve string started]")

    def sendmessage(self,msg):
        #send message after encoding
        message = msg.encode(self._encoding)
        msg_length = len(message)
        send_length = str(msg_length).encode(self._encoding)
        send_length += b' ' * (self._header - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def file_len(self,fname):
        #finding filelength to add to num_mes_recv so that it gets deleted when changing groups
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 2


c = clientobj()
c.startclient()     
