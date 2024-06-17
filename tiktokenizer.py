import numpy as np
import tiktoken
import time


class Tiktokenizer:

    def __init__(self, source='', target=''):
        self.models = []
        self.source = source
        self.target = target
        self.models = ['p50k_base', 'cl100k_base',
                       'r50k_base', 'gpt2']

    def cosine_similarity(self, v1=[], v2=[]):
        max_length = max(len(v1), len(v2))
        v1 = np.pad(v1, (0, max_length - len(v1)), 'constant')
        v2 = np.pad(v2, (0, max_length - len(v2)), 'constant')
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def vector_encoding(self, model_name='', value=''):
        if model_name in ['gpt-4']:
            enc = tiktoken.encoding_for_model("gpt-4")
        else:
            enc = tiktoken.get_encoding(model_name)
        return enc.encode(value)

    def run(self):
        output = {}
        for model in self.models:
            start = time.time()
            source_vector = self.vector_encoding(
                model_name=model, value=self.source)
            target_vector = self.vector_encoding(
                model_name=model, value=self.target)
            similarity = self.cosine_similarity(
                v1=source_vector, v2=target_vector)
            output[model] = {'value': similarity if similarity >
                             0 else 0.0, 'time': time.time() - start}
        return output
