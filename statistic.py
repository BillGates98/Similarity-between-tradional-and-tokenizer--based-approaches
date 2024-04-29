import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import seaborn as sns


class Statistics:

    def __init__(self, suffix=''):
        self.file = './outputs/' + suffix + '_data.csv'
        self.suffix = suffix
        self.columns = ['JW', 'HPP', 'p50k_base',
                        'cl100k_base', 'r50k_base', 'gpt2']  # 'JW',

    def read_csv(self):
        data = pd.read_csv(self.file, index_col=0)
        return data

    def run(self):
        output = {}
        data = self.read_csv()
        for column in self.columns:
            mean = data[column].mean()
            std = data[column].std()
            output[column] = {'mean': round(mean, 2), 'std': round(std, 2)}

        for column in output:
            print(column, output[column], '\n')
        return None


if __name__ == "__main__":
    def arg_manager():
        parser = argparse.ArgumentParser()
        parser.add_argument("--suffix", type=str, default="doremus")
        return parser.parse_args()

    args = arg_manager()
    print('Dataset Statistic : ', args.suffix)
    Statistics(suffix=args.suffix).run()
