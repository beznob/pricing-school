# 21 · Travel Money & Prepaid — the domain deep-dive

*(Consolidated from the former `pricing_manager_handbook` chapter 22. This
grounds every general principle in the real product, economics, players and
rules of UK travel money & prepaid FX cards.)*

## The products

- **Cash / foreign currency** — physical notes bought in branch, Post Office,
  online for collection/delivery. Price = **FX margin** (spread over interbank)
  + sometimes delivery.
- **Prepaid currency cards** (multi- or single-currency) — load £ → hold/spend
  in FX. Revenue across the **lifecycle**, not one sale.
- **Travel debit/credit & app-based FX** — fintech challengers (Wise, Revolut,
  Monzo) with low/transparent margins.
- **International payments / remittance** — adjacent corridor business.

## The revenue model — a bundle of price levers

FX margin (the spread — primary lever, where elasticity bites hardest) · card/
issuance fees · ATM withdrawal fees · **inactivity/dormancy fees** (high margin,
the classic Consumer Duty harm) · in-life FX and interchange · **breakage**
(unspent balances). The P&L splits into **new card sales, reloads, in-life
revenue** — each with its own margin, growth and risk (File 20 §2).

## Why FX margin is a hard pricing problem

- **Low transparency** — customers struggle to compare spreads (vs a clear
  £ fee); this is where margin lives *and* where conduct risk concentrates
  (File 02's implicit margin).
- **The reference rate is public** — the interbank/Google rate makes the spread
  implicitly benchmarkable; digital-savvy customers do compare → the digital
  channel is **elastic**.
- **Endogeneity is acute** — margin is pushed up in peak season exactly when
  demand is high → naive elasticity estimates are badly biased (File 03 §6).
- **Wholesale cost moves** — interbank rates/volatility are a natural
  **instrument** for identification and the reason to index B2B contracts.

## The channels and their economics

| Channel | Character | Elasticity | Economics |
|---|---|---|---|
| **Digital / online** | Price-transparent, self-serve | **Most elastic** (≈ −2.2 in the case study) | Low cost-to-serve; compete hard |
| **Retail branch** | Convenience, footfall | Moderate | High cost-to-serve (rent, cash, staff) |
| **Post Office / Postmaster** | Huge trusted network, walk-in | Inelastic (convenience) | **~45% Postmaster commission** — biggest gross, middling net |
| **TMC** | Contracted B2B2C corporate | **Least elastic** (≈ −0.7) | Negotiated; index-link; relationship-driven |
| **Agency / travel agents** | Bundled with holiday | Inelastic-ish | Agency payaway; cross-sell |

Postmaster commission is itself a strategic lever — model it two-sided
(File 19 §1), don't treat it as fixed.

## The competitors and the structural threat

- **Incumbents:** Travelex, Post Office Travel Money, supermarket FX, banks.
- **Fintech challengers:** Wise (mid-market rate + explicit ~0.33–0.6% fee),
  Revolut, Monzo, Starling — eroding the spread model.
- **The structural threat:** challengers move the market toward transparent,
  near-zero FX margin — a **Bertrand-style squeeze** on the spread (File 19 §5).
  Defence = differentiate on convenience, cash access, network reach, bundling,
  trust — and serve the less-elastic segments (convenience/older/cash-preferring,
  corporate) well; consider a transparent/subscription option for the
  price-sensitive (File 18 §8).

Directional market levels (see the master prompt's Honesty Rule — quote as
directional): high street ~4.6–5.2% below interbank on majors; online beats
branch walk-up by ~2–3%; buyback ~150–250 bps worse than sell; airport ~10%+
worse.

## The regulatory frame

- **FCA Consumer Duty** — fair value on the **total lifecycle cost** with
  vulnerable-customer focus; the inactivity-fee/breakage harm is the textbook
  issue (Files 07, 20 §4).
- **E-money & payments** — Electronic Money Regulations 2011 (issuance,
  safeguarding), PSRs 2017/PSD2, FX transparency expectations.
- **Consumer protection** — all-in pricing clear; no drip-revealed margins;
  genuine rate claims.

## The senior pricing agenda for this business

1. **Estimate channel FX-margin elasticity causally** (cost-shock IV /
   experiments); refresh on a cadence.
2. **Price the net contribution per channel** — harvest inelastic, compete in
   elastic (File 19 §1).
3. **Defend the spread against fintech** via differentiation, segmentation,
   bundling, possibly a transparent/subscription tier.
4. **Run the fair-value process** — total-cost assessment, vulnerable-customer
   testing, inactivity-fee remediation, annual governance.
5. **Own the AOP** by revenue line × channel, elasticity-consistent scenarios,
   defensible bridge (File 20 §3).

## Connecting to the case study

Realised in code in [`../fast_transaction_services/`](../fast_transaction_services/README.md):
`travel_money_simulator.py` (5 channels, FX margin, lifecycle, competitors),
`elasticity_models.py` (causal channel elasticity), `distribution_economics.py`
(channel net economics + margin support), `fair_value.py` (Consumer Duty),
`aop_scenario.py` (plan, scenarios, competitor index). See its
[`JD_alignment.md`](../fast_transaction_services/JD_alignment.md).

## Red flags

- One FX margin across channels with very different elasticity and economics.
- Ranking the Post Office channel on **gross** revenue while ~45% commission hides.
- Inactivity/breakage revenue with no fair-value justification.
- Ignoring the fintech spread-squeeze until margin has already gone.
- Fixed-rate B2B/TMC contracts with no FX index.
