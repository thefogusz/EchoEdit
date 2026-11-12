---
name: de-video
description: Make Data Echooo vertical videos (9:16 Thai) - talking-head edit (type 1), AI news with the mascot (type 2), animated storytelling (type 3: business / AI / solopreneur / biography). Use for any Data Echooo clip, script, caption, voice, music, SFX, mascot, background, render or review task in this repo.
---

# Data Echooo video pipeline (current state: 2026-11-12)

This file is the how. `docs/REF_SPEC.md` has every user review rule, numbered with the reason; read it before any edit.
`docs/REF_TYPE3_AUDIT.md` is the type 3 cutting playbook.
The user's own words win over this file. When they correct something, update this file and REF_SPEC in the same turn.

## Baseline (user, 2026-11-12): these three finals are the target for every new clip of their type
- Type 1: `deliverables/type1_talkinghead_forsample_v3.mp4` (job jobs/type1_talkinghead/2026-11-12_th_sample, plan_v3.py)
- Type 2: `deliverables/type2_news_fable52_v8.mp4` (job jobs/type2_news/2026-11-12_news_fable52, plan_v8.json)
- Type 3: `deliverables/type3_story_nvidia_p1_v3.mp4` (job jobs/type3_story/2026-11-12_story_nvidia, part1_scene_v3.py)
New clips start by copying the baseline job's pipeline and must be at least this good; the refs (refs/type1, AIพูด, refs/type3_yt) stay the direction to grow toward
(type 3 next step: ref-style layered art, see REF_TYPE3_AUDIT "Layer anatomy").

## What is fixed and what is swappable (user, 2026-11-12: the repo goes to the Data Echooo team)
Our job is the **principles that make the visuals work**: shot grammar, pacing, transitions, what moves on which word,
safe zones, caption rules, sound roles and levels. Assets are swappable and must never be hard-wired into a page.
- **Brand tokens: `brand/brand.json` is the only place.** `engine/web/de.js` reads it at load.
  - Colours: `colors` → `DE.color.<name>` (camelCase). Pages use `DE.color.*`, not hex literals.
  - Fonts: `fonts.<role>` = alias + family + faces (files in `brand/fonts`, licence beside them). Pages use only the aliases
    `DEHead` (Thai headline), `DEBody` (Thai body), `DELatin` (Latin display). A new font is a brand.json edit, no page edit.
  - Logo, safe zone, canvas, mascot: also brand.json.
- **Voices: `brand.json` → `voices`.** Add the team's own ElevenLabs voice as a profile (voice_id, model, speed, stability),
  point `by_type` at it, then `python pipelines/tts_elevenlabs.py script.txt out.mp3 --type type3` (or `--voice <profile|id>`).
  Check the new voice against the approved sample before building (rule §1).
- **Music / SFX / images:** chosen per job through provider routing below; the roles and levels (§2) stay.
- Any new hard-wired asset in a page is a bug: move it into brand.json or the job's scene data.
- After changing brand.json or engine/, rebuild the three baseline scenes and compare a few frames with the finals.

## Machine setup and rebuilding (any team member, any machine)
- First time: `python tools/setup.py` (venv, packages, Chromium, ffmpeg check, key file, Codex check, 2-second test of all
  three baselines). Then run Python through `.venv` (Windows `.venv\Scripts\python`, macOS/Linux `.venv/bin/python`).
- Artlist SFX + foley are in git (owner 2026-11-12: the SFX licence covers the team). Artlist MUSIC is not, and no script
  downloads it (music licence is per subscriber). `python tools/artlist_check.py` lists the missing tracks with their Artlist ID;
  each person downloads them with their OWN Artlist account (Artlist MCP `download_track` or artlist.io) at the listed path.
  Without it the mixer still runs and names each missing sound.
- Rebuild a baseline end to end: `python tools/rebuild.py type1|type2|type3` (`--preview 3` for a quick check). It holds the
  exact recipe of each final (music start, levels, cue set, clip cuts); a new clip copies that recipe.
- If something fails on a new machine, fix the repo (script, doc, requirements) so the next person does not hit it.

## Provider routing: scan, then offer (works on any machine; user rule 2026-11-12)
Never hard-wire one provider. At the start of a job (or when a step needs voice, timing, images, music or SFX):
1. Run `python tools/capabilities.py`. It checks API keys (presence only, never values), CLIs (codex, ffmpeg, earshot),
   Python packages and local libraries against `tools/providers.json`.
2. For every option marked ❓ (MCP), look for its `mcp_tools` names in your own connected tool list.
3. Offer the user the options that exist for the step at hand, cheapest first: free/local → inside a plan they already have
   (Codex on ChatGPT, Artlist) → pay-per-use (API key, paid MCP), with the price. Ask before any paid one (rule below).
   Example for images: "มี Codex CLI (ในแผน ChatGPT) / OpenAI API (เสียเงิน) / MCP ภาพ X (เสียเงิน ~N เครดิต) / ใช้ฉากในคลัง".
