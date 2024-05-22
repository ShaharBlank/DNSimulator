from collections import defaultdict
from typing import List, Dict, Tuple

import matplotlib.pyplot as plt

from src.request_utils import Request


def success_ratio(all_requests: List[Request]) -> float:
    """Calculate the success ratio of requests."""
    total_requests = len(all_requests)
    if total_requests == 0:
        return 0
    successful_requests = sum(1 for req in all_requests if req.is_completed)
    return successful_requests / total_requests


def average_processing_time(all_requests: List[Request]) -> float:
    """Calculate the average processing time of completed requests."""
    completed_requests = [req for req in all_requests if req.is_completed]
    if not completed_requests:
        return 0
    total_time = sum(req.end_processing_time - req.start_processing_time for req in completed_requests)
    return total_time / len(completed_requests)


def plot_success_ratio_3d(simulations: Dict[Tuple[float, int], List[Request]], queue_mechanism: str):
    """Plot the success ratio for varying parameters in 3D."""
    arrival_rates = []
    queue_sizes = []
    success_ratios = []

    for (arrival_rate, queue_size), requests in simulations.items():
        arrival_rates.append(arrival_rate)
        queue_sizes.append(queue_size)
        success_ratios.append(success_ratio(requests))

    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(arrival_rates, queue_sizes, success_ratios, c='r', marker='o')

    ax.set_xlabel('Arrival Rate')
    ax.set_ylabel('Queue Size')
    ax.set_zlabel('Success Ratio')
    ax.set_title(f'Success Ratio for {queue_mechanism} (3D)')

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


def analyze_simulations(simulations: Dict[Tuple[float, int], List[Request]], queue_mechanism: str):
    # Plot success ratio in 3D
    plot_success_ratio_3d(simulations, queue_mechanism)

    # Plot average processing time
    plot_average_processing_time(simulations, queue_mechanism)

