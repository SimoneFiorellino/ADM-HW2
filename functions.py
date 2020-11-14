import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def request_five(dataset):

    #use only rows with event_type == 'view'
    dataset_view = dataset[dataset.event_type == 'view']
    #number of views for hours
    count_view_hour = dataset_view.groupby([dataset_view.event_time.dt.hour]).event_time.count()

    hour_indexes = np.arange(0,24)
    hour_indexes_visited = zip(count_view_hour, hour_indexes)

    #find the part of the day most visited
    hour_most_visited = max(hour_indexes_visited)
    print(f'In what part of the day is your store most visited? {hour_most_visited[1]} o\'clock')
    print(f'Number of views: {hour_most_visited[0]}')

    #plot Number of views for each hour
    df = pd.DataFrame(list(zip(count_view_hour, hour_indexes))).set_index(1)
    ax = df.plot(kind='bar', title = 'Number of views for each hour')
    ax.legend(["number of views"]);

    #Create a plot that for each day of the week show the hourly average of visitors your store has.
    # 0 is monday
    num_days = []
    average_visitors = []
    #group by 'weekday' and then calculate the mean for each day of the week
    for wkday, frame in dataset_view.groupby([dataset_view.event_time.dt.weekday]):
        #print(f"Weekday: {wkday!r}")
        num_days.append(wkday)
        #print(frame.groupby([dataset.event_time.dt.hour]).event_time.count().mean())
        average_visitors.append(round(frame.groupby([dataset.event_time.dt.hour]).event_time.count().mean(), 3))
        

    #print "Hourly avarage of views for each day of the week"
    weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # my_zip = zip(num_days, average_visitors)
    # for i in my_zip:
    #     print(i)
    df = pd.DataFrame(list(zip(weekday, average_visitors))).set_index(0)
    ax = df.plot(kind='bar', title = 'Hourly average of views for each day of the week')
    ax.legend(["Hourly avarage of views"]);


def request_six(dataset):

    #calculate the overall conversion rate
    num = dataset[dataset.event_type == 'purchase'].product_id.count()      #number of purchases
    denom = dataset[dataset.event_type == 'view'].product_id.count()        #nukber of views
    overall_conv_rate = num / denom     #rate
    print('Find the overall conversion rate of your store:')
    print(f'Overall conversion rate: {round(overall_conv_rate, 3)}')
    #visualization of different between purchases and views
    tot = num + denom
    df = pd.DataFrame({'overall conversion rate': [(num/tot)*100, (denom/tot)*100]},
                  index=['purchases', 'views'])
    plot = df.plot.pie(y='overall conversion rate', figsize=(5, 5))
    plt.show()

    #number of purchases of each category
    purchases_dataset = dataset[dataset.event_type == 'purchase']
    purchases_dataset = purchases_dataset.dropna(subset=["category_code"])

    purchases_dataset.category_code.replace('(?=\.).*','',regex=True, inplace = True)   #we are looking only for the main category. '(?=\.).*' finds the word before the first point
    category_list = purchases_dataset.category_code.unique() #list of all main category

    #plot: Number of purchases of each category
    purchases_dataset = purchases_dataset.groupby([purchases_dataset.category_code]).category_code.count()
    purchases_dataset.plot.barh(figsize=(16,9), title="Number of purchases of each category")
    plt.show()

    #number of views of each category
    view_dataset = dataset[dataset.event_type == 'view']
    view_dataset = view_dataset.dropna(subset=["category_code"])

    view_dataset.category_code.replace('(?=\.).*','',regex=True, inplace = True)

    view_dataset = view_dataset.groupby([view_dataset.category_code]).category_code.count()
    
    #conversion rate of each category in decreasing order
    y = zip(purchases_dataset, view_dataset)
    zip_conversion_rate = zip(category_list, map(lambda y: round(y[0]/y[1], 3) , y))    #it crates an iterable object with 'category' and 'conversion rate'
    zip_conversion_rate = sorted(zip_conversion_rate, key = lambda t: t[1], reverse=True) #decreasing order for the plot

    #plot
    df = pd.DataFrame(list(zip_conversion_rate)).set_index(0)
    ax = df.plot(kind='bar', title = 'conversion rate of each category in decreasing order')
    ax.legend(["conv_rate"])
    ax.hlines(round(overall_conv_rate, 3), -10, 20, linestyles='dashed')
    ax.annotate('overall conversion rate',(6,round(overall_conv_rate, 3)+0.002));

#Prove that the pareto principle applies to your store.
def request_seven(dataset):

    my_sum = 0
    my_array = []
    x = dataset[dataset.event_type == 'purchase'].groupby([dataset.user_id])['price'].agg('sum').sort_values(ascending=False)
    
    for i in x:
        my_sum+=int(i)  #for every step i sum customer's expenses
        my_array.append(my_sum)
    
    #normalized array
    my_array_normalized = [float(i)/max(my_array) for i in my_array]
    
    #visualize our results
    plt.plot(my_array_normalized, '-gD', markevery=[int(len(my_array_normalized)/100*20)], label='% comes from about 20% of your customers')
    plt.legend(bbox_to_anchor=(1, 0.2), loc='upper right')
    plt.xlabel('customers')  
    plt.ylabel('%') 
    plt.title('80/20 rule')
    plt.show()

    sum_twenty = my_array[int(len(my_array_normalized)/100*20)-1]

    print(f'Most of the business, around {int((sum_twenty/my_array[-1])*100)}%, likely comes from about 20% of customers')