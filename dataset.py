from re import search
from math import inf


class DataSet:
    def __init__(self):
        self.examples = []
        self.attributes = []
        self.attributes_count = 0

    def set_attributes(self, attributes):
        self.attributes = tuple(attributes)
        self.attributes_count = len(attributes)

    def import_csv_file(self, file_path, data_set_max_size=None, separator=', '):
        if not self.attributes or not self.attributes_count:
            raise AttributeError("Please define an attribute list")

        data_set_max_size = inf if data_set_max_size is None else data_set_max_size

        with open(file_path, 'r') as file:
            line = file.readline()
            lines_read = 0
            while line and lines_read < data_set_max_size:
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
