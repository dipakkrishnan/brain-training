# Submissions

Submissions describe games produced for a challenge. The game itself can be hosted anywhere or provided as a separate source artifact.

Each JSON file should match `submission.schema.json` and include:

- the challenge attempted
- the model and harness used
- the skills supplied to the model
- a playable URL or local run instructions
- a short description for arena evaluators

Validate submissions with:

```sh
uv run brain-training validate-submissions
```
