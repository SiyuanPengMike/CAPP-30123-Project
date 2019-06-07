from mrjob.job import MRJob
from mrjob.step import MRStep

class MR_airport(MRJob):
# Collect unique airport IATA codes
	def mapper(self,_,line):
		if line.split(',')[0] != 'Year': 
			Org, Des = line.split(',')[16], line.split(',')[17]
			yield Org, 1
			yield Des, 1
	def reducer(self,name,counts):
		yield name, sum(counts)
		
if __name__ == '__main__':
	MR_airport.run()
