### Startup instructions for magnotether

- at any time, `rospack list` gives all ros packages


- roscore
- start pylon camera node <br> `roslaunch pylon_camera pylon_camera_node.launch`
- any time, you can see the output of camera <br> `rqt_image_view`
- launch led service <br> `roslaunch basic_led_strip_ros basic_led_strip.launch`

- to test lights <br> `rosrun basic_led_strip_ros test_service.py`

- to start experiment with LEDs 
   <br> `roslaunch magno_test shuffle_exp.launch` <br><br>
The above launch file starts file writing node, twyg_control.py, **AND** the led control node, RAND_LED_node.py
   <br> File-writing stops at end of experiment.
 
