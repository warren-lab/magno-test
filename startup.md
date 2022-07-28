### Startup instructions for magnotether

- at any time, `rospack list` gives all ros packages


- roscore
- start pylon camera node <br> `roslaunch pylon_camera pylon_camera_node.launch`
- any time, you can see the output of camera <br> `rqt_image_view`

- align the position of the fly <br> `rosrun magno_test flyalign.py`

- launch led service <br> `roslaunch basic_led_strip_ros basic_led_strip.launch`

- to test lights <br> `rosrun basic_led_strip_ros test_service.py`

- enter name of fly (e.g., fly1) in launch file <br> 'shuffle_exp.launch` and save
- to start experiment with LEDs 
   <br> `roslaunch magno_test shuffle_exp.launch` <br><br>mag
- to start real-time plotiing
   <br> `cd python_packages/magno_analysis/real_time_plot_for_mag` <br><br>
   <br> `python3 mag_rt_plot.py` <br><br>
- to save graphs, just close real-time plot by clicking x button   
The above launch file starts file writing node, twyg_control.py, **AND** the led control node, RAND_LED_node.py
**Note that fly name is set in the launch file**
   <br> File-writing stops at end of experiment.
 
