import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
import BlynkLib

BLYNK_TEMPLATE_ID = "TMPLjUtArN1v"
BLYNK_DEVICE_NAME = "IVP"
BLYNK_AUTH = "icLeCEHrb5DNB_uqb7OEsOqVBcZvtUY5"

dhtDevice = adafruit_dht.DHT11(board.D4)
Valve = 21
water = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(Valve, GPIO.IN)
GPIO.setup(water, GPIO.OUT)
blynk = BlynkLib.Blynk(BLYNK_AUTH)

blynk.run()
def callback(Valve): #วัดความชื้นในดิน
    if GPIO.input(Valve):
        print ("Wet")
        GPIO.output(water, GPIO.HIGH)
        blynk.virtual_write(0, "Wet") #++
    else:
        print ("Dry")
        GPIO.output(water, GPIO.LOW)
        blynk.virtual_write(0, "Dry") #++



while True:
    try:
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
        time.sleep(1.5)
        GPIO.add_event_detect(Valve, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
        GPIO.add_event_callback(Valve, callback)  # assign function to GPIO PIN, Run function on change
        blynk.virtual_write(1, temperature_c) 
        blynk.virtual_write(2, humidity)
        


    except RuntimeError as error:
        print("Error : {}".format(error.args[0]))
        time.sleep(2.0)
        continue
    except Exception as error:
        print("divce error")
        dhtDevice.exit()
        raise error
        time.sleep(2.0)