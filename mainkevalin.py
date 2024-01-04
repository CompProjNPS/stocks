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
root.geometry("640x480") 	#1600x900 is too large.
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
    # Dates in Linux are separated with /. And the year is two digit.
    # Fixing that. I leant this the hard way(and cursed you two dozen times)
    if '/' in start_date_entry.entry.get():
        start_date = start_date_entry.entry.get().split('/')
        end_date = end_date_entry.entry.get().split('/')
        start_date = '20'+start_date[2]+'-'+str(int(start_date[1]))+'-'+str(int(start_date[0]))
        end_date = '20'+end_date[2]+'-'+str(int(end_date[1]))+'-'+str(int(end_date[0]))
    else:
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

def data():
    #P/E ratio -> higher the better; maybe overvalued
    fPE = yf.Ticker(ticker).info['forwardPE']
    if fPE < 20:
        fPEstat = "Good"
    elif fPE < 25:
        fPEstat = "Average"
    else:
        fPEstat = "Bad" 
    #Price/Earnings-to-Growth lower than 1.0
    PEGratio = yf.Ticker(ticker).info['pegRatio']
    if PEGratio < 1:
        PEGratiostat = "Fairly priced to under-valued"
    elif PEGratio < 2:
        PEGratiostat = "Fairly priced"
    else:
        PEGratiostat = "Overvalued. Beware!"
    #debt to equity ratio. Always < 2.0 Industry dependent
    #pref. < 0.5 and < 0.1 is better
    dte = yf.Ticker(ticker).info['debtToEquity']
    if dte < 1:
        dtestat = ("Lesser debt than assets. Safe bet.")
    elif dte < 2:
        dtestat = ("Debt b/w 1 and 2 times of assets.")
    else:
        dtestat = ("High risk. Maybe fine in very large companies in fixed-heavy industries.")
    #Depends on size of company hence we don't comment 
    rg = yf.Ticker(ticker).info['revenueGrowth']
    return ((fPE, fPEstat), (PEGratio, PEGratiostat), (dte, dtestat), rg)
    '''
    To Arjun:
    Display the above in GUI
    if the data qualify the benchmarks -> Say it looks like a good investment and so on.
    '''

def plot():
    get_data()
    data = data()
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
