# Magnothether/BeeCam: Ring Lighting 
> This provides the entire documentation for installing and using the basic_led_strip library. 

## Helpful resources
> Arduino Installation on Linux Machine:
  * https://www.arduino.cc/en/Guide/Linux
  * https://ubuntu.com/tutorials/install-the-arduino-ide#1-overview
> Neopixel and Electronic Connections:
  * https://www.adafruit.com/product/3857?gclid=Cj0KCQiAgomBBhDXARIsAFNyUqOgMrLUboSAHr7kuYhoaguMZLZzfDgrJPi6Cy4hgADsPMzcwCge4mQaAiI2EALw_wcB
  * https://circuitpython.readthedocs.io/projects/neopixel/en/latest/
  * https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel
#### Initial Installation
> See the below site to install the latest version of Arduino for linux
  * https://www.arduino.cc/en/Guide/Linux
 
> After installing, open the terminal, and run the following command to convert from the zip

> ```tar xvf <FILENAME'>```

> After which point go into the newly created unzipped folder and run the following command:

> ```sudo ./install.sh```
  * Try first without running sudo, but if that doesn't work then implement the sudo command

> Now the application should install, and try initially running the application by writing:

> ```Arduino```

> The application is now open, attempt to connect your device by going to ```tools -> Board -> Board Manager``` and installing the necessary boards to the IDE. Then plug your device in, and select the appropriate board that represents it.

> Next connect to the device going to ```Tools -> Board -> Port``` and select the Port which your device is connected to.
 * NOTE: YOUR PORT MIGHT NOT DISPLAY YOUR DEVICE NAME....IF THIS IS THE CASE TRY ALL THE DIFFERENT PORT OPTIONS AVAILABLE UNTIL ONE WORKS FOR YOUR DEVICE

#### Arduino Library Installation
> First download the zip file with all relevant code and information from (https://github.com/willdickson/basic_led_strip/tree/master/software/python/basic_led_strip)

> Referring to this page the appropriate libraries will need to be installed. This can be done by either manually searching and determining which ones you need to add to your IDE, or by connecting your device and running frimware.ino. By running this file errors will produce indicating un what files you may be a library that you have not yet installed. 

> Some of the primary libraries will be:
 * Adafruit NeoMatrix
 * Adafruit NeoPixel
 * AdruinoJSON
 * Array
 * Streaming

> Other libraries may be required but these are the primary ones.

#### Uploading to Device
> Now proceed to upload to the device

#### Troubleshooting Post-Install
###### Issue 1 : Greyed out Port
> Resources:

###### Issue 2: ser_open: can't open device: Permission denied
> Resources:
 * https://support.arduino.cc/hc/en-us/articles/360016495679-avrdude-ser-open-can-t-open-device-Permission-denied-Linux-
 * https://forum.arduino.cc/t/permission-denied-on-dev-ttyacm0/475568
>  There are two methods to remedy this issue
* Method 1
  * Check the port under ```Tools -> Port```
  * If you are connected to the correct port then next open up a terminal and issue the following command:
  *      sudo usermod -a -G dialout <username> 
  * Then logout and log back in after this command has been issued
  * Try running a basic blick test, if you continue to get the same error then proceed with the next steps
  * Open a new terminal and enter the following command:
  *      ls -l <port> <- where <port> is the port path ex: /dev/ttyUSB0
  * You should get an output that looks like the following:
  *      crw-rw---- 1 <user> <group> 188, 0 5 apr 23.01 <port>
  * Finally add in your username, and the group name that was listed into the following command:
  *      sudo usermod -a -G <group> <username>
  * Again try and running a blink sketch, if the same error appears then proceed to method 2
 
* Method 2
  *  Run the following command:
  *     sudo chmod a+rw /dev/ttyUSB0
  * One of these methods should remedy this error

 


 
###### Issue 3: StaticJsonBuffer is a class from ArduinoJson 5. Please see ///// to learn how to upgrade your program to ArduinoJson version 6
> This error implies that we need to downgrade the current version to 5.13.4. This should fix this error, but refer to the produced link if it does not


## Incorporating Python Scripting
> Now the python scripts that will be used to communicate to the microcontroller can be utililzed in parallel with the already developed 

> The name of the virtual environment created was dubbed ```MagnoBee```
 
