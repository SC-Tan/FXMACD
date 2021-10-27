class FXMACD(QCAlgorithm):

    def Initialize(self):
        # Set the cash we'd like to use for our backtest
        self.SetCash(1000000)
        # Start and end dates for the backtest.
        self.SetStartDate(2015, 10, 7)
        #self.SetEndDate(2021, 10, 11)
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage)
        self.long_list = []
        self.short_list = []
        
        self.stop= False
        
        self.currencies = ["GBPJPY","AUDUSD"]
        self.AddForex("GBPJPY", Resolution.Daily)
        self.AddForex("AUDUSD", Resolution.Daily) 
        
        

    def OnData(self, data):
        if self.stop: 
            return 
        
        currencies = self.currencies 
        
        for currency in currencies:
            #self.Debug("The currency is running") 
            currency_data = self.History ([currency], 30 , Resolution.Daily) 
            MA21_Pre = currency_data.close[8:29].mean() 
            MA5_Pre = currency_data.close [24:29].mean() 
            MA21_Current = currency_data.close[9:30].mean() 
            MA5_Current = currency_data.close[25:30].mean() 
         
            #First Trade 
            #entry 
            if currency not in self.long_list and currency not in self.short_list: 
                self.Debug ("found currency" +str(currency)) 
                #Checking Bullish Crossover 
                if MA5_Pre < MA21_Pre and MA5_Current > MA21_Current: 
                    #self.Debug("checking long condition") 
                    self.SetHoldings (currency, 0.5) 
                    self.long_list.append(currency) 
                    
                #Checking Bearish Crossover 
                if MA5_Pre > MA21_Pre and MA5_Current < MA21_Current: 
                    #self.Debug("checking short condition") 
                    self.SetHoldings (currency, -0.5) 
                    self. short_list.append(currency) 
                    
                    
            #exit and again entry 
            if currency in self.long_list: 
                #Checking Bearish Crossover 
                if MA5_Pre > MA21_Pre and MA5_Current < MA21_Current: 
                    self.SetHoldings (currency, -0.5) 
                    self.long_list.remove(currency) 
                    self.short_list.append(currency) 
                        
            if currency in self.short_list: 
                #Checking Bullish Crossover 
                if MA5_Pre < MA21_Pre and MA5_Current > MA21_Current: 
                    self.SetHoldings (currency, 0.5) 
                    self.short_list.remove(currency) 
                    self.long_list.append(currency) 
                        
        if self.Portfolio.Cash <85000: 
            self.stop = True 
            self.Liquidate() 
