# clientserver
### Tl;dr
1. Run server.py either in the background or foreground.(stay connected to wifi please)
2. Copy the ip address shown by server.py into the code in client.py and save it (ip adreess only appears once in client so find it and replace, code will soon be changed to handle ip as an argument from terminal)
3. Run the any number of client.py files from any device in the same network, and voila you cans ent texts to groups now.
4. commands are typed just like normal messages. Will implement :help function to provide help inside app but for now,
   
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

### My thoughts
I started out from a video on youtube on websockets using python. So my was similar to their's at the beginning.
But that video only had code to send data to the server, everything else was built upon by me. Ofc changing ip for the cliennt is stupid, but i havent thougt of a workaround for it yet.

### Task checklist
#### MainTask
- [x] A server and client model, where each soldier and official acts as a client.
- [x] The system should follow a group based communication protocol, where a soldier from one troop can only see messages from soldiers from the same troop.(has groups, but doesnt follow a particular protocol)
- [x] A troop leader can send messages to everyone in his own troop, as well as see messages from other troop leaders.
- [x] The chief commander can see all messages but he should only be able to communicate directly with the troop leaders.
- [x] The whole model will be based on groups, so you will be required to create groups to maintain the communication protocols.(again, does have groups, but my communication protocol isnt based on groups)
- [ ] Dockerize the CLI.
#### Hacker Mode
- [x] Each client should be able to keep a record of his chat history over the past one week, and he would be able to download it in the form of a text file whenever he wants.
- [x] If any of the client is offline, the server should store messages along with the username of the recipient and send the messages to the client as soon as he is online, rather than giving an error message.
- [x] If a client receives a message, he should receive it with the name of the sender along with it. If the client sends a message, his own name should be printed along with the message on his own screen as given below.Army1: Hello guys, how are you doing? Army2: I am fine, what about you? Army3 (me): I am also fine.
- [ ] Finally, dockerize the whole application along with the client side database. You should learn Docker Compose for this.

### where my code is inefficient
