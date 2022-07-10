import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket Created")
sock.settimeout(5)
ip = socket.gethostbyname(socket.gethostname())
ip = "localhost"
port = 17340
print("Attempting Connection at " + ip + ", Port: " + str(port))
connection = sock.connect_ex((ip, port))
if (connection == 0):
    print("Connected")
    while True:
        try:
            msgBuffer = sock.recv(4096)
            if (msgBuffer.decode() == "Command"):
                command = input("Input Command: ").strip()
                sock.send(command.encode())
            elif (msgBuffer):
                print(msgBuffer.decode())
                if (msgBuffer.decode() == "Connection Closed"):
                    break
            else:
                break
        except:
            print("\nClient Interrupted")
            break
else:
    print("Timed Out or Connection Failed, Error Code: " + str(connection))