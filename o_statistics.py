import pandas as pd
from datetime import datetime

CLIENT_LOGS_COLUMNS = ['products', 'refused', 'duration']
STATS_COLUMNS = ['datetime', 'clients total',
                 'products', 'refused', 'served clients', 'lost clients', 'queue', 'throughput', 'utilization']


class Statistics(object):
    def __init__(self, step):
        self.client_logs = pd.DataFrame(columns=CLIENT_LOGS_COLUMNS)
        self.df = pd.DataFrame(columns=STATS_COLUMNS)

        self.step = step

    def add_log_entry(self, products: int, refused: bool, duration):
        """
        Adds new entry that holds a log data of certain client
        """
        new_info = pd.DataFrame(
            data=[[products, refused, duration]], columns=CLIENT_LOGS_COLUMNS)
        self.client_logs = pd.concat(
            [self.client_logs, new_info], axis=0, ignore_index=True)

    def add_dataset_entry(self, time: datetime, clients_total: int, products_total: int,
                          refused_total: int, served: int, lost: int, queue: int, time_served: int):
        """
        Adds new entry that holds a single time interval data
        """
        # Calculate the ability of the pick up point to serve clients efficiently
        throughput = round(served / clients_total,
                           2) if clients_total > 0 else 0
        # Calculate the paydesk occupation metric
        utilization = time_served / (self.step * 60)

        new_entry = pd.DataFrame(
            data=[[time, clients_total, products_total, refused_total,
                   served, lost, queue, throughput, utilization]],
            columns=STATS_COLUMNS)

        self.df = pd.concat([self.df, new_entry],
                            axis=0, ignore_index=True)

    def clear(self):
        self.df = pd.DataFrame(columns=self.df.columns)
        self.client_logs = pd.DataFrame(columns=self.client_logs.columns)
