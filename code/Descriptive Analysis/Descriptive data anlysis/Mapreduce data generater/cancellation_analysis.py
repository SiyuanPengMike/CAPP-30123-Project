from mrjob.job import MRJob
import re
import csv
from mrjob.step import MRStep

WORD_RE = re.compile(r"[\w]+")

class MR_cancellation(MRJob):

    def mapper(self, _, line):   
        row = next(csv.reader([line]))
        cancelled0 = row[21]
        try:
            cancelled = int(cancelled0)
            if cancelled==1:
                yield row[22], 1

        except:
            pass


    def combiner(self, name, value):
        yield name,sum(value)

    def reducer(self, name, value):
        yield name,sum(value)

if __name__ == '__main__':
    MR_cancellation.run()
