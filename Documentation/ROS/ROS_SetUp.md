# Guide to Setting up ROS for Ubuntu 20.04
> This guide will walk through the set up procedure for how to Set Up ROS on a machine using Ubuntu 20.04 LTS


## Install ROS Noetic:
Links for installation: 

Source 1: [How to Install ROS Noetic on Ubuntu 20.04 LTS](https://linoxide.com/how-to-install-ros-noetic-on-ubuntu-20-04/`) 

Source 2: [How To Install ROS Noetic on Ubuntu 20.04 LTS](https://idroot.us/install-ros-noetic-ubuntu-20-04/)

1. Update System Packages:
```
sudo apt update
```

update system if there is a new LTS version of Ubuntu
```
sudo apt upgrade
```
2. Add the ROS Noetic Repo to system
```
echo "deb http://packages.ros.org/ros/ubuntu focal main" | sudo tee /etc/apt/sources.list.d/ros-focal.list
```
3. Add the ROS keyring:
```
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
```

4. Update the system so ROS Noetic package info can be obtained from the repo

```
sudo apt update
```
5. Install the Ros Metapackage 
> Intall **ros-noetic-desktop-full**
> This package comes with all the packages in ros-noetic desktop, and also ros-noetic-perception and ros-noetic-simualtors packages
```
sudo apt install ros-noetic-desktop-full
```

6. Set up of Environment Variables
> This allows ROS to function
```
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc

```
verify this with:
```
tail ~/.bashrc
```
**output:**
```
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
source /opt/ros/noetic/setup.bash
```
Run the next command:

```
source ~/.bashrc
```
7. Check Installation
```
roscd
```
The above command changes the current directory. To further test the installation run **roscore** 

```
roscore
```

**output:**
```
SUMMARY
========

PARAMETERS
 * /rosdistro: noetic
 * /rosversion: 1.15.14

NODES

auto-starting new master
process[master]: started with pid [162314]
ROS_MASTER_URI=http://flyranch-OptiPlex-7080:11311/

setting /run_id to a8375ae0-904d-11ec-814f-0d913dcb71c8
process[rosout-1]: started with pid [162343]
started core service [/rosout]

```
