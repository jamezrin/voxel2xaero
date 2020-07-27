# voxel2xaero

Python3 script to convert waypoints created in the VoxelMap mod to Xaero's Map.

This script was created targeting the following mod versions:

- VoxelMap 1.9.19 (1.12.2)
- XaeroMap 20.17.0 (1.12.2)

## Running

Move the script to your base modpack directory (the same directory where saves, mods, etc reside) and execute it like this

```bash
python3 voxel2xaero.py "World name"
```

If your Voxelmap or Xaeromap base directory differs from the ones I found in my installation, you will have to use the `voxelmap-dir` and `xaeromap-dir` flags to specify where the files are located in your modpack instance.

## Options

You can change the relative directories for VoxelMap and XaeroMap if they are different in your modpack.

You can also make the initial of the waypoints be a letter of the alphabet that corresponds to the order in which they where created.

And you can also enable random colors for the waypoints instead of the white color by default.

```text
usage: voxel2xaero.py [-h] [--voxelmap-dir directory] [--xaeromap-dir directory] [--index-initial] [--random-color]
                      savename

Convert voxelmap data to xaero's map

positional arguments:
  savename              Name of the world to convert

optional arguments:
  -h, --help            show this help message and exit
  --voxelmap-dir directory
                        Voxelmap base directory
  --xaeromap-dir directory
                        Xaeromap base directory
  --index-initial       Assign letters from the alphabet in increments
  --random-color        Choose random colors instead of 0
```
