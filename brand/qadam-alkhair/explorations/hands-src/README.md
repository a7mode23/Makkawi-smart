# اليدين — مسودة العمل · Two hands, work in progress

Source for `two-hands-a*.png` and `one-hand-c*.png`. It runs from the
scratch folder next to `src/` (it imports `kit.py` and `glyphs.py` from there).
The hands are the Noto Emoji glyphs `palmDownHand` / `palmUpHand`
(SIL OFL 1.1, `ofl/notoemoji/NotoEmoji[wght].ttf` in google/fonts).

| File | Role |
| --- | --- |
| `hands3.py` | places the glyphs and the heart; `give_receive_facing` = option أ |
| `a2.py` | أ developed: heavier line, cuffs, tilt, a level pair of sparkles, light fill |
| `silhouette.py` → `silhouettes.json` | each hand's filled outline, traced with potrace |
| `lock3.py`, `measure.py`, `shot.py` | lockups, ink-box measuring, PNG export |
| `a3.py` | round 3: the dot of «خ» as a heart, darker giving hand, the lockups |
| `a3b.py`, `clear.py` | round 3 fixed: the hands move apart and the light, heart and sparkles sit in the largest circle that clears both hands |
| `c2.py` | option ج developed: one hand offering a glowing heart, the light kept clear of the hand |
| `c3.py` | ج round 2: finer finger lines in a bold outline, a filled sleeve, a shine on the heart |
| `opt_a.py`, `a2_final.py`, `a3_final.py`, `opt_c.py`, `c2_final.py`, `c3_final.py` | the exported sets |
