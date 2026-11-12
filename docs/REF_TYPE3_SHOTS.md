# REF type3 — shot-by-shot catalog, 0:00–4:00

Source: `refs/type3_yt/ref.mp4` ("How a Chinese Spy Got Inside Nvidia", 1280x720, 30 fps).
Method: 79 detected cuts (`cuts240.txt`) give 80 shots. For each shot we pulled 3 frames (start+0.1 s, middle, end-0.1 s), or 4–6 frames for shots over 5 s. We also pulled dense strips every 0.5–0.9 s over 0–53 s and 53–240 s to see moves inside shots. Working files: `refs/type3_yt/shots/` (`sheet_01..14.jpg`, `dense_A..H.jpg`, `index.txt`, `make.py`, `dense.py`).
Limits: still frames only. Easing and exact move timing are estimates to about ±0.3 s. "(?)" marks anything not certain. No audio analysis was done, so SFX claims are inferred from the picture.

---

## 1. Pattern summary

### 1.1 Shot inventory (80 detected shots, plus 4 undetected internal changes)

| Kind | Count | Share of 240 s (approx) | Notes |
|---|---|---|---|
| Wide / establishing, frontal "dollhouse" side view | ~32 | ~50 % | The workhorse. Flat frontal set, characters small to medium, lots of props that animate. |
| Medium / MCU character (dialogue or reaction) | ~12 | ~10 % | Almost always for a spoken line or a punch reaction. Usually 1–2.5 s. |
| Black text card (handwritten, word-by-word) | 10 (1 is the chapter title) | ~12 % (~29 s) | One every ~24 s. Always the punchline or twist sentence. |
| Top-down / overhead table | 5 | ~7 % | Used for money, documents and "plans": 15, 33, 44, 55, 61. |
| Close insert of an object or document | ~6 | ~5 % | Evidence board, under-table chip, enrollment form, ticket, plaque. |
| POV / viewfinder | 2 (+1 flash frame) | ~1 % | Telephoto camera POV, then a flash, then a printed photo. |
| Map / data-on-map | 2 (+1 diagram) | ~6 % | Opening world-map bar chart; Taiwan→America map; "86 of every $100" register diagram. |
| Metaphor diagram (split screen) | 2 | ~10 % | Chef vs chip, $600 couch vs chip towers. |
| True 3D (toon-shaded) | 4–5 | ~5 % | DC desk with rotary phone and title, Santa Clara tower, second phone desk, elevator-shaft dive (?), data-center corridor (2.5D/3D). |

Typical shot length: median ~2.3 s. Dialogue shots run 1.2–2.5 s. Explanation shots run 4–15 s, and the camera keeps moving inside them, so the long ones (71: 14.7 s, 72: 16.3 s) are really 3–4 "shots" joined by camera moves and panel wipes, not by cuts.

### 1.2 How one story beat is covered

A "beat" is one narration sentence or idea. The common coverage templates:

1. **Wide state, then insert proof, then reaction or punch card.** Example 0:25–0:32: under-table insert (13), then the counter reaches "$ BILLIONS", then a black card: "The kind China isn't allowed to have."
2. **One wide shot carries the whole sentence, and each noun gets its own pop-on.** The camera stays still and objects change *on the word*. Example 1:00–1:04: "sold almost everything" puts a red SOLD tag on each item, then each item disappears. Example 1:28–1:34: "tattoos… knife scars… taped up" puts each detail on the roommate as it is said.
3. **Dialogue ping-pong.** Wide two-shot for line 1, MCU or OTS for line 2, back to the wide for the gag. Each spoken line is its own shot of 1.2–2 s. Denny's waitress scene 2:22–2:28 = 4 shots for 4 lines (57–60). "Thirty days" scene 2:50–2:58 = 4 shots (66–69).
4. **Setup sentence, then a "But…" text card.** The twist line is pulled out of the picture and shown alone as text on black. Examples: 0:04, 0:20, 0:30, 0:51, 1:13, 1:48, 2:08, 2:43, 3:32.

Rate: about **1 shot per 3 s overall**. Narration (VO) sections run about 1 shot per sentence, but objects change 2–4 times inside the shot. Dialogue runs 1 shot per line. Explanation sections run 1 long moving shot for 3–5 sentences.

### 1.3 How camera moves are timed to words

