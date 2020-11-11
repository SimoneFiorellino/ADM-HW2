import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def request_five(dataset):

    #use only rows with event_type == 'view'
    dataset_view = dataset[dataset.event_type == 'view']
    dataset_view[dataset_view.index.duplicated()]
    #number of views for hours
    count_view_hour = dataset_view.groupby([dataset_view.event_time.dt.hour]).event_time.count()

    hour_indexes = np.arange(0,24)
    hour_indexes_visited = zip(count_view_hour, hour_indexes)
    #find the part of the day most visited
    hour_most_visited = max(hour_indexes_visited)
    print(f'In what part of the day is your store most visited? {hour_most_visited[1]} o\'clock')
    print(f'Number of views: {hour_most_visited[0]}')

    #Create a plot that for each day of the week show the hourly average of visitors your store has.
    num_days = []
    average_visitors = []
    #group by 'weekday' and then calculate the mean for each day of the week
    for wkday, frame in dataset_view.groupby([dataset_view.event_time.dt.weekday]):
        #print(f"Weekday: {wkday!r}")
        num_days.append(wkday)
        #print(frame.groupby([dataset.event_time.dt.hour]).event_time.count().mean())
        average_visitors.append(round(frame.groupby([dataset.event_time.dt.hour]).event_time.count().mean(), 3))
        

    #print the results
    my_zip = zip(num_days, average_visitors)
    for i in my_zip:
        print(i)