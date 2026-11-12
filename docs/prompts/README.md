# Image briefs (provider-neutral)

The exact briefs that made the baseline plates. Each one works as a Codex task (`python tools/run_codex.py <brief> <name>`),
or paste the "Locked style" paragraph + one plate line into any image API / MCP prompt.

| Brief | Made | Used by |
|---|---|---|
| codex_type2_plates.md | `assets/plates_min/p01-p13` | type 2 news (paper collage, minimal) |
| codex_type3_plates.md | `assets/plates/b01-b08` | type 3 story (bright flat vector, CI palette) |
| codex_type3_plates_topdown.md | `assets/plates/b09-b10` | type 3 top-down table shots |

Rules: keep the Locked style paragraph word for word inside a series (one look per clip). Colours in it are the brand.json
colours; if the brand colours change, change them here too. No readable text, logos or faces in plates (graphics go on top in code).
Output folders inside a brief (`out/...`) are relative to the Codex job folder; copy the PNGs into the job's `assets/` afterwards.
