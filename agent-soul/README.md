# Agent SOUL Framework

Persistent constitution pattern for autonomous AI agents.

## Concept

Each agent has a `SOUL.md` — a stable identity document that survives across sessions:
- Identity (name, role, owner relationship)
- Communication preferences (language, register, anti-patterns)
- Capabilities (what tools / accounts the agent controls)
- Autonomy boundaries (act vs ask)
- Memory rules (what to save, what not to)
- Verification / escalation patterns

## Why

Stateless LLMs forget context between sessions. SOUL.md gets injected on every conversation start, giving the agent consistent personality, boundaries, and operational rules without hardcoding them in the system prompt.

## Sample structure

See `SOUL.example.md` for a working template.
