"""Per-option ReACT loop — each option gets its own independent search loop (MCQ, max 6 rounds)."""
# Re-export from _common for backward compatibility
from agent.context._common import run_react_loop, MAX_ROUNDS, BATCH_MAX_ROUNDS

react_solve_one_option = run_react_loop