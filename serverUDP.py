import socket
import struct

def operator(l, op, r):
    if op == 1:
        l += r
    elif op == 2:
        l -= r
    elif op == 4:
        l *= r

    return l

host = "127.0.0.1"
port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

while True:
    packet, addr = s.recvfrom(1024)

    for i in range(0, len(packet), 1):
        print(hex(packet[i]), end = ' ', flush=True)
    print()

    op = packet[0]
    cnt = packet[1]
    data = packet[2:]

    result = data[0] >> 4
    v = data[0] & 0x0f
    result = operator(result, op, v)

    for i in range(1, int(cnt / 2), 1):
        result = operator(result, op, data[i] >> 4)
        result = operator(result, op, data[i] & 0x0f)
    print("i ?", i)
    if cnt % 2:
        result = operator(result, op, data[i + 1] >> 4)
    print(result)

    print(struct.pack('!i', result))
    s.sendto(struct.pack('!i', result), addr)


