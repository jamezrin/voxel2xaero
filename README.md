# voxel2xaero

Python3 script to convert waypoints created in the VoxelMap mod to Xaero's Map.

This script was created targeting the following mod versions:

- VoxelMap 1.9.19 (1.12.2)
- XaeroMap 20.17.0 (1.12.2)

## Running

Move the script to your base modpack directory (the same directory where saves, mods, etc reside) and execute it like this

- All world saves: `python3 voxel2xaero.py`
- Specific world save: `python3 voxel2xaero.py --savename "World name"`

If your Voxelmap or Xaeromap base directory differs from the ones I found in my installation, you will have to use the `voxelmap-dir` and `xaeromap-dir` flags to specify where the files are located in your modpack instance.

That also applies for the `saves-dir` but it\'s rare that you would have to change that, it\'s configurable just to not hardcode things

## Options

You can change the relative directories for VoxelMap and XaeroMap if they are different in your modpack.

You can also make the initial of the waypoints be a letter of the alphabet that corresponds to the order in which they where created.

And you can also enable random colors for the waypoints instead of the white color by default.

By the default the script overwrites the waypoints for the savename you want to convert, you can also change this with a flag, making it append instead.

```text
usage: voxel2xaero.py [-h] [--savename savename] [--voxelmap-dir directory] [--xaeromap-dir directory] [--saves-dir directory] [--index-initial]
                      [--random-color] [--append-output]

Convert VoxelMap data to Xaero's Map

optional arguments:
  -h, --help            show this help message and exit
  --savename savename   Only convert this world save
  --voxelmap-dir directory
                        Voxelmap base directory
  --xaeromap-dir directory
                        Xaeromap base directory
  --saves-dir directory
                        Saves base directory
  --index-initial       Assign letters from the alphabet in increments
  --random-color        Choose random colors instead of the first one
  --append-output       Append to the XaeroMap waypoints file instead of overwriting
```
