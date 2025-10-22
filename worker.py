from client import Client
from o_statistics import Statistics
from datetime import timedelta


# worker.py
class Worker():
    def __init__(self, step: float, stats: Statistics, pup):
        self.current_client = None
        self.time_served = 0
        self.statistics = stats
        self.pup = pup
        self.step_minutes = step * 60

    def assign_client(self, client: Client):
        self.current_client = client
        # Calculate watining time as soon as client gets to the paydesk
        wait_time = (self.pup.current_time - client.time_entered +
                     timedelta(minutes=self.time_served)).total_seconds() / 60
        self.current_client.time_waited = wait_time

        self.pup.in_service += 1

        if client.duration == 0:
            client.service()

    def work_interval(self, step=None):
        if self.current_client is None:
            return
        step = self.step_minutes if not step else step

        client = self.current_client
        time_remaining = step - self.time_served

        # Work on current client
        time_spent = min(time_remaining, client.duration)
        client.duration -= time_spent
        self.time_served += time_spent

        # Client finished?
        if client.duration == 0:
            self.statistics.add_log_entry(
                int(client.products), bool(client.refused), client.initial_duration, int(client.time_waited))

            self.pup.products_total += client.products
            self.pup.total_refused += client.refused
            self.pup.served_clients += 1
            self.pup.in_service -= 1

            self.current_client = None

    def end_shift(self):
        if self.current_client:
            remaining_time = self.current_client.duration
            self.work_interval(step=self.time_served + remaining_time)

    def reset_metrics(self):
        self.time_served = 0

    def is_available(self):
        return self.current_client is None and self.time_served < self.step_minutes
