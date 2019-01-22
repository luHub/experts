import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
 
import xml.etree.ElementTree as ET  

def extract_dataset(path):
    tree = ET.parse(path)  
    root = tree.getroot()

    time = []
    q = []
    def populate_x_y(xy_tuple):
        time.append(xy_tuple[0])
        q.append(int(xy_tuple[1]))

    xy_tuple = list(map(lambda elem: (elem.attrib['date'],elem.text),root))
    xy_sorted = sorted(xy_tuple,key=lambda tuple: tuple[0])
    list(map(lambda xy_tuple: populate_x_y(xy_tuple),xy_sorted))
    return time,q



q_path = 'Add path to questions trending XML'
q_label = 'Add a title'
time_q, ember_q = extract_dataset(q_path)

#ember_a = '/home/lucio/python_webscience_lucio/datasets_work/ember/trendings/answers_trending_ember.xml'
#a_path = '/home/lucio/python_webscience_lucio/datasets_work/angular/trendings/answers_trendings_angular.xml'
#a_label = 'A. Angular'
a_path = 'Add path to answers trending XML'
a_label = 'Add a title' 
time_a, ember_a = extract_dataset(a_path)


fig, ax = plt.subplots()
plt.xticks(rotation=70)
ax.plot_date(time_q, ember_q, linestyle='--', color='black', marker='', label=q_label)
ax.plot_date(time_a, ember_a, linestyle=':', color='black', marker='', label=a_label)

ax.legend() 
# ax.grid(True)
# ax.annotate('Test', (mdates.date2num(x[1]), y[1]), xytext=(15, 15), 
#             textcoords='offset points', arrowprops=dict(arrowstyle='-|>'))
reduced_ticks = []
labels = []
for index, val in enumerate(time_q):
    if not index%12 and index+3<len(time_q)-1:
        reduced_ticks.append(time_q[index+3])
        labels.append(time_q[index+3])
    else:
        labels.append('')
    
ax.set_xticklabels(labels)
fig.autofmt_xdate()
plt.show()
