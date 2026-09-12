# 0.3 · The skills map

Every accountability, responsibility, skill and attribute in the role profile (March
2026), with the step in the [track](../README.md) that teaches it, the code that
proves it, the panel notebook that rehearses it, and the one thing you should be
able to do before you tick it. Use it as a progress sheet. When every last column is
true, you are ready.

TMC throughout means the Travel Money Card, the prepaid product. See
[file 0.4](the_card_and_the_migration.md).

## Business accountabilities

| The job says you own | Taught in | Proved by | Rehearsed in | Tick when you can |
|---|---|---|---|---|
| Enterprise wide pricing strategy across retail, TMC and digital channels | files 1.3, 1.6, 1.7; file 0.4 | `engine/distribution_economics.py` (channel positioning), lab 1.3 | N7, the omnichannel lab | Say which channels to harvest and which to compete in, and why the answer follows from elasticity and net economics; then say how the card is priced across its life |
| Policy-setting for pricing tests, commercial trials and elasticity modelling | files 1.3, 2.1, 2.2, 2.3; labs 1.2, 2.2 to 2.6 | `engine/elasticity_models.py` (OLS against IV), lab 2.5 | N1, N2, N4, N10 | Design a regional test with a minimum detectable effect, write the decision rule before the data arrives, and explain why the naive elasticity is biased and in which direction |
| Margin modelling, margin support frameworks and revenue distribution across channels | files 1.1, 1.4, 1.7 §2; lab 1.1 | `margin_support_breakeven` in `engine/distribution_economics.py` | N5, N8 | State the discount break-even from memory and say when margin support is self funding |
| Channel product distribution strategy and pricing architecture | file 1.7 §1, file 0.2; lab 1.1 | `channel_pnl` and `margin_waterfall` | N6, N7 | Show that the same headline margin gives very different net contribution by channel, and price the net |
| Competitor monitoring and market intelligence processes | file 1.5, file 1.7 §5; lab 1.4 | `competitive_index` and `competitor_sensitivity` in `engine/aop_scenario.py` | N8 | Tell a promotional move from a structural one, and quantify the revenue hit from a price war |
| Product and channel pricing modelling and scenario analysis | file 3.2, file 3.3 §3; lab 3.1 | `run_scenarios` and `revenue_bridge` | N11 | Flex a plan under a standard scenario set and attribute the change to volume, margin, competitor and mix |
| AOP modelling for the pricing revenue lines | file 3.1, file 3.2, file 3.3 §3; lab 3.1 | `revenue_lines` in `engine/aop_scenario.py` | N5, N11 | Build an annual number by revenue line and channel, and say which part of the modelled effect you would plan |
| Pricing strategy support for Postmasters and the Post Office network | file 0.2 (the Postmaster layer), file 1.7 §1 | The `post_office` channel in `engine/travel_money_simulator.py` | N8 | Explain the two-layer payaway, quote the April 2026 changes (55% minimum share, £5 per card), and say why a decision that helps group profit can still hurt one side of the partnership |
| FCA Consumer Duty fair value compliance for all pricing activity | files 4.1, 4.2, file 3.3 §4; lab 4.1 | `engine/fair_value.py` and the generated assessment | N6, N9 | Run a price against value assessment by customer group to the FCA's 2024 standard, and name the remediation |
| Pricing expertise and modelling support to product, commercial and finance | files 3.2, 3.4 | `engine/pricing_charts.py` and `engine/db_helper.py` | Every sixty second answer | Give the headline, the reading and the caveat for each of the eight board charts |

## Business area responsibilities

| The job says | Taught in | Proved by | Tick when you can |
|---|---|---|---|
| Lead the TMC roadmap and migration project for prepaid cards | file 0.4 | Not proved by code. The file gives the parts of a card programme, the pricing decisions inside a migration and the vendor KPIs | Describe the commercial workstream of a processor migration, the fee schedule review it triggers, and the five questions you would ask in week one |
| Own the P&L for TMC: new card sales, reloads, in-life revenue | file 0.4, file 3.1 | `revenue_lines` in `engine/aop_scenario.py`; the card portfolio and `engine/fair_value.py` | Name the three lines with their drivers, define active card and revenue per active card, and bridge a month against plan |
| Primary liaison between internal teams, legal, finance and external vendors | file 3.2 §2 to §4, file 3.4, file 0.4 | The sixty second answers | Run a weekly status in the same shape every time, and raise a risk before it becomes an issue |
| Compliance and risk management through the procurement process | file 0.4, file 3.3 §5 | The procurement points in file 0.4 | Say what an e-money institution owes on an outsourced critical supplier: due diligence, resilience, exit plan, Compliance in the room from the start |

