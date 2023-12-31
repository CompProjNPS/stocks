from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import ttkbootstrap as ttk
from datetime import datetime

# Window

root=ttk.Window(themename='cyborg')
root.title("Stocks")
root.geometry("1600x900")
label = ttk.Label(root,text="Stock Price",font=('Comic Sans MS',36,'bold')).pack()

# create widgets
data_entry_frame = ttk.LabelFrame(root,text='Enter Data')
graph_frame = ttk.LabelFrame(root,text='Graph')

date_frame = ttk.Frame(data_entry_frame)
start_date_label = ttk.Label(date_frame, text = 'Start Date(YYYY-MM-DD)', font=('calibre',10, 'bold'))
end_date_label = ttk.Label(date_frame, text = 'End Date(YYYY-MM-DD)', font=('calibre',10, 'bold'))
start_date_entry = ttk.DateEntry(date_frame)
end_date_entry = ttk.DateEntry(date_frame)

run_frame = ttk.Frame(data_entry_frame)
ticker_label = ttk.Label(run_frame,text='Enter Ticker')
ticker_entry = ttk.Entry(run_frame)
plot_button = ttk.Button(run_frame,text="Plot")

# place widgets
data_entry_frame.pack(expand=True,fill='both',side='left',padx=25,pady=25)
graph_frame.pack(expand=True,fill='both',side='left',padx=25,pady=25)

date_frame.pack(expand=True)
start_date_label.grid(row=0,column=0,sticky='nsew',padx=12)
end_date_label.grid(row=1,column=0,sticky='nsew',padx=12,pady=12)
start_date_entry.grid(row=0,column=1,sticky='nsew',padx=12,pady=12)
end_date_entry.grid(row=1,column=1,sticky='nsew',padx=12,pady=12)

run_frame.pack(expand=True)
ticker_label.grid(row=0,column=0,padx=12,pady=12)
ticker_entry.grid(row=0,column=1,columnspan=2,sticky='nsew',padx=12,pady=12)
plot_button.grid(row=1,column=0,columnspan=3,sticky='nsew',padx=12,pady=12)


# Data
def get_data():
    global ticker
    global company
    global start_date
    global end_date

    ticker = ticker_entry.get()

    start_date = start_date_entry.entry.get().split('-')
    start_date = start_date[2]+'-'+str(int(start_date[1]))+'-'+str(int(start_date[0]))
    end_date = end_date_entry.entry.get().split('-')
    end_date = end_date[2]+'-'+str(int(end_date[1]))+'-'+str(int(end_date[0]))


    company=yf.download(
        tickers=ticker,
        start=start_date,
        end=end_date
        )
    
    return ticker, company, start_date, end_date


def plot():
    get_data()

    d = plt.figure(figsize=(14,5))
    sns.set_style("ticks")
    sns.lineplot(data=company,x="Date",y='Close',color='firebrick')
    sns.despine()
    str = "The Stock Price of " + ticker
    plt.title(str,size='x-large',color='blue')
    canvas = FigureCanvasTkAgg(d, master=graph_frame)   
    canvas.draw() 
    canvas.get_tk_widget().pack(expand=True,fill='both',padx=12,pady=12)


plot_button.configure(command=plot)

root.mainloop()