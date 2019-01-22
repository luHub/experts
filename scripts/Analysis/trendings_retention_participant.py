import csv
from functools import reduce
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import datetime
import numpy as np
import xml.etree.ElementTree as ET  
 
def is_present(arg,al):
    for item in al:
        if item == arg:
            return True
    return False  

def separate_retention(key,inv_years,participants):
    index = inv_years.index(key)
    pre_years = []
    for i in range(index+1, len(inv_years)):
        y = inv_years[int(i)]
        list(map(lambda x:pre_years.append(x),participants[y]))
    


    ret_p = list(filter(lambda i: is_present(i,set(participants[key])),set(pre_years)))
    new_p = list(filter(lambda i: not is_present(i,set(pre_years)),set(participants[key])))
    # print(len(ret_p)-len(new_p))
    # print('participants: ',key ,len(set(participants[key])))
    # print('prev_years_present',len(set(pre_years))) 
    # print('ret_p: ',len(ret_p)) 
    # print('new_p: ',len(new_p))

    return (new_p,ret_p)

def create_bar(N,new_p,ret_p,bar_ind,w):
    #for i in range(0,N):
    print(bar_ind)
    plt.bar(bar_ind, new_p, w,  color='none', edgecolor='black', hatch="--")
    plt.bar(bar_ind, ret_p, w, bottom = new_p,  color='black', edgecolor='black', hatch="----" )




def extract_dataset(path):
    tree = ET.parse(path)  
    root = tree.getroot()

    years = []
    participants = dict()
    yc = 0
    for item in root.iter('year'):
        year =  item.attrib['date']
        part = list(map(lambda elem: elem.text,root[yc]))  
        yc = yc + 1
        participants[year] = part
        years.append(year)
    inv_years = sorted(years,reverse=True)

    return sorted(years),dict(map(lambda y:(y,separate_retention(y,inv_years,participants)),inv_years))


trending_user_path = "Add path to participants in a year XML"
years, participants = extract_dataset(trending_user_path)
print('years: ',years)
#print('ember: ',ember_plot)

N = len(years)
participants_retained = list(map(lambda x: len(participants[x][1]),years))
participants_new = list(map(lambda x: len(participants[x][0]),years))
print('> ',participants_new)
print('> ',participants_retained)

    


ind = np.arange(N)
width = 0.15      
space = 0.02
bar_ind = list(map(lambda x: x+(width+space),ind))
create_bar(N,participants_new,participants_retained,bar_ind,width)


tick_pos = list(map(lambda x: x+1/2*width,bar_ind))
plt.ylabel('Participants')
# plt.title('Participants by new and active from previous years')
plt.xticks(tick_pos, years)
plt.yticks(np.arange(0, 7000, 500)) 
#plt.legend((pa[0], sb[0],tb[0],fb[0]), ('Angular', 'React','VUE','Ember'))
plt.show()

# react_ret = (0, 4124, 5600 )
# react_new = ( 13890, 17407, 13700 )

# vue_ret = (0, 4124, 5600 )
# vue_new = ( 13890, 17407, 13700 )


# ind = np.arange(N)    # the x locations for the groups
# width = 0.15       # the width of the bars: can also be len(x) sequence
# space = 0.02
# pa = plt.bar(ind, new, width,color='none', edgecolor='black', hatch="++")
# pa_r = plt.bar(ind, retained, width, bottom = new,color='none', edgecolor='black', hatch="++++" )

# second_bar_ind = list(map(lambda x: x+width+space,ind))
# sb = plt.bar(second_bar_ind, react_new, width, color='none', edgecolor='black', hatch="xx")
# sb_r = plt.bar(second_bar_ind, react_ret, width, bottom = react_new, color='none', edgecolor='black', hatch="xxxx" )

# third_bar_ind = list(map(lambda x: x+2*(width+space),ind))
# tb = plt.bar(third_bar_ind, vue_new, width,  color='none', edgecolor='black', hatch="--")
# tb_r = plt.bar(third_bar_ind, vue_ret, width, bottom = vue_new,  color='none', edgecolor='black', hatch="----" )

# fourth_bar_ind = list(map(lambda x: x+3*(width+space),ind))
# fb = plt.bar(fourth_bar_ind, vue_new, width, color='none', edgecolor='black', hatch="..")
# fb_r = plt.bar(fourth_bar_ind, vue_ret, width, bottom = vue_new, color='none', edgecolor='black', hatch="....")

# tick_pos = list(map(lambda x: x+1/2*width,second_bar_ind))
# plt.ylabel('Participants')
# plt.title('Participants by new and active from previous years')
# plt.xticks(tick_pos, ('2016', '2017', '2018'))
# plt.yticks(np.arange(0, 25000, 1000)) 
# plt.legend((pa[0], sb[0],tb[0],fb[0]), ('Angular', 'React','VUE','Ember'))
# plt.show()
