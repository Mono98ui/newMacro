#Visualiser les donnees avec backtrader
#Exporter en pdf
#la moyen et la sum de buy et sell
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.analyzers as btanalyzers
from ThreeTwelveCross import ThreeTwelveCross

cerebro = bt.Cerebro()

cerebro = bt.Cerebro(stdstats=False)  # remove the standard observers
cerebro.addobserver(bt.observers.Trades)

cerebro.addobserver(
        bt.observers.BuySell,
        barplot=True,
        bardist=0.015)

cerebro.addstrategy(ThreeTwelveCross)

data1 = btfeeds.GenericCSVData(
    dataname=self.tbthree,

    fromdate=self.start,
    todate=self.end,
    timeframe=self.timeframe ,
    nullvalue=0.0,

    dtformat=(self.dateFormat),

    datetime=0,
    high=1,
    low=1,
    open=1,
    close=1,
    volume=-1,
    openinterest=-1
) 
cerebro.adddata(data1, name='3-month-yield')

data2 = btfeeds.GenericCSVData(
    dataname="Data/{name}.csv".format(name=key),

    fromdate=self.start,
    todate=self.end,
    timeframe=self.timeframe ,
    nullvalue=0.0,

    dtformat=(self.dateFormat),

    datetime=0,
    high=self.threeColumn,
    low=self.threeColumn ,
    open=self.threeColumn ,
    close=self.threeColumn ,
    volume=-1,
    openinterest=-1
) 

cerebro.adddata(data2, name="{val} 3-month growth".format(val=value))

data3 = btfeeds.GenericCSVData(
    dataname="Data/{name}.csv".format(name=key),

    fromdate=self.start,
    todate=self.end,
    timeframe=self.timeframe ,
    nullvalue=0.0,

    dtformat=(self.dateFormat),

    datetime=0,
    high=self.twelveColumn,
    low=self.twelveColumn,
    open=self.twelveColumn,
    close=self.twelveColumn,
    volume=-1,
    openinterest=-1
)

data3.compensate(data2)  # let the system know ops on data1 affect data0
data3.plotinfo.plotmaster = data2
data3.plotinfo.sameaxis = True

cerebro.adddata(data3, name='{val} 12 month growth'.format(val=value))
cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='tradeanalyzer')

thestrats = cerebro.run()
thestrat = thestrats[0]

cerebro.plot()

result =  thestrat.analyzers.tradeanalyzer.get_analysis()
