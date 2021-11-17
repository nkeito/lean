from AlgorithmImports import *

from System.Drawing import Color
#from custommodels import CustomSlippageModel

class SMAStrategy(QCAlgorithm):

    def Initialize(self):

        import os
        
        self.SetStartDate(2000, 1, 1)  # Set Start Date
        self.SetEndDate(2021, 8, 31)  # Set End Date
        self.SetCash(100000)  # Set Strategy Cash
        self.PrevFee = 0
        
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)
        
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        #self.my_spy = self.AddData(MySPY, "MYSPY_", Resolution.Daily).Symbol

        #self.my_spy = self.AddData( My_spy, "MYSPY", Resolution.Daily ).Symbol
        
        lenght_fast = self.GetParameter("sma_lenght_fast")
        lenght_fast = 11 if lenght_fast is None else int(lenght_fast)
        lenght_slow = self.GetParameter("sma_lenght_slow")
        lenght_slow = 70 if lenght_slow is None else int(lenght_slow)
        
        self.max_leverage = 2.0       # Set total leverage you want
        self.qt_factor = self.GetParameter("qt")   
        self.qt_factor = 1.5 if self.qt_factor is None else float(self.qt_factor)# Set total leverage level you want to order each time
        
        self.sma_fast = self.SMA(self.spy, lenght_fast, Resolution.Daily)
        self.sma_slow = self.SMA(self.spy, lenght_slow, Resolution.Daily)
        
        self.tolerance = self.GetParameter("crossover_tolerance")
        self.tolerance = 0.0009 if self.tolerance is None else float(self.tolerance)
        #Set slippage model
        self.Securities[self.spy].SetSlippageModel(ConstantSlippageModel(0.0002))

        self.Securities[self.spy].SetSlippageModel(CustomSlippageModel(self))
        self.Securities[self.spy].SetFeeModel(CustomFeeModel())
        
        #Set Leverage interest model
        #self.Securities[self.spy].MarginModel = BuyingPowerModel(requiredFreeBuyingPowerPercent = 0.02)
        
        self.SetWarmUp(timedelta(lenght_slow))

        self.Schedule.On(self.DateRules.On(2021,8, 31), self.TimeRules.At(15,45),
                        self.ExitPositions)
        
        stockPlot = Chart("Trade Plot")
        
        stockPlot.AddSeries(Series("Buy", SeriesType.Scatter, "$", Color.Green, ScatterMarkerSymbol.Triangle))
        stockPlot.AddSeries(Series("Liquidate", SeriesType.Scatter, "$", Color.Red, ScatterMarkerSymbol.TriangleDown))
        
        self.AddChart(stockPlot)

  
    def OnData(self, data):
        
        if not self.sma_slow.IsReady:
            return

        price = self.Securities[self.spy].Price
        
        self.Plot("Trade Plot", "Price", price)
        self.Plot("Trade Plot", "SMA", self.sma_slow.Current.Value)
        self.Plot("Trade Plot", "SMA", self.sma_fast.Current.Value)
        
        total_leverage = float(self.Portfolio.TotalPortfolioValue) * self.max_leverage *.95
        qt = (total_leverage * (float(self.qt_factor)/self.max_leverage)) / price 
        
        holdings = self.Portfolio[self.spy].Quantity
        
        if not self.Portfolio.Invested:
            if self.sma_fast.Current.Value > self.sma_slow.Current.Value * (1 + float(self.tolerance)):
                self.MarketOrder(self.spy, qt)
                self.Plot("Trade Plot", "Buy", price)
                #self.Log( "Current fee: " + str( self.Portfolio[self.spy].TotalFees - self.PrevFee ) +" Total Fees: "+ str(self.Portfolio[self.spy].TotalFees) )
                self.PrevFee = self.Portfolio[self.spy].TotalFees
        else:
            if self.sma_fast.Current.Value < self.sma_slow.Current.Value * (1 - float(self.tolerance)):
                self.Liquidate()
                self.Plot("Trade Plot", "Liquidate", price)
        
        
    def ExitPositions(self):
        self.Liquidate()

class CustomFeeModel:
    def GetOrderFee(self, parameters):
        fee = max(1, parameters.Security.Price
                  * parameters.Order.AbsoluteQuantity
                  * 0.00001)
        return OrderFee(CashAmount(fee, 'USD'))

class CustomSlippageModel:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def GetSlippageApproximation(self, asset, order):
        # custom slippage math
        slippage = asset.Price * float(0.0001 * np.log10(2*float(order.AbsoluteQuantity)))
        #self.algorithm.Log("CustomSlippageModel: " + str(slippage))
        return slippage


"""
class MySPY(PythonData):

    def GetSource(self, config, date, isLive):
        source = "https://www.dropbox.com/s/6uzj42bnl34myri/SPY.csv?dl=1"
        return SubscriptionDataSource(source, SubscriptionTransportMedium.RemoteFile);

    def Reader(self, config, line, date, isLive):
        if not (line.strip() and line[0].isdigit()):
            return None

        data = line.split(',')


        _myspy = MySPY()

        try:
            _myspy.Symbol = config.Symbol
            _myspy.Time = datetime.strptime(data[0], '%Y-%m-%d') + timedelta(hours=15,minutes=45)

            _myspy.Value = float(data[1])
            
        except ValueError:
            return None
        
        return _myspy
        
"""