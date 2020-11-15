#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 07:42:23 2020

@author: eugeniobaldo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#rq2
def add_category(dataset):
    
    dataset=dataset.dropna(subset=["category_code"])
    sub_categories=dataset["category_code"].to_list()
    
    categories=[]
    for i in range(len(sub_categories)):
        sub_category=sub_categories[i]
        string=""
        for char in sub_category:
            if char!=".":
                string=string+char
            else:
                break
        categories.append(string)

    dataset["main_category"]=categories
    return dataset


    
def trending_products(dataset):
    dataset_purchase=dataset[dataset["event_type"]=="purchase"]
    dataset_sold_products=dataset_purchase.groupby(["product_id","main_category"]).product_id.count()\
    .sort_values(ascending=False)

    dataset_most_sold_products=dataset_sold_products[0:99]
    dataset_category_sales=dataset_most_sold_products.groupby("main_category").sum().sort_values(ascending=False)
    
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
    
def ten_most_sold(dataset):
    i=0
    
    dataset_purchase=dataset[dataset["event_type"]=="purchase"]
    dataset_sold_products=dataset_purchase.groupby(["product_id","main_category"]).product_id.count()\
    .sort_values(ascending=False)

    dataset_most_sold_products=dataset_sold_products[0:99]
    dataset_category_sales=dataset_most_sold_products.groupby("main_category").sum().sort_values(ascending=False)
    series_main_category=dataset_category_sales.index.to_series()
    
    while i<len(dataset_category_sales):
        category=series_main_category[i]
        dataset_new=dataset_purchase[dataset_purchase["main_category"]==category]
        result=dataset_new.groupby(["product_id","main_category"]).product_id.count()\
        .sort_values(ascending=False).head(10)
        print(category.upper())
        print(result)
        i=i+1
    return 
#rq3
    
def average_price(category_input, dataset_month):
    
    dataset_new=dataset_month[dataset_month["main_category"]==category_input]
    
    series=dataset_new.groupby(["brand","product_id","price"]).product_id.count()
    arr=(series.index)
    prices=[]
    brands=[]
    i=0
    while i<len(arr):
        prices.append(arr[i][2])
        brands.append(arr[i][0])
        i=i+1
    couple=zip(brands,prices)
    dataset2=pd.DataFrame(data=couple,columns=["brand","price"])  
    brand_average=dataset2.groupby(["brand"]).mean()
    
    return brand_average

def most_expensive_brands(categories,dataset):
    brands=[]
    prices=[]
    costly_brands=[]
    category_list=[]
    price_list=[]
    
    #the following cycle iterates for all the categories 
    # in order to find the most expensive brand for that category
    for cat in categories:
        dataset_new=dataset[dataset["main_category"]==cat]
        series=dataset_new.groupby(["brand","product_id","price"]).product_id.count()
        
        arr=series.index    #with this function it is obtained an array with:
                            #column0=brand
                            #column1=product_id
                            #column2=price
        
        prices=[]
        brands=[]
        i=0
        while i<len(series)  :
            prices.append(arr[i][2])   #select the price columns
            brands.append(arr[i][0])   #select the brand columns
            i=i+1
        couple=zip(brands,prices)   #creates a tuple of the brand and relative price
        dataset2=pd.DataFrame(data=couple,columns=["brand","price"]) #creating a new dataset with all tuples
        
        brand_max=dataset2.groupby(["brand"]).mean().sort_values(by=["price"],ascending=False) 
        
        
        
        price_max=brand_max.iloc[0].to_list()
        price_max_value=price_max[0]           
        brand_max=brand_max.index
        brand_max=brand_max[0]
        
        costly_brands.append(brand_max)
        category_list.append(cat)
        price_list.append(price_max_value)
    
    triple=list(zip(category_list,costly_brands,price_list))
    result=pd.DataFrame.from_records(triple,columns=["category","brand","average_price"]).sort_values(by=["average_price"])   
    result=result.reset_index(drop=True)
    return result
#rq4
def earnings(brand_name,dataset):
    
    brand_name=brand_name.lower()
    dataset_brand=dataset[dataset["brand"]==brand_name]
    dataset_brand=dataset_brand.dropna(subset=["brand"])
    dataset_brand=dataset_brand[dataset_brand["event_type"]=="purchase"]
    earnings_brand=dataset_brand["price"].sum()
    
    return earnings_brand

def price_difference(dataset):
    dataset_brand=dataset.dropna(subset=["brand","price"])
    dataset_brand=dataset_brand[dataset_brand["event_type"]=="purchase"]
    dataset_brand=dataset_brand.groupby(["brand"]).price.mean().sort_values()

    return dataset_brand

def earnings_loss(dataset1,dataset2):
    #obtaining the useful datasets 
    dataset_brand1=dataset1.dropna(subset=["brand","price"])
    dataset_brand1=dataset_brand1[dataset_brand1["event_type"]=="purchase"]
    dataset_brand1=dataset_brand1.groupby(["brand"]).price.sum().sort_values()
    series_brand1=dataset_brand1.sort_index()
    dataset_brand2=dataset2.dropna(subset=["brand","price"])
    dataset_brand2=dataset_brand2[dataset_brand2["event_type"]=="purchase"]
    dataset_brand2=dataset_brand2.groupby(["brand"]).price.sum().sort_values()
    series_brand2=dataset_brand2.sort_index()
    diff1=series_brand1.index.difference(series_brand2.index)
    diff2=series_brand2.index.difference(series_brand1.index)
    dataset_brand1=series_brand1.drop(diff1)
    dataset_brand2=series_brand2.drop(diff2)
    #here I computer the percentage variation
    percentage_change=[]
    
    for element in range(len(dataset_brand1)):

        value=round((dataset_brand2[element]-dataset_brand1[element])/(dataset_brand1[element])*100,2)
        
        percentage_change.append(value)
    
    percentage_series=pd.Series(data=percentage_change,index=dataset_brand1.index, name="variations between october and november per brand in percentage")
    percentage_series=percentage_series.sort_values()
    
    worst_performance=percentage_series[0:3]

    value_list=worst_performance.values
    brand_list=worst_performance.index
    for i in range(len(brand_list)):
        print(brand_list[i]," had a percentage decrease, between october 2019 and november 2019 of \n",value_list[i],"%")

    return 