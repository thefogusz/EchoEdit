# EchoEdit (Data Echooo vertical videos): working rules for Claude

Read `.claude/skills/de-video/SKILL.md` before any clip work, and `docs/REF_SPEC.md` before any edit or review.
They hold every rule agreed with the Data Echooo owner, with the reason. These rules here are how to work with the team.

## Talk
- Reply in Thai. Keep file names, tool names and commands as they are.
- Before generating a voice or a whole clip, agree the script, the hook (first 5 s) and the plan with the user first.
- Report honestly: what was checked (frames looked at, levels measured) and what was not.

## Money and accounts
- Anything that costs per use (ElevenLabs, image/video APIs, paid MCP tools): say what it is and the price, wait for a yes.
- Default routing (owner rule 2026-11-12): ElevenLabs = voice + word timing only, never images or video.
  Images = Codex CLI (`tools/run_codex.py`, inside a ChatGPT plan). Music/SFX = Artlist or `library/audio`.
- Never print, read aloud or commit an API key. Keys live in `~/.config/dataechooo/` only.

## Machine
- New machine or something missing: `python tools/setup.py` first. Python runs through `.venv`
  (Windows `.venv\Scripts\python`, macOS/Linux `.venv/bin/python`).
- Before choosing a provider: `python tools/capabilities.py typeN`, then check your own MCP tools, and offer the
  fewest-tool bundle (cheapest first).
- A baseline end to end: `python tools/rebuild.py typeN` (`--preview 3` to test).

## Quality bar
- The three clips in `deliverables/` are the minimum for their type. Compare every new clip with them.
- Look at full-size frames of every shot before showing anything (cut marks, clipped Thai text, tofu boxes, covered faces).
- Brand tokens (colours, fonts, voices) come only from `brand/brand.json`. Pages use `DE.color.*` and the font aliases.

## When the user corrects something
Write it into `.claude/skills/de-video/SKILL.md` and `docs/REF_SPEC.md` in the same turn (rule + date + reason),
so the next session and the next teammate start from the agreed state.

## Finishing a clip
`python tools/finalize_job.py <job> <final.mp4>` (dry run, show the list, then `--yes`). Commit only what the final
needs: no drafts, no renders in `out/`, no Artlist files, no third-party raw media, no keys. Branch per job, then a PR.
