import sys
import numpy as numpy
from math import radians
#from math import degrees
from math import atan2
from math import sin,cos
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
from matplotlib.transforms import Affine2D

class steer(object):
    def __init__(self):
        self.fig, self.ax = plt.subplots(1, 1)
        self.ax.set_aspect('equal')
        figsize=[3,3]
        self.ax.set_ylim((-figsize[1]//2,figsize[1]//2))
        self.ax.set_xlim((-figsize[0]//2,figsize[0]//2))
        self.fig.canvas.mpl_connect('key_press_event',self.press)
        self.x=0.0
        self.y=0.0
        self.yaw=0.0
        self.vx=0.0
        self.vy=0.0
        self.w=0.0
        self.size=0.2
        self.wheelangle=[0.0,0.0,0.0,0.0]
        self.wsize_w=0.01
        self.wsize_h=0.07
        self.wpos=0.1
        self.key=""
    def press(self,event):
        print('press', event.key)
        sys.stdout.flush()
        self.key=event.key
    def returnkey(self):
        return self.key
    def update(self):
        def relative_rectangle(w: float, h: float, center_tf, **kwargs):
            rect_origin_to_center = Affine2D().translate(w / 2, h / 2)
            return Rectangle(
                (0, 0), w, h, transform=rect_origin_to_center.inverted() + center_tf, **kwargs)

        to_body_center_tf = Affine2D().rotate(radians(self.yaw)).translate(self.x, self.y) + self.ax.transData
        body = relative_rectangle(self.size,self.size, to_body_center_tf, edgecolor='red',fill=False)

        body_center_to_left_front = Affine2D().rotate(self.wheelangle[0]).translate(-self.wpos, self.wpos)
        body_center_to_right_front = Affine2D().rotate(self.wheelangle[1]).translate(self.wpos, self.wpos)
        body_center_to_left_rear = Affine2D().rotate(self.wheelangle[2]).translate(-self.wpos, -self.wpos)
        body_center_to_right_rear = Affine2D().rotate(self.wheelangle[3]).translate(self.wpos, -self.wpos)

        left_front_wheel = relative_rectangle(
            self.wsize_w, self.wsize_h, body_center_to_left_front + to_body_center_tf,
            facecolor='black', edgecolor='black')
        right_front_wheel = relative_rectangle(
            self.wsize_w, self.wsize_h, body_center_to_right_front + to_body_center_tf,
            facecolor='black', edgecolor='black')
        left_rear_wheel = relative_rectangle(
            self.wsize_w, self.wsize_h, body_center_to_left_rear + to_body_center_tf,
            facecolor='black', edgecolor='black')
        right_rear_wheel = relative_rectangle(
            self.wsize_w, self.wsize_h, body_center_to_right_rear + to_body_center_tf,
            facecolor='black', edgecolor='black')
        #body = patches.Rectangle( xy=(self.x-self.size,self.y-self.size), angle=self.yaw, width=0.2, height=0.2, ec='#000000', fill=False)
        #wheel1 = patches.Rectangle( xy=(self.x+self.size-self.wp,self.y+self.size-self.wp), angle=self.yaw, width=0.01, height=0.07, ec='#000000', fill=False)
        #self.ax.add_patch(body)
        #self.ax.add_patch(wheel1)
        self.ax.add_patch(left_front_wheel)
        self.ax.add_patch(right_front_wheel)
        self.ax.add_patch(left_rear_wheel)
        self.ax.add_patch(right_rear_wheel)
        self.ax.add_patch(body)
        print("v({},{},{}),xy({},{}),yaw={},".format(self.vx,self.vy,self.w,self.x,self.y,self.yaw))
        plt.pause(0.01)
        body.remove()
        left_front_wheel.remove()
        right_front_wheel.remove()
        left_rear_wheel.remove()
        right_rear_wheel.remove()
    def move(self,vx,vy,w):
        self.wheelangle[0]=atan2(-vx+w*cos(self.yaw),vy-w*sin(self.yaw))#A
        self.wheelangle[1]=atan2(-vx-w*sin(self.yaw),vy-w*cos(self.yaw))#B
        self.wheelangle[2]=atan2(-vx-w*cos(self.yaw),vy+w*sin(self.yaw))#C
        self.wheelangle[3]=atan2(-vx+w*sin(self.yaw),vy+w*cos(self.yaw))#D
        self.x+=vx
        self.y+=vy
        self.yaw+=w
        self.vx=vx
        self.vy=vy
        self.w=w