## Skills

| The job asks for | Taught in | Proved by | Tick when you can |
|---|---|---|---|
| Pricing strategy, yield management, revenue optimisation | files 1.6, 1.7 §4; labs 1.3, 1.5 | `engine/dynamic_pricing.py` (Lerner rule, surge, bandits) | Derive the optimal margin from an elasticity, and explain the shadow price on a volume target |
| Building pricing models, elasticity analyses, margin scenarios | labs 1.2, 2.3, 2.5, 3.1 | The four engine models | Estimate, then check against `data/truth.json`, and say how far off you were |
| Designing and executing pricing tests and evaluating commercial outcomes | files 2.2, 2.3; labs 2.2, 2.4 | Lab 2.4 on the real A/B test in the data | Size a test, pick the metric, and explain why a permanent holdout is worth its cost |
| Distribution economics across retail, digital and agency channels | file 1.7 §1; lab 1.1 | `channel_pnl` | Read a margin waterfall out loud |
| Modelling and optimising multi-channel distribution arrangements | file 1.7 §1; the omnichannel lab | `channel_positioning` | Say what one rate across channels would cost and how you would test it |
| Postmaster or franchise-style distribution economics | file 0.2 | The Post Office commission in the simulator | Say what a payaway change does to the optimal branch margin and to the acquisition cost of a card |
| FCA Consumer Duty and fair value assessments for prepaid products | files 4.1, 4.2 | `generate_fair_value_assessment` | Write the assessment a compliance reviewer would accept |
| Regulatory pricing justifications and fair value documentation | file 4.2, file 0.2 (the FCA review) | The generated document | Explain why benchmarking alone fails the FCA's standard |
| Competition law and pricing governance | file 3.3 §4 and §5, file 1.7 §4 | Guardrails in `engine/dynamic_pricing.py` | Name the information exchange and resale price maintenance risks in a channel pricing design |
| Data modelling, Python, scenario analysis, visualisation | Every lab | The engine and the labs | Run the whole track from a clean checkout |
| SQL | [database usage](../appendix/database_usage.md), [SQL drills](../appendix/sql_learning_questions.md) | `engine/db_helper.py` | Write the eight commercial queries without looking |
| Excel financial modelling and BI tools (Power BI, Tableau) | Not built here, on purpose | The tables `db_helper.py` returns are tidy and warehouse shaped | Load `data/meridian.db` into Excel or Power BI and rebuild the P&L chart from `pricing_charts.py`. One evening, and it closes the gap honestly |
| R | Not covered | | Say so plainly; the methods transfer |
| Translating complex pricing models into clear commercial recommendations | files 3.2, 3.4; every panel notebook | The recommendation columns in the engine output | End every analysis with a decision, a downside and a way back |

## People

| The job says | Taught in | Tick when you can |
|---|---|---|
| Manage key internal and external stakeholders | file 3.2 §2 to §4, file 3.4 | Name each stakeholder's target and what your recommendation does to it before you present |
| Communicate risk, issues and status on a regular basis | file 0.4 (the RAID log and status cadence) | Keep a RAID log current and give a status update in the same shape every week |
| One direct report, the Manager, Pricing, Distribution & Revenue | file 3.3 §1 and §7 | Describe your first month with them: the metric dictionary, a review standard for any number that leaves the team, one project they own end to end |

## Ideal candidate profile and attributes

| The profile wants | Where it is covered | Tick when you can |
|---|---|---|
| Familiarity with financial technologies, platforms and providers in the prepaid and FX sector | file 0.2, file 0.4 | Name the parts of a card programme and the main UK travel money players, including the 2025 consolidation |
| Developing KPIs and performance metrics for vendor management | file 0.4 (the vendor scorecard) | Propose a processor scorecard and say which line matters most to revenue |
| Working with card processing schemes to create or migrate products | file 0.4 | Not something the folder can give you. Be honest about it, then show the shape of the work |
| Strategic: devise and execute a strategy, inspire others to own and deliver | The omnichannel proposal in the panel folder | Tell it as a story about sequencing and about getting others to own the pieces |
| Commercial awareness: management information in decision making, systems administration | file 3.3 §5 and §6 | Say what you would own in the rate engine and the price book: access, versioning, reversal |

## What this map does not cover

R is listed in the profile and is not taught here. Everything in the track is Python,
and the methods transfer. Excel and BI are pointed at rather than built. And the
migration is described, not done: the honest answer in the room is the plan and the
questions, not a claim.

The panel notebooks and the case study are built on simulated data. The skills are
real; the numbers are illustrative. See the honesty rule in the track README.
