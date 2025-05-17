import os
import time

IS_DEV = os.getenv("IS_DEV", "false").lower() == "true"

def dev_log(message):
    if IS_DEV:
        print(f"[DEV] {message}")

def timed_action(action_name, func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    dev_log(f"{action_name} выполнено за {elapsed:.3f} сек")
    return result 