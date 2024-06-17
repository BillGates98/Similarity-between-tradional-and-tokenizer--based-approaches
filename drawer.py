import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import seaborn as sns
import os


class Drawer:

    def __init__(self, suffix=''):
        self.file = './outputs/' + suffix + '_data.csv'
        self.suffix = suffix
        self.columns = ['JW', 'p50k_base',
                        'cl100k_base', 'r50k_base', 'gpt2']  # 'JW',
        if not os.path.exists('./outputs/' + self.suffix):
            os.makedirs('./outputs/' + self.suffix)

    def read_csv(self):
        data = pd.read_csv(self.file, index_col=0)
        return data

    def heap_map(self):
        data = self.read_csv()
        pd.set_option("expand_frame_repr", False)
        data.dropna(inplace=True)
        heap = sns.heatmap(data)
        plt.title(self.suffix)
        plt.savefig('./outputs/' + self.suffix + '/_heap_map.pdf')

    def curves(self):
        data = self.read_csv()
        ax = plt.gca()
        data.insert(1, "X", [x for x in range(0, len(data['JW']))], True)
        colors = {
            # 'HPP': 'red',
            'p50k_base': 'orange',
            'cl100k_base': 'pink',
            'r50k_base': 'brown',
            'gpt2': 'green',
            'JW': 'blue'
        }
        for x in self.columns:
            data.plot(kind='line',
                      x='X',
                      y=x,
                      color=colors[x], ax=ax)
        plt.title('Comparisons')
        plt.savefig('./outputs/' + self.suffix + '/_figure.pdf')

    def box_plot_similarity(self):
        data = self.read_csv()
        data = data.rename(
            columns={(column+'_value'): column for column in self.columns})
        plt.figure()
        data.insert(1, "X", [x for x in range(
            0, len(data['JW']))], True)
        data.plot.box(column=self.columns)
        plt.title('Dataset : ' + self.suffix)
        plt.savefig('./outputs/' + self.suffix + '/_boxplot_similarity.pdf')

    def box_plot_time(self):
        data = self.read_csv()
        data = data.rename(
            columns={(column+'_time'): column for column in self.columns})
        plt.figure()
        data.insert(1, "X", [x for x in range(0, len(data['JW']))], True)
        data.plot.box(column=self.columns)
        plt.title('Dataset : ' + self.suffix)
        plt.savefig('./outputs/' + self.suffix + '/_boxplot_time.pdf')

    def run(self):
        self.box_plot_similarity()
        pass
        self.box_plot_time()
        # self.heap_map()
        return None


if __name__ == "__main__":
    def arg_manager():
        parser = argparse.ArgumentParser()
        parser.add_argument("--suffix", type=str, default="doremus")
        return parser.parse_args()

    args = arg_manager()
    print('Dataset drawing : ', args.suffix)
    Drawer(suffix=args.suffix).run()
