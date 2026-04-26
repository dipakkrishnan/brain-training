# Submissions

Submissions describe games produced for a challenge. The game itself can be hosted anywhere or provided as a separate source artifact.

This repo is bring-your-own-harness. Generated game source should normally live outside this repo; submit one metadata JSON file here so the arena can evaluate it.

Each JSON file should match `submission.schema.json` and include:

- the challenge attempted
- the model and harness used
- the skills supplied to the model
- a playable URL or local run instructions
- a source URL, if available
- a short description for arena evaluators

Prefer a public playable URL in `play_url`. If the game is not hosted, use `play_url` for the best launch target available and include one-command local run instructions in `description`.

Validate submissions with:

```sh
uv run brain-training validate-submissions
```
