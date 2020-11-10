import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def request_seven(dataset):
    my_sum=0
    my_array = []
    x = dataset[dataset.event_type == 'purchase'].groupby([dataset.user_id])['price'].agg('sum').sort_values(ascending=False)
    
    for i in x:
        my_sum+=int(i)
        my_array.append(my_sum)

    my_array_normalized = [float(i)/max(my_array) for i in my_array]

    plt.plot(my_array_normalized, label='my plot')
    plt.legend(bbox_to_anchor=(1, 0.2))
    plt.show()

    count=0
    sum_twenty=0

    for i in my_array:
        count+=1
        
        if count==int(len(my_array)/100*20):
            sum_twenty+=i
            break
    #print(sum_twenty)

    return print(f'20% of purchases: {sum_twenty}\n80% of purchases: {max(my_array)-sum_twenty}\nRatio: {sum_twenty/max(my_array)}')