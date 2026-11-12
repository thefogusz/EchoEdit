# EchoEdit: ระบบทำคลิปแนวตั้งของ Data Echooo (9:16 ภาษาไทย)

ระบบนี้ให้ Claude Code (หรือ agent ที่อ่านสกิลได้) ทำคลิปได้ 3 แนว จนจบงาน:

| แนว | คืออะไร | คลิปมาตรฐาน (เป้าคุณภาพ) |
|---|---|---|
| 1 คนพูด | ตัดต่อคลิปคุณเซฟพูดหน้ากล้อง แบ่งจอบน-ล่าง ภาพแทรกของจริงขยับตรงคำ | `deliverables/type1_talkinghead_forsample_v3.mp4` |
| 2 ข่าว AI | เสียงพากย์ + มาสคอต + กระดาษคอลลาจ ข่าวก่อน แล้ว 3 ไอเดีย แล้ว CTA | `deliverables/type2_news_fable52_v8.mp4` |
| 3 เล่าเรื่อง | แอนิเมชันเล่าเรื่องธุรกิจ/AI/ชีวประวัติ แบบ 2.5D | `deliverables/type3_story_nvidia_p1_v3.mp4` |

**เริ่มที่นี่:** สกิลหลักอยู่ที่ `.claude/skills/de-video/SKILL.md` (Claude Code โหลดให้เองเมื่อเปิดโฟลเดอร์นี้)
กฎทุกข้อที่ตกลงกับเจ้าของพร้อมเหตุผลอยู่ที่ `docs/REF_SPEC.md` ส่วนการแตกเรฟแนว 3 อยู่ที่ `docs/REF_TYPE3_AUDIT.md` และ `docs/REF_TYPE3_SHOTS.md`

## ติดตั้ง (คำสั่งเดียว ครั้งเดียว)
ต้องมี Python 3.10+ (python.org) กับ git แล้วรัน
```
python tools/setup.py
```
สคริปต์จะทำให้ครบ: สร้าง `.venv` ติดตั้งแพ็กเกจ + Chromium, เช็ก ffmpeg (ถ้าไม่มีจะถามแล้วติดตั้งผ่าน winget/brew), สร้างไฟล์ใส่ key ElevenLabs,
เช็ก Codex CLI, สแกนเครื่องมือ แล้วทดลองเรนเดอร์ + มิกซ์ 2 วินาทีของคลิปมาตรฐานทั้ง 3 แนว ถ้ามีอะไรขาดจะบอกตรงๆ ว่าต้องทำอะไร
หลังติดตั้ง ใช้ Python ของ `.venv` (Windows `.venv\Scripts\python`, macOS/Linux `.venv/bin/python`)

สิ่งที่ต้องทำเองมีแค่นี้:
1. **ElevenLabs key:** วางใน `~/.config/dataechooo/elevenlabs.env` หลัง `ELEVENLABS_API_KEY=` (setup สร้างไฟล์ไว้ให้แล้ว ห้าม commit)
2. **เพลง Artlist ของคลิปมาตรฐาน (3 เพลง):** SFX กับ foley อยู่ใน repo แล้ว ใช้ได้ทั้งทีม แต่เพลงไม่อยู่ใน git และไม่มีสคริปต์โหลดให้ (ใบอนุญาตเพลงเป็นของแต่ละบัญชี) รัน `python tools/artlist_check.py` จะได้รายการเพลงที่ขาดพร้อม Artlist ID แล้วโหลดด้วยบัญชี Artlist ของตัวเอง (connector Artlist ใน Claude: `download_track` หรือเว็บ artlist.io) ไปวางตามพาธที่บอก ถ้าไม่มี ระบบยังทำงานได้ แค่มิกซ์ไม่มีเพลง
3. **Codex CLI (ถ้าจะวาดฉากใหม่):** `npm install -g @openai/codex` แล้ว `codex login` ด้วยบัญชี ChatGPT
4. **Connector ใน Claude (ไม่บังคับ):** Artlist, ElevenLabs ฯลฯ เชื่อมในบัญชี Claude ของแต่ละคนเอง ถ้าไม่มี ระบบใช้ API key กับไฟล์ในเครื่องแทน
5. **earshot (ไม่บังคับ ตรวจเสียงแบบ "ฟัง"):** `python tools/setup.py --earshot`

