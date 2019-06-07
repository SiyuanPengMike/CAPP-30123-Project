import datetime, warnings, scipy 
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import ConnectionPatch
from collections import OrderedDict
from matplotlib.gridspec import GridSpec
from mpl_toolkits.basemap import Basemap
from sklearn import metrics, linear_model
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from scipy.optimize import curve_fit
plt.rcParams["patch.force_edgecolor"] = True
plt.style.use('fivethirtyeight')
mpl.rc('patch', edgecolor = 'dimgray', linewidth=1)
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "last_expr"
pd.options.display.max_columns = 50
%matplotlib inline
warnings.filterwarnings("ignore")


count_flights = pd.read_csv('flight_count.txt', sep="\t",header = None)

airports = pd.read_csv('data/airports.dat', header = None, 
                   names = ['index', 'name', 'city', 'country', 'IATA', 'ICAO', 
                            'latitude', 'longitude', 'altitude', 'time zone', 
                            'DST', 'Tz database time zone', 'type', 'source'])

USA_airport = airports[(airports['country'] == 'United States')&(airports['IATA'] != '\\N')][['IATA','latitude','longitude']]


# This plot is used to show the number of delay flights for airports.
# The larger the number of delay airplanes in an airport, the larger of the circle to represent it.


plt.figure(figsize=(20,20))
#________________________________________
# define properties of markers and labels
colors = ['yellow', 'red', 'lightblue', 'purple', 'green']
size_limits = [1, 100, 1000, 10000, 100000, 1000000]
label_flight = []
for i in range(len(size_limits)-1):
    label_flight.append("{} <.< {}".format(size_limits[i], size_limits[i+1])) 
#____________________________________________________________
map = Basemap(resolution='i',llcrnrlon=-180, urcrnrlon=-50,
              llcrnrlat=10, urcrnrlat=75, lat_0=0, lon_0=0,)
map.shadedrelief()
map.drawcoastlines()
map.drawcountries(linewidth = 3)
map.drawstates(color='0.3')
#_____________________
# put airports on map
for index, (code, y,x) in USA_airport[['IATA', 'latitude', 'longitude']].iterrows():
    if code in count_flights:   
        x, y = map(x, y)
        isize = [i for i, val in enumerate(size_limits) if val < count_flights[code]]
        ind = isize[-1]
        map.plot(x, y, marker='o', markersize = 3*ind+5, markeredgewidth = 1, color = colors[ind],
                 markeredgecolor='k', label = label_flight[ind])
#_____________________________________________
# remove duplicate labels and set their order
handles, labels = plt.gca().get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))
key_order = ('1 <.< 100', '100 <.< 1000', '1000 <.< 10000',
             '10000 <.< 100000', '100000 <.< 1000000')
new_label = OrderedDict()
for key in key_order:
    new_label[key] = by_label[key]
plt.legend(new_label.values(), new_label.keys(), loc = 1, prop= {'size':11},
           title='Number of flights per year', frameon = True, framealpha = 1)
plt.show()