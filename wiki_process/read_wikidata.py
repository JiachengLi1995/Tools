#!/usr/bin/env python3

"""Get Wikidata dump records as a JSON stream (one JSON object per line)"""
# Modified script taken from this link: "https://www.reddit.com/r/LanguageTechnology/comments/7wc2oi/does_anyone_know_a_good_python_library_code/dtzsh2j/"

import bz2
import json
from collections import defaultdict
from tqdm import tqdm

def wikidata(filename):
    with bz2.open(filename, mode='rt') as f:
        f.read(2) # skip first two bytes: "{\n"
        for line in f:
            try:
                yield json.loads(line.rstrip(',\n'))
            except json.decoder.JSONDecodeError:
                continue

def extract_line(line):
    res = {}

    if 'id' in line:
        res['id'] = line['id']
    if 'labels' in line:
        if 'en' in line['labels']:
            res['name'] = line['labels']['en']['value']
            
    res['relations'] = defaultdict(list)
    if 'claims' in line:
        for relation, entity_list in line['claims'].items():
            for entity in entity_list:
                if 'mainsnak' in entity and 'datavalue' in entity['mainsnak'] and \
                    isinstance(entity['mainsnak']['datavalue']['value'], dict) and 'id' in entity['mainsnak']['datavalue']['value']:
                    
                    res['relations'][relation].append(entity['mainsnak']['datavalue']['value']['id'])
                   
    return res

if __name__ == '__main__':
    
    path = 'latest-all.json.bz2'
    output_file = 'wikidata.json'
    f_out = open(output_file, 'w', encoding='utf8')

    for record in tqdm(wikidata(path)):
        
        f_out.write(json.dumps(extract_line(record))+'\n')
        
    f_out.close()


       