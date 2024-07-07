import fire
from multiprocessing import Process, Manager, Queue
import os
import json
from behavior_eval.evaluation.action_sequence.action_sequence_evaluator import ActionSequenceEvaluator
from collections import defaultdict
import behavior_eval
from typing import Optional

def evaluate_llm_response(demo_name, result_list, lock, output_path, actions_raw):
    ase = ActionSequenceEvaluator(demo_name=demo_name)
    rst = {
        "identifier": demo_name,
        "llm_rst": ase.evaluate_all(actions_raw),
    }
    with lock:
        result_list.append(rst)
        # Append to the file in real-time
        with open(output_path, 'w') as f:
            json.dump(list(result_list), f, indent=4)

def worker_task(queue, result_list, lock, output_path):
    while True:
        task = queue.get()
        if task is None:  # Sentinel value to exit
            break
        demo_name, actions_raw = task
        evaluate_llm_response(demo_name, result_list, lock, output_path, actions_raw)

def evaluate_one_llm(llm_response_path, worker_num: Optional[int] = 1, result_dir: Optional[str] = './results'):
    manager = Manager()
    result_list = manager.list()
    lock = manager.Lock()

    llm_response_name = os.path.basename(llm_response_path).split('.')[0]
    output_path = os.path.join(result_dir, f'error_analysis/{llm_response_name}.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    llm_response = json.load(open(llm_response_path))

    # If output_path exists, load first, skip the processed ones
    if os.path.exists(output_path):
        existing_results = json.load(open(output_path))
        processed_identifiers = set([r["identifier"] for r in existing_results])
        llm_response = [r for r in llm_response if r["identifier"] not in processed_identifiers]
        result_list.extend(existing_results)
    
    worker_num = min(worker_num, len(llm_response))
    task_queue = Queue()
    workers = []

    for i in range(worker_num):
        worker = Process(target=worker_task, args=(task_queue, result_list, lock, output_path))
        worker.start()
        workers.append(worker)

    for response in llm_response:
        task_queue.put((response['identifier'], response['llm_output']))

    for i in range(worker_num):
        task_queue.put(None)

    for worker in workers:
        worker.join()

    result_list = list(result_list)  
    with open(output_path, 'w') as f:
        json.dump(result_list, f, indent=4)
    print(f"Results saved to {output_path}")

    summary = {
        "error_type": {},
        "goal_rst": {},
    }
    
    for item in result_list:
        identifier = item['identifier']
        rst = item['llm_rst']
        for k, v in rst.items():
            if k in summary:
                if isinstance(v, dict):
                    for kk, vv in v.items():
                        if vv is not None:
                            if isinstance(vv, int) or isinstance(vv, float):
                                summary[k][kk] = summary[k].get(kk, 0) + vv
                            elif isinstance(vv, bool):
                                summary[k][kk] = summary[k].get(kk, 0) + int(vv)
                            else:
                                summary[k][kk] = summary[k].get(kk, 0) + 1
                                
    output_path = output_path.replace('error_analysis/', 'summary/')
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=4)
    return summary

def evaluate_results(llm_response_dir, worker_num: Optional[int] = 1,result_dir: Optional[str] = './results'):
    os.makedirs(result_dir, exist_ok=True)
    for filename in os.listdir(llm_response_dir):
        file_path = os.path.join(llm_response_dir, filename)
        if os.path.isfile(file_path):
            print(f"Processing file: {file_path}")
            evaluate_one_llm(file_path, worker_num, result_dir)

if __name__ == '__main__':
    fire.Fire(evaluate_results)
