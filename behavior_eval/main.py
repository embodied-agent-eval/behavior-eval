import fire
from typing import Optional
<<<<<<< HEAD:behavior/main.py
from behavior_eval.evaluation.action_sequence.scripts.evaluate_results import evaluate_results as action_sequence_evaluate_results
from behavior_eval.evaluation.action_sequence.scripts.generate_prompts import generate_prompts as action_sequence_generate_prompts
from behavior_eval.evaluation.goal_interpretation.scripts.evaluate_results import evaluate_results as goal_interpretation_evaluate_results
from behavior_eval.evaluation.goal_interpretation.scripts.generate_prompts import generate_prompts as goal_interpretation_generate_prompts
from behavior_eval.evaluation.subgoal_decomposition.scripts.generate_prompts import generate_prompts as subgoal_decomposition_generate_prompts
=======
from behavior_eval.evaluation.action_sequence.scripts.evaluate_results import evaluate_results as action_sequence_evaluate_results
from behavior_eval.evaluation.action_sequence.scripts.generate_prompts import generate_prompts as action_sequence_generate_prompts
from behavior_eval.evaluation.goal_interpretation.scripts.evaluate_results import evaluate_results as goal_interpretation_evaluate_results
from behavior_eval.evaluation.goal_interpretation.scripts.generate_prompts import generate_prompts as goal_interpretation_generate_prompts
>>>>>>> 384c31586b4191b1cd21c66568a5160a563b3eb8:behavior_eval/main.py

def main(module:Optional[str]="action_sequence",func:Optional[str]="generate_prompts",worker_num:Optional[int]=1,llm_response_dir:Optional[str]=None):
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
        return f"Invalid module {module}, must be goal_interpretation,action_sequence,subgoal_decomposition,transition_modeling"
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
    elif module == "subgoal_decomposition":
        if func == "evaluate_results":
            raise NotImplementedError("This part is yet to be implemented")
        elif func == "generate_prompts":
            worker_num = worker_num if worker_num else 1
            subgoal_decomposition_generate_prompts(worker_num)


if __name__ == '__main__':
    fire.Fire(main)