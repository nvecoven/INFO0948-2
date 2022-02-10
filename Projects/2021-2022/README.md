# 2020-2021 Project

![house](img/house.png)

## Context

In this project, you will program a robotic agent that (i) gathers information about its environment using the sensors, (ii) plans a set of actions to respond appropriately to sensed data based on a pre-existing strategy, and (iii) executes a set of motor commands to carry out the actions that the plan calls for. The robot will be simulated in the robot simulator [CoppeliaSim](https://www.coppeliarobotics.com/).

The general framework for the project relies on [TRS](http://ulgrobotics.github.io/trs/), an open-source project developed by [Renaud Detry](http://renaud-detry.net/). You can find useful information there but all the information that you need is available in this new repository:
*   [detailed installation instructions](https://github.com/nvecoven/INFO0948-2/tree/main/Setup),
*   [complete demo of the youBot (Python)](https://github.com/nvecoven/INFO0948-2/tree/main/Setup/Python/Youbot),
*   [list of allowed/forbidden functions](https://github.com/nvecoven/INFO0948-2/tree/main/Setup/CoppeliaSim).

The [help](https://www.coppeliarobotics.com/helpFiles/) of the robot simulator CoppeliaSim is also a good source of information.

## Specific milestones

1. **Navigation**  
    For this milestone, the youBot will need to navigate in an unknown environment.

    <!-- you should build a custom controller for the youBot, which should use its holonomic properties. In particular, _we do not allow the use of pure pursuit controller controllerPurePursuit from Matlab's Robotics System Toolbox._ -->

    1. (compulsory): The youBot should explore the whole map (and build an appropriate representation), by accessing the GPS coordinates (i.e., `simxGetObjectPosition` can be used on the youBot's `ref`). For this milestone, you can also call `simxGetObjectOrientation` on the youBot's `ref` whenever needed.

    2. (compulsory): Same as (1.i), but `simxGetObjectPosition` cannot be used directly. The youBot has access to its distance to three beacons sending radio signals through the sensor. This information can be obtained through the function `youbot_beacon(vrep, clientID, beacons_handle, youbot_handle, flag, noise=True)` with `flag = 0`. For this milestone, you can also call `simxGetObjectOrientation` on the youBot's `ref` whenever needed.    

    3. (optional): Same as (1.i), but `simxGetObjectPosition` cannot be used directly. The youBot has access to its distance to three beacons sending radio signals only when it is inside a radius of 5 m to the beacon. This information can be obtained through the function `youbot_beacon(vrep, clientID, beacons_handle, youbot_handle, flag, noise=True)` with `flag = 1`. For this milestone, you can also call `simxGetObjectOrientation` on the youBot's `ref` whenever needed.

    The size of the house is fixed (see `house_2021.ttt`). However, the youBot does not know the layout of the house a priori. All obstacles are high enough to be detectable with the Hokuyo sensor. There are no holes or open doors leading outside the house. There are three tables around the house. The location of tables with objects is fixed, but the target table's location is not. Tables are cylinders, 800 mm in diameter, and 185 mm in height.


2. **Manipulation**  
    For this milestone, the youBot will need to access a “TargetTable” object, which position you will have to find thanks to the youBot's sensors. Note that this table is the same as the ones on which objects are initially lying. _To distinguish them, you can make the assumption that the "TargetTable" will always start empty (no objects initially lying on it)._

    1. (compulsory): The youBot should grab all the objects on the first table (where objects stand upright), without any falling on the ground and put them on the target table.

    2. (optional): The youBot should grab all the objects on both tables, without any falling on the ground and put them on the target table.

## Instructions

* You can work in teams of up to two people.

* Your deliverables must be submitted as a _zip_ archive on the [Montefiore submission platform](https://submit.montefiore.ulg.ac.be/).

* Important dates (unless otherwise noted, all project items are due by 11:59 pm):

    * :bangbang: 01/04/2021: midterm code and report,
    * :bangbang: end of May: final code and report,
    * :bangbang: June (during the exam session): final presentation.


## Midterm report

For the midterm report, we expect you to complete the **Navigation (1.i)**.

Each team must submit a _zip_ archive containing:

*   The source code of the youBot.

*   A short commented video or a link to the video (max. 5 minutes).

    In the video, the youBot should explore and eventually map its entire environment. The video should show the youBot in action but should also emphasize how the youBot plans its actions. For example, showing the evolution of the map as the youBot builds it, showing potential new targets to explore and how the youBot chooses one, showing the planned trajectory to the chosen target, etc.

    The video should last (at most) 5 minutes.

*   A short written report named `midterm-report.pdf` (max. 1 page).

    In the report, you should summarize the main points of your implementation. The report should _not_ consist of a list of functions that you used in your project. We are more interested in the _why_ than the _what_. For example, if you chose a specific pathfinding algorithm, explain why this one and not another. In addition, the report should contain a diagram of the finite state machine controlling your youBot.

    The report should be (at most) one page long using the provided LaTeX template ([ieeeconf.zip](docs/ieeeconf.zip)).


The midterm report is due on the [Montefiore submission platform](https://submit.montefiore.ulg.ac.be/) on 01/04/2021.

## Useful links

<!-- *   [Robotics System Toolbox](https://www.mathworks.com/products/robotics.html), by MathWorks
*   [Robotics Toolbox for MATLAB](https://petercorke.com/toolboxes/robotics-toolbox/), by Peter Corke -->
*   [OBS Studio](https://obsproject.com/), a free and open-source software suite for recording

## Montefiore server access via ssh

[Document borrowed from INFO2009.](docs/devoirs-ssh.pdf)


<!--
---
# 2020-2021 Project

Pour avoir une idée ....

## Goal

The goal is to blablabla ....

The main scene you will be working on is the "HOUSE" scene. You can find it in

```bash
~/trs/Setup/Coppelia/Scenes/House
```

In that folder, you will also find the appropriate instructions files needed for the objects placement
(in matlab and python format).

The robot you will use for this project is the youbot. All the scripts for language "YYY" relative to this bot are given in

```bash
~/trs/Setup/YYY/Youbot
``` -->
