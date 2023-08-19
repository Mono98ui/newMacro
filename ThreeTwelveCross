import backtrader as bt
#
# This class represent the strategy three twelve cross using the three month interval and the twelve month. 
#
class ThreeTwelveCross(bt.Strategy):


    def __init__(self):
        self.listTrades = []
        self.listDates = []
        #self.threemonthyield = self.datas[0].close
        self.threemonth = self.datas[1].close  # 3m growth rate
        self.twelvemonth = self.datas[2].close  # 12m growth rate
        self.crossover = bt.ind.CrossOver(self.threemonth, self.twelvemonth)  # crossover signal

    def next(self):
        self.listDates.append(self.datas[0].datetime.date(0))
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long
                self.listTrades.append(1)
            else:
                self.listTrades.append(0)

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position
            self.listTrades.append(-1)
        else:
            self.listTrades.append(0)
