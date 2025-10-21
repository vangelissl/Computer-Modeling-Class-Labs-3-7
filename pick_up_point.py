from o_statistics import Statistics
from client import Client
import datetime
import numpy as np


QUEUE_LIMIT = 15
STEP = 0.25


class PickUpPoint(object):
    """
    A class that represents a model of the order pick up point with one worker
    """

    def __init__(self, statistics: Statistics, current_time: datetime.datetime, step: float):
        self.current_time = current_time    # Current time of the simulation
        self.paydesk = Client()  # Client that is being served
        self.queue = 0  # Queue for the day
        self.time_waited = 0  # Time client has waited in the queue

        # Interval specific metrics:
        self.lost_clients = 0   # Number of clients who were lost due to queue limitations
        self.served_clients = 0  # Number of clients who were served
        self.count_client = 0   # Number of clients who have arrived
        self.products_total = 0  # Number of products for served clients
        self.total_refused = 0  # Number of clients who refused the product
        self.time_served = 0    # Time of paydesk occupation

        self.statistics = statistics

        self.step = step

    def increase_time(self):
        """Moves modeling time forward by one modeling time unit"""
        self.current_time += datetime.timedelta(hours=self.step)

    def client_arrived(self):
        """
        Determines the number of clients for the current time interval

        Calculates the queue and clients who were lost due to queue limitation
        """
        hour = self.current_time.hour

        # The potential number of client changes depending on an hour
        if hour < 14:
            Lam = 4
        elif hour < 17:
            Lam = 6
        else:
            Lam = 8

        self.count_client = np.random.poisson(Lam)
        # Calculate the queue overflow
        spots_available = QUEUE_LIMIT - self.queue
        overflowed = spots_available < self.count_client

        # Calculate the current queue and lost clients who didn't fit
        self.lost_clients = (self.count_client -
                             spots_available) if overflowed else 0
        if self.queue == 0:
            self.time_waited = 0
        self.queue += spots_available if overflowed else self.count_client

    def display_intermediate_info(self):
        print('\n*************')
        print(self.count_client, 'client(s) arrived in the past hour')

    def client_service(self):
        """
        Simulates the service action for a single time interval
        """
        time = 60 * self.step   # Convert time to minutes

        # Serve while there are clients during the interval
        while self.queue > 0 and time > 0:
            # Serve new client only if the paydesk is free
            if self.paydesk.duration == 0:
                # Generate the parameters of the client
                self.paydesk.service()

                # Contribute current client to the statisctical metrics
                self.products_total += self.paydesk.products
                self.total_refused += self.paydesk.refused

                # Log current client
                self.statistics.add_log_entry(
                    int(self.paydesk.products), bool(self.paydesk.refused), self.paydesk.duration, self.time_waited)

                # Update parameters to indicate client having been served
                self.queue -= 1
                self.time_waited += self.paydesk.duration
                self.served_clients += 1
                self.paydesk.products = 0

            # Remove amount of serving time
            time -= self.paydesk.duration

            # Determine if the client has been fully served during the interval
            if time >= 0:
                self.time_served += self.paydesk.duration
                self.paydesk.duration = 0   # Reset serving time
            else:
                self.time_served = self.step * 60
                self.paydesk.duration = -time   # Set time left to fully serve the client
                time = 0    # Indicate end of the current interval

    def reset_metrics(self):
        """
        Resets metrics to reuse them properly on the next iteration
        """
        self.served_clients = 0
        self.products_total = 0
        self.total_refused = 0
        self.time_served = 0
        self.time_waited = 0

    def end_shift(self):
        self.lost_clients = self.queue
        self.queue = 0

    def next_day(self):
        self.current_time += datetime.timedelta(hours=14)

    def end_interval_simulation(self):
        self.statistics.add_dataset_entry(self.current_time, self.count_client, int(self.products_total),
                                          self.total_refused, self.served_clients, self.lost_clients,
                                          self.queue, int(self.time_served))
        self.reset_metrics()
