import socket
import sys
import struct

# Variables from the arguments
# print(sys.argv) -> check the arguments stored as string type, see the single quote
host = sys.argv[1] # string
port = int(sys.argv[2]) # int
op = sys.argv[3]
cnt = len(sys.argv[4:])
print(host, port, op, cnt)

# Building the datagram packet sent to the server, the packet is the type of bytearray()
packet = bytearray()

# First byte
if op == '+':
    packet.append(1)
elif op == '-':
    packet.append(2)
elif op == '*':
    packet.append(4)

# Second byte
packet.append(cnt)

# Third byte
for i in range(4, cnt+3, 2):
    packet.append(int(sys.argv[i]) << 4 | int(sys.argv[i+1]))

if cnt % 2:
    packet.append(int(sys.argv[i+2]) << 4)

"""
for i in range(0, len(packet), 1):
    print(hex(packet[i]), end = ' ',flush=True)
"""

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(packet, (host, port))

result = s.recvfrom(1024)
print(struct.unpack('!i', result[0])[0])
