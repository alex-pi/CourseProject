import os
from globals import get_data_paths

data_paths = get_data_paths("http://www.illinois.edu")

print(data_paths['done'])
while True:
    if os.path.exists(data_paths['done']):
        print('Found it! Can be read?')

        count = 0
        for line in open(data_paths['positive_data_path']):
            count += 1
        print(f'Lines: {count}')
        break