- **The push-in lands on the key noun.** Shot 35: the push hits the checkbox "REFORM PROGRAM" on "by mistake". Shot 79: the push ends on the plaque as "plaque" is said. Shot 39: the push-in on the roommate happens on "his roommate".
- **Whip pan = "and the other one".** Shot 4 whips from Jensen to Alice on "She's Alice Huang". Shot 1→2 whips out of the dinner into the map on "most valuable company on Earth".
- **Pull-back = reveal scale or a hidden watcher.** Shot 6 pulls from the warm window to the wet exterior, then to the agents, on "Somewhere nearby". Shot 37 opens the bathroom into an endless corridor on "every single day". Shot 75 pulls back on the endless queue on "standing in the same line".
- **Tilt or crane up = power/top. Dive down = "didn't start at the top".** Shot 24 cranes up the Santa Clara tower to the Nvidia sign. Shot 26→27 dives down a shaft (floor counter going down) to a bathroom door.
- **Zoom-through = a change of world.** Shot 20 goes into the polaroid on the file. Shot 72 goes into the TV and comes out in the data center.
- **Rack focus (blur → sharp) opens a shot** on a short punch line (67 "Thirty days.") and on the viewfinder POV (16).
- **Static camera** is the default for gags and dialogue. Motion comes from props, not the lens.

### 1.4 When and why the mode switches

| Mode | When it is used | Why |
|---|---|---|
| Scene with characters (2D) | Default, about 65 % | Carries the story; dialogue is acted out. |
| Text card (black, handwriting typing on) | Every twist/punch sentence; the chapter title | Forces the viewer to *read* the hook. It also hides a scene change, and it costs nothing to make. |
| Map | Location jumps (Singapore→world, Taiwan→America) | Geography plus scale in one image. |
| Data diagram / counter | Any number: $ billions, 100 boys, $2,000,000, 1,000,000 chips, 10,000s chips, 86 of $100 | Numbers are never only spoken. They count up on screen. |
| Metaphor split screen | Technical explanation (CPU vs GPU, $600 vs giants) | Turns an abstract comparison into a left-vs-right picture. |
| Document / evidence | Spy-thread beats (MSS dossier, FILE 0414, rules sheet, enrollment form) | Feels like an investigation. Red marker, string, magnifier. |
| True 3D | Washington/"present-day spy thread" only (phone desk, tower, title) | Separates the *frame story* (3D, cool, noir) from the *biography flashback* (flat 2D, warm). |
| Flash-forward studio ("YEARS LATER", ON AIR) | Once, to give a quote in his adult voice | Adds a first-person aside without leaving the flashback. |

### 1.5 Recurring tricks (with first timestamp)

- **Ringing phone:** 3D rotary phone with "(( ))" ring marks (0:38). The callback at 0:46 shows a receiver being lifted (?) on a second desk.
- **Photos as proof:** polaroids pop in above the agents with each shutter (0:17–0:18). The viewfinder POV freezes into a white-bordered printed photo (0:37). The photo returns on "FILE 0414" (0:41).
- **Viewfinder POV:** corner brackets, red REC dot, centre reticle, "600mm f/4" text, rain bokeh on the lens, then a white flash frame (0:35–0:37).
- **Red marker / red string:** red string from photo to name, red circle drawn around the face (0:18). Red "CHINA" stamp plus red loops around her seat (0:32). Red X on the "no relation" link line (0:09).
- **Magnifier:** a magnifying glass slides over fine print and enlarges "FOR TROUBLED BOYS" (1:11).
- **Counters:** $1,816,157 → $ BILLIONS (0:27). 92 → 100 BOYS (1:22). Check $0 → $2,000,000 (1:44). 933,096 → 1,000,000 (2:59). ×1 → ×10,000 (3:08). 8,116 → 10,000s chips (3:29). "86 of every $100" (3:43). 9 PLATES (3:58).
- **Calendar flips / time tags:** wall calendar 1978 → 1993 with a palette shift from orange to teal (2:05). Desk calendar DAYS LEFT 30 → 29 (2:57). JUL → NOV 1997 "4 MONTHS" (2:59). Day tag WED/SUN on the mop scene (1:24). Corner tags: "DECADES LATER", "YEARS LATER", "SINGAPORE", "KENTUCKY", "SANTA CLARA, CALIF.", "2025".
- **Name lower-thirds:** small dark bar with a green accent line (0:07), joined by a dotted line to the other person's tag (0:09).
- **Pop-on labels for spoken words:** "VIP CUSTOMER", "SOLD", "BUSBOY"/"WAITER" tags, "ORDER!!", "POW", "3D", "AGE 9".
- **Stacked-object gag:** NVIDIA boxes stack up (0:11). Plates fall onto him on "more dishes" (2:03). Plates go up his arm (3:58).
- **Thought bubble:** a picture of a noisy home appears over Jensen (2:20).
- **Same frame, new era:** the identical Denny's wide is reused in 1978, 1993 and 2023. Only the calendar, palette and props change.

