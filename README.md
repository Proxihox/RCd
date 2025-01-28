# RCd

RCd is a framework to host Reverse Coding problems.
The primary issue with hosting a reverse coding challenge is the need to generate executables for various processors/Operating systems, which is pretty painful. Not to mention the need to attach external files along with the executable. This tool prevents all that hassle, by hosting your Reverse coding challenge.

Setting up and testing:

Git clone repository and run `./setup.sh` once to install requirements and compile the Reverse Coding file. Open the config.py file and fill in the variables as required. Launch the server using `python3 main.py` . 

Once you launch the server the terminal should show this :
```
Starting server...
PID:  525442
Connection command :
nc 127.0.1.1 65432
```
Open another terminal tab and enter the connection command.
You should be prompted to enter your roll number and register as a new user. Login again and try out the sample RC problems.
