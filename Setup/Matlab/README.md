# Linking the remote API with MATLAB

Install the Coppelia bindings for MATLAB:

1. You must copy three files from the directory of the Coppelia app (downloaded at the previous step) to the directory of the 
 robot you want to used, (subfolder YYY for robot named YYY). The three files you need to copy are named: 
      1. remApi.m
      2. remoteApiProto.m
      3. remoteApi.so (if you use Linux) or remoteApi.dll (if you use Windows) or remoteApi.dylib (if you use a Mac).
       If you have a choice between a 32-bit or 64-bit remoteApi, 
       pick the one that corresponds to your MATLAB install (32-bit MATLAB or 64-bit MATLAB). 
       If you have 32-bit MATLAB, pick the 32-bit remoteApi, even if your kernel is 64-bit.
       
You will find these files in the directory containing the V-REP app. 
Look in the programming/remoteApiBindings/lib/lib and programming/remoteApiBindings/matlab/matlab 
subdirectories of the Coppelia app directory (although this can change from version to version). 
You must copy these files to the appropriate robot directory within your copy of the GitHub repo.

2. In MATLAB, change to the robot directory. For robot YYY, On Linux/Mac:

```bash
cd xxx/Setup/Matlab/YYY"
```

Then perform a first connection test by typing:
```matlab
vrep=remApi('remoteApi');
vrep.delete();
```

If there is no error, the MATLAB bindings to V-REP are loaded! If there is an error, check the steps above, 
check the Troubleshooting section below, and read Coppelia's MATLAB bindings help. 
The Coppelia developers are actively supporting TRS. If you cannot solve this issue, post a question on the V-REP forums.

Startup Coppelia (Linux: ./vrep.sh from within V-REP's directory; Windows: in your Start menu), 
use the menu "File/Open Scene", and open ~/Setup/Coppelia/Scenes/binding_test.ttt. Hit "Start Simulation" in the Simulation menu. 
Then, back in MATLAB, go to the youbot folder. On Linux/Mac:

```bash
cd xxx/Setup/Matlab/Youbot"
```

Then run the binding_test script:
```matlab
binding_test();
```

If you see MATLAB replying Number of objects in the scene: 19, everything works! If not, as recommended above, 
post a question on the V-REP forums (the most common cause of errors is forgetting to start the simulation).