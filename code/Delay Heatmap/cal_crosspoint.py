import csv
import pandas as pd
import timeit
import multiprocessing
from dask import compute, delayed
import dask.multiprocessing


df = pd.read_csv("whole_data.csv")
# Only has a departure delay time for at least 30 minutes
# will be counted as a delay flight.
df30 = df[df['DepDelay']>30]

def cal_crosspoint(airline1,airline2, dic):
    '''
    Using the origin and destination of two filghts to generate the cross point
    for them. If these two flights indeed has a cross point, return its location;
    otherwise, just return 0.
    '''
    if airline1 == airline2:
        return 0
    else:
        origin1, dest1 = airline1
        x11,y11 = dic[origin1][0], dic[origin1][1]
        x12,y12 = dic[dest1][0], dic[dest1][1]
        origin2, dest2 = airline2
        x21,y21 = dic[origin2][0], dic[origin2][1]
        x22,y22 = dic[dest2][0], dic[dest2][1]

        k1 = (y12-y11)/(x12-x11)
        k2 = (y22-y21)/(x22-x21)

        x = (y21 - y11 + k1*x11-k2*x21)/ (k1-k2)
        y = k1*(x-x11)+y11

        xt11, xt12 = min(x11,x12), max(x11,x12)
        xt21, xt22 = min(x21,x22), max(x21,x22)

        if x>max(xt11, xt21) and x<min(xt12, xt22):
            return (x,y)
        else:
            return 0

dic = dict()
with open('airport-with-time.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        try:
        	'''
        	Generate the dictionary, in which key is the IATA code for that airport,
        	and value is the latitude and longitude for that airport.
        	'''
            dic[row[1]] = (float(row[3]),float(row[4]))
        except:
            pass

def each_day(year, month, day):
	'''
	Generate the cross point by any two delayed flights in the same day.
	Even though a point could be the cross point for multiple flight pairs,
	the weight of it will still be one (considering the weight for a point 
	just represent that this point is uncapable for flight in that day).
	'''
    df_m_d = df30[(df30['Year']==year)&(df30['Month']==month)&(df30['DayofMonth']==day)]
    inter_list = list()
    for i, (dep, air) in df_m_d[['Origin','Dest']].iterrows():
        inter_list.append((dep, air))
    inter_dict_m_d = dict()
    n = len(inter_list)
    for i in range(n):
        for k in range(i+1,n):
            try:
                inter_point = cal_crosspoint(inter_list[i], inter_list[k], dic)
                inter_dict_m_d[inter_point] = 1
            except:
                pass
    return inter_dict_m_d



num_cores = multiprocessing.cpu_count()
print('Number of available cores is', num_cores)


start_time = timeit.default_timer()

def gen_inter_dict(y, m, d):
    try:
        each_day_dict = each_day(y, m, d)
        inter_dict = dict()
        for key, value in each_day_dict.items():
            try:
            	'''
            	Summarize the points in the each day dictionary.
            	Round and summarize points into integer so that 
            	it could be represented in the heatmap.
            	'''
                (lat, lon) = key
                new_lat = round(lat)
                new_lon = round(lon)
                new_key = (new_lat, new_lon)
                inter_dict[new_key] = inter_dict.get(new_key,0) + value
            except:
                pass
        return inter_dict

    except:
        return dict()

# Generate the list to record the delayed computation issues prepared by Dask.
lazy_values = []
for y in range(1989,2009):
    for m in range(1,13):
        for d in range(1,32):
            lazy_values.append(delayed(gen_inter_dict)(y,m,d))

# Show the number of cores this computer has.
import multiprocessing
num_cores = multiprocessing.cpu_count()

# Compute these deplayed issues by Dask (parallel computing).
results_par  = compute(*lazy_values , scheduler=dask.multiprocessing.get, num_workers=num_cores)


elapsed_time = timeit.default_timer() - start_time
print('Elapsed time=', elapsed_time, 'seconds')

inter_dict = dict()
# Summarize all dicitonary(day based, 365) into one dictionary (year based, 1)
for i in results_par:
    for key,value in i.items():
        inter_dict[key] = inter_dict.get(key,0) + value

for key,value in inter_dict.items():
    inter_dict[key] = int(value / 20)

