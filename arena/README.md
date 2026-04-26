# Arena

The arena is the human evaluation loop for submitted games.

## Evaluation Loop

1. Choose a challenge.
2. Select two submissions for that challenge.
3. Ask an evaluator to play both games.
4. Record pairwise judgments.
5. Aggregate votes by challenge, model, harness, and skill set.

## Initial Pairwise Questions

- Which game would you rather play again?
- Which game felt more intellectually interesting?
- Which game better matched the challenge?
- Which game had clearer rules?
- Which game felt more novel?

## Suggested Vote Record

```json
{
  "challenge_id": "working-memory",
  "left_submission_id": "model-a-game",
  "right_submission_id": "model-b-game",
  "preferred_replay": "left",
  "preferred_interest": "right",
  "preferred_challenge_fit": "left",
  "preferred_clarity": "left",
  "preferred_novelty": "right"
}
```

The first implementation can be a simple local app or even a JSONL vote log. The important property is that every vote compares games from the same challenge.
