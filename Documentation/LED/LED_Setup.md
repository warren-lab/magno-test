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

#### Wiring:
* Materials:
  - Arduino uno or nano (https://store.arduino.cc/products/arduino-nano), (https://store-usa.arduino.cc/products/arduino-uno-rev3)
  - (ONLY FOR NANO) Screw Terminal Block for Nano (https://www.amazon.com/Aideepen-Terminal-Adapter-Expansion-ATMEGA328P-AU/dp/B0788MLRLK)
  - Jumper Wires (https://www.amazon.com/Elegoo-EL-CP-004-Multicolored-Breadboard-arduino/dp/B01EV70C78/ref=asc_df_B01EV70C78/?tag=hyprod-20&linkCode=df0&hvadid=222785939698&hvpos=&hvnetw=g&hvrand=12115955240910686715&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1024429&hvtargid=pla-362913641420&psc=1)
  - 1000 uF Capacitor (x1)
  - 470 ohm resistor (x1)
  - 5v 4amp power supply (https://www.amazon.com/5V-4000mA-switching-power-supply/dp/B01LY5TG5Y)
  - Jack to Screw terminal (for power supply) (https://www.digikey.com/en/products/detail/adafruit-industries-llc/368/5629434?utm_adgroup=Between%20Series%20Adapters&utm_source=google&utm_medium=cpc&utm_campaign=Shopping_Product_Connectors%2C%20Interconnects_NEW&utm_term=&utm_content=Between%20Series%20Adapters&gclid=Cj0KCQjw54iXBhCXARIsADWpsG9f1iGym2a9CS0VJY9Z8mUTLBP1-xZxIeuRASX4WO97f7HP8PMQRD8aAsv6EALw_wcB)

* Equipment:
  - Heat Gun
  - Soldering Iron etc.
  - Wire Strippers (20-30 AWG)

* See the Magnotether Diagram which indicates how the wiring should be performed. Soldering will need to be performed between the 
exposed wires of the LED NeoPixel and the new wire connecting it to the necessary path.

#### Powering Device and LED Strip:
* First, with the proper data cable for the arduino device attach that. Then run any necessary test blink sketches to make sure that the port is connected.

* Next, take the 5v 4amp power supply and plug it into the 2.1mm jack.

* Both the Arduino and the LEDs have power at this point.

#### Uploading to Device
> Now proceed to upload the sketch to the device

#### Troubleshooting Post-Install
###### Issue 1 : Greyed out Port
> Resources:
* https://askubuntu.com/questions/979170/arduino-ide-port-in-the-tool-is-greyed#:~:text=Solution%20%3A%20Grant%20permissions%20to%20read,is%20busy%20or%20already%20occupied.
* 
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


## Incorporating ROS:
> After successfully uploading the arduino sketch without any errors the ROS installation process should be performed. This will enable the ROS python scripts to communicate with the device and set certain LED's on and or off.
> If wanting to keep your python packages organized to avoid any issues between dependencies you could create a virtual environment. However, if your
machine is going to be solely utilized for Magnotether experiments then it is not necessary.
 
