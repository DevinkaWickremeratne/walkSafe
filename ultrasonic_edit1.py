#Libraries
import RPi.GPIO as GPIO
import time

#External Programs
import text_to_speech

#Disable Warnings for buzzer
GPIO.setwarnings(False)
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
buzzer = 23
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    distance = distance - 1
    
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            #if int(distance)>0 & int(distance)<400:
            dist = int(distance())
            #if int(dist)>0 & int(dist)<400:
            if int(dist)<10:
                print ("Measured Distance = %.1f cm" % dist)
                text_to_speech.robot("Warning")
                GPIO.output(buzzer,GPIO.HIGH)
                time.sleep(2)
            else:
                GPIO.output(buzzer,GPIO.LOW)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
