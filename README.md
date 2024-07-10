
# Installation and Usage Guide for `behavior_eval`

## Step 1: Install `behavior_eval`, `iGibson`, and `bddl`

### For Windows users:
1. Clone the `iGibson` repository:
   ```
   git clone https://github.com/embodied-agent-eval/iGibson.git --recursive
   ```
2. Navigate to the `iGibson` directory:
   ```
   cd iGibson
   ```
3. Install `iGibson`:
   In editable mode:
   ```
   pip install -e .
   ```
   Or user mode:
   ```
   pip install .
   ```
5. Install `behavior_eval`:
   ```
   pip install behavior_eval
   ```
### For other users:
1. Install `behavior_eval` directly:
   ```
   pip install behavior_eval
   ```
   
## Step 2: Download Assets for `iGibson`
```
python -m behavior_eval.utils.download_utils
```

## Usage
To run `behavior_eval`, use the following command:
```
python -m behavior_eval.main
```

### Parameters:
- `module`: Specifies the module to use. Options are:
  - `goal_interpretation`
  - `action_sequence`
  - `subgoal_decomposition`
  - `transition_modeling`
- `func`: Specifies the function to execute. Options are:
  - `evaluate_results`
  - `generate_prompts`
- `worker_num`: Number of workers for multiprocessing.
- `llm_response_dir`: Directory containing LLM responses (HELM outputs).
- `result_dir`: Directory to store results.

### Example Usage:
1. To generate prompts using the `action_sequence` module:
   ```
   python -m behavior_eval.main --module=action_sequence --func=generate_prompts
   ```

2. To evaluate results using the `action_sequence` module:
   ```
   python -m behavior_eval.main --module=action_sequence --func=evaluate_results --llm_response_dir=<your_llm_response_dir>
   ```

Replace `<your_llm_response_dir>` with the path to your LLM response directory.
