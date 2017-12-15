#!/usr/bin/env python
# Based on Dexter Industries line_follow1.py file
# CC-BY-NC-SA4.0
# Michael Palmateer, Shantelle Lanthrip, Anthony Disotell, Omari Fabor

from __future__ import print_function
from __future__ import division
from builtins import input

# the above lines are meant for Python3 compatibility.
# they force the use of Python3 functionality for print(), 
# the integer division and input()
# mind your parentheses!
import line_sensor
import time
import atexit
import gopigo
import signal
import sys
from gopigo import *

#Calibrate speed at first run
#100 is good with fresh batteries 
#125 for batteries with half capacity

fwd_speed = 35                         # Forward speed at which the GoPiGo should run.                                                         # If you're swinging too hard around your line
                                                        # reduce this speed.
poll_time=0.01                                          # Time between polling the sensor, seconds.
                                                         
slight_turn_speed=int(.6*fwd_speed)
fast_turn_speed=int(.3*fwd_speed)
turn_speed=int(.8*fwd_speed)

last_val=[0]*5                                          # An array to keep track of the previous values.
curr=[0]*5                                              # An array to keep track of the current values.

gopigo.set_speed(fwd_speed)

distance_to_stop=5
dist=us_dist(15)

gpg_en=1                                                        #Enable/disable gopigo
msg_en=1                                                       #Enable messages on screen.  Turn this off if you don't want messages.

#Get line parameters
line_pos=[0]*5
white_line=line_sensor.get_white_line()
black_line=line_sensor.get_black_line()
range_sensor= line_sensor.get_range()
threshold=[a+b/2 for a,b in zip(white_line,range_sensor)]       # Make an iterator that aggregates elements from each of the iterables.

#Positions to take action on
mid     =[0,0,1,0,0]    # Middle Position.
small_r =[0,1,1,0,0]    # Slightly to the right.
small_r1=[0,1,0,0,0]    # Slightly to the right.
small_l =[0,0,1,1,0]    # Slightly to the left.
small_l1=[0,0,0,1,0]    # Slightly to the left.


inter  =[1,1,1,1,1]    # Sensor reads intersection
turn_a  =[0,0,0,0,0]

                        
stop2   =[1,0,0,0,1]    # Sensor reads stop.
large_r2   =[1,0,0,0,0]
large_l2   =[0,0,0,0,1]

right0 = [1,1,1,1,0]
right1 = [1,1,1,0,0]

left0 = [0,0,1,1,1]
left1 = [0,1,1,1,1]

