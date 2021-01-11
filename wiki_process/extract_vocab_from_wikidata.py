import json
from tqdm import tqdm

input_file = './wikidata.json'
output_file = './wikidata_vocab.txt'

in_f = open(input_file, encoding='utf8')
out_f = open(output_file, 'w', encoding='utf8')

for line in tqdm(in_f):

    line = json.loads(line)

    try:
    
        name = line['name']
        identity = line['id']

        out_f.write(identity+'\t'+name+'\n')
    except:

        pass

out_f.close()