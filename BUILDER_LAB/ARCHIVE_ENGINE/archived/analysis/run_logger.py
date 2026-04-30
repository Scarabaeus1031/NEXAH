import json
import os
import datetime

def create_run_id():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def save_run(config, metrics, save_dir, prefix="run"):
    os.makedirs(save_dir, exist_ok=True)

    run_id = create_run_id()

    data = {
        "run_id": run_id,
        "config": config,
        "metrics": metrics
    }

    path = os.path.join(save_dir, f"{prefix}_{run_id}.json")

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✔ Run saved → {path}")

    return run_id