## สร้างคลิปมาตรฐานใหม่ทั้งคลิป (เช็กว่าเครื่องนี้ได้ผลเหมือนเจ้าของ)
```
python tools/rebuild.py type1      # หรือ type2 / type3,  --preview 3 = แค่ 3 วินาทีแรก
```
ทำครบทุกขั้นตามสูตรของไฟนอลจริง: เตรียม input (ฟุตเทจ, คลิปแทรก, ตัดเพลง) → scene → cue เสียง → เรนเดอร์ขนาน → มิกซ์ ผลอยู่ที่ `jobs/<งาน>/out/`

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
CLAUDE.md                  กติกาการทำงานของ Claude ในโปรเจกต์นี้ (ตอบไทย, ถามก่อนจ่ายเงิน ฯลฯ)
.claude/skills/de-video/   สกิลหลัก (วิธีทำทุกแนว + กฎ)
.claude/skills/thai-humanizer/, earshot/   สกิลเสริม (ขัดบทไทย, ตรวจเสียง) MIT
docs/                      กฎจากรีวิวเจ้าของ, ผลแตกเรฟ, prompts/ (brief วาดฉาก)
engine/                    ตัวเรนเดอร์ (render.py, render_par.py ขนาน), มิกซ์เสียง (mix.py), cue (cues.py), หน้าเรนเดอร์ (pages/), gl-transitions (vendor/, MIT)
pipelines/                 TTS/STT ของ ElevenLabs, ตัวสร้างฉาก news/talkinghead/story
tools/                     setup.py (ติดตั้ง), rebuild.py (สร้างคลิปมาตรฐาน), capabilities.py (สแกน), artlist_check.py, run_codex.py, finalize_job.py
brand/                     CI ของ Data Echooo: สี ฟอนต์ (OFL) โลโก้ มาสคอต
library/                   คลังกลาง: logos ทางการ, audio/voice (เสียงพากย์ไฟนอล), audio/sfx_elevenlabs, รายชื่อ Artlist
jobs/type1_talkinghead/ jobs/type2_news/ jobs/type3_story/   งานแต่ละชิ้น (สคริปต์ แผน ฉาก ตัวละคร input)
deliverables/              คลิปไฟนอลล่าสุด 1 ตัวต่อแนว
```

## ทำคลิปซ้ำ / เริ่มคลิปใหม่
- **คลิปใหม่:** สร้างโฟลเดอร์ใน `jobs/typeN_.../<YYYY-MM-DD>_<slug>/` แล้วก๊อปขั้นตอนจากคลิปมาตรฐานแนวเดียวกัน
- **ปิดไฟนอล:** `python tools/finalize_job.py <job> <final.mp4>` (ทดลองดูก่อน แล้วค่อยใส่ `--yes`)
- **ภาพใหม่:** brief ที่ใช้สั่งวาดฉากของคลิปมาตรฐานอยู่ใน `docs/prompts/` สั่งด้วย `python tools/run_codex.py docs/prompts/<brief>.md <ชื่องาน>`

## ปรับเปลี่ยนแบรนด์ / ฟอนต์ / เสียง (แก้ที่ `brand/brand.json` ที่เดียว)
- **สี:** `colors` หน้าเรนเดอร์ทุกหน้าอ่านจากที่นี่ (`DE.color.*`)
- **ฟอนต์:** `fonts` มี 3 บทบาท หัวข้อไทย / เนื้อความไทย / ตัวอังกฤษ เปลี่ยน `family` กับ `faces` แล้ววางไฟล์ฟอนต์ใน `brand/fonts` (ใส่ไฟล์ licence ด้วย) ไม่ต้องแก้หน้าใดเลย
- **เสียงพากย์:** `voices.profiles` เพิ่มเสียงของทีมบน ElevenLabs (voice_id, model, speed) แล้วชี้ `voices.by_type` ไปที่ชื่อนั้น
  `python pipelines/tts_elevenlabs.py script.txt out.mp3 --type type3` หรือ `--voice <ชื่อโปรไฟล์ หรือ voice_id>`
- **โลโก้ / safe zone / ขนาดจอ / มาสคอต:** อยู่ใน brand.json เช่นกัน
- สิ่งที่ repo นี้ล็อกไว้คือ**หลักการภาพ**: จังหวะตัด ทรานซิชัน ภาพขยับตรงคำ ตำแหน่งซับ บทบาทเสียงและระดับเสียง (ดูสกิลกับ `docs/REF_SPEC.md`) ส่วนตัว asset เปลี่ยนได้หมด

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
- `.claude/skills/thai-humanizer` และ `.claude/skills/earshot`: MIT (มีไฟล์ LICENSE)
- `library/audio/sfx`, `library/audio/foley`: Artlist SFX ใบอนุญาตครอบคลุมทีม (ที่มาแต่ละไฟล์ใน LICENSE.txt)
- เพลง Artlist และคลิปเรฟ: ไม่อยู่ใน repo
