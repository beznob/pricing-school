# 0.1 · The job and the evidence — Senior Manager, Pricing, Distribution & Revenue

The role profile (March 2026, Grade 4) mapped line by line to what this folder
teaches, what it proves in code, and what you say in the room. Read it twice: once
now to see the shape of the job, and once in the last week to check that the map is
true of you.

One reading matters before anything else. In this profile **TMC means the Travel
Money Card**, the prepaid multi-currency Mastercard that First Rate issues for the
Post Office. The lines "own the P&L for TMC, including new card sales, reloads and
in-life revenue" and "lead the TMC roadmap and migration project for prepaid cards"
only make sense that way. It does not mean a travel management company. Getting
that wrong in the interview would undo a lot of good preparation, so
[file 0.4](the_card_and_the_migration.md) is devoted to the card.

## The role in facts

| | |
|---|---|
| Title | Senior Manager, Pricing, Distribution & Revenue |
| Grade and date | Grade 4, role profile March 2026 |
| Team and location | Revenue Team, Botanica, Datchet |
| Reports to | Chief Revenue Officer |
| Direct report | Manager, Pricing, Distribution & Revenue |
| Internal relationships | Leadership Team, Executive Team, Product, IT, Risk & Compliance, most departments |
| External relationships | The existing and the current card processing partner, Post Office, card manufacturing bureaux, KYC partner, card scheme, others |
| Working alongside | A technical project manager |

Three things in that table shape the interview. You manage one person, so expect a
question about how you develop and delegate. The external list is the card supply
chain, which tells you the migration is real and current rather than aspirational.
And reporting to the Chief Revenue Officer means every number you bring is tested
commercially before it is tested technically.

## Business accountabilities

| The profile says | Taught in | Proved by | Say this |
|---|---|---|---|
| Develop and own the enterprise-wide pricing strategy across retail, TMC and digital channels | files 1.3, 1.6, 1.7; file 0.4 for the card | `channel_positioning` in `engine/distribution_economics.py`; lab 1.3; N7 | Compete where demand is elastic and cheap to serve, harvest where it is not. The card is priced across its lifecycle, not at the till |
| Lead policy-setting for pricing tests, commercial trials and elasticity modelling | files 2.1 to 2.3; labs 2.2 to 2.6 | `engine/elasticity_models.py` (OLS against IV); lab 2.5; N1, N4, N10 | Policy means rules: a minimum detectable effect before launch, a permanent holdout, and a decision rule written down before the data arrives |
| Manage margin modelling, margin support frameworks and revenue distribution across channels | files 1.1, 1.4, 1.7 §2; lab 1.1 | `channel_pnl`, `margin_waterfall`, `margin_support_breakeven`; N5 | No support without a break-even test, and always the net margin, never the headline |
| Own channel product distribution strategy and pricing architecture | file 1.7 §1, file 0.2 | `engine/distribution_economics.py`; N7 | The same FX margin gives very different net contribution by channel. Architecture is the fences and the metrics, not the numbers |
| Conduct and maintain competitor monitoring and market intelligence processes | file 1.5, file 1.7 §5; lab 1.4 | `competitive_index`, `competitor_sensitivity` in `engine/aop_scenario.py`; N8 | A total-cost price index on a daily cadence from legal sources, and every threat sized in pounds of contribution |
| Lead product and channel pricing modelling and scenario analysis | file 3.2, file 3.3 §3; lab 3.1 | `run_scenarios`, `revenue_bridge`; N11 | Every scenario runs through the elasticity, so volume responds and the plan stays internally consistent |
| Manage the AOP modelling for pricing-related revenue lines | file 3.1, file 3.3 §3; lab 3.1 | `revenue_lines`; N11 | Built bottom-up by line and channel, reconciled top-down, and only part of the modelled effect goes into the plan |
| Oversee pricing strategy support for Postmasters and the Post Office network | file 0.2, file 1.7 §1 | The `post_office` channel in the simulator; N8 | The payaway has two layers, First Rate to Post Office and Post Office to postmaster. From April 2026 postmasters receive at least 55% of travel product income and £5 per card, so the network's incentives have just moved |
| Ensure all pricing activity is compliant with FCA Consumer Duty fair value requirements | files 4.1, 4.2, file 3.3 §4; lab 4.1 | `engine/fair_value.py` and the generated assessment; N6, N9 | The FCA's October 2024 payments review said benchmarking against competitors is not a fair value assessment. Ours analyses cost, benefit and customer groups |
| Provide pricing expertise and modelling support to product, commercial and finance stakeholders | files 3.2, 3.4 | `engine/pricing_charts.py`, `engine/db_helper.py` | Headline first, then the reading, then the caveat before anyone finds it |

