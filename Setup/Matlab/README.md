# Matlab client

## Install the CoppeliaSim bindings for MATLAB

1.  You must copy three files from the directory of the CoppeliaSim app (downloaded at the [previous step](https://github.com/nvecoven/robotic_rework/tree/main/Setup/Coppelia)) to the directory of the robot you want to use (e.g., subfolder `myfavoriterobot` for the robot named `myfavoriterobot`). The three files you need to copy are named:
    *   `remApi.m`
    *   `remoteApiProto.m`
    *   `remoteApi.so` (if you use Linux) or `remoteApi.dll` (if you use Windows) or `remoteApi.dylib` (if you use a Mac).

        If you have a choice between a 32-bit or 64-bit remoteApi, pick the one that corresponds to your MATLAB install (32-bit MATLAB or 64-bit MATLAB). If you have 32-bit MATLAB, pick the 32-bit remoteApi, even if your kernel is 64-bit.

    You will find these files in the directory containing the CoppeliaSim app. Look in the `programming/remoteApiBindings/lib/lib` and `programming/remoteApiBindings/matlab/matlab` subdirectories of the CoppeliaSim app directory (although this can change from version to version). You must copy these files to the appropriate robot directory within your copy of the GitHub repo.

2.  In MATLAB, change to the robot directory. For robot `myfavoriterobot`, On Linux/Mac:
    ```bash
    cd ~/trs/Setup/Matlab/myfavoriterobot
    ```

    Then perform a first connection test by typing:
    ```matlab
    vrep=remApi('remoteApi');
    vrep.delete();
    ```

    If there is no error, the MATLAB bindings to CoppeliaSim are loaded! If there is an error, check the steps above, check the Troubleshooting section below, and read CoppeliaSim's MATLAB bindings help. The CoppeliaSim developers are actively supporting TRS. If you cannot solve this issue, post a question on the CoppeliaSim forums.

3.  Startup CoppeliaSim (Linux: `./coppeliaSim.sh` from within CoppeliaSim's directory; Windows: in your Start menu), use the menu "File/Open Scene", and open `~/Setup/Coppelia/Scenes/binding_test.ttt`. Hit "Start Simulation" in the Simulation menu.
Then, back in MATLAB, go to the `myfavoriterobot` robot folder. On Linux/Mac:

    ```bash
    cd ~/trs/Setup/Matlab/myfavoriterobot
    ```

    Then run the `binding_test` script:
    ```matlab
    binding_test();
    ```

    If you see MATLAB replying Number of objects in the scene: 19, everything works! If not, as recommended above, post a question on the CoppeliaSim forum (the most common cause of errors is forgetting to start the simulation).


## MATLAB tips

### Avoiding loops

MATLAB is an interpreted language. Despite recent progress in the JIT accelerator, running loops in MATLAB is still _much_ slower than running loops in native code. Since most MATLAB functions rely on a C implementation of large loops, it is good practice to always prefer calling a function over writing a loop when handling large datatypes. In your project, the two datatypes that you need to handle with care are images and point clouds (from the RGB camera, or from the 2D/3D laser scanners). **Handling images and point clouds with MATLAB functions or MEX functions instead of MATLAB loops will often make your code 100 times faster.**

An example of the computational cost of flipping an image with a loop vs. a MATLAB function is provided [here](https://github.com/ULgRobotics/trs/blob/master/matlab/test_loop_vs_native.m).

### Running code from files

The MATLAB JIT accelerator doesn't optimize code typed into the console, even though recent versions of MATLAB have greatly improved in terms of performance. To verify this behavior, run the function above by typing `test_loop_vs_native` in the console, then by copy-pasting the contents of the `test_loop_vs_native` function directly into the console. As a result of this behavior, always run your code from `.m` files.

### Use the toolboxes!

There are plenty of functions in Peter Corke's Robotics Toolbox that will help you with high-level algorithms (path planning, vision…), but also low-level computations (pose transformation, angle distance…). Don't forget to use them!

If you have them, MATLAB also has many interesting toolboxes for this project: for computer vision ([MATLAB Image Processing Toolbox](https://fr.mathworks.com/products/image.html), [MATLAB Computer Vision System](https://www.mathworks.com/products/computer-vision.html)), machine learning ([Statistics and Machine Learning](https://www.mathworks.com/products/statistics.html)), and robotics ([Robotics System](https://www.mathworks.com/products/robotics.html)), more specifically. Pay attention that not all of them are included in the student version of MATLAB.

### Useful functions/tools

*   The MATLAB `inpolygon` function
