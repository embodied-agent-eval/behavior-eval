import fire
from typing import Optional
from behavior.evaluation.action_sequence.scripts.evaluate_results import evaluate_results as action_sequence_evaluate_results
from behavior.evaluation.action_sequence.scripts.generate_prompts import generate_prompts as action_sequence_generate_prompts

def main(module:Optional[str]="action_sequence",func:Optional[str]="evaluate_result",worker_num:Optional[int]=1,llm_response_dir:Optional[str]=None):
    """
    module: goal_interpretation,action_sequence,subgoal_decomposition,transition_modeling
    func: evaluate_result,generate_prompts
    worker_num: number of workers for multiprocessing
    llm_response_dir: directory containing llm responses (helm outputs)
    """
    
    if func=="evaluate_result":
        if llm_response_dir is None:
            return "llm_response_dir is required for evaluate_result"
    if module == "action_sequence":
        if func == "evaluate_result":
            action_sequence_evaluate_results(llm_response_dir,worker_num)
        elif func == "generate_prompts":
            action_sequence_generate_prompts(worker_num)

if __name__ == '__main__':
    fire.Fire(main)