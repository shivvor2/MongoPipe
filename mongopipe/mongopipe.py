from pymongo.collection import Collection
from typing import List, Callable, Dict

class MongoPipe:
    def __init__(self, source: Collection, destination: Collection, ops: List[Callable], batch_size: int = 100):
        self.source = source
        self.destination = destination
        self.ops = ops
        self.batch_size = batch_size

    def process_document(self, doc: Dict) -> Dict:
        result = doc.copy()
        for op in self.ops:
            op_result = op(doc)
            result = self.deep_update(result, op_result)
        return result

    def process_batch(self, batch: List[Dict]):
        processed = []
        for doc in batch:
            processed_doc = self.process_document(doc)
            processed.append(processed_doc)
        if processed:
            self.destination.insert_many(processed)

    def run(self):
        cursor = self.source.find()
        batch = []
        for doc in cursor:
            batch.append(doc)
            if len(batch) >= self.batch_size:
                self.process_batch(batch)
                batch = []
        if batch:
            self.process_batch(batch)
            
    @staticmethod
    def deep_update(target: Dict, source: Dict) -> Dict:
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                target[key] = MongoPipe.deep_update(target[key], value)
            else:
                target[key] = value
        return target