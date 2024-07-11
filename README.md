# Installation and Usage Guide for `behavior-eval`

## Installation

### Step 1: Create a Conda Virtual Environment for `behavior-eval`
```
conda create -n behavior-eval python=3.8 -y
conda activate behavior-eval
```

### Step 2: Install `behavior-eval`
```
pip install behavior-eval
```

### Step 3: Install `iGibson`

There might be issues during the installation of `iGibson`. 

To minimize and identify potential issues, we recommend:

1. Review the system requirements section of the [iGibson installation guide](https://stanfordvl.github.io/iGibson/installation.html).

2. **Install CMake Using Conda (do not use pip)**: 
   ```
   conda install cmake
   ```

3. **Install `iGibson`**: 
   ```
   python -m behavior_eval.utils.install_igibson_utils
   ```
We've successfully tested the installation on Linux servers, Windows 10+, and Mac OS X.
### Step 4: Download Assets for `iGibson`
```
python -m behavior_eval.utils.download_utils
```

## Usage

To run `behavior-eval`, use the following command:

```
python -m behavior_eval.main
```

(By default, this will generate the prompts for action sequencing.)

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