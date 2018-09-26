import socket

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 12345

serverS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverS.bind( (UDP_IP_ADDRESS, UDP_PORT_NO) )

while True:
    data, addr = serverS.recvfrom(1024)
    print("Message: " + data.decode("utf-8"))