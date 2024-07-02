import fire
from multiprocessing import Process, Manager
import  os
import json
from behavior.evaluation.action_sequence.action_sequence_evaluator import ActionSequenceEvaluator
from collections import defaultdict
import behavior
from typing import Optional

def evaluate_llm_response(demo_name, result_list, lock, output_path,actions_raw):
    demo_path = os.path.join(behavior.vr_demo_path, demo_name + '.hdf5')
    ase = ActionSequenceEvaluator(demo_path=demo_path)
    rst = {
        "identifier": demo_name,
        "llm_rst": ase.evaluate_all(actions_raw),
    }
    with lock:
        result_list.append(rst)
        # Append to the file in real-time
        with open(output_path, 'w') as f:
            json.dump(list(result_list), f, indent=4)

def evaluate_one_llm(llm_response_path,worker_num: Optional[int] = 1):
    manager = Manager()
    result_list = manager.list()
    lock = manager.Lock()

    llm_response_name=os.path.basename(llm_response_path).split('.')[0]
    output_path = os.path.join(behavior.action_seq_result_path, f'error_analysis/{llm_response_name}.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    llm_response=json.load(open(llm_response_path))

    # if output_path exists, load first, skip the processed ones
    if os.path.exists(output_path):
        result_list=json.load(open(output_path))
        processed_identifiers=set([r["identifier"] for r in result_list])
        llm_response=[r for r in llm_response if r["identifier"] not in processed_identifiers]
    
    if worker_num > 1:
        worker_num = min(worker_num, len(llm_response))
        workers = []
        for i in range(worker_num):
            worker = Process(target=evaluate_llm_response, args=(llm_response[i]['identifier'], result_list, lock, output_path,llm_response[i]["llm_output"]))
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()
    else:
        for i in range(len(llm_response)):
            evaluate_llm_response(llm_response[i]['identifier'], result_list, lock, output_path,llm_response[i]["llm_output"])

    result_list = list(result_list)  # Convert from manager list to regular list
    with open(output_path, 'w') as f:
        json.dump(list(result_list), f, indent=4)
    print(f"Results saved to {output_path}")

    summary={
            "error_type":{
            },
            "goal_rst":{
            },
        }
    
    for item in result_list:
        identifier=item['identifier']
        rst=item['llm_rst']
        for k,v in rst.items():
            if k in summary:
                if isinstance(v,dict):
                    for kk,vv in v.items():
                        if vv is not None:
                            if isinstance(vv,int) or isinstance(vv,float):
                                summary[k][kk]=summary[k].get(kk,0)+vv
                            elif isinstance(vv,bool):
                                summary[k][kk]=summary[k].get(kk,0)+int(vv)
                            else:
                                summary[k][kk]=summary[k].get(kk,0)+1
    output_path=output_path.replace('error_analysis/','summary/')
    with open(output_path, 'w') as f:
        json.dump(summary,f,indent=4)
    return summary

def evaluate_all_llm(llm_response_dir,worker_num: Optional[int] = 1):
    os.makedirs(behavior.action_seq_result_path, exist_ok=True)
    for filename in os.listdir(llm_response_dir):
        file_path = os.path.join(llm_response_dir, filename)
        if os.path.isfile(file_path):
            print(f"Processing file: {file_path}")
            evaluate_one_llm(file_path,worker_num)

if __name__ == '__main__':
    fire.Fire(evaluate_all_llm)