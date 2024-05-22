from collections import defaultdict
from typing import List, Dict, Tuple

import matplotlib.pyplot as plt

from src.request_utils import Request, State


def success_ratio(all_requests: List[Request]) -> float:
    """Calculate the success ratio of requests."""
    total_requests = len(all_requests)
    if total_requests == 0:
        return 0
    successful_requests = sum(1 for req in all_requests if req.finish_state == State.FINISHED_SUCCESSFULLY)
    return successful_requests / total_requests


def average_processing_time(all_requests: List[Request]) -> float:
    """Calculate the average processing time of completed requests."""
    completed_requests = [req for req in all_requests if req.finish_state == State.FINISHED_SUCCESSFULLY]
    if not completed_requests:
        return 0
    total_time = sum(req.end_processing_time - req.start_processing_time for req in completed_requests)
    return total_time / len(completed_requests)


def plot_success_ratio(simulations: Dict[Tuple[float, int], List[Request]], queue_mechanism: str):
    """Plot the success ratio for varying parameters."""
    x_labels = []
    ratios = []

    for (arrival_rate, queue_size), requests in simulations.items():
        ratio = success_ratio(requests)
        x_labels.append(f"AR: {arrival_rate}, QS: {queue_size}")
        ratios.append(ratio)

    plt.figure(figsize=(14, 7))
    plt.bar(x_labels, ratios)
    plt.ylim(0, 1)
    plt.title(f'Success Ratio for {queue_mechanism}')
    plt.xlabel('Parameters (Arrival Rate, Queue Size)')
    plt.ylabel('Success Ratio')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def plot_average_processing_time(simulations: Dict[Tuple[float, int], List[Request]], queue_mechanism: str):
    """Plot the average processing time for varying parameters."""
    x_labels = []
    avg_times = []

    for (arrival_rate, queue_size), requests in simulations.items():
        avg_time = average_processing_time(requests)
        x_labels.append(f"AR: {arrival_rate}, QS: {queue_size}")
        avg_times.append(avg_time)

    plt.figure(figsize=(14, 7))
    plt.bar(x_labels, avg_times, color='orange')
    plt.title(f'Average Processing Time for {queue_mechanism}')
    plt.xlabel('Parameters (Arrival Rate, Queue Size)')
    plt.ylabel('Average Processing Time (s)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def requests_over_time(all_requests: List[Request]) -> Dict[int, int]:
    """Count the number of requests over time."""
    time_buckets = defaultdict(int)
    for req in all_requests:
        time_buckets[int(req.arrival_time)] += 1
    return time_buckets


def plot_requests_over_time(simulations: Dict[Tuple[float, int], List[Request]], queue_mechanism: str):
    """Plot the number of requests over time for varying parameters."""
    plt.figure(figsize=(10, 6))

    for (arrival_rate, queue_size), requests in simulations.items():
        time_buckets = requests_over_time(requests)
        times = sorted(time_buckets.keys())
        request_counts = [time_buckets[time] for time in times]
        label = f"AR: {arrival_rate}, QS: {queue_size}"
        plt.plot(times, request_counts, marker='o', label=label)

    plt.title(f'Number of Requests Over Time for {queue_mechanism}')
    plt.xlabel('Time')
    plt.ylabel('Number of Requests')
    plt.legend()
    plt.show()


def analyze_simulations(simulations: Dict[Tuple[float, int], List[Request]], queue_mechanism: str):
    """Perform a full analysis of the simulations."""
    # Plot success ratio
    plot_success_ratio(simulations, queue_mechanism)

    # Plot average processing time
    plot_average_processing_time(simulations, queue_mechanism)

    # Plot requests over time
    plot_requests_over_time(simulations, queue_mechanism)
