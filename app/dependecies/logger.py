import logging.config
import os

import yaml

config_path = os.path.join(os.path.dirname(__file__), 'configs', 'logging.yaml')

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

logging.config.dictConfig(config)
logger = logging.getLogger("student_group_assignment_solver")
