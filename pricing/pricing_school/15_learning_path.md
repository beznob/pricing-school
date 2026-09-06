# 15 · The Learning Path — commercial + technical, in the right order

*(The "how to actually get good" file. It sequences everything in this repo
— school files, notebooks, case study, master prompt — into one plan with
two interleaved tracks, aimed at the Senior Manager, Pricing, Distribution &
Revenue role.)*

## The principle: alternate the tracks

The job is a hybrid: a "commercially-fluent quant". Study accordingly —
**never do a technical week or a commercial week; alternate daily.** Each
technical idea sticks when you immediately ask "how would I sell this
decision?", and each commercial habit sticks when you ask "what analysis
would back this up?"

## Am I ready? — the self-test (do this first, and again at the end)

Say each of these out loud, unprepared. Score yourself honestly.

| # | Can I explain… | Track | Taught in |
|---|---|---|---|
| 1 | why a 2% price cut can eat half the profit per sale | C | 01 |
| 2 | where the profit hides in "0% commission" | C | 02 |
| 3 | elasticity, the −1 dividing line, and the markup rule | T | 03 |
| 4 | price–volume–mix, and the leakage waterfall | C | 04 |
| 5 | why "CI crosses zero" ≠ "didn't work", and the EV framing | T | 05 |
| 6 | control groups, DiD, MDE, and the neighbour problem | T | 06 |
| 7 | the fairness check that passes while the harm is real | C | 07 |
| 8 | promo vs structural, and why never to blanket-match | C | 08 |
| 9 | censored sales and the stock death-spiral | T | 09 |
| 10 | which distribution for order sizes / counts / tails | T | 11 |
| 11 | the conversion-model → elasticity → optimise workflow | T | 12 |
| 12 | conversion/combined-ratio/AOP, and the pre-wiring playbook | C | 13 |

8+ confident: go straight to the notebooks and the question bank.
Under 8: run the plan below.

## The four-week plan

**Rhythm:** ~1 hour/day. Read → do the practice questions → say one answer
out loud. Weekends: run one notebook and read its 60-second answer aloud.

### Week 1 — Money mechanics (foundation)
- Mon–Thu: school **01 → 04** (one per day). These four are the language of
  every meeting you'll ever sit in.
- Fri: school **11** (distributions) — light read, focus on the "use it
  when" rules.
- Weekend: run the case study once
  (`python ../fast_transaction_services/run_role_case_study.py`) and just
  *read* the printed output. Recognise the words you learned this week.

### Week 2 — Evidence (the technical spine)
- Mon: school **05** (uncertainty). Tue: school **06** (experiments).
- Wed: school **12** (the DS workflow) — the big one; take two days if needed.
- Thu–Fri: notebooks **N4** then **N5** — read top to bottom, run them,
  read the 60-second answers aloud.
- Weekend: re-answer question-bank sections **A and B** (file 14) cold.

### Week 3 — Judgement (the commercial spine)
- Mon: school **07** (fairness). Tue: school **08** (competition).
  Wed: school **09** (stockouts). Thu: school **13** (KPIs & stakeholders).
- Fri: notebooks **N6** and **N8** — the fairness trap and the competitor
  game, now with numbers.
- Weekend: question-bank **D** cold, plus draft your three **E** stories
  (STAR shape) from your own career.

### Week 4 — Integration (sound senior)
- Mon: notebooks **N1 + N3** (the Head-of-Data pair: geo tests, censoring).
- Tue: notebooks **N2 + N9** (scale + production guardrails).
- Wed: notebooks **N7 + N10 + N11** (portfolio, DML, the runbook) — skim
  the code, own the answers.
- Thu: the master prompt's Part 4 (concept curriculum) and Part 7 (the
  twelve scenarios) — it should now read as revision, not news.
- Fri: full mock — all 12 self-test items + question bank end to end, out
  loud, timed.
- Weekend: rest. Then re-run the self-test table above.

## The compressed path (48 hours before an interview)

1. Re-run the self-test; patch only the failures with their school files.
2. Run **N4**; drill its 60-second answer until automatic — it's the single
   highest-leverage answer in the repo.
3. Read question bank (file **14**) end to end, out loud.
4. Re-read the master prompt's **Honesty Rule** (numbers are directional;
   under-claim) and its FX cheat-sheet.
5. Sleep. Fluency beats coverage.

## How the repo's layers fit together (the map)

```
pricing_school/           ← the WORDS and the ideas (you are here)
      ↓
fres_prep/ notebooks      ← the ideas PROVEN in code, one interview
      ↓                     question each, with spoken answers
fast_transaction_services/← the full runnable business: simulator,
      ↓                     elasticity engine, fair value, AOP
FRES_MASTER_PREP_PROMPT   ← the senior-level roadmap, panel strategy,
                            twelve scenarios, honesty rules
```

Anything unclear at a lower layer: drop down one level. Anything too easy:
climb one. The glossary (file **10**) works at every level.

The rungs between the layers are written out for you: each Part 1 file ends
with **"Where this idea goes — the ladder"** (its simple idea, rung by rung,
up to the production version and the code), files 11–12 open with a
bridge-in table mapping their sections back down to the foundations, and
File 00 carries the one-line master map of all ten ladders. If a notebook
ever feels like a leap, the missing rung is in one of those three places.

## The three habits that outlast the plan

1. **Every average → "averaged over whom?"** (Files 05, 07)
2. **Every result → "compared to what control?"** (File 06)
3. **Every recommendation → "what's the downside, and can we reverse it?"**
   (Files 05, 13)

Ask those three questions relentlessly and you will out-perform most people
with better maths — because the maths is rarely the binding constraint;
the thinking is.
