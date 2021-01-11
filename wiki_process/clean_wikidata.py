## clean wikidata that do not contain 'name' or 'relation' length is 0

import json
from tqdm import tqdm

vocab_file = './wikidata_vocab.txt'
input_file = './wikidata.json'
output_file = './wikidata_cleaned.json'

f_vocab = open(vocab_file, encoding='utf8')
vocab = set()
for line in f_vocab:
    line = line.rstrip()
    identity, entity = line.split('\t')
    vocab.add(identity)
f_vocab.close()

f_in = open(input_file, encoding='utf8')
f_out = open(output_file, 'w',encoding='utf8')

for line in tqdm(f_in):
    line = json.loads(line)

    if line['id'] in vocab and len(line['relations'])>0:

        f_out.write(json.dumps(line)+'\n')

f_in.close()
f_out.close()