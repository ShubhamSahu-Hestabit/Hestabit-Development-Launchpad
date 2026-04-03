import logging
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

logger = logging.getLogger(__name__)

# Shared executor instance used by CoderAgent
executor = LocalCommandLineCodeExecutor(work_dir=".")