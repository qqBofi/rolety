import board
import digitalio
import time


class shade:
    def __init__(self, name, inL, inR, outL, outR):
        self.name = name
        # input pins
        self.inL = digitalio.DigitalInOut(inL)
        self.inR = digitalio.DigitalInOut(inR)
        self.inL.direction = digitalio.Direction.INPUT
        self.inR.direction = digitalio.Direction.INPUT
        #self.inL.pull = digitalio.Pull.DOWN
        #self.inR.pull = digitalio.Pull.DOWN
        self.inL.pull = digitalio.Pull.UP
        self.inR.pull = digitalio.Pull.UP
        # output pins
        self.outL = digitalio.DigitalInOut(outL)
        self.outR = digitalio.DigitalInOut(outR)
        self.outL.direction = digitalio.Direction.OUTPUT
        self.outR.direction = digitalio.Direction.OUTPUT
        # rele ON if in grounded
        self.outL.value = True
        self.outR.value = True
        # how many seconds to open
        # 0 = closed, 26sec = open
        self.real = 0
        self.desired = 0
        self.isClosed = 0
        self.isOpen = 26
        self.gapSize = 3
        self.state = ""
        self.previousL = False
        self.previousR = False
        self.smallGap = False

    def yn(self, b):
        if b:
            r = "1"
        else:
            r = "0"
        return r

    def outstr(self):
        r = "{} {} {}/{} | in {}/{} | out {}/{}".format(
            self.name,
            self.state,
            self.real,
            self.desired,
            self.yn(self.inL.value),
            self.yn(self.inR.value),
            self.yn(self.outL.value),
            self.yn(self.outR.value),
        )
        return r

    def outhtm(self):
        r = "<tr><td>{}</td><td>{} {}/{}</td><td>{}/{}</td><td>{}/{}</td></tr>".format(
            self.name,
            self.state,
            self.real,
            self.desired,
            self.yn(self.inL.value),
            self.yn(self.inR.value),
            self.yn(self.outL.value),
            self.yn(self.outR.value),
        )
        return r

    def shadeReset(self,rValue):
        if rValue == "isopen":
            self.real = self.isOpen
        if rValue == "isclosed":
            self.real = self.isClosed
        self.desired = self.real

    def shadeStop(self):
        self.state = "STOP"
        self.desired = self.real
        self.outL.value = True
        self.outR.value = True

    def shadeOpen(self):
        if self.state == "STOP":
            self.state = "OPEN"
            self.desired = self.isOpen
        else:
            self.shadeStop()

    def shadeClose(self):
        if self.state == "STOP":
            self.state = "CLOSE"
            self.desired = self.isClosed
        else:
            self.shadeStop()

    def shadeSmallGap(self):
        self.smallGap = True
        self.shadeClose()

    def shadeStat(self):
        # for debug
        print("shade {}: inL {} inR {}".format(self.name, self.inL.value, self.inR.value))

    def shadeMove(self):
        # self.shadeStat()
        if self.state == "STOP" and not(self.inL.value):
            self.shadeOpen()
        elif self.state == "OPEN" and not(self.inL.value) and (self.previousL):
                self.shadeStop()
        if self.state == "STOP" and not(self.inR.value):
            self.shadeClose()
        elif self.state == "CLOSE" and not(self.inR.value) and (self.previousR):
            self.shadeStop()

        # if close already closed, try to move more down
        if self.real == 0 and not(self.inR.value):
            self.real = 2

        if self.real < self.desired:
            # if it was moving opposite direction
            # then turn off movement and wait not to kill motor
            if self.outR.value:
                self.outR.value = not(False)
                time.sleep(0.5)
            self.outL.value = not(True)
            self.real = self.real + 1
        if self.real > self.desired:
            if self.outL.value:
                self.outL.value = not(False)
                time.sleep(0.5)
            self.outL.value = not(False)
            self.outR.value = not(True)
            self.real = self.real - 1
        if self.real == self.desired:
            self.shadeStop()
        self.previousL = self.inL.value
        self.previousR = self.inR.value
        if self.smallGap and self.real == 0:
            self.desired = self.gapSize
            self.smallGap = False
        # cannot have both relays open (grounded IN)
        if not(self.outL.value) and not(self.outR.value):
            self.shadeStop()

''' for non PULUP
    def shadeMove(self):
        self.shadeStat()
        if self.state == "STOP" and self.inL.value:
            self.shadeOpen()
        elif self.state == "OPEN" and self.inL.value and not(self.previousL):
                self.shadeStop()
        if self.state == "STOP" and self.inR.value:
            self.shadeClose()
        elif self.state == "CLOSE" and self.inR.value and not(self.previousR):
            self.shadeStop()

        # if close already closed, try to move more down
        if self.real == 0 and self.inR.value:
            self.real = 2

        if self.real < self.desired:
            # if it was moving opposite direction
            # then turn off movement and wait not to kill motor
            if self.outR.value:
                self.outR.value = not(False)
                time.sleep(0.5)
            self.outL.value = not(True)
            self.real = self.real + 1
        if self.real > self.desired:
            if self.outL.value:
                self.outL.value = not(False)
                time.sleep(0.5)
            self.outL.value = not(False)
            self.outR.value = not(True)
            self.real = self.real - 1
        if self.real == self.desired:
            self.shadeStop()
        self.previousL = self.inL.value
        self.previousR = self.inR.value
        if self.smallGap and self.real == 0:
            self.desired = self.gapSize
            self.smallGap = False
        # cannot have both relays open (grounded IN)
        if not(self.outL.value) and not(self.outR.value):
            self.shadeStop()
'''
