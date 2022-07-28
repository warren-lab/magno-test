# Using Catkin and Cloning to add Packages to ROS:
> Catkin is included when ROS is installed

## Build a Catkin Workspace:
link: [Build Catkin Workspace](http://wiki.ros.org/catkin/Tutorials/create_a_workspace)
link: https://classes.cs.uchicago.edu/archive/2021/spring/20600-1/computer_setup.html
additional link: https://wiki.nps.edu/display/RC/Setting+up+a+ROS+package+from+Git
1. Check to see if there is a Catkin workspace already built:

```
cd ~/catkin_ws
```
**If you are not immediately sent into the appropriate directory then issue the following commands:**
first:
```
source /opt/ros/noetic/setup.bash
```
second: now build the catkin workspace
```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/
catkin_make
```
third: now need to add `source catkin_ws/devel/setup.bash command to your ~/.bashrc file`
```
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
```
2. After the workspace has been created (DONT NEED TO DO FOLLOWING STEP):
http://wiki.ros.org/catkin/Tutorials/create_a_workspace
> if you are building ROS from source to achieve Python 3 compatibility, 
> and have setup your system appropriately
> (ie: have the Python 3 versions of all the required ROS Python packages installed, such as catkin)
> the first catkin_make command in a clean catkin workspace must be:
```
catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3
```
> This will configure catkin_make with Python 3. You may then proceed to use just catkin_make for subsequent builds.

3. Exit out of the terminal, and then open a new terminal and run the following:
```
roscd
```
4. The ouput of the above command should take you to ~/catkin_ws/devel. If this worked sucessfully and you are within the directory then proceed to step 5. 

If not then need to perform the following to change where roscd 
link: https://answers.ros.org/question/286880/how-to-make-roscd-go-to-catkin_wsdevel-instead-of-optroskinetic/

```
source devel/setup.bash
```

5.  With the `roscd` command able to direct you to `~/catkin_ws/devel` now enter the catkin workspaces' src folder and subsequently clone the repository in question to that folder.
    - Enter the folder:
    ``` 
    cd ~/catkin_ws/src 
    ```
    - clone the repository from Will Dickson (https://github.com/willdickson/basic_led_strip_ros)
    ```
    git clone https://github.com/willdickson/basic_led_strip_ros.git
    ```
6. Next...
```
cd ~/catkin_ws && catkin_make
```

7. Then...
```
source devel/setup.bash
```
8. Open a second terminal and run `roscd`
Do this to ensure that it will take you to 
`~/catkin_ws/devel`

9. In the first terminal run `roscore` this is so that the nodes will be able to communicate with one another:
link: [roscore] http://wiki.ros.org/roscore
```
roscore
```
10. In the second terminal run 
```
roslaunch basic_led_strip_ros basic_led_strip.launch 
```

11. This will likely produce errors:
    - **Python Version:** One error that can be fixed is the conversion of all the python files from python 2 to python3. Ros Noetic utilizes python3 so it is important that this is done.
        - a way that this can be accomplished is to use the python package `2to3` or the package `modernize` these packages both essentially perform the same function. Both methods will be explained below:   
            1. Python conversion using `2to3`
                - link: https://docs.python.org/3/library/2to3.html
                - link: https://www.geeksforgeeks.org/automate-the-conversion-from-python2-to-python3/
                ```
                pip install 2to3
                ```
                - to change the folder or file in question perform the following (important to note that the file or folder will be overwritten with the python3 
                version. 
                ```
                2to3 [file or folder] -w
                ```
            2. Python conversion `using modernize`:
                - link: https://pypi.org/project/modernize/
                ```
                sudo pip install modernize
                ```
                - with modernize the file in question will be rewritten to python3 but will have a version saved in pythoon2 
                ```
                python3 -m modernize -w [filename.py]
                ```

12. Test LED Connection:
    * Run the following command in a separate terminal window after the basic_led_strip_node has been launched.

    ```
    rosrun rosrun basic_led_strip_ros test_service.py
    ``` 
    * If no LED lights turn on then check the connections that were made back in the LED_Setup section. Reference the diagram as well to be sure that the wiring is appropriately configured. 

