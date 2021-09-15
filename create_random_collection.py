import os, random, sys

source = os.path.abspath(sys.argv[1])
dest = os.path.abspath(sys.argv[2])

all_filenames = [fn for fn in os.listdir(source) if fn.split('.')[-1] == 'gif']
randomized_files = sorted(all_filenames, key = lambda x: random.random())

current_number = len(os.listdir(dest))

for filename in randomized_files:
  command = f'mv {source}/{filename} {dest}/{current_number:04d}.gif'
  print(command)
  os.system(command)
  current_number += 1
  