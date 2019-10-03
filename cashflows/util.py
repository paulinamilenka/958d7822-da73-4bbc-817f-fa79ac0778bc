
#Librerias
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
    def __init__(self,amount,t):
        self.amount = amount
        self.t = t

    def present_value(self,interest_rate):
        return self.amount * (1+interest_rate) ** -(self.t)

class InvestmentProject(object):
    RISK_FREE_RATE = 0.08

    def __init__(self, cash_f, hurdle_rate=RISK_FREE_RATE):
        cashflows_p = {str(flow.t): flow for flow in cash_f}
        self.cashflow_max_p = max((flow.t for flow in cash_f))
        self.cash_f = []
        for t in range(self.cashflow_max_p + 1):
            self.cash_f.append(cashflows_p.get(str(t), Cashflow(t=t, amount=0)))
        self.hurdle_rate = hurdle_rate if hurdle_rate else InvestmentProject.RISK_FREE_RATE

    @staticmethod
    def from_csv(filepath, hurdle_rate=RISK_FREE_RATE):
        cash_f = [Cashflow(**row) for row in pd.read_csv(filepath).T.to_dict().values()]
        return InvestmentProject(cash_f=cash_f, hurdle_rate=hurdle_rate)

    @property
    def internal_return_rate(self):
        return np.irr([flow.amount for flow in self.cash_f])

    def plot(filepath, show=False):
        """Plot Cashflows
        The `plot` function creates a bar plot (fig) where x=t and y=amount.
        :param show: boolean that represents whether to run `plt.show()` or not.
        :return: matplotlib figure object.
        """
        # TODO: implement plot method

        inf = pd.read_csv(filepath)
        plot = inf.plot.bar(x="t", y="amount")
        fig = plot.get_figure()
        if show:
            plt.show()
        return fig






    def net_present_value(self, interest_rate=None):
        """ Net Present Value
        Calculate the net-present value of a list of cashflows.
        :param interest_rate: represents the discount rate.
        :return: a number (currency) representing the net-present value.
        """
        # TODO: implement net_present_value method
        if interest_rate==None:
            interest_rate=self.hurdle_rate
        amount = [flow.amount for flow in self.cash_f]
        t = [flow.t for flow in self.cash_f]
        n=len(t)
        pv=[]
        for i in range (n):
            a=amount[i]
            m=t[i]
            v = Cashflow(amount=a,t=m)
            pv.append(v.present_value(interest_rate=interest_rate))
        npv=0
        for i in range(len(pv)):
            npv += pv[i]
        return npv



    def equivalent_annuity(self, interest_rate=None):
        """ Equivalent Annuity
        Transform a set of cashflows into a constant payment.
        :param interest_rate: represents the interest-rate used with the annuity calculations.
        :return: a number (currency) representing the equivalent annuity.
        """
        # TODO: implement equivalent_annuity methdo
        if interest_rate==None:
            interest_rate=self.hurdle_rate
        t = [flow.t for flow in self.cash_f]
        n = max(t)
        P = self.net_present_value(interest_rate)
        annuity = P * (interest_rate/(1-(1+interest_rate) ** -n))
        return annuity

    def describe(self):
        return {
            "irr": self.internal_return_rate,
            "hurdle-rate": self.hurdle_rate,
            "net-present-value": self.net_present_value(interest_rate=None),
            "equivalent-annuity": self.equivalent_annuity(interest_rate=None)
        }

