#!/usr/bin/env python3

import numpy as np

# Nathan Englehart (Summer, 2024)

np.random.seed(123)

class MutualFund():
    
    def __init__(self, ticker):
        self.ticker = ticker

class Stock():
    
    def __init__(self, price, ticker):
        self.price = price
        self.ticker = ticker

class Bond(Stock):
    pass

class Portfolio():
  
    def __init__(self, cash=0, stocks = {},  mfs = {}):

        self.cash = cash
        self.stocks = stocks
        self.mfs = mfs

    def __str__(self):
        return (f'Cash: {self.cash}\n'
                f'Stocks: {self.stocks}\n'
                f'Mutual Funds: {self.mfs}')

    def addCash(self,cash):
        
        """ Adds cash to portfolio 
            
            Args:

                cash::[[Float]]
                    Cash to add to portfolio

        """

        self.cash += cash

    def buyStock(self,shares, stock):
        
        """ Adds given number of shares of stock with given symbol

        Args:

            shares::[[Integer]]
                Number of shares to purchase

            stock::[[Stock Object]]
                Stock object to buy

        """

        price = stock.price 
        ticker = stock.ticker

        self.stocks.setdefault(ticker, 0)
        self.stocks[ticker] += shares 
        self.cash -= price * shares

    def sellStock(self, shares, stock):
        
        """ Removes the given number of shares of the given stock (if the at that quantity of shares currently exists in the portfolio)

        Args:

            shares::[[Integer]]
                Number of shares to sell

            stock::[[Stock Object]]
                Stock object to sell

        """
        
        price = stock.price
        ticker = stock.ticker

        try:
            if(self.stocks[ticker] >= shares):
                self.stocks[ticker] -= shares
                self.cash += np.random.uniform(low = 0.5 * price * shares, high = 1.5 * price * shares, size = None) 
            else:
                print("Fewer shares owned than the requested quantity to sell")
        except:
            print("No ticker symbol for given stock") 

    def buyMutualFund(self, fractional_shares, mf):
        
        """ Buys the given number of fractional shares of the given mutual fund

            Args:

                fractional_shares::[[Integer]]
                    Number of fractional shares to buy

                mf::[[Mutual Fund Object]]
                    Mutual fund object to buy

        """

        price = 1
        ticker = mf.ticker

        self.mfs.setdefault(ticker, 0)  
        self.mfs[ticker] += fractional_shares 
        self.cash -= price * fractional_shares

    def sellMutualFund(self, fractional_shares, mf):

        """ Sells the given number of fractional shares of the given mutual fund

            Args:

                fractional_shares::[[Integer]]
                    The number of fractional shares to sell

                mf::[[Mutual Fund Object]]
                    Mutual fund object to sell

        """

        price = 1
        ticker = mf.ticker

        try:
            if(self.mfs[ticker] >= fractional_shares):
                self.mfs[ticker] -= fractional_shares
                self.cash += np.random.uniform(low = 0.9 * shares, high = 1.2 * shares, size = None) 
            else:
                print("Fewer fractional shares owned than the requested quantity to sell")
        except:
            print("No ticker symbol for given mutual fund") 

    def buyBond(self, shares, bond):
        
        """ Adds given number of shares of stock with given symbol

        Args:

            shares::[[Integer]]
                Number of shares to purchase

            stock::[[Stock Object]]
                Stock object to buy

        """

        price = stock.price 
        ticker = stock.ticker

        self.stocks.setdefault(ticker, 0)
        self.stocks[ticker] += shares 
        self.cash -= price * shares

    def sellStock(self, shares, stock):
        
        """ Removes the given number of shares of the given stock (if the at that quantity of shares currently exists in the portfolio)

        Args:

            shares::[[Integer]]
                Number of shares to sell

            stock::[[Stock Object]]
                Stock object to sell

        """
        
        price = stock.price
        ticker = stock.ticker

        try:
            if(self.stocks[ticker] >= shares):
                self.stocks[ticker] -= shares
                self.cash += np.random.uniform(low = 0.5 * price * shares, high = 1.5 * price * shares, size = None) 
            else:
                print("Fewer shares owned than the requested quantity to sell")
        except:
            print("No ticker symbol for given stock") 



portfolio = Portfolio()
portfolio.addCash(300.50)
s = Stock(20,"HFH")
portfolio.buyStock(5,s)
mf1 = MutualFund("BRT")
mf2 = MutualFund("GHT")
portfolio.buyMutualFund(10.3, mf1)
portfolio.buyMutualFund(2, mf2)
print(portfolio)

# using inheritance add bonds to the mix
