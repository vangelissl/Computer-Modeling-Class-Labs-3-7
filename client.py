import numpy as np
from scipy.stats import bernoulli

# Constant time in minutes:
REVIEW_TIME = 3		# time to review single product
PAYMENT_TIME = 1  # time to pay for the whole order
REFUSAL_TIME = 4  # time of product refusal


class Client(object):
    """
    A class that represents a client model in a order pick up point system
    """

    def __init__(self):
        self.products = 0
        self.duration = 0
        self.refused = 0

    def service(self):
        """
        Generates unique values of the client parameters
        """
        self.refused = bernoulli.rvs(0.1)
        self.products = int(np.random.geometric(0.3)) - self.refused
        self.duration = self.refused * REFUSAL_TIME + \
            self.products * REVIEW_TIME + PAYMENT_TIME
