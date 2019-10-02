import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Cashflow(object):
    """Cashflow
    Create a cashflow-class definition.

    Attributes:
        * amount - monetary amount at time t.
        * t - integer representing time.

    Methods:
        * present_value(self, interest_rate) - returns the present value of the cashfow given a interest-rate.
    """
    def _init_(self,amount,t):
        self.amount = amount
        self.t = t
    def present_value(self,interest_rate):
        return self.amount * (1-(1+interest_rate) ** -(self.t))/ interest_rate


class InvestmentProject(object):
    RISK_FREE_RATE = 0.08

    def _init_(self, cashflows, hurdle_rate=RISK_FREE_RATE):
        cashflows_positions = {str(flow.t): flow for flow in cashflows}
        self.cashflow_max_position = max((flow.t for flow in cashflows))
        self.cashflows = []
        for t in range(self.cashflow_max_position + 1):
            self.cashflows.append(cashflows_positions.get(str(t), Cashflow(t=t, amount=0)))
        self.hurdle_rate = hurdle_rate if hurdle_rate else InvestmentProject.RISK_FREE_RATE

    @staticmethod
    def from_csv(filepath, hurdle_rate=RISK_FREE_RATE):
        cashflows = [Cashflow(**row) for row in pd.read_csv(filepath).T.to_dict().values()]
        return InvestmentProject(cashflows=cashflows, hurdle_rate=hurdle_rate)

    @property
    def internal_return_rate(self):
        return np.irr([flow.amount for flow in self.cashflows])

    def plot(filepath, show=True):
        """Plot Cashflows
        The `plot` function creates a bar plot (fig) where x=t and y=amount.
        :param show: boolean that represents whether to run `plt.show()` or not.
        :return: matplotlib figure object.
        """
        # TODO: implement plot method

        data = pd.read_csv(filepath)
        plot = data.plot.bar(x="t", y="amount")
        fig = plot.get_figure()
        plt.show()
        return fig





    def net_present_value(self, interest_rate=None):
        """ Net Present Value
        Calculate the net-present value of a list of cashflows.
        :param interest_rate: represents the discount rate.
        :return: a number (currency) representing the net-present value.
        """
        # TODO: implement net_present_value method
        raise NotImplementedError



    def equivalent_annuity(self, interest_rate=None):
        """ Equivalent Annuity
        Transform a set of cashflows into a constant payment.
        :param interest_rate: represents the interest-rate used with the annuity calculations.
        :return: a number (currency) representing the equivalent annuity.
        """
        # TODO: implement equivalent_annuity methdo
        raise NotImplementedError

    def describe(self):
        return {
            "irr": self.internal_return_rate,
            "hurdle-rate": self.hurdle_rate,
            "net-present-value": self.net_present_value(interest_rate=None),
            "equivalent-annuity": self.equivalent_annuity(interest_rate=None)
            }


