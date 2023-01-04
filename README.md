## mars_rover_project
For at least three decades, scientists have advocated the return of geological samples from Mars. One early concept was the Sample Collection for Investigation of Mars (SCIM) proposal, which involved sending a spacecraft in a grazing pass through Mars's upper atmosphere to collect dust and air samples without landing or orbiting.


As of late 1999, the MSR mission was anticipated to be launched from Earth in 2003 and 2005. Each was to deliver a rover and a Mars ascent vehicle, and a French supplied Mars orbiter with Earth return capability was to be included in 2005. Sample containers orbited by both MAVs were to reach Earth in 2008. This mission concept, considered by NASA's Mars Exploration Program to return samples by 2008, was cancelled following a program review


In this project, we did a computer vision for robotics. We are going to build a Sample & Return Rover in simulation. Mainly, we’ll control the robot from images streamed from a camera mounted on the robot. The project aims to do  -- autonomous mapping and navigation given an initial map of the environment -- . Realistically speaking, the hard work is done now that you have the mapping component! You will have theoption to choose whether to send orders like the throttle, brake, and steering with each new image the rover's camera produces.       ![image](https://user-images.githubusercontent.com/105971383/210525288-5db9d1ad-a93d-40f7-827e-98c179b5f086.png)


## Phase 1 – Basic Operation:
we inserted the image at the bottom right when we're running in autonomous mode is packed with information. 
In this image, our map of -navigable terrain-, -obstacles- and -rock sample locations- is overplotted with the ground truth map. In addition, some overall statistics are presented
we mapped 40% of the environment at 97% -- 100% fidelity and located at least four rocks samples.

## Run the Code

To run the automated code included in this repository:
* Activate the conda environment with `source activate envName'
* Run `python ./code/drive_rover.py` to start the automation logic (this communicates with the simulator directly)
* Start the simulator (double click `Roversim.x86_64`) and choose "Autonomous Mode."

## Notebook Analysis
This [Jupyter Notebook]([./code/Rover_Project_Test_Notebook.ipynb](https://github.com/Renal-Tarek/mars_rover_project/blob/main/final_notebook.ipynb)) includes all of the major functions, which are broken out into individual sections as follows:

## Color Thresholding for the navigalbe terrain:
This function which takes the original image or the bird eye image to extract the information of the road and apply a threshold on it, where the value that above the 160 is suitable for the road and  make it white  While the value below the 160 is black.

## Color Thresholding for the obstacles:
This function which takes the original image or the bird eye image to extract the  information of the obstacles (mountains and the big rocks) and apply a threshold on it, where the value that above the 160 is suitable for the obstacles and make it white While  the value below the 160 is black.

## Color Thresholding for the rocks:
This function which take the bird view of the original image and apply hsv that convert the image  from RGB to HSV to trace the yellow rock , then using inRange function to check if the image  has a rock that has a colour allocate between the upper and lower limit , if the object has a colour  in the range then we make a mask that is a binary image of the extraction of the rock then return i.

## Perspective Transformation, and Rover-centric Coordinates:
Convert the binary image to have rover centric coordinates by translating it so that 
the base of the identified area is at (0, 0). The rover's x axis represents the front of  the rover.
:param binary_img: Numpy 2d array (x, y) of the binary image
:return: Tuple of Numpy 1d float arrays of the x and y pixels after the original pixels have been translated.

## World Coordinates and make a video from processed image data
In order to fill out the world map, the image's rover-centric coordinates must be transformed into world coordinates. By performing a perspective transformation and color threshold, it is possible to calculate a suitable path the rover can use to drive forward. Here is a video of the rover navigating through the simulation while populating the world map.

https://user-images.githubusercontent.com/105971383/210530210-be04d2fb-5723-42fd-b11e-7dd400be0524.mp4


## Autonomous Navigation and Mapping
The Python files within this repository hook into the simulation and allow the rover to be fully autonomous in its goal of mapping the environment and collecting all the sample rocks before returning back to the starting position.


## Performance and output

![WhatsApp Image 2023-01-04 at 12 04 48 PM (2)](https://user-images.githubusercontent.com/105971383/210532004-03bb6ae4-56b2-4cb1-af5b-7f878a613a7f.jpeg)
