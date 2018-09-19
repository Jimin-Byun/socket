import socket
import sys
from urllib.parse import urlparse

def getHtml (host, resource):
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((host, 80))
    #s.sendall("GET / HTTP/1.1\r\nHost: www.cnn.com\r\n\r\n")
    data = "GET " + resource + " HTTP/1.1\n"+"HOST: "+host+"\r\n\r\n"
    # without encoding - no enter
    s1.send(data.encode(encoding="utf-8"))
    data = s1.recv(1024)
    #print(data)
    data_str = data.decode("utf-8")
    #print(data_str)
    s1.close()
    return data_str

def html2text(data_str):
    idx = data_str.find("<HTML>")
    data_str = data_str[idx:]
    #print(data_str)

    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect((host, 10010))

    while True:
        data = s2.recv(1024)
        string = data.decode("utf-8")
        #print(string)
        if "READY" in string:
            break

    s2.send(data_str.encode(encoding="utf-8"))

    while True:
        data = s2.recv(1024)
        string = data.decode("utf-8")
        print(string)
        if "ICS 226 HTML CONVERT COMPLETE" in string:
            break

    s2.close()

if __name__ == "__main__":
    # command line arguments start from no.1, file name is argv[0]
    url = sys.argv[1]
    parsed = urlparse(url)
    #print(parsed)
    host = parsed.netloc
    resource = parsed.path
    #print(host, resource)
    result = getHtml(host, resource)
    html2text(result)
