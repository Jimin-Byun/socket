import socket

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 12345
Message = "Practice".encode("utf-8")

clientS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientS.sendto(Message, (UDP_IP_ADDRESS, UDP_PORT_NO))