4. Keep the creative brief provider-neutral: the same TASK text (style paragraph + per-shot list + reference frames) works as a
   Codex task, an API prompt or an MCP prompt. Save outputs to the job's `assets/` the same way whatever made them.
5. Remember the user's choice per capability in the job folder (`providers_chosen.json`) and reuse it for the rest of the job.
6. Prefer the bundle that finishes the whole type with the FEWEST tools: `python tools/capabilities.py type2` lists, per needed
   capability, what works here; `tools/providers.json` → `bundles.examples` (A: ElevenLabs only; B: ElevenLabs + Artlist;
   C: Codex + ElevenLabs + Artlist = owner's setup; D: ElevenLabs + this repo's library). If the user has Artlist or the
   library covers it, music/SFX need no generation. Owner rule still applies to the owner: ElevenLabs = voice only, images = Codex.
7. Artlist files are NOT in the repo (licence). `library/audio/ARTLIST_MANIFEST.md` lists every track/SFX used; a teammate
   downloads them with their own Artlist account into the same paths.

## 0. Ground rules (all types)
- **Paid services.**
  - ElevenLabs: voice only (TTS + Scribe timing). Music/SFX there were approved once. Never images or video.
  - Images: Codex CLI inside the ChatGPT plan: `python tools/run_codex.py docs/prompts/<brief>.md <job-name>` (briefs in `docs/prompts/`).
  - Music + SFX: Artlist (`download_track` records the licence). The baseline set: `library/audio/artlist_manifest.json` (Artlist ID + path; add every new Artlist file there). SFX: commit new ones to library/audio/sfx or foley. Music: download only with the current user's own Artlist account, never commit it.
  - Thai TTS alternative: Paxa Labs (optional, outside this repo; needs its own script + key). Default is the ElevenLabs profile in brand.json.
  - Anything new that costs money: quote the price and ask first. Report what was spent.
- **Brand CI.** Colours only from `brand/brand.json` / `DE.color`:
  - blue #214AFF primary; ice #F3F7FF; teal #00C2BB; sky #9EE8FF; ink #1A1B1E; cream #FFF8EC
  - orange #FE4C1C = CTA / one accent only
  - Fonts: Kanit, IBM Plex Sans Thai, Red Hat Display, Sarabun. Thai is never italic.
- **Brand marks of others are never altered.** Use official lockups in official colours (Wikimedia originals in `assets/logos/*_official|*_lockup.svg`).
- **Third-party media** (news clips, X posts, screenshots) is fair use when credited on screen; never present it as ours.
- **Facts.** News is reported as the source says it, with no twist or opinion. Every number has a source in the job's script fact table.
- **Canvas.** 1080×1920 @30 fps. Captions are phrase sets (whole phrases, never word-by-word karaoke), 60–62 px Kanit, white with an ink stroke.
- **Visual on the word.** A number, logo or label appears when it is spoken. Check word times. Numerals ("$40") do not auto-align to Thai speech ("สี่สิบ"), so pin them with `caption_starts`.
- **No info that only repeats the caption.** Hide captions while a text card, title or end card shows the same words.
- **No white flash / dark dip at cuts.** A 1–3 frame flash reads as a flicker.
- **Research before inventing.** Check skills, repos and refs first (docs/REF_SPEC.md, open-source projects such as gl-transitions).
  - Code: MIT repos only.
  - Ideas: from any repo, NonCommercial included.

## 1. Voice
- Profiles live in `brand/brand.json` → `voices` (swap there). Current: type 2 + 3 = ElevenLabs **Aidan - Social Media Influencer** `EOVAuWqgSZN2Oel78Psj`, `eleven_v4`.
  - Scribe: attach the chosen take URL with `creative_attach_reference_file`, then transcribe that node. A speech node gives its FIRST take.
  - `engine/tighten.py` trims pauses (>0.28 s to 0.18 s, tempo 1.1).
- Type 3: same Aidan profile since 2026-11-12 (Paxa ran out of credits; user: "use the same voice as type 2"). Whole script in one call;
  ElevenLabs returns character timing, so no Scribe pass. Paxa khaotom stays an option (`paxa_api` in providers.json).
  - Rejected: mooping/satay/kaprao at default settings ("tired, odd, not funny").
- Script tone: natural spoken Thai, never narrate the structure (no "ข่าวครบแล้ว…"). The user approves the script before any TTS.

