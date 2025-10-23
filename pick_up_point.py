from o_statistics import Statistics
import datetime
import numpy as np
from worker import Worker
from collections import deque
from client import Client


QUEUE_LIMIT = 15
STEP = 0.25


class PickUpPoint(object):
    """
    A class that represents a model of the order pick up point with one worker
    """

    def __init__(self, statistics: Statistics, current_time: datetime.datetime, step: float, c: int):
        self.current_time = current_time    # Current time of the simulation
        self.queue = deque()  # Queue for the day
        self.immediate_service = deque()
        self.in_service = 0

        # Interval specific metrics:
        self.lost_clients = 0   # Number of clients who were lost due to queue limitations
        self.served_clients = 0  # Number of clients who were served
        self.count_client = 0   # Number of clients who have arrived
        self.products_total = 0  # Number of products for served clients
        self.total_refused = 0  # Number of clients who refused the product
        self.immediately_served = 0

        self.statistics = statistics

        # Create workers
        self.workers = [Worker(step, statistics, self) for _ in range(c)]

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
        available_workers = self.get_available()
        immediate_service_capacity = min(available_workers, self.count_client)
        self.immediately_served = immediate_service_capacity
        # Calculate the queue overflow
        spots_available = QUEUE_LIMIT - len(self.queue)
        overflowed = spots_available < (
            self.count_client - immediate_service_capacity)

        # Calculate the current queue and lost clients who didn't fit
        self.lost_clients = (self.count_client -
                             (spots_available + immediate_service_capacity)) if overflowed else 0

        size = spots_available + immediate_service_capacity if overflowed else self.count_client
        for _ in range(size):
            self.queue.append(Client(self.current_time))

        for _ in range(immediate_service_capacity):
            client = self.queue.popleft()
            self.immediate_service.append(client)

    def client_service(self):
        # Assign immediate service clients first
        if self.immediate_service:
            for worker in self.workers:
                if worker.is_available() and self.immediate_service:
                    client = self.immediate_service.popleft()
                    worker.assign_client(client)

        # All workers work their intervals
        for worker in self.workers:
            worker.work_interval()

            def able_to_serve():
                return any(w.is_available() for w in self.workers)

            while able_to_serve() and len(self.queue) > 0:
                for worker in self.workers:
                    if worker.is_available() and len(self.queue) > 0:
                        client = self.queue.popleft()
                        worker.assign_client(client)
                        worker.work_interval()

    def reset_metrics(self):
        """
        Resets metrics to reuse them properly on the next iteration
        """
        self.served_clients = 0
        self.products_total = 0
        self.total_refused = 0
        self.immediately_served = 0

        for worker in self.workers:
            worker.reset_metrics()

    def get_available(self):
        return sum(int(worker.is_available()) for worker in self.workers)

    def end_shift(self):
        self.lost_clients = len(self.queue)
        self.queue.clear()

        if self.in_service:
            for worker in self.workers:
                worker.end_shift()

    def next_day(self):
        self.current_time += datetime.timedelta(hours=14)

    def end_interval_simulation(self):
        av_time_served = sum(
            w.time_served for w in self.workers) / len(self.workers)

        self.statistics.add_dataset_entry(self.current_time, self.count_client, int(self.products_total),
                                          self.total_refused, self.served_clients, self.immediately_served, self.lost_clients, self.in_service,
                                          len(self.queue), int(av_time_served))
        self.reset_metrics()
