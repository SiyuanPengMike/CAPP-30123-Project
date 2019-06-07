from mrjob.job import MRJob
from mrjob.step import MRStep

class MR_connecting(MRJob):
	# Collect each information for flight
	def mapper(self,_,line):
		# Use origin, destination, firm and flight as key, departure and arrival delay time as value, record the information
		if line.split(',')[0] != 'Year': 
			CRSDep, CRSArr, Flight, Firm, Org, Des = line.split(',')[5], line.split(',')[7], line.split(',')[9], line.split(',')[8], line.split(',')[16], line.split(',')[17]
			Depdelay, Arrdelay = line.split(',')[15], line.split(',')[14]
			if Depdelay != 'NA' :
				Depdelay = int(Depdelay)
			if Arrdelay != 'NA':
				Arrdelay = int(Arrdelay)
			label2 = '{} to {} firm {} flight {}'.format(Org, Des, Firm, Flight)
				
			yield label2, (Depdelay, Arrdelay, 1)
	def combiner(self,name,counts):
		# Calculate the sum of departure delay, arrival delay and number of flights for each flight respectively.
		def sumdelay(x):
			List1 = []
			List2 = []
			List3 = []
			for k in x:
				if k[0] != 'NA':
					List1.append(k[0])
				if k[1] != 'NA':
					List2.append(k[1])
					List3.append(1)	
			return (sum(List1), sum(List2), sum(List3))
		yield (name, sumdelay(counts))
	def reducer(self,name,counts):
		# Calculate the average departure and arrival delay for each flight
		def avgdelay(x):
			List1 = []
			List2 = []
			List3 = []
			for k in x:
				List1.append(k[0])
				List2.append(k[1])
				List3.append(k[2])
			Depdelay, Arrdelay, counts = sum(List1), sum(List2), sum(List3)
			if counts == 0:
				return 'All flight cancelled'
			return (Depdelay/counts, Arrdelay/counts)
		yield name, avgdelay(counts)
		
if __name__ == '__main__':
	MR_connecting.run()