## 2. Sound
- **Music:** instrumental, fun and tight, **steady loudness** (1 s loudness std ≤ ~1.5 dB). NOT airy or corporate ("ฟังแล้วง่วง").
  - Find on Artlist, rank with earshot, measure steadiness, and let the user pick when it's a new format.
  - Type 2: Ariel Shalom "Groove Express" from 0:42.
  - Type 3: light instrumental underscore with NO heavy beat, like the ref (user 2026-11-12). Particels (pizzicato, childlike) was rejected; funk/hip-hop beds are for type 2 only. Pick: Dor Ben Lulu "Moments Apart" from 0:29 (closest to the ref by earshot), mixed VERY quiet (`--music-db -24 --duck-db -6`). Transitions approved by the user: gl-transitions (MIT) Directional + real motion blur (sub-frame average) for place changes, CrossZoom for zoom punch, Overexposure for white flash; plain cut on phrase starts everywhere else.
- **SFX:** real Artlist recordings in `library/audio/sfx/` (LICENSE.txt maps role → title). Roles:
  - whoosh ×4 variants, swish_paper, paper, pen, pop/pop_2, logo, click, counter, shutter
  - stab, swell, tick, rewind, chime
- **Type 2 cues** (`engine/cues.py news`):
  - light whoosh on every cut (−15 dB)
  - paper on docs, pen on highlights, counter + pop on numbers, click/pop on cards, logo pop, shutter on clips, swish on photos
- **Type 3 cues** (`engine/cues.py story`):
  - whoosh only on whip-pan place changes
  - reverse swell peaking into cards / punch-throughs
  - stab on the chapter title, rewind on flashbacks
  - clock under music drop-outs; pops on tags; counter on numbers
- **Mix** (`engine/mix.py`):
  - stereo; music bed −12 dB under the voice in gaps, gentle −4 dB duck
  - voice EQ; round-robin variants ±4 % pitch
  - `--music-mute "t0-t1,…"` for voice-only tension
  - final −14 LUFS
  - After a mix (if earshot is installed: `python tools/setup.py --earshot`): `<.venv python> -m earshot critique <mp4>` (see the earshot skill). If it is not installed, say the sound was not checked by ear.

## 3. Render
- `engine/render_par.py --page P --data D --out O --duration S --jobs 4`: same lossless PNG frames and x264 settings as render.py, split into parallel chunks and joined by stream copy, with a frame-count check. Type 3 v1: 61 s in 6 min.
- `engine/render.py … --stills 1.5,8,20` for PNG stills. Always look at stills of every shot before a full render.
- Pages: `window.setup(data)` + deterministic `window.renderAt(t)`. Reset canvas state (textAlign, shadows, dash) every frame. Video inside pages must be WebM/VP9.
- QA: contact sheet + `blackdetect` + frames around every transition. Never claim done without looking.

