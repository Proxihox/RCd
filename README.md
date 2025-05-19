# RCd

RCd is a framework to host Reverse Coding problems.
There are 2 issues with the standard format of providing an executable binary to the participants:
1. The need to generate separate executables for every OS
2. Participants using decompilers to obtain the pattern
This tool prevents all that hassle, by hosting your Reverse coding challenge on a server, which every OS can connect to and provides a fair playing ground to everyone.

You can host this RC framework on a server and allow participants to query the server over the internet. Read [the Guide](Guide.md) on how to host the server on the cloud.

## Quick set up and local testing:

Git clone repository and run `./setup.sh` once to install requirements and compile the Reverse Coding file. Open the `config.py` file and fill in the variables as required. Launch the server using `python3 main.py` . 

Once you launch the server the terminal should show this :
```
Starting server...
PID:  134158
<ip> <port> :
127.0.1.1 8080
```

## Connecting to the local server

Unix based OS's can directly connect to the server using netcat:
```
nc -v <ip> <port>
```
Window's user's will need to enable `telnet` and then run the above command, replacing `nc` with `telnet`.

You should be prompted to enter your email ID and register as a new user. Login again and try out the sample RC problems.