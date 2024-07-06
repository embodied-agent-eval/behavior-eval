import os
import json
import behavior
import fire
from multiprocessing import Process, Manager
import behavior
from behavior.evaluation.action_sequence.action_sequence_evaluator import ActionSequenceEvaluator
from behavior.evaluation.subgoal_decomposition.subgoal_prompts_utils import get_subgoal_prompt


def get_llm_output(demo_name, result_list, lock, output_path):
    env = ActionSequenceEvaluator(demo_name=demo_name)
    try:
        prompt = get_subgoal_prompt(env)
    except:
        raise Exception(f"Failed to generate prompt for {demo_name}")
    rst = {
        "identifier": demo_name,
        "llm_prompt": prompt,
    }
    with lock:
        result_list.append(rst)
        with open(output_path, 'w') as f:
            json.dump(list(result_list), f, indent=4)

def generate_prompts(worker_num: int = 1):
    with open(behavior.demo_name_path) as f:
        demo_list = json.load(f)
    
    manager = Manager()
    result_list = manager.list()
    lock = manager.Lock()

    output_path = os.path.join(behavior.subgoal_dec_result_path, 'reconstructed_prompts', 'subgoal_decomposition_prompts.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if worker_num > 1:
        worker_num = min(worker_num, len(demo_list))
        workers = []

        for i in range(worker_num):
            worker = Process(target=get_llm_output, args=(demo_list[i], result_list, lock, output_path))
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()
    else:
        for demo_name in demo_list:
            get_llm_output(demo_name, result_list, lock, output_path)
    
    result_list = list(result_list)
    with open(output_path, 'w') as f:
        json.dump(list(result_list), f, indent=4)
    print(f"Results saved to {output_path}")
    return result_list

if __name__ == "__main__":
    fire.Fire(generate_prompts)