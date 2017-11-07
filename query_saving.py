import json
import requests
import pandas as pd
import argparse
import time
import urllib.request, json 
import os
from utils import *

parser = argparse.ArgumentParser(description='Process query saving by ids.')
parser.add_argument('--ids', default='otvety_cooking_id.txt')
parser.add_argument('--path_to', default='jsons/')
parser.add_argument('--name_of_file', default='cooking')
parser.add_argument('--step', default='1000')


args = parser.parse_args()

ids_path = args.ids
name_of_file = args.name_of_file
path_to = args.path_to
step = int(args.step)

create_if_not_exist(path_to)

ids = [x.strip() for x in open('{}'.format(ids_path),'r').readlines()]
mail_ru_template = "https://otvet.mail.ru/api/v2/question?qid={}"

def save_part_of_data(ids, path=path_to, name_of_file=name_of_file,i = 0):
    jsons = []
    for id_ in ids: 
        try:
            with urllib.request.urlopen(mail_ru_template.format(id_)) as url:
                data = json.loads(url.read().decode())
                jsons.append(data)
        except:
            time.sleep(10)
    f = open('{}/{}_{}.txt'.format(path, name_of_file, i), 'a')
    for js in jsons:        
        f.write(json.dumps(js, f))


#saving
for i, part_i in enumerate(range(0, len(ids), step)):
    print('{}/{}'.format(i, len(ids) // step))
    if i == 5:
        break 
    save_part_of_data(ids[part_i:part_i + step], path_to, name_of_file, i)
        
#merging
filenames = ['{}/{}'.format(path_to, x) for x in os.listdir(path_to)]

with open('{}.txt'.format(name_of_file), 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