## 4. Type 2: AI news (paper collage, mascot host)
1. **Order: report the news fully first** (source wording: "with human guidance", "about", "earlier version"…).
   - Then a natural bridge (user's line: "ลองมาดูสามไอเดียที่น่าสนใจสำหรับ … กันบ้าง").
   - Then 3 ideas, each tied to a strength + a number. Then the CTA.
2. Shots: `plan_vN.json` → `pipelines/news/build_shots.py jobs/<job> plan_vN.json` (asserts: no empty-start shot, shots tile the timeline) → `engine/pages/news3.html` + `engine/web/collage.js`.
   - Piece kinds: doc (screenshot + highlighter via `engine/tools/grab_doc.py`), photo, video (credited), card, logo (official), num (count-up), tape.
3. Look:
   - Calm entrances (rise ~60 px + fade 0.45 s; no spin, no bounce).
   - One minimal Codex plate per beat in a locked CI collage style + a hairline grid (1 px, rgba(33,74,255,.06)), brightness 100%.
   - Take the Vox-like rhythm, never copy the ref's look.
4. **Mascot** (`DE.Mascot`): type 2 only.
   - A bust pinned to the bottom edge; moves to centre as host at section changes.
   - Lip-sync from RMS, blink, poses/emotes. Never covers the face of a speaker or the key insert; never floats mid-frame.
5. Current job: `jobs/type2_news/2026-11-12_news_fable52` (plan_v8.json + splice_v8.json → deliverables/type2_news_fable52_v8.mp4).

## 5. Type 3: animated story (our CI, the ref's format)
- **Ref:** `refs/type3_yt` (not in git: https://www.youtube.com/watch?v=_MG4v3foET8, "How a Chinese Spy Got Inside Nvidia", Paper Billions; the audit docs hold what we took from it). Take its format, pacing and transitions (REF_TYPE3_AUDIT). Do **not** take its dark mood.
  - Ours is bright Data Echooo: ice-white sets, cobalt main colour, sky/teal accents, one orange touch.
  - White pills with blue text, brand-blue name tags with leader lines, small colour logo bug.
- **No mascot in type 3**, not even on the end card. The end card is the logo + orange "กดติดตาม" + the story's own cast waving.
- **Cast:** `engine/web/toon.js`, round-head characters drawn in code (identical in every shot, blink, faces, poses, walk).
- **Plates:** Codex, locked brand style paragraph (`docs/prompts/codex_type3_plates*.md`), empty sets with an open floor.
- **Page:** `engine/pages/story2d.html`. Shot fields:
  - `plate`, `cam{z,x,y}`, `actors[keys]`, `props` (dish, tray, napkin, box, contract, check, chip, crowd), `fg` occluder
  - `chip`, `tags`, `counters`, `links`
  - `card` (`lines` or `title`), `rewind`, `cta`, `in:"whip"`, `out:"punch"`
  - `pill` = top tension device
- **Cutting (audit):**
  - median ~2 s
  - cold open → motto card (music drops) → chapter title (stab, music back)
  - whip on place changes; rewind year counter into flashbacks
  - jump cuts on locked sets; diagram link that breaks
  - punch-through into the big number; voice-only stretch with a clock before the cliffhanger
- **Job:** `jobs/type3_story/2026-11-12_story_nvidia`.
  - Script and fact check: `script_part1.md`
  - Scene: `part1_scene_v3.py` writes `scene.json` + `music_mute.txt`
  - Then `engine/cues.py story` → `render_par` → `mix --music-mute` (all of it: `python tools/rebuild.py type3`)

## 6. Type 1: talking head (คุณเซฟ)
- Refs `refs/type1/ref01.mp4`, `ref02.mp4` (client files, not in git; what they do is written below). Baseline footage: the forsample test clip (`input/footage.mp4`, already captioned, SD 360x640). Ask for raw footage before judging cut quality.
- What the refs do (audited 2026-11-12 at 5 fps):
  - split top/bottom: the speaker is cropped into one half, the face is never covered
  - the other half shows real content that changes on the word: a toggle flips, a checklist ticks, AI boxes and labels appear, logos come in one by one with a row collecting underneath
  - full-screen cutaways: a screen recording over a blurred copy of itself, scrolling; a product card
  - full-face punch-ins with a counter while the speaker gestures
  - nothing is static
- Pipeline v3:
  1. `pipelines/stt_elevenlabs.py` (Scribe, word timestamps) → `input/words.json`
  2. `engine/tools/face_track.py` → `assets/face.json`
  3. job `plan_v3.py`: segments `full|split|cut`, inserts `logos|job|stat|post|versus|race|grid|crowd` timed with `W("word")`
  4. `engine/pages/talkinghead3.html`, render with `render_par`
- Split scale 1.4 keeps the source's burned-in captions out of the speaker box. Captions are off in `full` when the footage already has them.
- Numbers on screen need a source line (e.g. HubSpot 2025, 66% of marketers use AI daily, via Digiday).
- Logos: official files only (`library/logos`).

## 7. Folders, library, finalizing (user rule 2026-11-12)
- Jobs by type: `jobs/type1_talkinghead/`, `jobs/type2_news/`, `jobs/type3_story/` → `<YYYY-MM-DD>_<slug>/` (input/, assets/, out/, scripts, scene/plan files).
- Shared sounds live in `library/audio/` (music = full licensed tracks with a mood table in `library/README.md`; sfx = Artlist roles; sfx_elevenlabs = older ElevenLabs set, the only SFX in the repo without Artlist). Every new licensed/generated music or SFX goes there, never only inside a job. Add a row to library/README.md.
- Mixer: `--sfx-dir library/audio/sfx`. Music level default −15 dB / duck −6 dB (user: v7 music was too loud at −12/−4).
- **When the user calls a clip final:** `python tools/finalize_job.py <job> <final.mp4>` (dry run) → show the list → run with `--yes`. It deletes unused drafts, renders, stills, QA sheets, stems, old plan/scene versions and voice test takes; keeps the final, its picture, the newest plan/scene/cues, scripts and input/.
- Paxa voice consistency: generate the whole script in ONE call (per-line calls at temperature 0.7 drift: pitch 107-152 Hz vs the approved 182 Hz sample, user heard "not the voice I chose"). Check median pitch against the approved sample before building.
- ElevenLabs by API key (user, 2026-11-12, after Paxa ran out of credits): key in `~/.config/dataechooo/elevenlabs.env` (`ELEVENLABS_API_KEY=`; never read it aloud, print it or commit it). `python pipelines/tts_elevenlabs.py script.txt out.mp3 --voice <id>` voices the WHOLE script in one call and writes per-character timing (out.json), so no Scribe pass.
- Re-using lines from an older take (user liked the v3 hook + closing): cut the old take by word times, RMS-match to the current take, 10 ms fades, rebuild words.json, then remap every plan time piecewise (see jobs/type2_news/.../splice_v8.json and plan_v8.json). Re-sync the visuals around the new words by hand (numbers land on the spoken number).
- render_par on the news page: 68.7 s in 9.4 min (was ~25 min single).

