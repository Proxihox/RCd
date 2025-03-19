# RCd

RCd is a framework to host Reverse Coding problems.
There are 2 issues with the standard format of providing an executable binary to the participants:
1. The need to generate separate executables for every OS
2. Participants using decompilers to obtain the pattern
This tool prevents all that hassle, by hosting your Reverse coding challenge on a server, which every OS can connect to and provides a fair playing ground to everyone.

Setting up and testing:

Git clone repository and run `./setup.sh` once to install requirements and compile the Reverse Coding file. Open the `config.py` file and fill in the variables as required. Launch the server using `python3 main.py` . 

Once you launch the server the terminal should show this :
```
Starting server...
PID:  134158
<ip> <port> :
127.0.1.1 8080
```

# Connecting to the server
You need to connect to the server using a web socket. Users can access through this [colab notebook](https://colab.research.google.com/drive/1jeKH3Nfrz2U-exz415XC-Z_ezeXpFLQy?usp=sharing). Make sure to replace the `<ip> <port>` with the server's details.

Alternatively Unix based OS's can directly connect to the server using netcat:
```
nc -v <ip> <port>
```

You should be prompted to enter your email ID and register as a new user. Login again and try out the sample RC problems.

Guide on how to host it publicly coming soon.