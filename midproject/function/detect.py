#Libraries
import RPi.GPIO as gpio
import time

class HumanDetect:
    def __init__(self, PIN):
        gpio.setmode(gpio.BOARD)
        gpio.setup(PIN, gpio.IN, pull_up_down=gpio.PUD_UP)
        self.detect = False
        self.PIN = PIN
        self.gpio = gpio

    def action(self, channel):
        print ("Motion detected")
        self.gpio.cleanup()
        self.detect = True

    def setDetect(self):
        try:
            self.gpio.add_event_detect(self.PIN, gpio.RISING, callback=self.action, bouncetime=200)
        except:
            self.gpio.cleanup()

    def isActive(self):
        return self.detect

class ConfirmDetect:

    def __init__(self, TRIGGER, ECHO):
        #GPIO Mode (BOARD / BCM)
        gpio.setmode(gpio.BCM)
        #set GPIO direction (IN / OUT)
        gpio.setup(TRIGGER, gpio.OUT)
        gpio.setup(ECHO, gpio.IN)
        self.gpio = gpio
        self.TRIGGER = TRIGGER
        self.ECHO = ECHO

    def distance(self):
        # set Trigger to HIGH
        self.gpio.output(self.TRIGGER, True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        self.gpio.output(self.TRIGGER, False)

        start_time = time.time()
        stop_time = time.time()

        # save start_time
        while self.gpio.input(self.ECHO) == 0:
            start_time = time.time()

        # save time of arrival
        while self.gpio.input(self.ECHO) == 1:
            stop_time = time.time()

        # time difference between start and arrival
        time_elapsed = stop_time - start_time
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (time_elapsed * 34300) / 2
        return distance

    def end(self):
        self.gpio.cleanup()
