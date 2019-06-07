from mrjob.job import MRJob
from mrjob.step import MRStep

class MR_connecting(MRJob):
	def mapper(self,_,line):
		'''
		Collect information for each flight, 
		divide them into groups by their origins and destinations. 
		use origin and destination as key, 
		use firm and flight number , planned departure and arrival time as values. 
		'''
		if line.split(',')[0] != 'Year': 
			CRSDep, CRSArr, Flight, Firm, Org, Des = int(line.split(',')[5]), int(line.split(',')[7]), line.split(',')[9], line.split(',')[8], line.split(',')[16], line.split(',')[17]
			Depdelay, Arrdelay = line.split(',')[15], line.split(',')[14]
			if Depdelay != 'NA' :
				Depdelay = int(Depdelay)
			if Arrdelay != 'NA':
				Arrdelay = int(Arrdelay)
			label1 = '{} to {}'.format(Org, Des)
			label2 = '{} to {} firm {} flight {}'.format(Org, Des, Firm, Flight)
				
			yield label1, (Firm+Flight, CRSDep, CRSArr)
	
	def reducer(self,name,counts):
		# Summarize information of all flights for each route
		def sumflight(x):
			List = []
			List2 = []
			for k in x:
				if k[0] not in List:
					List.append(k[0])
					List2.append(k)
			return List2
		yield name, sumflight(counts)
if __name__ == '__main__':
	MR_connecting.run()
