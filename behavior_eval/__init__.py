import logging
import os
import yaml

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

__version__ = "1.0"

# Load global configuration
config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "global_config.yaml")
logger.debug(f"Loading configuration from {config_path}")
try:
    with open(config_path) as f:
        global_config = yaml.load(f, Loader=yaml.FullLoader)
        logger.debug(f"Loaded global configuration: {global_config}")
except Exception as e:
    logger.error(f"Failed to load configuration: {e}")
    raise

# Override paths from environment variables if set
demo_name_path = os.environ.get("BEHAVIOR_DEMO_NAMES", global_config.get("demo_name_path"))
demo_name_path = os.path.expanduser(demo_name_path)
logger.debug(f"Demo Name Path: {demo_name_path}")

demo_stats_path = os.environ.get("BEHAVIOR_DEMO_STATS", global_config.get("demo_stats_path"))
demo_stats_path = os.path.expanduser(demo_stats_path)
logger.debug(f"Demo Name Path: {demo_stats_path}")

action_seq_result_path = os.environ.get("BEHAVIOR_ACTION_SEQ_RESULT", global_config.get("action_seq_result_path"))
action_seq_result_path = os.path.expanduser(action_seq_result_path)
logger.debug(f"Action Sequence Result Path: {action_seq_result_path}")

goal_int_result_path = os.environ.get("BEHAVIOR_GOAL_INT_RESULT", global_config.get("goal_int_result_path"))
goal_int_result_path = os.path.expanduser(goal_int_result_path)
logger.debug(f"Goal Intention Result Path: {goal_int_result_path}")

goal_int_resources_path = os.environ.get("BEHAVIOR_GOAL_INT_RESOURCE", global_config.get("goal_int_resources_path"))
goal_int_resources_path = os.path.expanduser(goal_int_resources_path)
logger.debug(f"Goal Intention Resource Path: {goal_int_resources_path}")



root_path = os.path.dirname(os.path.realpath(__file__))

if not os.path.isabs(demo_name_path):
    demo_name_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), demo_name_path)
if not os.path.isabs(demo_stats_path):
    demo_stats_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), demo_stats_path)
if not os.path.isabs(action_seq_result_path):
    action_seq_result_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), action_seq_result_path)
if not os.path.isabs(goal_int_result_path):
    goal_int_result_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), goal_int_result_path)
if not os.path.isabs(goal_int_resources_path):
    goal_int_resources_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), goal_int_resources_path)
