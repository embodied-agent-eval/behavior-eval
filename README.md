# Installation and Usage Guide for `behavior-eval`

## Installation

### Step 1: Install `behavior-eval`, `iGibson`, and `bddl`

#### For Windows Users:

1. Clone the `iGibson` repository:
   ```
   git clone https://github.com/embodied-agent-eval/iGibson.git --recursive
   ```
2. Navigate to the `iGibson` directory:
   ```
   cd iGibson
   ```
3. Install `iGibson`:
   - Editable mode:
     ```
     pip install -e .
     ```
   - User mode:
     ```
     pip install .
     ```
4. Install `behavior-eval`:
   ```
   pip install behavior-eval
   ```

#### For Other Users:

1. Install `behavior-eval` directly:
   ```
   pip install behavior-eval
   ```

### Step 2: Download Assets for `iGibson`

```
python -m behavior_eval.utils.download_utils
```

### Note:

There might be issues during the installation of iGibson. Please see the system requirements section of the [iGibson installation guide](https://stanfordvl.github.io/iGibson/installation.html).

We have successfully tested the installation on Linux servers, Windows 10+, and Mac OS X.

To minimize and identify the potential issues, we recommend the following steps:

1. **Create a Conda Virtual Environment**.
2. **Install CMake Using Conda**: 
   ```
   conda install cmake
   ```
3. **Use pip Install with Verbose Mode**:
   ```
   pip install -v behavior-eval
   ```

## Usage

To run `behavior-eval`, use the following command:

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
