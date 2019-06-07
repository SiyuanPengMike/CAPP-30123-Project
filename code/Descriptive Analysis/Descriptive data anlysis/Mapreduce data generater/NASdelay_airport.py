from mrjob.job import MRJob
import re
import csv
from mrjob.step import MRStep

WORD_RE = re.compile(r"[\w]+")

class MR_NASdelay(MRJob):

    def mapper(self, _, line):   
        row = next(csv.reader([line]))
        origin = row[16]
        NASdelay0 = row[26]
        try:
            NASdelay = int(NASdelay0)
            yield origin, NASdelay
        except:
            pass

    def reducer(self, name, value):
        delay_list = list(value)
        yield name,sum(delay_list)/len(delay_list)

if __name__ == '__main__':
    MR_NASdelay.run()