class IntersectionCounter:
    right_turns = 0
    left_turns = 0
    turn = 0
    total_turns = 0

    def left_turn(self):
        if self.left_turn == 0:
            self.turn = (self.turn / 2)
        elif self.left_turn == 1:
            self.turn = (self.turn - 1) #left turn inludes a turn around so we need to subtract it
            self.turn = (self.turn / 2) #we divide by two b/c the rover tech goes twice
        elif self.left_turn == 2:
            self.turn = ((self.turn - 2) / 2) #for the second turn left
        else:
            print("ERROR")

    def total_turn(self):
        #Calculating the total number of intersections by
        #adding the turn arounds and right turn
        self.total_turns = self.turn + self.right_turns
        #This was just checking to make sure the values were correct
        print('The rover turned {} times'.format(self.total_turns))

    def full_map(self):
        #Statement to know where rover is - hard coded. Must start the rover from the
        #same location every time for this to make sense.
        if self.total_turns == 0:
            print("Obstacle detected between nodes [1,2]") #(right_num=1)
        elif self.total_turns == 1:
            print("Obstacle detected between nodes [2, 3]") #(right_num=1, turn_num=2)
        elif self.total_turns == 3:
            print("Obstacle detected between nodes [3, 2] - ERROR")#(right_num=2, turn_num=2)--->(Shouldn't occur)
        elif self.total_turns == 4:
            print("Obstacle detected between nodes [2, 4]")#(right_num=3, turn_num=2)
        elif self.total_turns == 5:
            print("Obstacle detected between nodes [4, 5]")#(right_num=3, turn_num=4)
        elif self.total_turns == 7:
            print("Obstacle detected between nodes [5, 4] - ERROR")#(right_num=4, turn_num=4)
        elif self.total_turns == 8:
            print("Obstacle detected between nodes [4, 6]")#(right_num=4, turn_num=6)
        elif self.total_turns == 10:
            print("Obstacle detected between nodes [6, 4] - ERROR")#(right_num=5, turn_num=6)
        elif self.total_turns == 11:
            print("Obstacle detected between nodes [4, 7]")#(right_num=6, turn_num=6)
        elif self.total_turns == 12:
            print("Obstacle detected between nodes [7, 8]")#(right_num=7, turn_num=6)
        elif self.total_turns == 14:
            print("Obstacle detected between nodes [8, 7] - ERROR")#(right_num=7, turn_num=8)
        elif self.total_turns == 15:
            print("Obstacle detected between nodes [7, 9]")#(right_num=8, turn_num=8)
        elif self.total_turns == 16:
            print("Obstacle detected between nodes [9, 10]")#(right_num=9, turn_num=8)
        elif self.total_turns == 17:
            print("Obstacle detected between nodes [10, 11]")#(right_num=9, turn_num=10)
        elif self.total_turns == 19:
            print("Obstacle detected between nodes [11, 12]")#(right_num=9, turn_num=12)
        elif self.total_turns == 21:
            print("Obstacle detected between nodes [12, 13] - ERROR")#(right_num=10, turn_num=12)
        elif self.total_turns == 22:
            print("Obstacle detected between nodes [13, 14]")#(right_num=11, turn_num=12)
        elif self.total_turns == 23:
            print("Obstacle detected between nodes [14, 15]")#(right_num=12, turn_num=13, left_num=1)
        elif self.total_turns == 24:
            print("Obstacle detected between nodes [15, 16]")#(right_num=12, turn_num=15, left_num=1)
        elif self.total_turns == 26:
            print("Obstacle detected between nodes [16, 15] - ERROR")#(right_num=13, turn_num=15, left_num=1)
        elif self.total_turns == 27:
            print("Obstacle detected between nodes [15, 17]")#(right_num=13, turn_num=17, left_num=1)
        elif self.total_turns == 29:
            print("Obstacle detected between nodes [17, 15]")#(right_num=14, turn_num=17, left_num=1)
        elif self.total_turns == 30:
            print("Obstacle detected between nodes [15, 18]")#(right_num=15, turn_num=18, left_num=2)
        elif self.total_turns == 31:
            print("Obstacle detected between nodes [18, 19]")#(right_num=16, turn_num=18, left_num=2)
        elif self.total_turns == 32:
            print("Obstacle detected between nodes [19, 20]")#(right_num=17, turn_num=18, left_num=2)
        elif self.total_turns == 34:
            print("No obstacles detected")

ic = IntersectionCounter()

#Converts the raw values to absolute 0 and 1 depending on the threshold set
def absolute_line_pos():
        raw_vals=line_sensor.get_sensorval()
        for i in range(5):
                if raw_vals[i]>threshold[i]:
                        line_pos[i]=1
                else:
                        line_pos[i]=0
        return line_pos
        
#GoPiGo actions

def go_straight():
        if msg_en:
                print("Going straight")
        if gpg_en:
                gopigo.set_speed(fwd_speed)
                gopigo.fwd()
        
def turn_slight_left():
        if msg_en:
                print("Turn slight left")
        if gpg_en:
                gopigo.set_right_speed(slight_turn_speed)
                gopigo.set_left_speed(fwd_speed)
                gopigo.fwd()

def turn_fast_left():
        if msg_en:
                print("Turn fast left")
        if gpg_en:
                gopigo.set_right_speed(fast_turn_speed)
                gopigo.set_left_speed(fwd_speed)
                gopigo.fwd()
                
