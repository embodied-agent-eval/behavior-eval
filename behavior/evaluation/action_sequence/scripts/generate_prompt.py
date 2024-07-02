import os
import json
from typing import Optional
from multiprocessing import Process, Manager
import behavior
from behavior.evaluation.action_sequence.action_sequence_evaluator import ActionSequenceEvaluator
import fire

def get_llm_prompt(demo_name, result_list, lock, output_path):
    demo_path = os.path.join(behavior.vr_demo_path, demo_name + '.hdf5')
    env = ActionSequenceEvaluator(demo_path=demo_path)
    prompt = env.get_prompt()
    rst = {
        "identifier": demo_name,
        "llm_prompt": prompt,
    }
    with lock:
        result_list.append(rst)
        # Append to the file in real-time
        with open(output_path, 'w') as f:
            json.dump(list(result_list), f, indent=4)

def main(worker_num: Optional[int] = 1):
    with open(behavior.demo_name_path) as f:
        demo_list = json.load(f)

    manager = Manager()
    result_list = manager.list()
    lock = manager.Lock()

    output_path = os.path.join(behavior.action_seq_result_path, 'reconstructed_prompts/action_sequence_prompts.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if worker_num > 1:
        worker_num = min(worker_num, len(demo_list))
        workers = []
        for i in range(worker_num):
            worker = Process(target=get_llm_prompt, args=(demo_list[i], result_list, lock, output_path))
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()
    else:
        for demo_name in demo_list:
            get_llm_prompt(demo_name, result_list, lock, output_path)

    result_list = list(result_list)  # Convert from manager list to regular list

    print(f"Results saved to {output_path}")
    return result_list

# Example usage
if __name__ == "__main__":
    fire.Fire(main)