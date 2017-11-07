import os

def create_if_not_exist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

