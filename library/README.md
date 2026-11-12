# Shared library (reuse across clips)

User rule (2026-11-12): every licensed or generated sound goes here, so future clips can pick it up.
On "final" a clip's job folder keeps only what is needed to rebuild it (see `tools/finalize_job.py`).

## audio/music: full licensed tracks (Artlist, user's subscription)
| File | Mood | Used in | Good section |
|---|---|---|---|
| artlist_ariel-shalom_groove-express.wav | tight, fun instrumental funk, steady (user's pick for type 2) | type2 news_fable52 | from 0:42 (steady); 0:34-0:40 is a breakdown |
| artlist_francesco-dandrea_particels.wav | playful pizzicato, childlike (rejected for type 3) | - | from 0:28 |
| artlist_liam-mansfield_a-little-curious.wav | light curious underscore, no heavy beat, very steady | - | from 0:38 |
| artlist_dor-ben-lulu_moments-apart.wav | soft ambient underscore, almost no beat; closest to the type 3 ref (earshot cos 0.44) | type3 story_nvidia | from 0:29; play VERY quiet |

Cut a bed per clip into the job's `input/` (`ffmpeg -ss <start> -t <dur> -i <track> -af afade=t=in:d=0.25 music_bed.wav`).

## audio/sfx: Artlist SFX by role (LICENSE.txt maps each file to its Artlist title)
whoosh (4 variants), swish_paper, paper, pen, pop/pop_2, logo, click, counter, shutter, stab, swell, tick, rewind, chime, riser.
`engine/mix.py --sfx-dir library/audio/sfx` round-robins `<role>.wav`, `<role>_2.wav` …

## audio/sfx_elevenlabs
The older ElevenLabs-made SFX (approved earlier). Ours, so it is in the repo: use it when the Artlist files in audio/sfx are not downloaded. v7+ uses audio/sfx.

## audio/voice: final narration / speaker tracks of finished clips (reuse for re-edits, recaps, cut-downs)
| File | Clip | Voice |
|---|---|---|
| type1_th_sample_speaker.wav | type 1 forsample test (final v3) | the speaker's own audio |
| type2_news_fable52_aidan_v8.wav | type 2 news Fable 5.2 (final v8) | ElevenLabs Aidan, v3-take hook + closing spliced in |
| type3_nvidia_p1_aidan.wav | type 3 NVIDIA Part 1 (final v3) | ElevenLabs Aidan, one take |

