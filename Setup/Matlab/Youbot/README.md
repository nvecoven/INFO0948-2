# First test of the youbot

In MATLAB, run the startup_robot.m file provided via the Git repository. 
```matlab
run('XXX/Setup/Matlab/Youbot/startup_robot.m');
```

This line needs to be run every time MATLAB restarts. 
You may want to add it to your MATLAB startup file. 
This first checks whether P. Corke's RVC toolbox is downloaded (and downloads it if it's not),
 and then updates MATLAB's path so that it can find the toolbox functions and the V-REP binding.

