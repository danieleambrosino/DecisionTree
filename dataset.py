from re import search
from math import inf
from random import sample


class DataSet:
    def __init__(self, max_size=None):
        self.examples = []
        self.imported_examples = []
        self.attributes = []
        self.attributes_count = 0
        self.max_size = inf if max_size is None else max_size

    def set_attributes(self, attributes):
        self.attributes = tuple(attributes)
        self.attributes_count = len(attributes)

    def import_csv_file(self, file_path, separator=', '):
        if not self.attributes or not self.attributes_count:
            raise AttributeError("Please define an attribute list")

        with open(file_path, 'r') as file:
            line = file.readline()
            lines_read = 0
            while line and lines_read < self.max_size:
                lines_read += 1
                example = line.split(separator)
                for attribute in self.attributes:
                    key = attribute.index
                    value = example[key]
                    if search(r"^\d+$", value):
                        example[key] = int(value)
                    else:
                        example[key] = value.strip()
                self.examples.append(example)
                line = file.readline()

        if lines_read < self.max_size:
            self.max_size = lines_read

        self.imported_examples = self.examples

    def shuffle_examples(self, size):
        if size > self.max_size:
            size = self.max_size
        self.examples = sample(self.imported_examples, size)
