# News v6 script — Claude Fable 5.2 (draft for approval, before TTS)

**Order (user, 2026-11-12): tell the news completely first, then the use cases.** v4/v5 jumped from "launched" straight into examples.
Primary source: https://www.anthropic.com/claude-fable-and-mythos-5-2 (9 Nov 2026). News part = source wording, no opinion.
Target ≈ 55 s. Voice: Aidan, eleven_v4. Look: paper collage (ref AIพูด.mp4 + gbro-collage-broll, MIT).

## 1. Hook (≈4 s)
caption: โค้ดเกิน 90% ใน Anthropic / ตอนนี้ Claude เป็นคนเขียน / โดยมีคนคอยกำกับ
tts: [excited] โค้ดเกินเก้าสิบเปอร์เซ็นต์ใน Anthropic ตอนนี้ Claude เป็นคนเขียน โดยมีคนคอยกำกับ!

## 2. The news (≈25 s)
caption:
และวันที่ 9 พ.ย. / เขาเปิดตัว Claude Fable 5.2 / กับ Claude Mythos 5.2
โมเดลที่เก่งที่สุดของเขา / สำหรับงานเทคนิคยากๆ
สองตัวนี้คือโมเดลเดียวกัน / Fable มีระบบกันการใช้ผิดทางไซเบอร์และชีววิทยา / เลยเปิดให้ทุกคนใช้
ส่วน Mythos / ให้เฉพาะองค์กรที่ผ่านการตรวจสอบ
เก่งขึ้นทั้งเขียนโค้ด / คิดวิเคราะห์ และอ่านภาพ
ตอบเร็วขึ้นสูงสุด 30% / ราคาถูกลง / $8 ต่อล้านโทเคนขาเข้า / $40 ขาออก
ใช้ได้แล้ววันนี้ / บน Claude, AWS, Google Cloud และ Azure
tts:
และวันที่เก้าพฤศจิกายน เขาเปิดตัว Claude Fable ห้าจุดสอง กับ Claude Mythos ห้าจุดสอง โมเดลที่เก่งที่สุดของเขา สำหรับงานเทคนิคยากๆ
สองตัวนี้คือโมเดลเดียวกัน Fable มีระบบกันการใช้ผิดทางไซเบอร์และชีววิทยา เลยเปิดให้ทุกคนใช้ ส่วน Mythos ให้เฉพาะองค์กรที่ผ่านการตรวจสอบ
เก่งขึ้นทั้งเขียนโค้ด คิดวิเคราะห์ และอ่านภาพ ตอบเร็วขึ้นสูงสุดสามสิบเปอร์เซ็นต์ ราคาถูกลง แปดดอลลาร์ต่อล้านโทเคนขาเข้า สี่สิบดอลลาร์ขาออก
ใช้ได้แล้ววันนี้ บน Claude, AWS, Google Cloud และ Azure

## 3. Use cases — ours, framed as suggestions (≈20 s, fast)
caption:
ลองมาดู 3 ไอเดียที่น่าสนใจ / สำหรับ Fable 5.2 กันบ้าง
หนึ่ง งานโค้ดใหญ่ / FrontierCode 49.1% สูงสุดที่ Anthropic ทดสอบ / เหมาะกับงานรื้อหรือย้ายระบบ
สอง งาน 3D / Unity บอกว่าสร้างฉาก 3D จากศูนย์ได้ดีขึ้นชัด / ทำเกมหรือสื่อ 3D ลองเลย
สาม อ่านกราฟ / Chartography 73.4% สูงสุดในตารางเทียบ / โยน dashboard ให้สรุปได้เลย
tts:
ลองมาดูสามไอเดียที่น่าสนใจ สำหรับ Fable ห้าจุดสอง กันบ้าง
หนึ่ง งานโค้ดใหญ่ คะแนน FrontierCode สี่สิบเก้าจุดหนึ่งเปอร์เซ็นต์ สูงสุดที่ Anthropic ทดสอบ เหมาะกับงานรื้อหรือย้ายระบบ
สอง งานสามดี Unity บอกว่าสร้างฉากสามดีจากศูนย์ได้ดีขึ้นชัด ทำเกมหรือสื่อสามดี ลองเลย
สาม อ่านกราฟ Chartography เจ็ดสิบสามจุดสี่เปอร์เซ็นต์ สูงสุดในตารางเทียบ โยน dashboard ให้สรุปได้เลย

## 4. CTA (≈5 s)
caption: ชอบไอเดียไหน คอมเมนต์บอก / กดติดตาม Data Echooo / ข่าว AI สรุปให้ทุกสัปดาห์
tts: [cheerful] ชอบไอเดียไหน คอมเมนต์บอก กดติดตาม Data Echooo ข่าว AI สรุปให้ทุกสัปดาห์

## Fact check (claim → source wording)
| Claim | Source |
|---|---|
| >90% of code by Claude, with guidance | "Over 90% of the changes merged into Anthropic's core codebase are now written by Claude (with human guidance)" |
| 9 Nov, Fable 5.2 + Mythos 5.2 | newsroom date Nov 9, 2026; title "Introducing Claude Fable 5.2 and Claude Mythos 5.2" |
| most capable for hard technical work | "Our most capable models for daunting technical work" |
| same model; Fable safeguards → all users; Mythos for vetted orgs | "Claude Fable and Claude Mythos are the same underlying model. Fable has strong cybersecurity and biology safeguards ... available to all users. Organizations ... can apply for access to Mythos" |
| better coding, reasoning, vision | "improvements in areas like coding, reasoning, and vision" |
| up to 30% faster; lower price $8 / $40 per M tokens | "outputs up to 30% faster than Claude Fable 5.1 ... available at a lower price: $8 per million input tokens and $40 per million output tokens" |
| available today: Claude, AWS, Google Cloud, Azure | "available today on all platforms, including Amazon Web Services, Google Cloud, and Microsoft Azure" |
| FrontierCode 49.1% highest released model tested | "At Xhigh effort, Fable 5.2 reaches 49.1%, the highest score of any released model we've tested" |
| Unity 3D | Unity quote: "building higher-quality 3D scenes from scratch" |
| Chartography 73.4% top of table | benchmark table |
Use-case lines ("เหมาะกับ…", "ลองเลย", "โยน dashboard…") are our suggestions, placed after the news.

- Revision: bridge line changed (user): "ข่าวครบแล้ว มาดู…" announced the structure out loud. Now a natural bridge.
