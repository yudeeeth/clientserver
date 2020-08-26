# clientserver
### Tl;dr
##### If your username isn't recognised as possible, it will ask you to type in
For ease during development and testing
#### Without Docker
1. Run server.py either in the background or foreground.(stay connected to wifi please)
2. Copy the ip address shown by server.py and use it as an argument when calling client.py (or you can set a default value by editing the file)
3. Run the any number of client.py files from any device in the same network, and voila you can send texts to groups now.
4. commands are typed just like normal messages. 
5. Type :help and enter to display list of commands and descriptions. This command will display the following in the terminal
   
#### With Docker
1. Run dockerimagescript.sh after chmod-ing it.
 > chmod +x dockerimagescript.sh
 > ./dockerimagescript.sh
 
2. Run 
 > docker exec -it sockets_client_1 /bin/bash
### Commands Inside Program
   ##### Chiefcomander can shift to any group he wants using the following commands:
   
      > :h 
      
      -default group contains the **H**eads (Troop leaders)
      
      > :n 
      
      -**N**avy troop group
      
      > :a 
      
      -**A**irforce troop group
      
      > :r 
      
      -A**R**my troop group
    
    ##### Troopleaders can only *toggle* between the troop leader group and their troop's group
      
      > :t 
      
      -**T**oggle between groups
    ##### Everone can use the following commands
    
      > :d
      
      -to download a weeks worth of chat from the group they are calling this from.
      
      > logmeout
      
      -logs user out

### If you 're using dockers
Whyy?
Anyway. for now I ve written a script to install the right images with right names(because i dint want to put (Dockerfile)them on different files and stuff). It will also call docker compose for you, **call it with sudo if you havent configured docker to work without sudo** so run the script, and you ll have conntainers running. by default, sicne containers are running togethor in compose they have the ips configured right, just ssh into client container by using 
 > docker exec -it client /bin/bash
 
 then run,
 > python3.6 client.py
 
 voila, ssh into this container as many times as you want and it will be a different client. This will  only work if these are the only runnign conatiners, else you will have to pass the server ip as mentioned below as an argument.
 
 If you want to run the client image on your own, not the one already running,(again, why?) you can run, it make sure its connected to the same network(which it will be by default), and find the server's container ip by using 
 > docker inspect container-name 
 
 and pass that as an argument while calling client.py as such
 > python3.6 client.py 172.17.0.2 

### My thoughts
I started out from a video on youtube on websockets using python. So my was similar to their's at the beginning.
But that video only had code to send data to the server, everything else was built upon by me. Ofc changing ip for the client is stupid, but i havent thought of a workaround for it yet.
Please do read the last secction for some drawbacks in this code.

### Task checklist
#### MainTask
- [x] A server and client model, where each soldier and official acts as a client.
- [x] The system should follow a group based communication protocol, where a soldier from one troop can only see messages from soldiers from the same troop.**_(has groups, but doesnt follow a particular protocol)_**
- [x] A troop leader can send messages to everyone in his own troop, as well as see messages from other troop leaders.
- [x] The chief commander can see all messages but he should only be able to communicate directly with the troop leaders.
- [x] The whole model will be based on groups, so you will be required to create groups to maintain the communication protocols.**_(again, does have groups, but my communication protocol isnt based on groups)_**
- [x] Dockerize the CLI.
#### Hacker Mode
- [x] Each client should be able to keep a record of his chat history over the past one week, and he would be able to download it in the form of a text file whenever he wants.
- [x] If any of the client is offline, the server should store messages along with the username of the recipient and send the messages to the client as soon as he is online, rather than giving an error message.
- [x] If a client receives a message, he should receive it with the name of the sender along with it. If the client sends a message, his own name should be printed along with the message on his own screen as given below.Army1: Hello guys, how are you doing? Army2: I am fine, what about you? Army3 (me): I am also fine.**_(Didnt use buffers for this, but didnt notice issues when )_**
- [x] Finally, dockerize the whole application along with the client side database. You should learn Docker Compose for this.

### where my code is inefficient or downright stupid

1. If a new message is recieved while one is typing a message, the typed message will be taken out of buffer, and hence has to be retyped.
2. One has to change the ip address present in the client program everytime, because the local ip given to server changes everytime server is run.(Incase of dockers, ip will change if more containers are running before using docker compose)
3. No way to stop the server from inside the server(have to use a special account to shut down server)
4. Code is not clean as can be, in a few places the code has multiple if conditions to catch edge cases which could have been removed if *see the next point*
5. Only strings are transfered thru the sockets and are printed as is without parsing. This and the previous point could have been avoided by passing serialised objects through the socket. But since this project was simple enough, i thought i could handle it with just strings. Which i did, at the expanse of code readability.
6. it might have bugs when a large number of clients are connected (and send messages simultaneously) since i couldnt debug this on my own.
