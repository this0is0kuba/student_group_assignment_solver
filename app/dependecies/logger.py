import logging.config
import os

import yaml

config_path = os.path.join(os.path.dirname(__file__), 'configs', 'logging.yaml')

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

if os.getenv("TEST_MODE"):  # this prevents creating app.log file in test mode.
    del config["handlers"]["file"]
    del config["loggers"]["student_group_assignment_solver"]

logging.config.dictConfig(config)

if os.getenv("TEST_MODE"):
    logger = logging.getLogger("student_group_assignment_solver_test")
else:
    logger = logging.getLogger("student_group_assignment_solver")

