# Artlist media used by this repo

SFX + foley: committed (owner 2026-11-12: the SFX licence covers the team).
Music: NOT committed. Each person downloads it with their OWN Artlist account (music licence is per subscriber; nothing here downloads it).
`python tools/artlist_check.py` lists the missing tracks with their Artlist ID (`artlist_manifest.json`). Download each (Artlist MCP `search_music` / `search_sfx` → `download_track`, or artlist.io) and save it under the path shown.

## Music → library/audio/music/
| File | Artlist title (artist) | Used in |
|---|---|---|
| artlist_ariel-shalom_groove-express.wav | Groove Express (Ariel Shalom) | type 2 bed (from 0:42) |
| artlist_dor-ben-lulu_moments-apart.wav | Moments Apart (Dor Ben Lulu / Borden Lulu) | type 3 bed (from 0:29) |
| artlist_liam-mansfield_a-little-curious.wav | A Little Curious (Liam Mansfield) | type 1 bed (from 0:38) |
| artlist_francesco-dandrea_particels.wav | Particels (Francesco D'Andrea) | rejected for type 3 (kept for reference) |
Job beds (`jobs/*/input/music_bed*.wav`) are cuts of these: `ffmpeg -ss <start> -t <dur> -i <track> -af afade=t=in:d=0.3 music_bed.wav`.

## SFX → library/audio/sfx/ and foley → library/audio/foley/
See `library/audio/sfx/LICENSE.txt` and `library/audio/foley/LICENSE.txt`: every role file is mapped to its Artlist title and artist.
(`chime.mp3`, `riser.mp3` in sfx/ and everything in `sfx_elevenlabs/` were generated on ElevenLabs and ARE committed.)
