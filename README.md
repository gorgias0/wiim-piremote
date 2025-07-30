# wiim-piremote
Python script to send http commands to WIIM device via IR remote and lirc

## Hardware needed

- Raspberry pi zero 2W
- TSOP4838 IR-receiver 38 kHz e.g.  https://www.electrokit.com/tsop4838-ir-modul-38-khz

This would probably work with any raspberry pi that has a network interface.
It is very convenient using a zero w with wifi, just a power cable needed.

## How to get started (basic overview)

- Install lirc `apt install lirc`
- Install python3 if needed `apt install python3`
- Create a venv for the python project and install lirc and requests (perhaps not needed)
- Install lirc for python `pip3 install lirc`
- Install requests for python `pip3 install requests`

### Lirc config

- Edit /boot/firmware/config.txt and add: `dtoverlay=gpio-ir,gpio_pin=14` (if using pin 14 for the IR reciever)
- Download a lircd.conf for your remote at https://sourceforge.net/p/lirc-remotes/code/ci/master/tree/remotes/
  - Put this file in /etc/lirc
- Edit lirc_options.conf and set:

```
  driver = default
  device = /dev/lirc0
```

### Run the python script and check output for commands from the remote (uncomment print(command) in remote.py)

`python3 remote.py`

Adjust codes/commands for your remote and wiim device in remote.py

See available commands at https://developer.arylic.com/httpapi/#http-api

### Create a service that runs on startup
E.g. adjust ir.service with correct paths and put in /etc/systemd/system

See https://alfredobarron.medium.com/how-to-run-python-script-as-a-service-on-ubuntu-22-613c4e825b6b

