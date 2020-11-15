
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import time

#rq1 (a)
def on_avg_userSess(dataset):
    #Getting event-type on every user_session
    OnAverage_operation = dataset.pivot_table(index=['user_session','event_type'], aggfunc='size')

    #Getting Average of events users perform 
    plt.figure(figsize=(16,8))
    daataf = np.round(OnAverage_operation.groupby(['event_type']).mean(),3)
    daataf['removefromCart'] = np.round(daataf['cart']-daataf['purchase'],3)
    plt.title("Operation on Average in session by User",fontsize=17)
    plt.xlabel("Events",fontsize=15)
    plt.ylabel("Number of times",fontsize=15)
    plt.xticks(rotation=15)
    plt.bar(['Cart ({})'.format(daataf['cart']),'Purchase ({})'.format(daataf['purchase']),'View ({})'
             .format(daataf['view']),'RemoveFromCart ({})'.format(daataf['removefromCart'])],daataf,
            width = 0.6,align='edge',bottom=0)
#(b)   
def user_view_prod(dataset):
    OnAverage_viewProduct = dataset.pivot_table(index=['user_id','product_id'],
                                                    columns=['event_type'],aggfunc='size')
    Index_label = OnAverage_viewProduct[OnAverage_viewProduct['cart']>0]
    Index_label = Index_label.drop(['purchase'],axis=1)
    Index_label.head(15)
    return Index_label,OnAverage_viewProduct

#(c)
def find_prob(OnAverage_viewProduct):
    Index_label_C = OnAverage_viewProduct[OnAverage_viewProduct['purchase']>1]
    Index_label_C = Index_label_C.drop(['view'],axis=1)
    Index_label_C = Index_label_C.fillna(0)
    Index_label_C['probability in %'] = np.round((Index_label_C['purchase'] / (Index_label_C['cart']+Index_label_C['purchase'])*100),1)

    #Probability Product Wise
    Index_label_C.head(10)
    return Index_label_C

#(e)
def avg_on_viewPurch(dataset):
    dataset = dataset.sort_index(by=["user_id"])#h(10000000)
    Sample = dataset[["user_id","product_id","event_time","event_type"]]
    Sample = Sample.sort_index(by=["user_id","event_time","product_id"])
    get_data = Sample.groupby(by=["user_id","product_id"]).sum()
    get_data = get_data[get_data['event_type'].str.contains('cart')]
    jj = get_data['event_time'].str.slice(0, 19)
    jl = get_data['event_time'].str.slice(23, 42)
    jj = pd.DataFrame(jj)
    jl = pd.DataFrame(jl)

    get_data['View Time'] = jj['event_time']
    get_data['Purchase / Cart Time'] = jl['event_time']
    up_data = get_data
    up_data = up_data[~up_data['event_type'].isin(['cart'])]

    # Data with View Time and Cart Time Separated
    toShow_data = up_data
    
    s1 = up_data['View Time']
    s2 = up_data['Purchase / Cart Time']
    s1Time = []
    s2Time = []

    for i in range(0,len(s2)):
        s1Time.append(time.strptime(s1[i], "%Y-%m-%d %H:%M:%S"))
        s2Time.append(time.strptime(s2[i], "%Y-%m-%d %H:%M:%S"))

    in_min = []
    for i in range(len(s1Time)):
        in_min.append((time.mktime(s2Time[i]) - time.mktime(s1Time[i])) / 60.0)
    avg_mins = in_min
    up_time = []
    for i in in_min:
        if i>=1440:
            data = (i/60)/24
            up_time.append(str(np.round(data,2))+" days")
        elif i>=60:
            data = i/60
            up_time.append(str(np.round(data,2))+" hours")
        elif i>=1:
            data = i
            up_time.append(str(np.round(data,0))+" minutes")
        else:
            data = i*60
            up_time.append(str(np.round(data,0))+" seconds")

    up_data['Difference'] = up_time
    final_data = up_data
    
    return toShow_data, final_data, avg_mins