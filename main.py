import sys
from steerrobo import *

robot=steer(False)
def main():
    vx=0.0
    vy=0.0
    w=0.0
    while True:
        key=robot.returnkey()
        if key=="up":
            vy+=0.1
        elif key=="left":
            vx-=0.1
        elif key=="down":
            vy-=0.1
        elif key=="right":
            vx+=0.1
        elif key=="b":
            vx=vy=w=0.0
        elif key=="z":
            w+=0.01
        elif key=="x":
            w-=0.01
        elif key=="r":
            robot.reset()
        if robot.collision():
            vx=0.0
            vy=0.0
            w=0.0
        robot.resetkey()
        robot.move(vx,vy,w)
        robot.update()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
