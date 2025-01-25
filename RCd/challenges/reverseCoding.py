import sys
def start():
    state = 0
    while(True):
        s = input().strip()
        if(s == "-1"):
            state = 0
            print("Main Menu")
        elif(state == 0):
            state = int(s)
            print("Entered problem ",s)
        elif(state == 1):
            a,b = map(int,s.split(' '))
            print(a+b)
        else:
            a,b = map(int,s.split(' '))
            print(a*b)

start()
        