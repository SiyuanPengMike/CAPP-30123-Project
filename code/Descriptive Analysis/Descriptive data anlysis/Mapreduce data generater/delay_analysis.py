from mrjob.job import MRJob
import re
import csv
from mrjob.step import MRStep

WORD_RE = re.compile(r"[\w]+")

class MR_delay_analysis(MRJob):

    def mapper(self, _, line):   
        row = next(csv.reader([line]))
        month = row[1]
        delay0  = row[14]
        try:
            delay = int(delay0)
            if delay>=15:
                yield month, delay
        except:
            pass

    def reducer(self, name, value):
        delay_list = list(value)
        yield name,sum(delay_list)/len(delay_list)

if __name__ == '__main__':
    MR_delay_analysis.run()
