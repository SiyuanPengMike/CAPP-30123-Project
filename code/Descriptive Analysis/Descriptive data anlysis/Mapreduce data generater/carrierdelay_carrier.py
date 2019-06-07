from mrjob.job import MRJob
import re
import csv
from mrjob.step import MRStep

WORD_RE = re.compile(r"[\w]+")

class MR_carrierdelay(MRJob):

    def mapper(self, _, line):   
        row = next(csv.reader([line]))
        carrier = row[8]
        carrierdelay0 = row[24]
        try:
            carrierdelay = int(carrierdelay0)
            yield carrier, carrierdelay
        except:
            pass

    def reducer(self, name, value):
        delay_list = list(value)
        yield name,sum(delay_list)/len(delay_list)

if __name__ == '__main__':
    MR_carrierdelay.run()
