#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 17:22:03 2020

@author: eugeniobaldo
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def trending_products(dataset):
    dataset_purchase=dataset[dataset["event_type"]=="purchase"]
    dataset_sold_products=dataset_purchase.groupby(["product_id","main category"]).product_id.count()\
    .sort_values(ascending=False)

    dataset_most_sold_products=dataset_sold_products[0:99]
    dataset_category_sales=dataset_most_sold_products.groupby("main category").sum().sort_values(ascending=False)
    
    plt.figure()
    dataset_category_sales.plot.barh(figsize=(16,9),\
    title="categories sales of the most 100 trending products during the month",\
    color="lightblue", edgecolor="yellow", alpha=0.5)

    plt.show()
    return dataset_category_sales


    
    
    
def subcategories(dataset):
    dataset_view=dataset[dataset["event_type"]=="view"]
    dataset_viewed=dataset_view.groupby(["product_id","category_code"]).product_id.count()\
    .sort_values(ascending=False)
    dataset_most_viewed=dataset_viewed[0:99]
    dataset_category_views=dataset_most_viewed.groupby("category_code").sum().sort_values(ascending=False)
   
    plt.figure()
    dataset_category_views.plot.barh(figsize=(16,9),\
                                 title="sub_categories views of the most 100 trending products during the month",\
                                  color="lightblue", edgecolor="yellow", alpha=0.5)
    plt.show()
    return dataset_category_views
    
def ten_most_sold(dataset,dataset_category_sales):
    i=0
    
    dataset_purchase=dataset[dataset["event_type"]=="purchase"]
    dataset_sold_products=dataset_purchase.groupby(["product_id","main category"]).product_id.count()\
    .sort_values(ascending=False)

    dataset_most_sold_products=dataset_sold_products[0:99]
    dataset_category_sales=dataset_most_sold_products.groupby("main category").sum().sort_values(ascending=False)
    series_main_category=dataset_category_sales.index.to_series()
    
    while i<len(dataset_category_sales):
        category=series_main_category[i]
        dataset_new=dataset_purchase[dataset_purchase["main category"]==category]
        result=dataset_new.groupby(["product_id","main category"]).product_id.count()\
        .sort_values(ascending=False).head(10)
        print(category.upper())
        print(result)
        i=i+1
    return 
    