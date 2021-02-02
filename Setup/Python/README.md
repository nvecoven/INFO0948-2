# Python client

## Install the CoppeliaSim bindings for Python

1.  You must copy three files from the directory of the CoppeliaSim app (downloaded at the [previous step](https://github.com/nvecoven/robotic_rework/tree/main/Setup/Coppelia)) to the directory of the robot you want to use (e.g., subfolder `myfavoriterobot` for the robot named `myfavoriterobot`). The three files you need to copy are named:
    *   `sim.py`
    *   `simConst.py`
    *   `remoteApi.so` (if you use Linux) or `remoteApi.dll` (if you use Windows) or `remoteApi.dylib` (if you use a Mac).

        If you have a choice between a 32-bit or 64-bit remoteApi, pick the one that corresponds to your Python version.

    You will find these files in the directory containing the CoppeliaSim app. Look in the `programming/remoteApiBindings/lib/lib` and `programming/remoteApiBindings/python/python` subdirectories of the CoppeliaSim app directory (although this can change from version to version). You must copy these files to the appropriate robot directory within your copy of the GitHub repo.
