"""
Question-solving context strategies.
Each module handles one question type (per-option MCQ, batch MCQ, TF).
"""

from agent.context.per_option import react_solve_one_option
from agent.context.batch import solve_batch
from agent.context.tf import solve_tf
from agent.context._common import build_single_option_context

__all__ = ["react_solve_one_option", "solve_batch", "solve_tf", "build_single_option_context"]