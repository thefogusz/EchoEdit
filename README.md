# EchoEdit: ระบบทำคลิปแนวตั้งของ Data Echooo (9:16 ภาษาไทย)

ระบบนี้ให้ Claude Code (หรือ agent ที่อ่านสกิลได้) ทำคลิปได้ 3 แนว จนจบงาน:

| แนว | คืออะไร | คลิปมาตรฐาน (เป้าคุณภาพ) |
|---|---|---|
| 1 คนพูด | ตัดต่อคลิปคุณเซฟพูดหน้ากล้อง แบ่งจอบน-ล่าง ภาพแทรกของจริงขยับตรงคำ | `deliverables/type1_talkinghead_forsample_v3.mp4` |
| 2 ข่าว AI | เสียงพากย์ + มาสคอต + กระดาษคอลลาจ ข่าวก่อน แล้ว 3 ไอเดีย แล้ว CTA | `deliverables/type2_news_fable52_v8.mp4` |
| 3 เล่าเรื่อง | แอนิเมชันเล่าเรื่องธุรกิจ/AI/ชีวประวัติ แบบ 2.5D | `deliverables/type3_story_nvidia_p1_v3.mp4` |

**เริ่มที่นี่:** สกิลหลักอยู่ที่ `.claude/skills/de-video/SKILL.md` (Claude Code โหลดให้เองเมื่อเปิดโฟลเดอร์นี้)
กฎทุกข้อที่ตกลงกับเจ้าของพร้อมเหตุผลอยู่ที่ `docs/REF_SPEC.md` ส่วนการแตกเรฟแนว 3 อยู่ที่ `docs/REF_TYPE3_AUDIT.md` และ `docs/REF_TYPE3_SHOTS.md`

## ติดตั้ง (ครั้งเดียว)
1. Python 3.11+ แล้วติดตั้งแพ็กเกจ: `pip install -r requirements.txt` และ `python -m playwright install chromium`
2. ติดตั้ง ffmpeg + ffprobe ให้เรียกได้จาก PATH (Windows: `winget install Gyan.FFmpeg`)
3. API key (ถ้ามี) ไม่เก็บใน repo ให้เก็บในเครื่องตัวเอง:
   - ElevenLabs: `~/.config/dataechooo/elevenlabs.env` ใส่บรรทัด `ELEVENLABS_API_KEY=...`
   - Paxa (เสียงไทย, ไม่บังคับ): `~/.config/koubo/paxa.env`
4. เพลงและ SFX จาก Artlist **ไม่ได้อยู่ใน repo** (ใบอนุญาตห้ามแจกไฟล์ดิบ) ดูรายชื่อใน `library/audio/ARTLIST_MANIFEST.md` แล้วโหลดด้วยบัญชี Artlist ของตัวเองไปไว้ที่พาธเดิม
5. ไม่บังคับ: earshot (ตรวจเสียง), Codex CLI (วาดภาพในแผน ChatGPT)

## มีเครื่องมืออะไรใช้ได้บ้าง (สแกนก่อนทุกงาน)
```
python tools/capabilities.py type2
```
สคริปต์จะเช็กว่าเครื่องนี้มี API key / CLI / ไลบรารีอะไร (ไม่แสดงค่า key) แล้วบอกว่าแต่ละขั้นทำได้ทางไหน ส่วน MCP ให้ Claude เช็กจากเครื่องมือที่เชื่อมอยู่
จากนั้นเลือก**ชุดที่ใช้เครื่องมือน้อยที่สุด** เช่น
- **ชุด A:** ElevenLabs ที่เดียว (เสียง + เวลาคำ + ภาพ + เพลง/SFX ถ้าบัญชีมีครบ)
- **ชุด B:** ElevenLabs (เสียง + ภาพ) + Artlist (เพลง/SFX ไม่ต้องเจน)
- **ชุด C:** Codex (ภาพ) + ElevenLabs (เสียง) + Artlist (เพลง/SFX) ← ชุดที่เจ้าของใช้อยู่
- **ชุด D:** ElevenLabs (เสียง) + ใช้ฉาก/ตัวละคร/เสียงในคลังของ repo นี้
บริการที่เสียเงินต่อครั้งต้องบอกราคาและรอคำตอบก่อนเสมอ (รายละเอียด `tools/providers.json`)

## โครงสร้างโฟลเดอร์
```
.claude/skills/de-video/   สกิลหลัก (วิธีทำทุกแนว + กฎ)
docs/                      กฎจากรีวิวเจ้าของ, ผลแตกเรฟ, system design
engine/                    ตัวเรนเดอร์ (render.py, render_par.py ขนาน), มิกซ์เสียง (mix.py), cue (cues.py), หน้าเรนเดอร์ (pages/), gl-transitions (vendor/, MIT)
pipelines/                 TTS/STT ของ ElevenLabs, ตัวสร้างฉาก news/talkinghead/story
tools/                     สแกนเครื่องมือ (capabilities.py), ล้างไฟล์ร่างตอนไฟนอล (finalize_job.py)
brand/                     CI ของ Data Echooo: สี ฟอนต์ (OFL) โลโก้ มาสคอต
library/                   คลังกลาง: logos ทางการ, audio/voice (เสียงพากย์ไฟนอล), audio/sfx_elevenlabs, รายชื่อ Artlist
jobs/type1_talkinghead/ jobs/type2_news/ jobs/type3_story/   งานแต่ละชิ้น (สคริปต์ แผน ฉาก ตัวละคร input)
deliverables/              คลิปไฟนอลล่าสุด 1 ตัวต่อแนว
```

