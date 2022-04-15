import numpy as np
import pandas as pd
import random
from numpy import array


class Individual:
    """Each individual represents a different portfolio."""

    counter = 0
    universe = None

    @classmethod
    def set_stock_universe(cls, universe: pd.DataFrame):
        """Add the universe of assets as class attribute."""
        cls.universe = universe

    @classmethod
    def create_random(cls):
        """Create a new individual which represents a different allocation."""
        pfolio_length = random.randint(1, 20)
        portfolio_stocks = np.array(random.sample(range(1, cls.universe.shape[1]), pfolio_length))
        portfolio_weights = np.array(random.sample(range(1, 21), pfolio_length))
        portfolio_weights = portfolio_weights / portfolio_weights.sum()

        return Individual(portfolio_idx=portfolio_stocks, portfolio_weights=portfolio_weights)

    def __init__(self, portfolio_idx: array, portfolio_weights: array) -> None:
        """Each individual is created with an array of indices and an array of weights."""
        self.portfolio_idx = portfolio_idx
        self.portfolio_weights = portfolio_weights
        self.__class__.counter += 1

    def get_sharpe(self) -> float:
        """Return the sharpe ratio of the portfolio, also acts as the fitness function to maximize."""
        hist_ret = np.log(self.prices()).diff().dropna()
        cov_returns = hist_ret.cov()
        ret = hist_ret.mean().T @ self.portfolio_weights
        risk = np.sqrt(self.portfolio_weights @ cov_returns.values @ self.portfolio_weights)
        sharpe_ratio = ret.sum() / risk
        return sharpe_ratio

    def expected_return(self) -> float:
        """Return the mean expected returns of the portfolio.

        Returns:
            ret: Expected returns for the given portfolio.

        """
        hist_ret = np.log(self.prices()).diff().dropna()
        ret = self.portfolio_weights @ hist_ret.mean().T
        return ret

    def prices(self) -> pd.DataFrame:
        """Return closing prices of this porfolio.

        Returns:
            Dataframe with the closing prices of the portfolio.

        """
        return self.universe.iloc[:, self.portfolio_idx]

    def risk(self) -> float:
        """Return the risk for this portfolio.

        Returns:
            risk: Risk for the current portfolio.

        """
        hist_ret = np.log(self.prices()).diff().dropna()
        cov = hist_ret.cov()
        risk = np.sqrt(self.portfolio_weights @ cov.values @ self.portfolio_weights)
        return risk
