import os
import ast
import json
import fire
import behavior
from typing import Optional
from multiprocessing import Process, Manager
from behavior.evaluation.subgoal_decomposition.subgoal_eval_utils import evaluate_task, get_all_raw_task_goal, get_all_task_list, EvalStatistics

def run_llm_response(demo_name, result_dict, lock, llm_plan_path, eval_stat_path):
    report = evaluate_task(demo_name, llm_plan_path)
    goal_info = report[-1]
    with lock:
        eval_statistics = EvalStatistics(get_all_task_list(), eval_stat_path)
        if report[0] != 'Correct':
            eval_statistics.update_eval_rst_dict(demo_name, False, str(report[:-1]), goal_info)
        else:
            eval_statistics.update_eval_rst_dict(demo_name, True, str(report[:-1]), goal_info)
        eval_statistics.save_eval_rst_dict()
    ...