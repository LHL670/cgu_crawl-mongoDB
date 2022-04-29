import socket
if __name__=='_main_':
        
    hostname=socket.gethostname()
    IPAddr=socket.gethostbyname(socket.gethostname())
    print("Your Computer Name is:"+hostname)
    print("Your Computer IP Address is:"+IPAddr)
