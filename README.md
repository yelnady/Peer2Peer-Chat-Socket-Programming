# Peer2Peer-Chat-Socket-Programming
This a small chat application using socket programming in python, allowing you to talk to many peers with a Decentralized Replicated Data Store

This program facilitates **peer-to-peer communication** by allowing the **Decentralized Replicated Data Store (DRDC)** to add an unlimited number of users . Users can exchange messages or fake data using their respective port numbers. Additionally, the program supports **network discovery** and ensures **data store consistency**. 

By the end of the program, **each peer** connected to the network will have all the transactions or messages that have been **sent** and **received** since the start of the program stored in **its data store**.



## Implemented use case:

![](https://github.com/yelnady/Peer2Peer-Chat-Socket-Programming/blob/master/implemented_use_case.jpeg)

## System Architecture:

![](https://github.com/yelnady/Peer2Peer-Chat-Socket-Programming/blob/master/system_arch.002.jpeg)

## System Design:

![](https://github.com/yelnady/Peer2Peer-Chat-Socket-Programming/blob/master/system_design.003.jpeg)

## Details: 
- **Sender**: allow the peer class to perform **the sending functionality** in a **thread** so it can **send messages** to any other peer **using its port**. It also has some useful methods as sending messages or **broadcasting me** to others. 
- **Receiver**:  allowing  the  peer  to  **continuously  check**  if  there’s  anyone  to communicate with me. It also **runs in another thread** which is turned on by the peer instance. 
- **Peer**:  This class  is  **the  initiator**  of  any  **new peer** wants  to  be  added to  our Decentralized Replicated Data Store. Its responsibility to take the **name** of the user and its **port**, then runs the sender and receiver objects in **two different threads.** 
- **User**: It’s a small entity that holds only the **name**, **host** and the **peer** of the user. 
- **Datastore**(repository):This class have many useful functions such as **add\_to\_queue** which handles the **problem of caching** and **not to overwhelm** the datastore with  many  data.  So,  its  responsibility to  take  data into  queue  and to  free  the queue and so on…  
- **DRDC**: This is called the **peer communication management**, it can **print** the current  users,  **broadcast**  the  msg  which  is  the  network  discovery  role,  also continuously **synchronize the data** with the datastore of each node or each pair, so the **datastore will be consistent among all others**. 



## `Installation Guide`:
- To **start** using this application all you want is a **python terminal**. 
- First, open a terminal in the direcotory of the program: `DRDC.py` → this will start your application. 
- Then to **start adding peers** to your program or to your network, in a new terminal, type again : `peer.py` → this will **add a new peer** to your application. 
- **No need** to install any modules or servers to start using this application 
- You must assure that you have python 3.7 or above if any. 
- This program is built using **Python in PyCharm IDE** as part of my study in **CS252 – CU – FCAI – Software Engineering II – 2019**.
