# You can achieve this using Python's serial-asyncio package. 
# I'm assuming your sensor data is coming in as strings and you just want to read it as such. 
# You'll need to install serial-asyncio if you haven't already by running pip install pyserial-asyncio.
# Here's a basic script that should accomplish what you're asking:


import asyncio
import serial_asyncio
import time

class Sensor1Protocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.start_time = None

    def data_received(self, data):
        if self.start_time is not None:
            elapsed = (time.time() - self.start_time) * 1000  # convert to milliseconds
            print(f'Sensor1 data: {data.decode()}, Elapsed time: {elapsed} ms')

class Sensor2Protocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.start_time = None

    def data_received(self, data):
        if self.start_time is None:
            self.start_time = time.time()
            sensor1.start_time = self.start_time
        elapsed = (time.time() - self.start_time) * 1000  # convert to milliseconds
        print(f'Sensor2 data: {data.decode()}, Elapsed time: {elapsed} ms')

async def main():
    global sensor1
    loop = asyncio.get_event_loop()

    _, sensor1 = await serial_asyncio.create_serial_connection(loop, Sensor1Protocol, '/dev/ttyUSB0', baudrate=9600)
    _, sensor2 = await serial_asyncio.create_serial_connection(loop, Sensor2Protocol, '/dev/ttyUSB1', baudrate=115200)

    await asyncio.sleep(4)
    sensor1.transport.close()
    sensor2.transport.close()

sensor1 = None
asyncio.run(main())

# This script will open connections to two serial ports, 
# /dev/ttyUSB0 for Sensor 1 and /dev/ttyUSB1 for Sensor 2 with the specified baud rates. 
# It will start to print data as it's received from the sensors, along with the elapsed time since data first arrived from Sensor 2. 
# After 4 seconds, it will close the connections to the sensors.

# Please note that the asyncio.run(main()) requires Python 3.7 and above. 
# If you are using an older version, you may need to get an event loop with asyncio.get_event_loop(), 
# create a task with loop.create_task(main()) and run the event loop with loop.run_forever(). 
# If you encounter any issues with the above code, please provide more details about your sensors and how they send data, 
# so I can give you a more accurate answer.


#----------
# dibawah ini kalo pake Bing
#----------
# Sure, here is a simple Python script that does what you described. 
# This script uses the serial_asyncio and asyncio libraries to communicate with the two sensors. 
# It uses asyncio tasks to read data from both sensors in an asynchronous manner.

# The script keeps track of the time elapsed since the first data is received from the second sensor. 
# It performs data acquisition for 4 seconds after that point, regardless of whether or not data is received from the first sensor.

import asyncio
import serial_asyncio
import time

class Sensor:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.data = None
        self.start_time = None

async def acquire_data(sensor):
    reader, writer = await serial_asyncio.open_serial_connection(url=sensor.port, baudrate=sensor.baudrate)

    while True:
        line = await reader.readline()
        sensor.data = line.decode().strip()
        if sensor.start_time is None:
            sensor.start_time = time.time()
        elapsed_time = (time.time() - sensor.start_time) * 1000  # in milliseconds
        print(f"Sensor on {sensor.port}: {sensor.data}, Elapsed Time: {elapsed_time} ms")

        if sensor.port == 'dev/ttyUSB1' and elapsed_time > 4000:  # 4 seconds have passed
            break

    writer.close()
    await writer.wait_closed()

async def main():
    sensor1 = Sensor('dev/ttyUSB0', 9600)
    sensor2 = Sensor('dev/ttyUSB1', 115200)

    while sensor2.data is None:  # wait until there is data in sensor2
        await asyncio.sleep(0.1)

    await asyncio.gather(
        acquire_data(sensor1),
        acquire_data(sensor2),
    )

if __name__ == '__main__':
    asyncio.run(main())

# This script will continuously read data from both sensors, 
# print the data and the elapsed time since the first reading from each sensor. 
# The acquisition will stop 4 seconds after the first data is received from sensor2.

# Please note that the serial_asyncio module is not a standard library module 
# and must be installed separately using pip:

pip install pyserial-asyncio

# Also, please replace 'dev/ttyUSB0' and 'dev/ttyUSB1' with the actual serial port addresses of your sensors.
# Lastly, please note that you'll need Python 3.7 or later to run this script as it uses the asyncio.run() function which was added in Python 3.7.