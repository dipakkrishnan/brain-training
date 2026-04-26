# Contributing

Brain Training Arena is a bring-your-own-harness benchmark. You may use any model, agent, prompt, framework, runtime, or hosting setup. This repo standardizes the challenge, submission metadata, and evaluation loop.

## Submit a Game

1. Pick a challenge from `challenges/<challenge-id>/CHALLENGE.md`.
2. Optionally provide one or more skill files from `skills/<skill-id>/SKILL.md` to the model.
3. Build a playable game using your own harness.
4. Host the game or provide a source URL with one-command local run instructions.
5. Add one JSON file under `submissions/`.
6. Run validation:

```sh
uv run brain-training validate-submissions
```

7. Open a pull request.

## Submission Policy

Submission PRs should normally be metadata-only. Generated game source should live in a separate repo, hosted app, or artifact.

Each submission JSON must match `submissions/submission.schema.json`.

Required fields:

- `id`
- `challenge_id`
- `title`
- `model`
- `harness`
- `skills_used`
- `play_url`
- `source_url`
- `intended_cognitive_skill`
- `session_length_minutes`
- `description`

Prefer a public playable URL in `play_url`. If the game is not hosted, use the best launch target available and include one-command local run instructions in `description`.

## Evaluation

Arena evaluation compares submissions for the same challenge. Evaluators judge pairwise matchups on:

- replay preference
- intellectual interest
- challenge fit
- clarity
- novelty

Local votes are written to `arena/votes.jsonl`, which is ignored by git.
