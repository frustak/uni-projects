import threading
from typing import List


CENTER_SPACE = 40


def print_centered(text: str):
    """Print a custom centered string."""
    print(f" {text} ".center(CENTER_SPACE, "*"))


def wait_for_threads(threads: List[threading.Thread]):
    """Wait for all threads to finish"""
    for thread in threads:
        if thread.is_alive():
            thread.join()
