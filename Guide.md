# Making your own RC using RCd

This is a step-by-step guide to host your RC using RCd.

## Local setup 

Git clone this repository and run `./setup.sh` once to install requirements and compile the Reverse Coding file. 
### Configuration
Open the `RCD/config.py` file. 
Change the `RCNAME` to the name of your event. Set `LOGS` to true for debugging purposes. If you want people to make an account with their email id as username and login every time they want to access the server, set `LOGIN` to true.

You can skip this paragraph if you have set `LOGIN` to false.
If you want people to verify their emails when creating an account, set `VERIFY_MAIL` to true, and then follow the the [insturctions](RCd/mail/Instructions.md) to setup an automated OTP mailer. 
Read the comments under `PASSWORD_SECURITY_LEVEL`, to set restrictions on the password.

## Local Testing

The repository comes with a few sample problems. To add your own problems, read [Making your own problems](#making-your-own-problems)
Open terminal and make sure you are inside folder with `main.py`. Launch the server using `python3 main.py`.
Once you launch the server the terminal should show something like this :
```
Starting server...
PID:  134158
<ip> <port> :
127.0.1.1 8080
```
This means that the server is now running locally on your laptop. To test that its working properly, run the following command in another terminal window. 
```
nc -v <ip> <port>
```
Replace `<ip>` and `<port>` with the values printed by the server when it was launched. `nc` only works on linux. Replace `nc` with `telnet` if you are on windows. Unfortunately local testing can't be done on a mac, due to firewall restrictions.

Once you connect to the server, follow the prompts and test the server. 

## Making your own problems

Currently, there is support for making problems in C++ only. Support for python will be added soon.
Go to [RCd/challenges/RC.cpp](RCd/challenges/RC.cpp). This file contains a template for you to add your questions. You only need to create new `problem` objects. Refer to this detailed [problem making](RCd/challenges/problemMaking.md) guide
Once you have updated your problems, run `./setup.sh` once more to compile the file, then launch the server again using `python3 main.py` and test your problems. 

## Hosting on cloud 
I recommend using Google Compute Engine (GCE) to host this server. Refer to this [GCE Starter Guide](https://tangible-plantain-df6.notion.site/Gcloud-Compute-1bbb509ab4c4809dabaeece6aedadee3?pvs=4) to get started hosting on the server. I recommend using scp to your local server code to the VM instance. Make sure you have removed firewall protection for the port. SSH onto the VM instance then follow the steps to setup and launch the server that you did earlier. 
Use `gcloud compute instances list` to get the external IP of the VM instance. The command to connect to the server will be 
```
nc -v <external IP> <port>
```
Google compute engine will make this server accessible to the public internet, and you should be able to connect to the server from any device connected to the internet.

For people on windows/mac, the best option to connect to the server would be through google colab : 
You need to connect to the server using a web socket. Users can access through this [colab notebook](https://colab.research.google.com/drive/1jeKH3Nfrz2U-exz415XC-Z_ezeXpFLQy?usp=sharing). Make sure to replace the `<ip> <port>` with the server's details.