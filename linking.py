from rdflib import Graph
from compute_files import ComputeFile
import argparse
from tqdm import tqdm
import time
import numpy as np
import validators
import pandas as pd
from similarity_measures import SimilarityMeasure


class Linking:
    def __init__(self, source='', target='', truth='', suffix='', random_size=100):
        self.source = source
        self.target = target
        self.truth = truth
        self.suffix = suffix
        self.truth_subjects = {}
        self.random_size = random_size

    def load_graph(self, file=''):
        graph = Graph()
        graph.parse(file)
        return graph

    def extract_subjects(self, graph=None):
        output = {}
        for s, p, o in graph:
            if not s in output:
                output[s] = []
            output[s].append((p, o))
        return output

    def extract_ground_truths(self, file=None):
        output = []
        graph = self.load_graph(file=file)
        for s, _, o in graph:
            output.append((s, o))
        return output

    def string_chain(self, entity=[]):
        output = []
        for p, o in entity:
            if not validators.url(str(o)):
                value = str(o)
                words = value.split(' ')
                is_bad = False
                for word in words:
                    if len(word) > 24:
                        is_bad = True
                if not is_bad:
                    output.append(value)
        return output

    def compute_similarity_score(self, entity1=[], entity2=[]):
        output = {}
        literals1 = self.string_chain(entity=entity1)
        literals2 = self.string_chain(entity=entity2)
        if len(literals1) > 0 and len(literals2) > 0:
            for value1 in literals1:
                for value2 in literals2:
                    tmp = SimilarityMeasure(source=value1, target=value2).run()
                    for key, value in tmp.items():
                        if not key in output:
                            output[key] = []
                        output[key].append(value)
            for key, values in output.items():
                output[key] = np.mean(values)
        return output

    def entity_comparisons(self, candidates=[], source_bunches={}, target_bunches={}):
        output = {'source': [], 'target': []}
        for s, t in tqdm(candidates):
            if s in source_bunches and t in target_bunches:
                source = source_bunches[s]
                target = target_bunches[t]
                sim = self.compute_similarity_score(
                    entity1=source, entity2=target)
                # print(s, t, sim)
                if len(sim.keys()) > 0:
                    output['source'].append(s)
                    output['target'].append(t)
                    for key, value in sim.items():
                        if not key in output:
                            output[key] = []
                        output[key].append(value)
        return output

    def deep_building_of_entities(self, file=''):
        graph = self.load_graph(file=file)
        subjects = self.extract_subjects(graph=graph)
        return subjects

    def save_results(self, data={}):
        df = pd.DataFrame.from_dict(data)
        df.to_csv("./outputs/" + self.suffix + "_data.csv")
        return None

    def orchestrator(self):
        source_entities = self.deep_building_of_entities(
            file=self.source)
        target_entities = self.deep_building_of_entities(
            file=self.target)
        ground_truth_entities = self.extract_ground_truths(file=self.truth)

        result = self.entity_comparisons(
            candidates=ground_truth_entities,
            source_bunches=source_entities,
            target_bunches=target_entities)
        self.save_results(data=result)
        print('End with success !')
        return None

    def run(self):
        return self.orchestrator()


if __name__ == "__main__":
    def detect_file(path='', type=''):
        files = ComputeFile(input_path=path).build_list_files()
        for v in files:
            if type in v:
                return v
        return None

    def arg_manager():
        parser = argparse.ArgumentParser()
        parser.add_argument("--input_path", type=str, default="./inputs/")
        parser.add_argument("--suffix", type=str, default="doremus")
        parser.add_argument("--random_size", type=int, default=100)
        return parser.parse_args()

    start = time.time()
    args = arg_manager()
    source = detect_file(path=args.input_path+args.suffix, type='source')
    target = detect_file(path=args.input_path+args.suffix, type='target')
    truth = detect_file(path=args.input_path+args.suffix, type='same_as')

    print('Dataset : ', args.suffix)

    Linking(source=source, target=target,
            truth=truth, suffix=args.suffix, random_size=args.random_size).run()
    print('Running Time : ', (time.time() - start), ' seconds ')
