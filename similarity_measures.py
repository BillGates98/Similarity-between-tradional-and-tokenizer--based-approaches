from strsimpy.jaro_winkler import JaroWinkler
import time
from tiktokenizer import Tiktokenizer
from hpp_similarity import StringSimilarity


class SimilarityMeasure:

    def __init__(self, source='', target=''):
        self.source = source
        self.target = target
        self.models = ['p50k_base', 'cl100k_base',
                       'r50k_base', 'gpt2']

    def jaro_winkler(self):
        start = time.time()
        jarowinkler = JaroWinkler()
        value = jarowinkler.similarity(self.source, self.target)
        return {'value': value if value else 0.0, 'time': time.time()-start}

    def hpp(self):
        start = time.time()
        measure = StringSimilarity(self.source, self.target)
        value = measure.run()
        return {'value': value if value else 0.0, 'time': time.time()-start}

    def tik_tokenizer(self):
        measure = Tiktokenizer(source=self.source, target=self.target)
        value = measure.run()
        return value

    def run(self):
        if len(self.source) == 0 or len(self.target) == 0:
            tmp = {
                'JW': {'value': 0.0, 'time': 0.0},
                # 'HPP': {'value': 0.0, 'time': 0.0}
            }
            for model in self.models:
                tmp[model] = {'value': 0.0, 'time': 0.0}
            return tmp
        output = {
            'JW': self.jaro_winkler(),
            # 'HPP': self.hpp(),
        }

        tik_tokens = self.tik_tokenizer()
        for model in tik_tokens:
            output[model] = tik_tokens[model]
        return output
