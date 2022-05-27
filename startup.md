### Startup instructions for magnotether

- at any time, `rospack list` gives all ros packages


- roscore
- start pylon camera node <br> `roslaunch pylon_camera pylon_camera_node.launch`
- any time, you can see the output of camera <br> `rqt_image_view`
- launch led service <br> `roslaunch basic_led_strip_ros basic_led_strip.launch`

- to test lights <br> `rosrun basic_led_strip_ros test_service.py`

- to start experiment with LEDs <br>*First* `rosrun magno_test twyg_control.py` <br> *Second* `rosrun basic_led_strip_ros Rand_led_node.py`
 