### 1.6 Transition grammar

- **Hard cut:** about 85 % of joins.
- **Cut to/from a black text card:** 10 times. The card always enters by hard cut, and the text types on word by word in sync with the VO.
- **Whip pan with motion blur:** 1→2 and inside 4. A tilt-down blur in 12→13 matches on the green glow under the table.
- **Flash frame:** 17 (camera shutter), 21–22 (white/beige after the zoom into the photo).
- **Zoom-through:** 20 (into the photo, then the chapter title), 72 (into the TV, then the data center).
- **Panel slide-on / split screen:** inside 61 and 71. New panels slide in from an edge and cover half the frame.
- **Rack focus in:** 67.
- **Music gap with no VO, 40.7–43.9 s:** used for the title card and the chapter card "The Man With the Key".

---

## 2. Top 15 reusable techniques (vertical 9:16 notes in brackets)

| # | Technique | Example | How to reuse |
|---|---|---|---|
| 1 | **Punch line as a black text card, handwriting typed word-by-word with the VO** | 0:04 "having dinner with a Chinese spy." / 0:20 "Jensen has no idea." | One per 20–30 s. Only the twist sentence. [9:16: centre it, 2 lines max, big] |
| 2 | **Every number becomes an on-screen counter** | 0:27 $1,816,157 → "$ BILLIONS"; 1:44 check $0 → $2,000,000 | Count up, end on a rounded word ("BILLIONS", "10,000s"). |
| 3 | **Objects change on the noun while the camera stays still** | 1:00 SOLD tags, then furniture vanishes; 1:28 tattoos/scars/bandage appear one per word | Cheap and readable. Key each pop to a word in the VO. |
| 4 | **Viewfinder POV, then a flash, then a printed photo** | 0:35.7–0:38.0 (shots 16–18) | Instantly says "being watched". [9:16: viewfinder brackets fit a tall frame well] |
| 5 | **Evidence board: pin, red string, red marker circle** | 0:18 MSS dossier "ALICE HUANG" | For any "they knew" or "identified" beat. |
| 6 | **Top-down table for deals, money and plans** | 0:32 table + CHINA stamp; 2:28 three $200 stacks → $600; 2:16 napkin sketch turns into a 3D wireframe | Hands enter from the frame edges. Very clear on mobile. |
| 7 | **Whip pan between two people for "he… / she…" intros** | 0:06–0:10 Jensen → Alice, name tags joined by a dotted line plus a red X | [9:16: whip vertically, or stack the tags] |
| 8 | **Pull-back reveal of a hidden watcher or endless scale** | 0:13 window → hotel facade → agents; 1:23 endless stall corridor; 3:36 endless queue | Time the end of the move to the reveal word ("nearby", "every day", "same line"). |
| 9 | **3D frame story vs 2D flashback** | 0:38 3D desk + ringing phone + title; 0:44 3D tower crane-up | Present-day thread in another render style. The viewer always knows "when" they are. |
| 10 | **Ringing phone as the story trigger plus title reveal** | 0:38–0:41 "phone call from Washington", title fades in over the 3D desk | Hook → phone rings → title → chapter card. |
| 11 | **Zoom-through an object into a new world** | 0:41 into the polaroid; 3:24 into the TV → data center | Use for a time jump or a jump in scale. |
| 12 | **Same frame, new era (calendar flip + palette shift)** | 2:05 Denny's 1978 orange → 1993 teal; 3:49 same diner 2023 | Re-use one background. Change the date tag, palette and props. |
| 13 | **Split-screen metaphor with sliding panels** | 3:03 chef ×1 vs chip ×10,000 → army of line cooks; 2:31 $600 couch vs chip-giant towers | [9:16: stack top/bottom instead of left/right] |
| 14 | **Magnifier or push-in on fine print** | 1:11 "FOR TROUBLED BOYS"; 1:16 push to the checked "REFORM PROGRAM" box | Turns "it wasn't what they thought" into a visual. |
| 15 | **Dialogue ping-pong with 1 line = 1 shot, then a gag punch from a prop** | 2:50–2:58 "how long?"–"Thirty days"–"if it doesn't sell?"–"Twenty-nine" (calendar flips); 1:57–2:04 BUSBOY/WAITER tags → plates fall | Keep each line 1.2–2 s. The last beat is a prop gag in the wide shot. |

