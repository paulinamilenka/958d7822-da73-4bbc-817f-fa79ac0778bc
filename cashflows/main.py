import fire
import json

from util import InvestmentProject


class Main(object):

    @staticmethod
    def describe_investment(filepath, hurdle_rate=None):
        investment_project = InvestmentProject.from_csv(filepath=filepath, hurdle_rate=hurdle_rate)
        description = investment_project.describe()
        print(json.dumps(description, indent=4))

    @staticmethod
    def plot_investment(filepath, save="", show=""):
        # TODO: implement plot_investment method
        if show:
            fig = InvestmentProject.plot(filepath=filepath,show=show)
            if save:
                fig.savefig(".png")



if __name__ == "__main__":
    fire.Fire(Main)
