# Brain Training Game Designer

Use this skill when creating a brain-training game for a challenge.

## Design Process

1. Restate the target cognitive skill in concrete player behaviors.
2. Propose a core loop that can be learned in under 60 seconds.
3. Define the game state, legal actions, scoring, and end condition.
4. Add difficulty knobs that preserve the target cognitive skill.
5. Identify why the game should become more interesting with replay.
6. Specify failure cases where the game might become confusing, too random, or too shallow.
7. Produce a playable artifact and concise rules.

## Game Design Checklist

- The cognitive target is exercised by repeated player decisions.
- The rules are short enough to explain before play.
- The scoring system rewards the intended skill.
- Randomness creates variety without overwhelming skill.
- The first move is obvious.
- A full session can finish in the requested time.
- The game has at least one meaningful difficulty knob.

## Submission Expectations

The final output must be evaluable by a human. Prefer a public playable web URL. If hosting is not available, provide a source URL with one-command local run instructions.

Provide:

1. Playable artifact
   - preferred: public playable URL
   - acceptable: public source URL with one-command local run instructions

2. Submission metadata JSON matching `submissions/submission.schema.json`
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

3. Evaluator notes
   - concise rules summary
   - intended cognitive skill
   - expected session length
   - anything needed to launch or understand the game

Do not treat design prose alone as a complete answer. The output should make it possible for someone else to play the game and submit it to the arena.
