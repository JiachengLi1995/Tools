from transformers import RobertaTokenizerFast, AutoModelForMaskedLM
from tqdm import tqdm
import torch

test_file = '../../review_lm_pretrain/Amazon_Review_dev.txt'
device = 'cuda'


tokenizer = RobertaTokenizerFast.from_pretrained('./tmp/roberta-base/checkpoint-10000')
test = []
f = open(test_file, encoding='utf8')
for line in f:
    test.append(line.strip())
f.close()
test = test[:100000]
encodings = tokenizer('\n\n'.join(test), return_tensors='pt')

max_length = 512
stride = 512

for j in range(1, 10):
    model_name = f'./tmp/roberta-base/checkpoint-{j}0000'
    model = AutoModelForMaskedLM.from_pretrained(model_name).to(device)
    lls = []
    for i in tqdm(range(0, encodings.input_ids.size(1), stride)):
        begin_loc = max(i + stride - max_length, 0)
        end_loc = min(i + stride, encodings.input_ids.size(1))
        trg_len = end_loc - i    # may be different from stride on last loop
        input_ids = encodings.input_ids[:,begin_loc:end_loc].to(device)
        target_ids = input_ids.clone()
        target_ids[:,:-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)
            log_likelihood = outputs[0] * trg_len

        lls.append(log_likelihood)

    ppl = torch.exp(torch.stack(lls).sum() / end_loc)
    print(ppl)