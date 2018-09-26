import socket

host = "rtvm.cs.camosun.bc.ca"
resource = "/ics226/lab1test4.html"

#create sockets for each port
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect socket to the web server
s1.connect((host, 80))
#What does "impleting HTTP 1.1" mean? Is it to request the page to the web server?
#s.sendall("GET / HTTP/1.1\r\nHost: www.cnn.com\r\n\r\n")
#request1 = "GET" + " " + resource + " " + "HTTP/1.1\n" \ + "Host: " + host + "\n\n"
request = "GET " + resource + " HTTP/1.1\n" + "HOST: " + host + "\r\n\r\n"
s1.send(request.encode(encoding="utf-8"))

#connect socket to the html2text server
s2.connect((host, 10010))
while True:
    data = s2.recv(1024).decode("utf-8")
    #print(data)
    if "READY" in data:
        break

#What is difference between [] and ""?
data, prev, curr = "","",""
state = 1

while state !=4:
    if state == 1:
        print("-----------------State 1--------------------")
        data = prev + curr
        if ("<HTML>" in data.upper() and "</HTML>" in data.upper()):
            html_idx = data.index("<HTML>")
            data = data[html_idx:]
            s2.send(data.encode("utf-8"))
            state = 3
        elif "<HTML>" in data.upper():
            html_idx = data.index("<HTML>")
            data = data[html_idx:]
            s2.send(data.encode("utf-8"))
            prev = curr
            state = 2
        else:
            prev = curr
            curr = s1.recv(1024).decode("utf-8")
            #print(curr)

    # to receive long data from the web server
    elif state == 2:
        print("-----------------State 2--------------------")
        curr = s1.recv(1024).decode("utf-8")
        while curr:
            data = prev + curr
            if "</HTML>" in data.upper():
                s2.send(curr.encode("utf-8"))
                state = 3
                break
            else:
                s2.send(curr.encode("utf-8"))
                prev = curr
                curr = s1.recv(1024).decode("utf-8")

    #turn to receive data from the html2text server
    elif state == 3:
        print("-----------------State 3--------------------")
        data, prev, curr = "", "", ""
        curr = s2.recv(1024).decode("utf-8")
        while curr:
            data = prev + curr
            print(curr, end='')
            if "ICS 226 HTML CONVERT COMPLETE" in data.upper():
                state = 4
                break
            prev = curr
            curr = s2.recv(1024).decode("utf-8")
print('')
s1.close()
s2.close()