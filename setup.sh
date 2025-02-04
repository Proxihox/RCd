#!/bin/bash
from RCd.src.users.User import key_generation
pip install -r requirements.txt
g++ -o RC.out  RCd/challenges/RC.cpp

key_generation()