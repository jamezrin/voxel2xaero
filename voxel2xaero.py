#!/usr/bin/python3

import os
import functools
import argparse
import random

class VoxelMapWaypoint(object):
  def __init__(self,
    name=None, dim=None,
    x=None, y=None, z=None,
    r=None, g=None, b=None,
    suffix=None, world=None,
    enabled=False):
    self.name = name
    self.dim = dim
    self.x = x
    self.y = y
    self.z = z
    self.r = r
    self.g = g
    self.b = b
    self.suffix = suffix
    self.world = world
    self.enabled = enabled

class DimensionData(object):
  def __init__(self, dimension):
    self.dimension = dimension
    self.waypoints = []

def acc_waypoints_by_dim(dataset, waypoint):
  dimension_data = None
  if waypoint.dim in dataset:
    dimension_data = dataset[waypoint.dim]
  else:
    dimension_data = DimensionData(waypoint.dim)

  dimension_data.waypoints.append(waypoint)
  dataset[waypoint.dim] = dimension_data
  return dataset

def group_waypoints_by_dim(waypoints):
  return functools.reduce(acc_waypoints_by_dim, waypoints, {})

class MissingBaseDirectoryError(Exception):
  pass

class MissingSourceFileError(Exception):
  pass

def check_dir_args(voxelmap_dir, xaeromap_dir, saves_dir):
  if not os.path.exists(voxelmap_dir):
    raise MissingBaseDirectoryError('voxelmap directory does not exist')

  if not os.path.exists(xaeromap_dir):
    raise MissingBaseDirectoryError('xaero map directory does not exist')

  if not os.path.exists(saves_dir):
    raise MissingBaseDirectoryError('world saves base directory does not exist')

def boolean_to_string(val):
  return 'true' if val else 'false'

