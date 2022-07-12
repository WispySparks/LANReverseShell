import socket
privateKey: str = "?!(asLK03,,yB/["
sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket Created")
sock.settimeout(15)
ip: str = "localhost"
port: int = 17340
print("Attempting Connection at " + ip + ", Port: " + str(port))
connection: int = sock.connect_ex((ip, port))
if (connection == 0):
    print("Connected")
    while True:
        try:
            msgBuffer = sock.recv(4096)
            if (msgBuffer.decode() == "Command"):
                command: str = input("Input Command: ").strip()
                sock.send((privateKey + " " + command).encode())
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