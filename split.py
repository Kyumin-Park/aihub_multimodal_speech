import random
import argparse

def split_train_dev_test(filelist, ratio='8:1:1', seed=123):
    ratio_split = ratio.split(':')
    assert len(ratio_split) == 3, "Ratio must consist of three components"
    ratio_split = [float(x) for x in ratio_split]
    sum_ratio = sum(ratio_split)
    train_ratio, dev_ratio, test_ratio = [x / sum_ratio for x in ratio_split]

    with open(filelist, 'r', encoding='utf-8') as f:
        total_data = f.readlines()

    random.seed(seed)
    random.shuffle(total_data)
    total_len = len(total_data)
    train_span, dev_span = train_ratio * total_len, dev_ratio * total_len

    train_data = total_data[:train_span]
    dev_data = total_data[train_span:dev_span]
    test_data = total_data[dev_span:]

    with open(filelist.replace('.txt', '_train.txt'), 'w', encoding='utf-8') as f:
        f.writelines(train_data)
    with open(filelist.replace('.txt', '_dev.txt'), 'w', encoding='utf-8') as f:
        f.writelines(dev_data)
    with open(filelist.replace('.txt', '_test.txt'), 'w', encoding='utf-8') as f:
        f.writelines(test_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='speech_dataset/filelist.txt',
                        help='path to filelist.txt')
    parser.add_argument('--ratio', type=str, default='8:1:1',
                        help='train:dev:test ratio, separated by :')
    parser.add_argument('--seed', type=int, default=123, help='seed')

    args = parser.parse_args()

    split_train_dev_test(args.path, args.ratio, args.seed)