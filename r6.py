import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# def conversion_rate(zip_list):
#     return zip_list[0]/zip_list[1]

def request_six(dataset):
    num = dataset[dataset.event_type == 'purchase'].groupby([dataset.product_id]).product_id.count().sum()
    denom = dataset[dataset.event_type == 'view'].groupby([dataset.product_id]).product_id.count().sum()
    overall_conv_rate = num / denom
    print(f'Overall conversion rate: {overall_conv_rate}')

    purchases_dataset = dataset[dataset.event_type == 'purchase']
    purchases_dataset = purchases_dataset.dropna(subset=["category_code"])

    purchases_dataset.category_code.replace('(?=\.).*','',regex=True, inplace = True)
    category_list = purchases_dataset.category_code.unique()

    purchases_dataset = purchases_dataset.groupby([purchases_dataset.category_code]).category_code.count()
    purchases_dataset.plot.barh(figsize=(16,9),\
                                    title="Number of purchases of each category",\
                                    color="white", edgecolor="black", alpha=0.5)
    plt.show()

    view_dataset = dataset[dataset.event_type == 'view']
    view_dataset = view_dataset.dropna(subset=["category_code"])

    view_dataset.category_code.replace('(?=\.).*','',regex=True, inplace = True)

    view_dataset = view_dataset.groupby([view_dataset.category_code]).category_code.count()
    
    y = zip(purchases_dataset, view_dataset)
    
    zip_conversion_rate = zip(category_list, map(lambda y: y[0]/y[1] , y))
    zip_conversion_rate = sorted(zip_conversion_rate, key = lambda t: t[1], reverse=True)
    for i in zip_conversion_rate:
        print(i)