def turn_slight_right():
        if msg_en:
                print("Turn slight right")
        if gpg_en:
                gopigo.set_right_speed(fwd_speed)
                gopigo.set_left_speed(slight_turn_speed)
                gopigo.fwd()
                
def turn_fast_right():
        if msg_en:
                print("Turn fast left")
        if gpg_en:
                gopigo.set_right_speed(fast_turn_speed)
                gopigo.set_left_speed(fwd_speed)
                gopigo.fwd()
        
def stop_now():
        if msg_en:
                print("Stop")
        if gpg_en:
                gopigo.stop()
        
def go_back():
        if msg_en:
                print("Go Back")
        if gpg_en:
                gopigo.set_speed(turn_speed)
                gopigo.bwd()

def turn_right():
    if msg_en:
        print("Turn right")
    if gpg_en:
        gopigo.enc_tgt(0,1,15)
        gopigo.fwd()
        time.sleep(.9)
        gopigo.stop()
        time.sleep(1)
        gopigo.set_speed(80)
        gopigo.enc_tgt(1,1,35)
        gopigo.right_rot()
        time.sleep(.7)
        gopigo.stop()
        time.sleep(1)
        curr = absolute_line_pos()
        ic.right_turns += 1

def turn_left():
    if msg_en:
        print("Turn left")
    if gpg_en:
        gopigo.enc_tgt(0,1,6)
        gopigo.fwd()
        time.sleep(1.1)
        curr = absolute_line_pos()
        
def turn_around():
        if msg_en:
                print("Turn around")
                
        if gpg_en:
                gopigo.bwd()
                curr = absolute_line_pos()
                gopigo.enc_tgt(0,1,5)
                gopigo.stop()
                time.sleep(.5)
                gopigo.set_speed(80)
                gopigo.enc_tgt(1,1,35)
                gopigo.left_rot()
                time.sleep(.7)
                gopigo.stop()
                time.sleep(1)
                curr = absolute_line_pos()
                ic.turn += 1

def stop_final(signal, frame):
    gopigo.stop()
    ic.total_turn()
    sys.exit(0)

signal.signal(signal.SIGINT, stop_final)

              
#Action to run when a line is detected
def run_gpg(curr):

        while True:
                atexit.register(gopigo.stop)
                dist = us_dist(15)
                last_val = curr
                curr = absolute_line_pos()

                #If an obstacle is detected, turn around
                #print("Dist:",dist,'cm')
                if dist<distance_to_stop:
                        print("Stopping")
                        gopigo.stop()
                        ic.total_turn()
                        ic.full_map()
                        sys.exit()
                
                #if the line is in the middle, keep moving straight
                #if the line is slightly left of right, keep moving straight
                elif curr==mid:
                        go_straight()
                
        #If the line is towards the slight left, turn slight right
                elif curr==small_l or curr==small_l1:
                        turn_slight_right()
                        
        #If the line is towards the large left, turn large right
                elif curr==large_l2:
                        turn_fast_right()
                
        #If the line is towards the slight right, turn slight left
                elif curr==small_r or curr==small_r1:
                        turn_slight_left()

        #If the line is towards the large right, turn large left
                elif curr==large_r2:
                        turn_fast_left()

        #If the line is right or an intersection is detected, turn right
                elif curr == right0 or curr == right1 or curr == inter:
                        turn_right()
               
        #If the line is left, turn left
                elif curr == left0 or curr == left1:
                        turn_left()

        #If a dead end is detected, turn around
                elif curr == turn_a:
                        turn_around()

                else:
                        curr == absolute_line_pos()
                
while True:
        last_val=curr
        curr=absolute_line_pos()
        print(curr)
        run_gpg(curr)
        
        #white line reached
        if curr== stop2:
                if msg_en:
                        print("White found, last cmd running")
                for i in range(5):
                        run_gpg(last_val)
        else:
                run_gpg(curr)
