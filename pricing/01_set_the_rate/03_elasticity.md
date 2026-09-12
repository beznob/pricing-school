# 1.3 · Elasticity — how customers react when you change the price

This is the single most important idea in pricing. Take it slowly.

## 1. The question elasticity answers

> **"If I raise my price by 1%, how many percent of my volume do I lose?"**

That's it. Elasticity is just that answer, written as a number.

- Elasticity **−2**: raise price 1% → lose 2% of volume. Customers react strongly.
- Elasticity **−0.5**: raise price 1% → lose only 0.5%. Customers barely react.

The minus sign is there because volume moves *opposite* to price (price up,
volume down). In conversation people often drop the sign and say "elasticity
of 2", meaning −2.

## 2. The formula (one line, then we're done with it)

> **Elasticity = (% change in volume) ÷ (% change in price)**

Example: you raise the price 4% and sales fall 6%.
Elasticity = (−6%) ÷ (+4%) = **−1.5**.

## 3. The magic dividing line: −1

Whether the number is **bigger or smaller than 1** (ignoring the sign)
decides what a price change does to your **revenue**:

- **Elastic** (|elasticity| > 1, e.g. −2): volume reacts *more* than price.
  Raise price → revenue **falls** (you lose more sales than the extra price
  makes up for). Cutting price can *grow* revenue.
- **Inelastic** (|elasticity| < 1, e.g. −0.5): volume reacts *less* than
  price. Raise price → revenue **rises**. You have pricing power.
- **Unit elastic** (exactly −1): revenue stays flat whatever you do.

### Feel it with numbers

100 sales/week at £10 → revenue £1,000. You raise the price 10% to £11.

| Elasticity | Volume falls by | New volume | New revenue |
|---|---|---|---|
| −2 (elastic) | 20% | 80 | £880 — **worse** |
| −1 (unit) | 10% | 90 | £990 — flat |
| −0.5 (inelastic) | 5% | 95 | £1,045 — **better** |

## 4. Why different customers have different elasticities

Elasticity isn't a property of the product — it's a property of the
**customer's situation**:

- **Can they compare easily?** Online customers see five rates in ten
  seconds → very elastic (around −2 or stronger).
- **Can they wait or go elsewhere?** Someone at the airport gate cannot →
  very inelastic (that's why airport rates are terrible).
- **Are they spending their own attention?** A business account holder whose
  travel agent handles currency barely notices the rate → inelastic.

In the repo's simulated business: digital channel ≈ −2.2 (most sensitive),
high-street walk-up ≈ −1.3, contracted business channel ≈ −0.7 (least).
Same product, three different elasticities. **This is why one price for
everyone is almost always wrong** — more in [File 4.1](../04_satisfy_the_regulator/01_segments_and_fairness.md) and [file 1.5](05_competition.md).

## 5. From elasticity to the "right" price — the markup rule

There is a classic rule (the **Lerner rule**, after economist Abba Lerner)
linking elasticity to the best profit-making price:

> **The profit-maximising margin (as a share of price) = 1 ÷ |elasticity|**

- Elasticity −2 → best margin ≈ 1/2 = **50% of the price**.
- Elasticity −4 → best margin ≈ 1/4 = **25%**.
- More sensitive customers → thinner margin. Makes sense: squeeze elastic
  customers and they leave.

**Worked example:** it costs you £1 to provide the service and your customers
have elasticity −2. Rule says margin should be 50% of price, i.e. price = £2
(cost £1 + margin £1 = 50% of £2). ✓

**The catch (worth knowing early):** the rule only produces an answer when
customers are *elastic* (|elasticity| > 1). For inelastic customers it says
"raise the price forever", which is obviously wrong — in real life
competitors and regulators stop you long before that. When a pricing model
tells you to charge the maximum allowed, treat it as a **warning to
double-check**, not an instruction.

## 6. The trap that catches real companies (preview)

To *measure* elasticity you compare price changes with volume changes in
your data. But here's the trap: firms **raise prices exactly when demand is
strong** (peak summer). So in the data, high prices sit next to high volumes
— and a naive analysis concludes "price doesn't hurt volume" or even "raising
price *increases* volume". The measurement is poisoned by your own pricing
habits. This is called **endogeneity** (the price was set *because of* the
demand you're trying to measure). [File 2.2](../02_prove_the_change/02_tests_and_experiments.md) explains the honest fixes; the
one-line version is: *create price changes that have nothing to do with
demand* (a controlled test), and measure those.

## 7. Check yourself

**Q1.** You cut the price 5% and volume rises 4%. What's the elasticity? Did
revenue go up or down?

**Q2.** Customers at elasticity −0.8. Your CFO wants more revenue. Raise or
cut the price?

**Q3.** Cost per unit £3, customer elasticity −3. What price does the
markup rule suggest?

---

### Answers

**A1.** 4 ÷ (−5) = **−0.8** — inelastic. You cut the price and volume didn't
respond enough: revenue **fell** (e.g. 100×£10=£1,000 → 104×£9.50=£988).

**A2.** **Raise.** Inelastic customers lose you less volume than the price
gain. (But check fairness — [File 4.1](../04_satisfy_the_regulator/01_segments_and_fairness.md) — and competition — [File 1.5](05_competition.md) — first.)

**A3.** Margin = 1/3 of price. Price − cost = price/3 → price = **£4.50**
(margin £1.50 = one third of £4.50). ✓

---

## Where this idea goes — the elasticity ladder

Every "deep" thing about elasticity in this repo is this file's number with
more machinery around it. Rung by rung:

1. **This file:** elasticity = %Δvolume ÷ %Δprice — one number per segment,
   read off two clean changes.
2. **The honesty rung ([File 2.1](../02_prove_the_change/01_averages_and_uncertainty.md)):** any measured elasticity is an *estimate*
   with a range. "−1.8, plausibly −2.4 to −1.2" and "−1.8, plausibly −4 to
   +0.4" justify completely different decisions — always ask for the range.
3. **The trap rung ([File 2.2](../02_prove_the_change/02_tests_and_experiments.md)):** the estimate only means something if the
   price changes in your data had *nothing to do with demand* (§6's
   endogeneity). Experiments exist precisely to create that clean variation.
   This is the single most common way real elasticity numbers are wrong.
4. **The grown-up form ([The workflow appendix](../appendix/data_science_workflow.md) §2):** in production, elasticity lives
   inside a conversion model. The coefficient on log(relative price) **is**
   this file's number — "a 1% price rise changes conversion by about X%" —
   just measured for every quote at once instead of one segment at a time.
5. **The payoff rung ([The workflow appendix](../appendix/data_science_workflow.md) §3):** the markup rule (§5) is the shortcut
   version of full price optimisation — sweep candidate prices, expected
   profit = (price − cost) × P(buy), take the top. Same idea; the model
   simply replaces the single number with a curve.
6. **In code:**
   [`../engine/elasticity_models.py`](../engine/elasticity_models.py)
   climbs rungs 2–5 on simulated data and shows what ignoring rung 3 costs —
   **45% of profit**, the case study's headline result. Then
   [`../05_the_panel/N2_hierarchical_elasticity.ipynb`](../05_the_panel/N2_hierarchical_elasticity.ipynb)
   estimates *thousands* of elasticities at once without drowning in noise.
