import logging.config
import yaml

with open('configs/logging.yaml', 'r') as file:
    config = yaml.safe_load(file)

logging.config.dictConfig(config)
logger = logging.getLogger("student_group_assignment_solver")
