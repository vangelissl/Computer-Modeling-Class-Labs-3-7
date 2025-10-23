import pandas as pd
from datetime import datetime

CLIENT_LOGS_COLUMNS = ['products', 'refused', 'duration', 'time waited']
STATS_COLUMNS = ['datetime', 'clients total',
                 'products', 'refused', 'served clients', 'immediately served', 'lost clients', 'being served', 'queue', 'throughput', 'utilization']
AVERAGED_COLUMNS = ['rho', 'q_0', 'p_refusal', 'p_q', 'Q',
                    'A', 'k_occupied', 'L_q', 'l_s', 'W_q', 'W_s', 'idle']


class Statistics(object):
    def __init__(self, step):
        self.client_logs = pd.DataFrame(columns=CLIENT_LOGS_COLUMNS)
        self.df = pd.DataFrame(columns=STATS_COLUMNS)

        self.step = step

    def add_log_entry(self, products: int, refused: bool, duration, time_waited: int):
        """
        Adds new entry that holds a log data of certain client
        """
        new_info = pd.DataFrame(
            data=[[products, refused, duration, time_waited]], columns=CLIENT_LOGS_COLUMNS)
        self.client_logs = pd.concat(
            [self.client_logs, new_info], axis=0, ignore_index=True)

    def add_dataset_entry(self, time: datetime, clients_total: int, products_total: int,
                          refused_total: int, served: int, immediately_served: int, lost: int, in_service: int,  queue: int, time_served: int):
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
                   served, immediately_served, lost, in_service, queue, throughput, utilization]],
            columns=STATS_COLUMNS)

        self.df = pd.concat([self.df, new_entry],
                            axis=0, ignore_index=True)

    def get_averaged_data(self):
        df = self.df
        queue_time_avg = self.client_logs['time waited'].mean()
        queue_size_avg = df['queue'].mean()
        occupied_workers_avg = df['being served'].mean()
        clients_num = len(self.client_logs)

        averaged_series = pd.Series({
            'rho': df['clients total'].mean() / df['served clients'].mean(),
            'q_0': len(df[(df['queue'] == 0) & (df['being served'] == 0)]) / len(df),
            'p_refusal': df['lost clients'].sum() / df['clients total'].sum(),
            'p_q': (self.client_logs['time waited'] > 0).sum() / clients_num - df['lost clients'].sum() / clients_num,
            'Q': df['served clients'].sum() / df['clients total'].sum(),
            'A': df['served clients'].mean(),
            'k_occupied': occupied_workers_avg,
            'L_q': queue_size_avg,
            'L_s': queue_size_avg + occupied_workers_avg,
            'W_q': queue_time_avg,
            'W_s': queue_time_avg + self.client_logs['duration'].mean(),
            'idle': 1 - df['utilization'].mean()
        })

        return averaged_series

    def clear(self):
        self.df = pd.DataFrame(columns=self.df.columns)
        self.client_logs = pd.DataFrame(columns=self.client_logs.columns)
