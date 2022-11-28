import csv
import tree


class Dataset:
    def __init__(self, filename):
        self.filename = filename
        self.data = self._get_data()
        self.header = []
        self.training_data = []
        self.tree = None
        # self.prepare_data()

    def _get_data(self):
        csv.register_dialect('tabs', delimiter=',')

        with open(self.filename, newline='') as csvfile:
            return list(csv.reader(csvfile, dialect='tabs'))

    @staticmethod
    def get_headers(data):
        return data[0]

    def prepare_data(self, numeric_cols, ignore_cols):

        training_data = [[0 for x in range(len(self.data[0]) - len(ignore_cols))] for y in range(len(self.data))]

        for i in range(1, len(self.data)):
            for j in range(len(self.data[0])):
                if j in numeric_cols:
                    # print(type(training_data[i][j]), training_data[i][j])
                    self.data[i][j] = float(self.data[i][j])

        cols = 0
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if j in ignore_cols and i == 0:
                    cols += 1
                else:
                    training_data[i][j - cols] = self.data[i][j]

        self.header = training_data[0]
        self.training_data = training_data

        print(self.header)
        # print(self.training_data)

    def call_tree(self):
        self.tree = tree.main(self)


# dataset = Dataset('/Users/jaimesantosorozco/Documents/Clases/Mates/proyecto/regtree/creditos.csv', [1, 4, 6], [0, 2])
