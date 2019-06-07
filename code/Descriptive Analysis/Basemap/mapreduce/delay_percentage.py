from mrjob.job import MRJob
import re
import csv
from mrjob.step import MRStep

WORD_RE = re.compile(r"[\w]+")

class MR_delay_percentage_origin(MRJob):
  
  def mapper(self, _, line):
  	row = next(csv.reader([line]))
  	origin = row[16]
  	delay = row[15]
  	try:
  		delay = int(delay)
  		if delay>0:
  			yield origin,1
  		else:
  			yield origin,0
  	except:
  		pass

  def reducer(self, name, value):
    delay_list = list(value)
    yield name, sum(delay_list)/len(delay_list)

if __name__ == '__main__':
  MR_delay_percentage_origin.run()