def extract_xz_coords(waypoint):
  if waypoint.dim == -1:
    return (waypoint.x // 8, waypoint.z // 8)
  else:
    return (waypoint.x, waypoint.z)

def extract_initial(idx, index_initial, waypoint):
  if index_initial:
    return chr(min(ord('A') + idx, ord('Z')))
  else:
    return waypoint.name[0].upper()

def extract_color(random_color, waypoint):
  if random_color:
    return random.randrange(16)
  else:
    return 0

def voxelmap_assign_kv(waypoint, k, v):
  if k == "name":
    waypoint.name = v
  elif k == "dimensions":
    waypoint.dim = int(v[:v.index('#')])
  elif k == "x":
    waypoint.x = int(v)
  elif k == "y":
    waypoint.y = int(v)
  elif k == "z":
    waypoint.z = int(v)
  elif k == "red":
    waypoint.r = float(v)
  elif k == "green":
    waypoint.g = float(v)
  elif k == "blue":
    waypoint.b = float(v)
  elif k == "suffix":
    waypoint.suffix = v
  elif k == "world":
    waypoint.world = v
  elif k == "enabled":
    waypoint.enabled = (v == "true")

# returns list of VoxelMapWaypoint
def parse_voxelmap_file(voxelmap_dir, savename):
  point_path = os.path.join(voxelmap_dir, f'{savename}.points')
  waypoints = []
  try:
    with open(point_path, 'r') as f:
      for n, line in enumerate(f):
        if n < 3: continue
        pairs = line.split(',')
        waypoint = VoxelMapWaypoint()
        for o, pair in enumerate(pairs):
          k, v = pair.split(':')
          voxelmap_assign_kv(waypoint, k, v)
        waypoints.append(waypoint)
  except IOError:
    raise MissingSourceFileError('could not open voxelmap points file')
    
  return waypoints

def voxel2xaero(xaeromap_dir, index_initial, random_color, append_output, savename, waypoints):
  grouped_waypoints = group_waypoints_by_dim(waypoints)

  savename_path = os.path.join(xaeromap_dir, savename)
  if not os.path.isdir(savename_path):
    os.makedirs(savename_path)

  for dim, data in grouped_waypoints.items():
    dim_path = os.path.join(savename_path, f'dim%{dim}')

    if not os.path.isdir(dim_path):
      os.makedirs(dim_path)

    waypoints_path = os.path.join(dim_path, 'waypoints.txt')
    with open(waypoints_path, 'a' if append_output else 'w') as f:
      for idx, waypoint in enumerate(data.waypoints):
        initial = extract_initial(idx, index_initial, waypoint)
        x, z = extract_xz_coords(waypoint)
        color = extract_color(random_color, waypoint)

        # some defaults
        waypoint_type = 0
        waypoint_set = 'gui.xaero_default'
        rotated_tp = False
        rotation_yaw = 0
        waypoint_global = False

        waypoint_line = 'waypoint:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}'.format(
          waypoint.name, initial,
          x, waypoint.y, z,
          color, boolean_to_string(not waypoint.enabled),
          waypoint_type, waypoint_set,
          boolean_to_string(rotated_tp), rotation_yaw,
          boolean_to_string(waypoint_global),
        )

        f.write(f'{waypoint_line}\n')

def convert_savename(voxelmap_dir, xaeromap_dir, index_initial, random_color, append_output, savename):
  waypoints = parse_voxelmap_file(
    voxelmap_dir,
    savename,
  )

  voxel2xaero(
    xaeromap_dir,
    index_initial,
    random_color,
    append_output,
    savename,
    waypoints
  )

def parse_args():
  parser = argparse.ArgumentParser(description='Convert VoxelMap data to Xaero\'s Map')
  parser.add_argument('--savename', metavar='savename', type=str, help='Only convert this world save')
  parser.add_argument('--voxelmap-dir', dest='voxelmap_dir', metavar='directory', type=str, help='Voxelmap base directory', default='mods/VoxelMods/voxelMap')
  parser.add_argument('--xaeromap-dir', dest='xaeromap_dir', metavar='directory', type=str, help='Xaeromap base directory', default='XaeroWaypoints')
  parser.add_argument('--saves-dir', dest='saves_dir', metavar='directory', type=str, help='Saves base directory', default='saves')
  parser.add_argument('--index-initial', dest='index_initial', action='store_true', default=False, help='Assign letters from the alphabet in increments')
  parser.add_argument('--random-color', dest='random_color', action='store_true', default=False, help='Choose random colors instead of the first one')
  parser.add_argument('--append-output', dest='append_output', action='store_true', default=False, help='Append to the XaeroMap waypoints file instead of overwriting')
  args = parser.parse_args()
  return args

def convert_specific_savename(voxelmap_dir, xaeromap_dir, index_initial, random_color, append_output, savename):
  print(f'Converting "{savename}" waypoints...')
  try:
    convert_savename(
      voxelmap_dir,
      xaeromap_dir,
      index_initial,
      random_color,
      append_output,
      savename,
    )

    print('Successfully converted waypoints')
  except MissingSourceFileError as e:
    print(f'error: {e}')
    exit(-1)

def convert_all_savenames(voxelmap_dir, xaeromap_dir, saves_dir, index_initial, random_color, append_output):
  saves = os.listdir(saves_dir)
  for savename in saves:
    print(f'Converting "{savename}" waypoints... ', end='')
    try:
      convert_savename(
        voxelmap_dir,
        xaeromap_dir,
        index_initial,
        random_color,
        append_output,
        savename,
      )
      print('OK')
    except MissingSourceFileError as e:
      print('NO DATA')

def run():
  args = parse_args()
  try:
    check_dir_args(
      args.voxelmap_dir,
      args.xaeromap_dir,
      args.saves_dir,
    )
  except MissingBaseDirectoryError as e:
    print(f'error: {e}')
    exit(-1)

  if args.savename:
    convert_specific_savename(
      args.voxelmap_dir,
      args.xaeromap_dir,
      args.index_initial,
      args.random_color,
      args.append_output,
      args.savename,
    )
  else:
    convert_all_savenames(
      args.voxelmap_dir,
      args.xaeromap_dir,
      args.saves_dir,
      args.index_initial,
      args.random_color,
      args.append_output,
    )

if __name__ == '__main__':
  run()
