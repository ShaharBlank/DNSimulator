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


def plot_success_ratio_3d(simulations: Dict[Tuple[float, int], List[Request]], queue_mechanism: str):
    """Plot the success ratio for varying parameters in 3D."""
    arrival_rates = []
    queue_sizes = []
    success_ratios = []

    for (arrival_rate, queue_size), requests in simulations.items():
        arrival_rates.append(arrival_rate)
        queue_sizes.append(queue_size)
        success_ratios.append(success_ratio(requests))

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(arrival_rates, queue_sizes, success_ratios, c='r', marker='o')

    ax.set_xlabel('Arrival Rate')
    ax.set_ylabel('Queue Size')
    ax.set_zlabel('Success Ratio')
    ax.set_title(f'Success Ratio for {queue_mechanism} (3D)')

    plt.show()


def analyze_simulations(simulations: Dict[Tuple[float, int], List[Request]], queue_mechanism: str):
    # Plot success ratio in 3D
    plot_success_ratio_3d(simulations, queue_mechanism)
