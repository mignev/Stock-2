from abc import abstractmethod, ABC
import numpy as np
import pandas as pd
from entities.Factory import AbstractFactory


class FormulatorAbstract(ABC):
    @abstractmethod
    def calculate(self, *args, **kwargs): pass


class AnnualMeanRiskReturns(FormulatorAbstract):
    def calculate(self, df):
        simple_returns = (df / df.shift(1)) - 1
        companies = df.columns.tolist()

        price_volatility = round(
            simple_returns[companies].std() * 250 ** 0.5 * 100, 3).tolist()
        returns = round(
            simple_returns[companies].mean() * 250 * 100, 3).tolist()

        data = []
        for index, ticker in enumerate(companies):
            dictionary = {
                'price_volatility': price_volatility[index], 'ticker': ticker, 'annual_mean_return': returns[index]}
            data.append(dictionary)
        return data


class AnnualMeanLogRiskReturnsFactory(AbstractFactory):
    def factory(self):
        return AnnualMeanRiskReturns()


class HistoryPriceNormalized(FormulatorAbstract):
    def calculate(self, df):
        normalized_price = round(df / df.iloc[0] * 100, 2)
        return normalized_price


class HistoryPriceNormalizedFactory(AbstractFactory):
    def factory(self):
        return HistoryPriceNormalized()


class Resampler(FormulatorAbstract):
    def calculate(self, df):
        df = df.head(1).append(
            df.loc[(df.index.day == 31) & (df.index.month == 12) | (df.index.day == 30) & (df.index.month == 6)])
        return df


class ResamplerFactory(AbstractFactory):
    def factory(self):
        return Resampler()


class EqualWeightMaker(FormulatorAbstract):
    def calculate(self, number_of_tickers):
        ratio = 1/number_of_tickers
        weights = np.array([])
        for i in range(number_of_tickers):
            weights = np.append(weights, ratio)
        weights /= np.sum(weights)
        return weights


class EqualWeightMakerFactory(AbstractFactory):
    def factory(self):
        return EqualWeightMaker()


class PortfolioRiskReturn(FormulatorAbstract):
    def calculate(self, df):

        """calculator portfolio returns """
        number_assets = len(df.columns.tolist())
        weights = EqualWeightMakerFactory().factory().calculate(number_assets)
        # calculate portfolio returns using the mean of the annual simple returns and equal weights
        simple_returns = (df/df.shift(1)) - 1
        annual_simple_returns = simple_returns.mean() * 250
        portfolio_returns = round(
            np.dot(annual_simple_returns, weights) * 100, 3)

        """
        calculate the portfolio volatility based on the deviation
        of the mean of the annual log returns and equal weights"""
        log_returns = np.log(df/df.shift(1))
        cov_matrix_annual = log_returns.cov() * 250
        portfolio_variance = np.dot(weights.T, np.dot(cov_matrix_annual, weights))
        portfolio_volatility = round(portfolio_variance ** 0.5 * 100, 3)

        """ calculating systematic and unsystematic risk"""
        stocks_risks = 0
        list_stocks = df.columns.tolist()
        for i in range(number_assets):
            stock = list_stocks[i]
            stock_variance = log_returns[stock].var() * 250
            calculation = weights[i] ** 2 * stock_variance
            stocks_risks += calculation
        idiosyncratic_risk = portfolio_variance - stocks_risks
        systematic_risk = portfolio_variance - idiosyncratic_risk

        idiosyncratic_risk = round(idiosyncratic_risk * 100, 3)
        systematic_risk = round(systematic_risk * 100, 3)
        portfolio_variance = round(portfolio_variance * 100, 3)

        data = {'portfolio_returns': portfolio_returns,
                'portfolio_volatility': portfolio_volatility,
                'systematic_risk': systematic_risk,
                'idiosyncratic_risk': idiosyncratic_risk,
                'portfolio_variance': portfolio_variance
                }

        return data


class PortfolioRiskReturnFactory(AbstractFactory):
    def factory(self):
        return PortfolioRiskReturn()


class Divider:
    @staticmethod
    def divide(num1, num2, rounder=None):
        if rounder is not None:
            return round((num1 / num2) - 1,  rounder)
        else:
            return (num1 / num2) - 1


class EfficientFrontierSharpe(FormulatorAbstract):
    def calculate(self, df):
        # calculate daily and annual returns of the stocks
        log_returns = np.log(df/df.shift(1))
        annual_log_returns = log_returns.mean() * 250
        num_assets = len(df.columns.tolist())

        # get daily and covariance of returns of the stock
        cov_annual = log_returns.cov() * 250

        # empty lists to store returns, volatility and weights of imiginary portfolios
        result = []
        max_sharpe_ratio = float('-inf')
        min_volatility = float('inf')
        max_sharpe_portfolio = {}
        min_volatility_portfolio = {}

        # set the number of combinations for imaginary portfolios
        num_portfolios = 2000

        # set random seed for reproduction's sake
        np.random.seed(101)

        for i in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            returns = np.sum(weights * annual_log_returns)
                # np.dot(weights, returns_annual)
            volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
            sharpe = returns / volatility

            # create dictionary with calculations and push into results array
            portfolio = {'returns': returns,
                         'volatility': volatility,
                         'sharpe_ratio': sharpe,
                         'weights': list(weights)
                         }

            if sharpe > max_sharpe_ratio:
                max_sharpe_ratio = sharpe
                max_sharpe_portfolio = portfolio

            if volatility < min_volatility:
                min_volatility = volatility
                min_volatility_portfolio = portfolio

            result.append(portfolio)
        return {'frontier': result,
                'max_sharpe': [max_sharpe_portfolio],
                'min_volatility': [min_volatility_portfolio]
                }


class EfficientFrontierSharpeFactory(AbstractFactory):
    def factory(self):
        return EfficientFrontierSharpe()
