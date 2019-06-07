from mrjob.job import MRJob
import re
import csv
from mrjob.step import MRStep

WORD_RE = re.compile(r"[\w]+")

class MR_delay_status(MRJob):

    def mapper(self, _, line):   
        row = next(csv.reader([line]))
        delay0 = row[15]
        diverted0 = row[23]
        cancelled0 = row[21]
        try:
            delay, diverted, cancelled = int(delay0),int(diverted0),int(cancelled0)
            if diverted==1:
                yield "diverted",1
            elif cancelled==1:
                yield "cancelled",1
            elif delay<15:
                yield "no delay",1
            elif delay>=15 and delay<60:
                yield "slightly delay",1
            elif delay>=60:
                yield "highly delay",1


        except:
            pass


    def combiner(self, name, value):
        yield name,sum(value)

    def reducer(self, name, value):
        yield name,sum(value)

if __name__ == '__main__':
    MR_delay_status.run()
