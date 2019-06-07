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

# Import the final_dict calculated in the cal_crosspoint.py
final_dict = inter_dict

#________________________________________
# define properties of markers and labels
colors = ['#EEE8AA', '#FFA07A', '#F08080', '#FF6347', '#DC143C', '#800000', '#000000']
size_limits = [0, 1000, 5000, 20000, 40000, 60000, 100000, 750000]
label_delay_new = []
for i in range(len(size_limits)-1):
    label_delay_new.append("{} <.< {}".format(size_limits[i], size_limits[i+1])) 

plt.figure(figsize=(20,20))
#____________________________________________________________
map = Basemap(resolution='i',llcrnrlon=-180, urcrnrlon=-50,
              llcrnrlat=10, urcrnrlat=75, lat_0=0, lon_0=0,)
map.shadedrelief()
map.drawcoastlines()
map.drawcountries(linewidth = 3)
map.drawstates(color='0.3')
#_____________________
# put airports on map
for key, value in final_dict.items():
    (lat, lon) = key
    x, y = map(lon, lat)
    isize = [i for i, val in enumerate(size_limits) if val <= value]
    ind = isize[-1]
    map.plot(x, y, marker='s', markersize = 9, markeredgewidth = 1, color = colors[ind], alpha=0.6,
             markeredgecolor='k', label = label_delay_new[ind])
#_____________________________________________
# remove duplicate labels and set their order
handles, labels = plt.gca().get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))
key_order = label_delay_new
new_label = OrderedDict()
for key in key_order:
    new_label[key] = by_label[key]
plt.legend(new_label.values(), new_label.keys(), loc = 1, prop= {'size':11},
           title='Delayed Number', frameon = True, framealpha = 1)
plt.show()

