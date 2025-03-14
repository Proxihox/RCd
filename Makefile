SRC_DIR=RCd
SRC_FILES=$(wildcard $(SRC_DIR)/*)

all : RC.out build

requirements: 
	pip install -r requirements.txt

RC.out : RCd/challenges/RC.cpp
	g++ -o RC.out  RCd/challenges/RC.cpp

build : RC.out Dockerfile $(SRC_FILES)
	echo "${SRC_FILES}"
	sudo docker build . -t proxihox/rcd:latest