## Business area responsibilities

These four lines are the part of the profile the pricing literature does not cover,
and the part a candidate is most likely to skate over.

| The profile says | Taught in | Proved by | Say this |
|---|---|---|---|
| Lead the TMC roadmap and migration project for prepaid cards | file 0.4 | Not proved by code here. The file gives the anatomy of a card programme, the pricing decisions inside a migration, and the vendor KPIs | Honest position: I have not run an issuer processor migration. Here is how I would run the commercial workstream, what the fee schedule review has to pass, and the five questions I would ask in week one |
| Own the P&L for TMC, including new card sales, reloads and in-life revenue | file 0.4, file 3.1 | `revenue_lines` in `engine/aop_scenario.py` builds those three lines by name; the card portfolio in `engine/travel_money_simulator.py`; `engine/fair_value.py` on the same portfolio | Three lines, three drivers: cards sold, reloads per active card, and spend against dormancy in life. Inactivity fees are revenue and conduct risk at once |
| Stakeholder management: primary liaison between internal teams, legal, finance and external vendors | file 3.2 §2 to §4, file 3.4, file 0.4 | Every sixty second answer in the panel folder | Answer first, options with a recommendation, the pound prize and the pound risk, and no surprises for Compliance |
| Compliance and risk management through the procurement process | file 0.4, file 3.3 §5 | The procurement checklist in file 0.4 | An e-money institution's critical suppliers fall under outsourcing and operational resilience expectations, so Compliance and Risk are in the tender from the start |

## Principal tasks, the skills

| The profile asks for | Where the track covers it |
|---|---|
| Pricing strategy, yield management, revenue optimisation | files 1.6, 1.7 §4; labs 1.3, 1.5; `engine/dynamic_pricing.py` |
| Building pricing models, elasticity analyses, margin scenarios | labs 1.2, 2.3, 2.5, 3.1; the four engine models |
| Designing and executing pricing tests and evaluating commercial outcomes | files 2.2, 2.3; labs 2.2, 2.4; N1, N4 |
| Distribution economics across retail, digital and agency channels | file 1.7 §1; lab 1.1; `channel_pnl` |
| Modelling and optimising multi-channel distribution arrangements | `channel_positioning`; N7; the omnichannel lab |
| Postmaster or franchise-style distribution economics | file 0.2, the Postmaster section; `post_office` in the simulator |
| FCA Consumer Duty and fair value assessments for prepaid products | files 4.1, 4.2; lab 4.1; N6 |
| Regulatory pricing justifications and fair value documentation | `generate_fair_value_assessment`; file 4.2 is the worked document |
| Competition law and pricing governance | file 3.3 §4 and §5; guardrails in `engine/dynamic_pricing.py` |
| Data modelling, Python, R, SQL, Excel financial modelling, scenario analysis, visualisation | Every lab; `engine/pricing_finance.py`; the SQL drills. R is not covered and Excel is a one evening exercise in the skills map |
| BI tools for pricing and revenue reporting | Not built here. The tables `db_helper.py` returns are warehouse shaped; see the skills map |
| Translating complex pricing models into clear commercial recommendations | files 3.2, 3.4; the recommendation columns in every engine output |

The full tick list, with the one thing to be able to do for each, is the
[skills map](skills_map.md).

## People

The profile asks you to manage key internal and external stakeholders and to
communicate risk, issues and status on a regular basis. File 0.4 carries the RAID
log and the status cadence for the migration, and file 3.2 carries the stakeholder
map. Two things to have ready for the people question: what you would do in the
first month with your direct report (agree the metric dictionary, set a review
standard for any number that leaves the team, give them the permanent holdout as a
first project they own end to end), and how you communicate a risk upward before it
becomes an issue.

## Ideal candidate profile, and where you stand

