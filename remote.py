import lirc # type: ignore
import requests # type: ignore
from requests.packages.urllib3.exceptions import InsecureRequestWarning # type: ignore
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# ip of the wiim device on local network
BASE_URL="https://192.168.0.241/httpapi.asp?command="

def send(command):
    return requests.get(BASE_URL + command, verify=False) # ignore SSL warnings

def ProcessIRRemote():

    #get IR command
    #keypress format = (hexcode, repeat_num, command_key, remote_id)
    try:
        keypress = conn.readline()
    except:
        keypress=""

    if keypress != "" and keypress != None:

        data = keypress.split()
        sequence = data[1]
        command = data[2]

        #ignore command repeats
        if sequence != "00":
           return

        # uncomment to see what commands your remote sends
        # print(command) 

        if command == "KEY_DOWN":
            send("setPlayerCmd:vol--")
        elif command == "KEY_UP":
            send("setPlayerCmd:vol%2b%2b")
        elif command == "KEY_LEFT":
            send("setPlayerCmd:prev")
        elif command == "KEY_RIGHT":
            send("setPlayerCmd:next")
        elif command == "KEY_ENTER":
            send("setPlayerCmd:onepause")
        elif command == "KEY_NEXT":
            status = send("getPlayerStatus").json()
            if status == None or status['status'] != 'play': return # dont seek if not playing
            curpos = int(status['curpos'])
            totlen = int(status['totlen'])
            seekpos = int(curpos + 15 * 1000)
            if seekpos >= totlen - 1000: return # dont seek past the end
            seekpos = int(seekpos / 1000)
            send("setPlayerCmd:seek:" + str(seekpos)) # forward 15 sec
        elif command == "KEY_PREVIOUS":
            status = send("getPlayerStatus").json()
            if status == None or status['status'] != 'play': return # dont seek if not playing
            curpos = int(status['curpos'])
            seekpos = int((curpos - 15 * 1000) / 1000)
            if seekpos < 0: seekpos = 0
            send("setPlayerCmd:seek:" + str(seekpos)) # back 15 sec

conn = lirc.LircdConnection()
conn.connect()
print("Listening...")

while True:
      ProcessIRRemote()