Honourable mentions: corner location/time tags in small caps (0:01 SINGAPORE, 1:17 KENTUCKY); map with a pop-up character and a flight arc (0:53); rack-focus open on a one-word reply (2:52); thought bubble (2:20); "YEARS LATER" studio aside for an adult first-person quote (1:25).

---

## 3. Full per-shot table

Columns: # | time (s) | narration (srt) | size/angle | camera inside the shot | object/character animation | 2D/3D | transition out | mode.
"VO" = narrator. Quoted dialogue = character voice.

| # | Time | Narration | Size / angle | Camera | Animation | 2D/3D | Out | Mode |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.00–1.90 | "In Singapore," | Wide two-shot, eye level, restaurant booth | Very slight push-in (?) | Both chat. Green glow spills from under the tablecloth (chip under table). "SINGAPORE" tag types in, bottom-left | 2D + glow FX | Whip pan with motion blur (frame at 2.0) | Scene |
| 2 | 1.90–4.03 | "the boss of the most valuable company on Earth…" | High-angle world map (dark navy) | Slow drift right / pull-out | Light columns (bars) rise from the map per company. Nvidia's green column is tallest and gets a crown | 2.5D bars on a flat map | Hard cut to black | Map + data |
| 3 | 4.03–6.20 | "…is having dinner with a Chinese spy." | Text card | Static | Handwritten white text types on word by word | 2D | Hard cut | Text card |
| 4 | 6.20–10.63 | "He's Jensen Huang, who runs Nvidia. She's Alice Huang, no relation, and…" | MCU Jensen, then MCU Alice | Push-in on Jensen, then whip pan right (~8.4) to Alice | Jensen lifts chopsticks and laughs. Lower-third "JENSEN HUANG / NVIDIA" slides in. Then "ALICE HUANG" tag, a dotted line between the tags, and a red X stamp on "no relation" | 2D | Hard cut | Scene + labels |
| 5 | 10.63–13.20 | "…she runs one of his biggest customers." | Wide two-shot | Static | Waiter enters right. Green NVIDIA boxes stack up next to Alice. "VIP CUSTOMER" tag pops | 2D | Hard cut | Scene |
| 6 | 13.20–17.60 | "But here's the strange part. Somewhere nearby, American agents are taking pictures." | MS through a rainy window → wide hotel facade ("HOTEL") → MS two agents on the opposite roof | Continuous pull-out through the window, then lateral track to the agents (single move, or a hidden cut (?)) | Rain. Agents with a long-lens camera on a tripod; one holds a paper | 2D layered parallax | Cut on shutter | Scene |
| 7 | 17.60–17.93 | (cont.) | Same MS agents | Static | Polaroid #1/#2 pop in above their heads (shutter beat) | 2D | Cut (detector hit the pop) | Scene + overlay |
| 8 | 17.93–18.37 | (cont.) | Same | Static | Polaroid #3 pops in | 2D | Hard cut | Scene + overlay |
| 9 | 18.37–20.37 | "They know exactly who she is." | Frontal insert: corkboard dossier with "MSS" tab, "ALICE HUANG" label, "SINGAPORE" note | Slight push-in | Gloved hand pins Alice's photo. Red string draws to her name. Red marker circle draws around the photo | 2D | Hard cut to black | Document / evidence |
| 10 | 20.37–22.03 | "Jensen has no idea." | Text card | Static | Types on | 2D | Hard cut | Text card |
| 11 | 22.03–24.37 | "To our customers!" | Medium two-shot | Slow push-in | Jensen raises a wine glass; Alice raises hers | 2D | Hard cut | Scene (dialogue) |
| 12 | 24.37–26.63 | "To friends." | MCU two-shot, glasses up | Holds, then fast tilt down with blur onto the glowing table | Glasses clink | 2D | Blur tilt, matched on the green glow | Scene (dialogue) |
| 13 | 26.63–29.80 | "Under that table, her company is buying billions of dollars of his chips." | Low under-table insert (legs, hands) | Slight push (?) | Hand slides a glowing green chip across. A hand reaches. Counter "$1,816,157" rolls up, then turns into "$ BILLIONS" (green). NVIDIA boxes under the table | 2D, chip with glow (looks 2D, not 3D (?)) | Hard cut to black | Scene insert + counter |
| 14 | 29.80–32.00 | "The kind China isn't allowed to have." | Text card | Static | Types on | 2D | Hard cut | Text card |
| 15 | 32.00–35.73 | "This is the story of how China got a spy into that seat," | Top-down overhead of the round table, both diners | Static | Red "CHINA" star stamp fades/slams in, top-right. Red loops scribble around Alice's seat (marker circle; exact shape unsure) | 2D | Hard cut | Diagram-like scene |
| 16 | 35.73–37.23 | "and who was watching." | POV through a telephoto viewfinder: corner brackets, REC dot, centre reticle, "600mm f/4", rain drops on the lens | Slight push / focus settle (?) | Window shows the pair dining; bokeh drops drift | 2D | White flash | POV |
| 17 | 37.23–37.27 | — | Flash frame (white, 1 frame) | — | Shutter flash | 2D | — | Transition |
| 18 | 37.27–37.97 | — | The same POV image, now a white-bordered printed photo, tilted | Small settle/tilt | Photo "lands" | 2D | Hard cut | POV → photo |
| 19 | 37.97–41.03 | "It starts with a phone call from Washington." | 3D: close on a rotary phone on a green-felt desk, Capitol dome through the window → wider desk with lamp, TOP SECRET file, photo | Dolly back / up from the phone to a wide desk | Phone vibrates with "(( ))" ring marks. Title "HOW A CHINESE SPY GOT INSIDE NVIDIA" fades in, "SPY" in red | Full 3D, toon shaded | Push into the file | 3D frame story + title |
| 20 | 41.03–41.73 | (no VO) | 3D insert of the polaroid on "FILE 0414" (Jensen + Alice) | Fast push-in / zoom-through | Title fades out | 3D | Zoom-through into a bright frame | 3D insert |
| 21 | 41.73–41.77 | — | Beige glow frame | — | — | — | — | Transition |
| 22 | 41.77–41.80 | — | Grey-beige frame | — | — | — | — | Transition |
| 23 | 41.80–43.90 | (no VO, music) | Chapter card "The Man With the Key" | Static | Text holds | 2D | Hard cut | Chapter card |
| 24 | 43.90–46.10 | "But to see why that call mattered, you need to know who picked it up." | Low-angle night city, skyscraper; "SANTA CLARA, CALIF." tag | Crane/tilt up the tower to the roof with the green Nvidia sign | Window lights | 3D | Hard cut | 3D establishing |
| 25 | 46.10–47.63 | (cont.) | 3D desk at night (same prop language as DC), rotary phone | Slight push | Receiver lifted / ring (?) | 3D | Hard cut | 3D scene |
| 26 | 47.63–50.27 | "Because the man in the leather jacket didn't start at the top." | Back view, Jensen at a rooftop railing over the city, searchlights | Slow push-in, then the camera dives straight down a shaft (floor-number indicator counts down, ~50.0) | Searchlight sweeps | 2D scene + 3D-ish shaft | Continuous dive | Scene → move |
| 27 | 50.27–53.10 | "He started in a bathroom in Kentucky." | Dark room, single bulb, door with a toilet sign → black text card (~51.5) | Static at the bottom of the dive | Text types on | 2D | Hard cut | Scene → text card (undetected internal cut) |
| 28 | 53.10–60.13 | "Jensen's story begins in Taiwan. At nine, he and his older brother were put on a plane to relatives in America." | Illustrated paper map with clouds | Push-in to Taiwan, then zoom-out and pan east across the Pacific | Taiwan turns orange; pin and "TAIWAN" label. Two boys pop up on the island; "AGE 9" tag. Dotted flight arc; USA fills blue "AMERICA"; tiny kids land in California | 2D map, cloud parallax | Hard cut | Map |
| 29 | 60.13–64.33 | "To pay for a good school, his parents sold almost everything they owned." | Wide side-on living room (dollhouse) | Static | Parents with a "SCHOOL" letter. Red "SOLD" tags pop on the TV, bike, lamp, sofa; each item vanishes until the room is empty | 2D | Hard cut | Scene (list gag) |
| 30 | 64.33–68.17 | "Oneida Baptist Institute. A boarding school in Kentucky." | Wide porch at dusk; relatives on a swing, two boys on suitcases | Static | School brochure (church-like school picture) hangs on the porch | 2D | Hard cut | Scene |
| 31 | 68.17–69.50 | "Very strict." | MS uncle next to an "OUR RULES" poster with a stern photo | Static | He points at the poster | 2D | Hard cut | Scene (dialogue) |
| 32 | 69.50–71.00 | "Strict is good." | Wide porch, aunt shows the brochure to a boy | Static | Brochure held out | 2D | Hard cut | Scene (dialogue) |
| 33 | 71.00–72.97 | "It wasn't a fancy boarding school." | Top-down table: rules sheet, brochure corner, two boys' heads at the edges | Static | Magnifying glass slides in and enlarges "FOR TROUBLED BOYS"; boys' eyes widen | 2D | Hard cut to black | Document insert |
| 34 | 72.97–75.43 | "It was a reform school for troubled kids," | Text card | Static | Types on | 2D | Hard cut | Text card |
| 35 | 75.43–77.73 | "and the relatives had signed them up by mistake." | Wide kitchen, two relatives at the counter with a form | Fast push-in (motion blur) to the form | Checkbox "REFORM PROGRAM" ticked; label pops | 2D | Hard cut | Scene → insert |
| 36 | 77.73–80.70 | "His brother was sent to work the school's tobacco fields." | Wide farm, red barn, sun; "KENTUCKY" tag | Slight drift; the field rises in the last frame (tilt down (?)) | Brother carries a basket of leaves and walks off | 2D | Hard cut | Scene |
| 37 | 80.70–85.87 | "Jensen got the bathrooms. A hundred teenage boys' worth, every single day." | MS Jensen mopping between stalls → deep corridor of endless stalls → MCU tired face | Push / dolly; the stalls stretch to infinity, then back to close | Counter "92 BOYS" → "100 BOYS"; day tag WED/SUN flips; bucket, mop | 2D with deep perspective | Hard cut | Scene + counter |
| 38 | 85.87–88.37 | "I just wished they would be a bit more careful." | MS adult Jensen in a studio, "ON AIR" neon, mic; framed photo of kid-Jensen; "YEARS LATER" tag | Static / slight | He laughs as he speaks | 2D | Hard cut | Flash-forward aside |
| 39 | 88.37–94.17 | "His roommate was seventeen, covered in tattoos and knife scars, and taped up from his latest fight." | Wide dorm (bunks, lockers, door); little Jensen with a suitcase | Slow push-in toward the roommate | Roommate steps in. Skull tattoos, scars and face bandage appear one per phrase | 2D | Hard cut | Scene (list gag) |
| 40 | 94.17–97.20 | "He was the toughest kid in the school. And he couldn't read." | Wide hallway, lockers, boys in line, board "NO RUNNING / LIGHTS OUT 9PM / CHORES LIST" | Pan right (with blur) toward the board | The board text scrambles into scribbles and a "?" (his view) | 2D | Hard cut | Scene |
| 41 | 97.20–98.57 | "What's this say?" | Wide dorm | Static | Roommate holds out a red book | 2D | Hard cut | Scene (dialogue) |
| 42 | 98.57–99.80 | "I can teach you." | Same wide | Static | Jensen holds the book ("READING") | 2D | Hard cut | Scene (dialogue) |
| 43 | 99.80–102.20 | "Then I teach you the bench press." / "Deal." | MS roommate; bulb on a cord swings | Static | He lifts skull dumbbells; the bulb swings | 2D | Hard cut | Scene (dialogue) |
| 44 | 102.20–103.57 | — | Top-down: Jensen on a bench, roommate spotting; "POW" sticker | Static | Bar wobbles | 2D | Hard cut | Scene (gag) |
| 45 | 103.57–108.77 | "Decades later, Jensen gave that school two million dollars for a new building. It's called Huang Hall." | Wide frontal red-brick building, crowd; "DECADES LATER" tag | Slight push-in | Big check counts $0 → $1,166,190 → $2,000,000. "HUANG HALL" sign drops; confetti | 2D | Hard cut to black | Scene + counter |
| 46 | 108.77–112.27 | "The boy who cleaned its bathrooms put his name on the front door." | Text card | Static | Types on (long line, small) | 2D | Hard cut | Text card |
| 47 | 112.27–115.50 | "At fifteen, he took the graveyard shift at Denny's." | Wide diner interior, warm orange, 1978 calendar | Follows teen Jensen walking in from the right | Clock labels "10 PM" → "3 AM" (?) appear; "1978" tag; DENNY'S neon flickers on | 2D | Hard cut | Scene |
| 48 | 115.50–117.37 | "Dishes first." | Wide kitchen sink, manager + Jensen, plate stack | Static | Manager talks, steam/bubbles | 2D | Hard cut | Scene (dialogue) |
| 49 | 117.37–121.60 | "And then?" / "Then busboy." / "Then, if you're lucky, waiter." | Same wide kitchen | Static | Tag "BUSBOY" pops (he holds a bus tub), then "WAITER" (he holds a notepad) | 2D | Hard cut | Scene (dialogue) |
| 50 | 121.60–123.10 | "And then?" | MCU Jensen hopeful at the sink | Push-in | Bubbles | 2D | Hard cut | Reaction |
| 51 | 123.10–124.67 | "Then more dishes." | Wide kitchen | Static | Giant plate tower drops from the top of frame next to him | 2D | Hard cut | Gag |
| 52 | 124.67–128.60 | "And in nineteen ninety-three, he went back to Denny's. Not to work." | Same diner wide as 47 | Static | Calendar flips 1978 → 1993; palette shifts from orange to teal; booths change; "1993" tag; manager offers an apron | 2D | Hard cut to black | Scene (time jump in place) |
| 53 | 128.60–129.70 | "To start a company." | Text card | Static | Types on | 2D | Hard cut | Text card |
| 54 | 129.70–136.50 | "In a corner booth in East San Jose, Jensen and two engineer friends, Chris Malachowsky and Curtis Priem, sketched…" | Wide frontal booth at the window; "BERRYESSA RD / EAST SAN JOSE" street sign highlighted with a light ellipse; mirrored DENNY'S neon | Slow push-in | Jensen slides in; the two friends pop in; name lower-thirds | 2D | Hard cut | Scene + labels |
| 55 | 136.50–138.77 | "…a chip for three-D graphics." | Top-down table insert, coffee cups, napkin | Static | Pen draws a square; it becomes a green 3D wireframe cube with a "3D" label | 2D with a fake-3D wireframe | Hard cut | Insert |
| 56 | 138.77–142.53 | "He liked the place because it was quieter than home, and the coffee was cheap." | Wide booth, "BOTTOMLESS COFFEE 49¢" sign | Static | Thought bubble of a noisy home; coffee steam | 2D | Hard cut | Scene |
| 57 | 142.53–143.73 | "Anything else, boys?" | Wide booth, waitress foreground right | Static | Waitress enters | 2D | Hard cut | Scene (dialogue) |
| 58 | 143.73–144.97 | "A graphics chip." | OTS from the waitress, notepad foreground | Slight push | Pen on pad | 2D | Hard cut | Scene (dialogue) |
| 59 | 144.97–146.67 | "We have pancakes." | MS waitress with a pancake menu | Static | Holds up the menu | 2D | Hard cut | Scene (dialogue) |
| 60 | 146.67–148.33 | "Then three more coffees." | Wide booth | Static | "3" pops; coffee pour arc | 2D | Hard cut | Gag |
| 61 | 148.33–157.43 | "Each founder put in two hundred dollars. Six hundred dollars, about the price of a used couch, to take on the biggest chip companies in the world." | Top-down table, chip sketch on a napkin | Static. Panels slide in: couch panel enters at ~153.8, then the tower panel drops in over the right half at ~154.8 | Three hands slide in "$200" stacks, which merge to "$600". Couch with "USED" and a "$600" tag. Giant blue corporate towers with generic logos dwarf a tiny Nvidia shop | 2D | Hard cut | Top-down → split-screen metaphor |
| 62 | 157.43–162.60 | "It nearly died. When its make-or-break chip finally shipped in nineteen ninety-seven," | Wide dim office, JUL 1997 calendar, boxes, CRTs | Static | Chip box on the desk glows | 2D | Hard cut to black | Scene |
| 63 | 162.60–165.50 | "Nvidia had about one month of payroll left." | Text card | Static | Types on | 2D | Hard cut | Text card |
| 64 | 165.50–167.93 | "The company's unofficial motto became" | Same office wide | Static | Monitor glow | 2D | Hard cut | Scene |
| 65 | 167.93–171.30 | "Our company is thirty days from going out of business." | Wide office, staff from behind, Jensen standing on a desk | Static | Banner across the top types the motto; red "30 DAYS" scrawl on the window | 2D | Hard cut | Scene + kinetic type |
| 66 | 171.30–172.73 | "So how long have we got?" | OTS employee, Jensen, desk calendar "DAYS LEFT 30" | Static | — | 2D | Hard cut | Scene (dialogue) |
| 67 | 172.73–174.27 | "Thirty days." | MS Jensen + big "DAYS LEFT 30" calendar | Rack focus blur → sharp, slight push | He gestures | 2D | Hard cut | Scene (dialogue) |
| 68 | 174.27–176.60 | "And if the new chip doesn't sell?" | MS engineer at a desk with a glowing chip | Static | Chip glow | 2D | Hard cut | Scene (dialogue) |
| 69 | 176.60–178.40 | "Twenty-nine." | Wider office | Static | Calendar flips 30 → 29; "ORDER!!" pops on the engineer's phone | 2D | Hard cut | Gag |
| 70 | 178.40–180.77 | "It sold, about a million of them in four months." | Wide loading dock, conveyor, truck | Static | Boxes ride into the truck; wall calendar flips to NOV 1997, "4 MONTHS"; counter 933,096 → 1,000,000 | 2D | Hard cut | Scene + counter |
| 71 | 180.77–195.43 | "And here's the trick that later made it a giant. A normal computer chip is one brilliant chef cooking a whole wedding dinner, one plate at a time. Nvidia's chip is ten thousand line cooks, each flipping one pancake at the very same moment." | Stage, red curtains, spotlight → split screen | Slight push on the stage. The chef panel slides in from the left (~186) and splits the frame 50/50. The right panel later turns into the cooks | Jensen as a magician (top hat) pulls out a chip; it grows giant. Chef serves plates one at a time ("×1"). Chip core goes from 1 core to a grid of 10,000 ("×10,000"). The right panel becomes rows of line cooks flipping pancakes in sync | 2D | Hard cut | Metaphor diagram |
| 72 | 195.43–211.73 | "For video games, that meant explosions. Then researchers noticed that artificial intelligence needs exactly that: millions of tiny sums, all at once. ChatGPT was trained on a supercomputer built from tens of thousands of Nvidia chips." | Wide kid bedroom, TV → TV close → data-center corridor | Static, then push-in into the TV (~207), zoom-through to a white screen, then the data center | Game explosions on the TV. Two researchers enter from both sides with clipboards. The TV shows a number grid. Server racks light up green in a wave toward the camera; counter 8,116 → 9,708 → "10,000s NVIDIA CHIPS" | 2D room; corridor in 2.5D/3D perspective | Hard cut | Scene → zoom-through → diagram |
| 73 | 211.73–212.40 | "And suddenly every AI company on Earth…" | Wide Nvidia storefront at night, light beams, queue | Static | Light rays | 2D | Hard cut to black | Scene |
| 74 | 212.40–215.83 | "…was standing in the same line." | Text card | Static | Types on | 2D | Hard cut | Text card |
| 75 | 215.83–216.80 | — | Wide street | Fast pull-back / pan: the queue runs down the whole street | Queue of colourful figures | 2D layered | Hard cut | Scene reveal |
| 76 | 216.80–218.10 | "One of everything, please." | MS counter, shelves of green chips, "NOW SERVING 12", take-a-number dispenser | Static | Customer orders; Jensen pulls a ticket | 2D | Hard cut | Scene (dialogue) |
| 77 | 218.10–221.10 | "Take a number." / "Forty thousand?" | MS customer → ticket "40,000" thrust at the camera → shelves "NOW SERVING 13" | Push / tilt following the ticket, then a pan to the shelves (?) | Ticket gets big; the serving number ticks 12 → 13 | 2D | Hard cut | Scene (dialogue gag) |
| 78 | 221.10–228.70 | "That's your place in line." / "By twenty twenty-five, about eighty-six of every hundred dollars spent on AI chips went to Nvidia." | Wide through the shop window (crowd); undetected cut at ~222.0 to a dark-green diagram | Static | "2025" tag; "86 / OF EVERY $100" types in; a grid of 100 bills fills in, then 86 bills fly into the big green Nvidia register; small grey registers left/right; register display counts up from $0 | 2D | Hard cut | Scene → data diagram |
| 79 | 228.70–236.17 | "In twenty twenty-three, Denny's put a plaque on the booth. It calls it 'the booth that launched a one-trillion-dollar company.'" | Same Denny's wide (2023, cream/red palette, balloons) → close on the plaque | Static, then push-in (~231.5) to the plaque | Worker on a ladder hangs the plaque; "2023" tag | 2D | Hard cut | Scene → insert |
| 80 | 236.17–240.00 | "At the party, the boss of that company put on an apron, balanced ten plates up his arm, and served the tables." | Wide crowd, Jensen centre | Slight push | Jensen waves; plates stack up his arm with a counter "9 PLATES" (continues past 4:00) | 2D | (continues) | Scene + counter |

### Undetected internal changes (no cut in `cuts240.txt`)
- ~8.4 s, inside 4: whip pan Jensen → Alice.
- ~15 s, inside 6: window → exterior (move or hidden cut (?)).
- ~50.0 s, end of 26: dive down the shaft.
- ~51.5 s, inside 27: bathroom door → black text card.
- ~153.8 / 154.8 s, inside 61: split-screen panels slide in.
- ~186 s, inside 71: chef panel slides in. ~191 s: chip → line cooks.
- ~207 s, inside 72: zoom into the TV → data center.
- ~222.0 s, inside 78: shop window → 2025 register diagram.
- ~231.5 s, inside 79: wide → plaque close.
