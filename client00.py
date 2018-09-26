import socket
import sys
from urllib.parse import urlparse

def getText (host, resource):
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((host, 80))
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((host, 10010))

    #send request to both servers
    data = "GET " + resource + " HTTP/1.1\n"+"HOST: "+host+"\r\n\r\n"
    s1.send(data.encode(encoding="utf-8"))
    while True:
        data = s2.recv(1024)
        string = data.decode("utf-8")
        # print(string)
        if "READY" in string:
            break

    #send data to the 'html2text' server that received from 'getHtml' server
    previous = []
    current = s1.recv(1024).decode("utf-8")
    while True:


        previous += current
        if previous.find("<HTML>") and previous.find("</HTML>"):
            idx = previous.find("<HTML>")
            previous = previous[idx:]
            s2.send(previous.encode(encoding="utf-8"))
            break
        if previous.find("<HTML>"):

            idx = previous.find("<HTML>")
            previous = previous[idx:]
            s2.send(previous.encode(encoding="utf-8"))

        if not previous.find("<HTML>"):
                previous = current
                current = s1.recv(1024).decode("utf-8")

    s1.close()
    s2.close()

if __name__ == "__main__":
    # command line arguments start from no.1, file name is argv[0]
    url = sys.argv[1]
    parsed = urlparse(url)
    #print(parsed)
    host = parsed.netloc
    resource = parsed.path
    #print(host, resource)
    getText(host, resource)
