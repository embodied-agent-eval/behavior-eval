import fire
from typing import Optional
from behavior.evaluation.action_sequence.scripts.evaluate_results import evaluate_results as action_sequence_evaluate_results
from behavior.evaluation.action_sequence.scripts.generate_prompts import generate_prompts as action_sequence_generate_prompts
from behavior.evaluation.goal_interpretation.scripts.evaluate_results import evaluate_results as goal_interpretation_evaluate_results
from behavior.evaluation.goal_interpretation.scripts.generate_prompts import generate_prompts as goal_interpretation_generate_prompts

def main(module:Optional[str]="action_sequence",func:Optional[str]="evaluate_results",worker_num:Optional[int]=1,llm_response_dir:Optional[str]=None):
    """
    module: goal_interpretation,action_sequence,subgoal_decomposition,transition_modeling
    func: evaluate_results,generate_prompts
    worker_num: number of workers for multiprocessing
    llm_response_dir: directory containing llm responses (helm outputs)
    """
    
    if func=="evaluate_results":
        if llm_response_dir is None:
            return "llm_response_dir is required for evaluate_results"
    if func not in ["evaluate_results","generate_prompts"]:
        return "Invalid function, must be evaluate_results or generate_prompts"
    if module not in ["goal_interpretation","action_sequence","subgoal_decomposition","transition_modeling"]:
        return "Invalid module, must be goal_interpretation,action_sequence,subgoal_decomposition,transition_modeling"
    if module == "action_sequence":
        if func == "evaluate_results":
            action_sequence_evaluate_results(llm_response_dir,worker_num)
        elif func == "generate_prompts":
            action_sequence_generate_prompts(worker_num)
    elif module == "goal_interpretation":
        if func == "evaluate_results":
            goal_interpretation_evaluate_results(llm_response_dir)
        elif func == "generate_prompts":
            goal_interpretation_generate_prompts()

if __name__ == '__main__':
    fire.Fire(main)