| The profile wants | What this folder gives you | What you bring from your own career |
|---|---|---|
| Expert pricing and economic understanding and modelling | The whole track and the engine | Your own elasticity and optimisation work |
| Familiarity with financial technologies, platforms and providers in the prepaid and FX sector | File 0.2 names the market and file 0.4 names the parts of a card programme: issuer, scheme, issuer processor, bureau, KYC provider, app and tokenisation | Any processor, scheme or fintech platform you have worked with, named plainly |
| Developing KPIs and performance metrics for vendor management | The vendor KPI table in file 0.4 | A vendor you actually managed against a scorecard |
| Ideally, working with card processing schemes to create or migrate products | A gap. File 0.4 gives you the vocabulary and the shape of the work | Say plainly if you have not done it, then show you know what it involves |
| Degree in Economics, Finance, Mathematics or related; five years in pricing, revenue management or commercial finance; pricing strategy in financial services, retail or payments | Your CV, not the folder | Lead with the closest domain |
| Strong financial modelling | File 3.1 and `engine/pricing_finance.py`, doctested | A model that went into a real plan |
| Knowledge of FCA Consumer Duty fair value frameworks | Files 4.1, 4.2 and the FCA findings in file 0.2 | Any fair value work you have documented |
| Excellent communication and stakeholder management | Files 3.2, 3.4 and the sixty second answers | A decision you got through a sceptical room |

## Personal attributes

**Strategic.** The profile wants someone who can devise and execute a strategy and
inspire others to own and deliver it. The omnichannel proposal in the panel folder
is the worked example: a strategy sized, sequenced, tested and staged so that the
irreversible step comes last. Tell it as a story about getting other people to own
the pieces.

**Commercial awareness.** The profile names management information in decision
making, and proficiency in systems administration. The second phrase is unusual in
a pricing profile and most likely means owning the configuration of the rate engine
and the price book: who can change a rate, how a change is versioned, how it is
reversed. File 3.3 §5 is the material. Say you would want to own that access rather
than borrow it.

## Five interview stories this folder lets you tell

1. **"Our elasticity was wrong and it was costing us margin."** Naive regression
   said demand was almost inelastic because the desk raises the margin in peak
   season. An instrument built on wholesale cost showed digital customers at about
   minus 2.2. Pricing on the biased number over-charges and loses roughly 45% of
   profit. (`engine/elasticity_models.py`, N10)
2. **"The headline FX margin lies about channel profitability."** The Post Office
   network earns the highest gross revenue and pays a large share of it away to the
   network; digital drops almost all of its revenue to contribution. Price the net
   and position each channel by its own elasticity. (`engine/distribution_economics.py`, N7)
3. **"Uniform price moves destroy value; targeted ones create it."** A blanket 10%
   rise in FX margin reduces contribution because blended demand is elastic, while
   harvesting the inelastic channels and competing in the elastic ones lifts it.
   (`engine/aop_scenario.py`)
4. **"We found and fixed a Consumer Duty fair value problem."** Vulnerable customers
   paid more for less benefit, driven by inactivity fees eroding unspent balances.
   The assessment documented it and the remediation named fee caps and balance
   returns. (`engine/fair_value.py`, file 4.2, N6)
5. **"I can defend the AOP under scrutiny."** Elasticity-aware scenarios and a
   revenue bridge that attributes every pound of change to volume, margin,
   competitor and mix, including the downside of a price war. (`engine/aop_scenario.py`, N11)

## Honest gaps, and how you would close them on the job

The migration is the biggest one. Nothing here has run a processor migration; file
0.4 gives the structure and the questions, and the right answer in the room is the
plan, not a claim. Vendor management is close behind: the KPI table is a starting
point, and the credible version is a scorecard you have actually used. R is not
taught here and Excel and Power BI are only pointed at. And the data behind every
figure is simulated, so the first month is about swapping the simulator for
transaction data and securing identification with live regional tests.

## Going deeper

The rest of the [track](../README.md) is the conceptual companion to this evidence:
the foundation files in stages 1, 2 and 4, the senior reference in files 1.6, 1.7
and 3.3, the market in file 0.2 and the card in file 0.4. The
[question bank](../05_the_panel/interview_qa_bank.md) expands the five stories
above into rehearsed answers.
