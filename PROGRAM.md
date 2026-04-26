You are participating in Brain Training Arena, a BYOH benchmark for AI-generated brain-training games.

Your task is to create one playable game for the challenge in:

challenges/working-memory/CHALLENGE.md

Use the game-design guidance in:

skills/brain-training-game-designer/SKILL.md

Your output must be evaluable by a human. Build a complete playable game, not just a design description.

Requirements:

- The game must exercise working memory.
- The game should be playable by one person in 3-5 minutes.
- A new player should understand the loop within 60 seconds.
- Include clear rules, scoring, and a complete play loop.
- Include at least one difficulty progression or adaptive difficulty mechanism.
- Skill should matter more than luck.
- No account creation or paid services.
- Prefer a browser-playable game.

Deliverables:

1. A playable game artifact.
   - Preferred: browser-playable local app or hosted URL.
   - Acceptable: source repo with one-command local run instructions.

2. A submission JSON matching:
   submissions/submission.schema.json

3. Brief evaluator notes:
   - rules summary
   - intended cognitive skill
   - expected session length
   - launch instructions

Use this metadata:

- challenge_id: working-memory
- skills_used: ["brain-training-game-designer"]
- harness: HARNESS_NAME
- model: MODEL_NAME

Before finishing:

- Run the game locally if possible.
- Run any tests or build checks that are appropriate.
- Make sure the submission JSON validates with:
  uv run brain-training validate-submissions

Do not stop at a plan. Implement the game and produce the submission metadata.