## ทำคลิปซ้ำ / เริ่มคลิปใหม่
- **เรนเดอร์คลิปมาตรฐานใหม่:** รันสคริปต์ฉากของงานก่อน (ไฟล์ `scene*.json` ไม่อยู่ใน repo เพราะผูกกับพาธเครื่อง) เช่น `python jobs/type3_story/2026-11-12_story_nvidia/part1_scene_v3.py` แล้วตามขั้นในสกิล (`engine/cues.py` → `engine/render_par.py` → `engine/mix.py`)
- **คลิปใหม่:** สร้างโฟลเดอร์ใน `jobs/typeN_.../<YYYY-MM-DD>_<slug>/` แล้วก๊อปขั้นตอนจากคลิปมาตรฐานแนวเดียวกัน
- **ปิดไฟนอล:** `python tools/finalize_job.py <job> <final.mp4>` (ทดลองดูก่อน แล้วค่อยใส่ `--yes`)
- **แนว 1 หลัง clone:** ไฟล์ภาพสำหรับเรนเดอร์ไม่อยู่ใน repo ให้สร้างจากฟุตเทจก่อน
  `ffmpeg -i jobs/type1_talkinghead/2026-11-12_th_sample/input/footage.mp4 -an -c:v libvpx-vp9 -b:v 2M -r 30 jobs/type1_talkinghead/2026-11-12_th_sample/assets/footage.webm`
- **แนว 2 หลัง clone:** คลิปวิดีโอแทรกจาก X (`assets/media/v5-v7.webm`) ไม่อยู่ใน repo (ลิขสิทธิ์เจ้าของโพสต์) ที่มาอยู่ใน `CREDITS.txt` และ `assets/media/3d_clips.json`

## สำหรับทีม: ใช้ต่อและพัฒนาต่อ
- **กฎอยู่ที่เดียว:** แก้วิธีทำงานที่ `.claude/skills/de-video/SKILL.md` แล้วจดเหตุผลใน `docs/REF_SPEC.md` (ข้อใหม่ต่อท้าย พร้อมวันที่และใครขอ) agent ตัวถัดไปจะทำตามเอง
- **เพิ่มเครื่องมือ/บริการใหม่:** เพิ่ม option ใน `tools/providers.json` (kind api/cli/mcp/local, cost, env หรือ cli ที่ต้องมี, คำสั่ง run) แล้วรัน `python tools/capabilities.py typeN` ดูว่าเห็น ไม่ต้องแก้โค้ดสแกน
- **เพิ่มแนวคลิปใหม่:** หน้าเรนเดอร์ใหม่ใน `engine/pages/` (ต้องมี `setup(data)` กับ `renderAt(t)` ที่ได้ภาพเดิมทุกครั้งจากเวลาเดียวกัน) + สคริปต์สร้าง scene ในงาน + บรรทัดใน `bundles` ของ providers.json + หัวข้อใหม่ในสกิล
- **เป้าคุณภาพ:** คลิปใน `deliverables/` คือมาตรฐาน งานใหม่ต้องไม่ต่ำกว่านี้ เปลี่ยนมาตรฐานได้เมื่อเจ้าของรับรองคลิปใหม่เป็นไฟนอล
- **ห้าม commit:** API key, ไฟล์ดิบ Artlist, คลิปเรฟ, ดราฟต์/เรนเดอร์ทดลอง (`out/`, `work/` ถูก ignore อยู่แล้ว) ปิดงานด้วย `finalize_job.py` ก่อน commit ทุกครั้ง
- **ทำงานร่วมกัน:** แตก branch ต่องาน (`job/<slug>` หรือ `engine/<เรื่อง>`) แล้วเปิด PR อย่าแก้หน้าเรนเดอร์ของแนวอื่นในงานเดียวกัน ถ้าแก้ `engine/` ให้ build scene ของคลิปมาตรฐานทั้ง 3 ใหม่ว่ายังผ่าน

## ใบอนุญาตของที่อยู่ใน repo
- โค้ดของเราเอง: ของ Data Echooo
- `engine/vendor/gl-transitions`: MIT (มีไฟล์ LICENSE)
- `brand/fonts`: SIL OFL
- `library/logos`: เครื่องหมายการค้าของแต่ละบริษัท ใช้แบบทางการ ห้ามแก้สี/รูปทรง
- เพลง/SFX Artlist และคลิปเรฟ: ไม่อยู่ใน repo
