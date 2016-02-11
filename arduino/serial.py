import serial
import time #remove this once the arduino has been tested with a single led

serialCom = serial.Serial('dev/ttyUSB0')
print(serialCom.name)

while True:
	serialCom.write("PWR9-COM9-COD9-SBY9-AUX0")
	time.sleep(5)
	serialCom.write("PWR0-COM9-COD9-SBY9-AUX0")
	time.sleep(5)

serialCom.close()