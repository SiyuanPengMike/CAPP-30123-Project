from mrjob.job import MRJob
import re
import csv
from mrjob.step import MRStep

WORD_RE = re.compile(r"[\w]+")

class MR_flightcount(MRJob):
  
  def mapper(self, _, line):
    row = next(csv.reader([line]))
    origin = row[16]
    yield origin, 1

  def combiner(self, name, value):
    yield name,sum(value)

  def reducer(self, name, value):
    yield name,sum(value)

if __name__ == '__main__':
  MR_flightcount.run()
