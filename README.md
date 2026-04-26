# Brain Training Arena

A thin benchmark and arena for evaluating AI-generated brain-training games.

The core question:

> Given the same challenge and game-design skill, which models produce games that humans find fun, novel, replayable, and intellectually interesting?

This is a bring-your-own-harness project. Models, coding agents, runtimes, and hosting setups can vary. The repo defines the shared challenges, optional skills, submission metadata, and arena evaluation protocol.

## Repository Shape

```text
challenges/
  working-memory/
    CHALLENGE.md
  probabilistic-reasoning/
    CHALLENGE.md
  verbal-fluency/
    CHALLENGE.md

skills/
  brain-training-game-designer/
    SKILL.md
  game-evaluator/
    SKILL.md

submissions/
  submission.schema.json
  example-working-memory.json

arena/
  README.md
```

## Concepts

- Challenge: the assignment a model must satisfy.
- Skill: reusable guidance that may be supplied to a model or evaluator.
- Submission: metadata for a generated playable game.
- Arena: the human pairwise evaluation loop.

## CLI

Run the app:

```sh
uv run brain-training list-challenges
uv run brain-training list-skills
uv run brain-training validate-submissions
```

Install dependencies and create/update the local environment:

```sh
uv sync
```
