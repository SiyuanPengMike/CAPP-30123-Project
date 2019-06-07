# import data and build arrays and dictionaries to store data
airports = []
with open('airports.txt','r') as f:
	for line in f:
		airport = line.split('"')[1]
		airports.append(airport)
flights = dict()
with open('timelist.txt','r') as f:
	for line in f:
		line = line.strip()
		flight = line.split('"')[1]
		origin_pairs = line.split('[')[2:]
		final_list = []
		for pair in origin_pairs:
			pair = pair.strip('],')
			pair = pair.strip(']]')
			elements = pair.split(',')
			elements[0] = elements[0].strip('"')
			if len(elements[1]) == 2:
				elements[1] = '00'+elements[1]
			elif len(elements[1]) == 3:
				elements[1] = '0'+elements[1]
			elif len(elements[1]) == 1:
				elements[1] = '000'+elements[1]
			if len(elements[2]) == 2:
				elements[2] = '00'+elements[2]
			elif len(elements[2]) == 3:
				elements[2] = '0'+elements[2]
			elif len(elements[2]) == 1:
				elements[2] = '000'+elements[2]
			final_list.append((elements[0],elements[1],elements[2]))
		flights[flight] = final_list
# generate straight flight list and potential transition pair dictionary
def pair_list(airport, flight):
	# for each pair of airports,check whether there is straight flight between them
	direct = []
	connect = []
	for Org in airport:
		for Des in airport:
			if Org != Des:
				if "{} to {}".format(Org, Des) in flight:
					direct.append((Org, Des))
				else:
					connect.append((Org, Des))
	return direct, connect
def connect_dict(airport, flight):
	''' 
	for each pair of airports that don't have straight flight, 
	try to find a third airport for transition and store the possible route
	'''
	direct, connect = pair_list(airport, flight)
	connect_dict = dict()
	count = 0
	for pair1 in connect:
		count+=1
		Org, Des = pair1
		label = '{} to {}'.format(Org, Des)
		connect_dict[label] = []
		for mid in airport:
			if (Org, mid) in direct and (mid, Des) in direct:
				connect_dict[label].append((Org, mid, Des))
		print(count)
	return connect_dict
connect_dict = connect_dict(airports, flights)
# store the dictionary of possible transition routes for each pair of airports that don't have straight flight in a text file
f = open('connect_dict.txt', 'w')
f.write(str(connect_dict))
f.close()