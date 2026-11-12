# Type 3 ref audit: cut rhythm and transition gimmicks ("secret sauce")

Ref: refs/type3_yt/ref.mp4 ("How a Chinese Spy Got Inside Nvidia", Paper Billions, 19:48, 16:9).
Method (2026-11-12): ffmpeg scdet on 0:00-4:00 (79 cuts), 10 fps frame strips ±0.45 s around 36 cuts
(refs/type3_yt/tr2/sheet*.jpg), earshot timeline on 0:00-1:25 (sound on every cut).

## Rhythm (measured)
- Shot length: median **2.3 s** (p25 1.5 s, p75 3.5 s). Our Part 1 v1 averaged 3.2 s: too slow.
- The camera is never static: every shot pushes in, pans, or something moves.
- About every 15-20 s, one key sentence sits alone on a black card, typed on letter by letter.
  The voice keeps going, so the picture "breathes".

## Visual transitions and gimmicks (seen in the strips)
| # | Gimmick | Where in the ref | What it does |
|---|---|---|---|
| V1 | **Whip pan**: 2-3 frames of horizontal motion smear between two places | 0:01.9 dinner → world map | Fast place change, never a plain cut |
| V2 | **Match cut on an object/light**: push into an object, next shot starts on the same object from another angle | 0:26.6 green chip glow → chip under the table | Ties two scenes with one thing |
| V3 | **Punch-through**: camera dives into a photo/document, white-out, then a title | 0:41.7 photo → white → "The Man With the Key" | Big section change |
| V4 | **Black type-on card**: key line alone, handwritten font, typed | 0:04, 0:06, 0:20, 0:22, 0:30, 0:32, 0:42, 0:50, 1:13 | Punctuation and suspense |
| V5 | **Diegetic flash**: camera flash, polaroids pop in, viewfinder frame tilts | 0:17.6-0:18.4, 0:37.2 | Evidence, "someone is watching" |
| V6 | **Diagram over the scene**: top-down view, red lines, X marks, name tags | 0:10.6, 0:32-0:35 | Explains relations at a glance |
| V7 | **Locked set, jump cuts**: same background, characters/props change between cuts | 1:04-1:11 porch | Cheap rhythm, time passing |
| V8 | **Map with an animated route arc** | 0:53-1:00 | Place/time jump |
| V9 | **Time tunnel**: light streaks rushing at the camera | 0:50.3 | Flashback |
| V10 | **Magnifier reveal** on a document | 1:11-1:13 | Detail reveal |
| V11 | **Chapter title after the cold open** (~40 s in) | 0:41.8 | Hook first, title second |

## Sound on transitions (earshot, 0:00-1:25)
- Music: **light instrumental underscore, no heavy beat** (user correction 2026-11-12; earshot mis-tagged it as funk because it heard the voice mixed in). Loudness is steady: LRA 2.5 LU, -14.5 LUFS.
- **Music drops out completely** from 0:18 to 0:39: voice only, for tension. It comes back on the chapter title:
  a 0.65 s silent gap (0:40.25), then a whoosh, then an **orchestral stab** (0:41.8).
- **Risers/reverse swells peak on the cut** into big moments (0:07.5, 0:22.1, 0:27.8, 0:36.3).
- A whip-pan whoosh sits on place changes (0:18.5).
- Pops sit on UI elements, tags and polaroids (0:01.4, 0:25.6, 0:44.5). Glockenspiel notes accent reveals (0:13.3, 0:32.6).
- 89% of cuts have a sound onset within 100 ms. Most of them are a narration onset or a small accent, not a whoosh on every cut.

## How we apply it (type 3, our CI)
1. Cut faster: median ~2.3 s. Split long beats into 2-3 shots, or use jump cuts on one plate (V7).
2. Cold open → title card. The hook ends on the motto card, then a chapter title "NVIDIA: 30 วันก่อนเจ๊ง".
   Music drops before the title, then whoosh + stab.
3. Use a different transition for each kind of change:
   - place change → whip pan (V1)
   - flashback → time tunnel with a rolling year counter in brand blue (V9); this is our data angle
   - big reveal → punch-through to white (V3)
   - same object across scenes → match cut (V2): napkin chip sketch → NV1 box
4. Tension stretch (1997 runway) runs voice-only with a clock tick; music returns for the CTA (S1).
5. Risers/swells peak on the cuts into cards. Pops go on tags. Do not whoosh every cut: about 1 in 3 cuts, on place changes only.

## Layer anatomy of one ref frame (user-flagged, 2026-11-12: "เขามีเลเยอร์ยัน bg")
Dinner shot (0:01-0:04): 1) background wall + window bokeh lights, softly blurred (depth of field);
2) characters sharp, soft gradient shading on the heads, warm rim/halo light from behind, candle light from below;
3) foreground table, cloth, glasses, flowers, candle = the key light source;
4) a cut-away layer UNDER the table (green glow, a gloved hand passing the chip): one frame tells two stories;
5) a small location label at the bottom-left.
=> Our art must be produced as SEPARATE layers (BG, characters, FG props, light sources) and composited with blur by depth,
rim light, light pools, glows and particles, with per-layer parallax on camera moves. Palette stays bright CI.
