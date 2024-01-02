from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from tkinter import * 
from tkinter.ttk import *

start_date = '2020-12-1'
end_date='2023-2-2'                 #Get dates from drop down calendar. Make a function like getdate()
ticker=input("Enter the ticker")    #Name of ticker -> accept input from textbox getticker()
company=yf.download(tickers=ticker,start=start_date,end=end_date)



def plot():
    d=plt.figure(figsize=(14,5))
    sns.set_style("ticks")
    sns.lineplot(data=company,x="Date",y='Close',color='firebrick')
    sns.despine()
    str="The Stock Price of " + ticker
    plt.title(str,size='x-large',color='blue')
    canvas = FigureCanvasTkAgg(d, 
                               master = root)   
    canvas.draw() 
    canvas.get_tk_widget().pack()

root=Tk()
root.title("Lorem Ipsum")
root.geometry("1920x1080")
label = Label(root, text ="Hello World !").pack()
plot_button = Button(master = root,  
                     command = plot,  
                     text = "Plot") 
plot_button.pack() 
root.mainloop()
