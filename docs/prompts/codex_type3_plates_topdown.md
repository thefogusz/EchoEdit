# Task: 2 top-down background plates for the same animated story reel (image generation)

Generate 2 vertical images with your image generation tool. Save each as PNG in `out/story_brand/` (portrait 9:16 if possible, else 2:3, at least 1024 px wide).
Match the existing plates in `out/story_brand/` (b01..b08): open them and copy their exact style, palette, light and detail level.
These are TOP-DOWN shots, camera looking straight down at a table, used for "plans and money" moments; small props are drawn on top later by code, so keep the centre of the table clear.

## Locked style (use verbatim at the start of every prompt)
Flat 2D vector illustration background for a bright, friendly animated explainer, clean simple shapes, soft gentle gradients, no outlines, airy and optimistic. Strict palette: mostly very light ice blue and white (#F3F7FF, #FFFFFF), cobalt blue (#214AFF) as the main accent, light sky blue (#9EE8FF) and teal (#00C2BB) as secondary accents, ONE small touch of orange (#FE4C1C), dark ink (#1A1B1E) only for tiny details. Soft daylight, gentle soft shadows. No people, no hands, no readable text, no logos.

## Plates
1. `b09_diner_top.png` → straight top-down view of a diner table: white table top filling most of the frame, three coffee cups on saucers near the edges, a sugar jar, a napkin dispenser at one edge, a cobalt booth seat visible at the top and bottom edges. Centre of the table empty.
2. `b10_desk_top.png` → straight top-down view of a 1990s office desk / meeting table: light table top filling the frame, a beige keyboard and a desk lamp at the edges, a coffee mug, a few pens, a closed folder at one corner. Centre of the table empty.

Acceptance: 2 PNGs with exactly these names, portrait, at least 1024 px wide, same style as b01-b08, no people, no readable text or logos.
Write only inside `out/story_brand/`. Final answer: list of files with pixel sizes.
