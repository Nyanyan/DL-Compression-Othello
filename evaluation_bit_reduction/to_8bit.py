from tqdm import tqdm

dv = 16
with open('txt_eval_joined.txt', 'r') as f:
    data_file = f.read().splitlines()
with open('txt_eval_8bit_joined.txt', 'w') as f:
    for datum in tqdm(data_file):
        elem = max(-4091, min(4091, int(datum)))
        elem = round(elem / dv)
        f.write(str(elem) + '\n')
