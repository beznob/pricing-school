# 01 · Set the rate

Deciding what to charge. This stage is the arithmetic and the judgement behind a
number on the rate board.

The steps below are numbered as in the [track](../README.md). The first eight are
done in one pass. The last five come back to this folder after later stages, because
optimising a price needs an honest demand model (stage 2) and the competition lab
needs the fairness lab (stage 4). That is not a detour; it is the order the skills
actually build in.

Every prose file ends with practice questions and answers. Do them before you open
the lab beside it, and in the lab say what number you expect before each cell runs.

## First pass

| Step | Do this | What it teaches | Done when you can |
|---|---|---|---|
| 3 | Read [1.1 Price, cost and profit](01_price_cost_and_profit.md) | Price, cost, contribution, margin, break-even | Explain why a 2% price cut can eat half the profit per sale |
| 4 | Read [1.2 Percentages and basis points](02_percentages_and_basis_points.md) | Percentages against percentage points against basis points, and how an FX spread actually works | Say where the profit hides in "0% commission" |
| 5 | Run [lab 2.1](../02_prove_the_change/lab_01_data_foundation.ipynb), which lives in stage 2 because it is about data grain, but builds the world every lab reads | The Meridian FX dataset and its answer key | The `data/` folder exists and you can say what grain the price is set at |
| 6 | Run [lab 1.1](lab_01_price_cost_and_profit.ipynb) | Margin against markup, the cost taxonomy, the discount break-even, the price waterfall, the price volume mix bridge | Compute the discount break-even and read a waterfall out loud |
| 7 | Read [1.3 Elasticity](03_elasticity.md) | How demand reacts to price, the minus one dividing line, the markup rule | State the dividing line and the markup rule |
| 8 | Run [lab 1.2](lab_02_demand_and_elasticity.ipynb) | Willingness to pay, the demand curve, elasticity and semi-elasticity, the Lerner rule, cross-price effects | Estimate an elasticity and check it against `truth.json` |
| 9 | Read [1.4 Price, volume, mix and leakage](04_price_volume_mix_and_leakage.md) | Why profit moved, and where the price leaks between the board and the till | Split a profit move three ways and name three leaks |
| 10 | Read [1.5 Competition](05_competition.md) | Price wars, and how not to start one | Tell a promotional move from a structural one, and say why never to blanket match |

Then go to [stage 2](../02_prove_the_change/).

## Second pass, after stage 2

| Step | Do this | What it teaches | Done when you can |
|---|---|---|---|
| 20 | Run [lab 1.3](lab_03_price_optimisation.ipynb) | Profit curves, constrained optimisation and shadow prices, promotions and incrementality, the lifetime value correction | Find a profit maximising price and say why a static optimiser is too aggressive |
| 21 | Read [1.6 Strategy and offer design](06_strategy_and_offer_design.md) | The strategy ladder, fences and price discrimination, willingness to pay research, bundling and tiers. Senior reference | Walk the ladder and name three fences |
| 22 | Read [1.7 Channels, promotions and revenue management](07_channels_promotions_revenue_management.md) | Channel net economics, the discount break-even, promotion governance, dynamic pricing guardrails. Senior reference | Price the pocket, not the list, and quote the break-even formula from memory |
| 23 | Run [lab 1.5](lab_05_dynamic_pricing_ladder.ipynb) | Dynamic pricing as one idea plus five upgrades, ending with a sales target as a constraint | Explain the shadow price on a volume target |

Then [stage 4](../04_satisfy_the_regulator/).

## Third pass, after stage 4

| Step | Do this | What it teaches | Done when you can |
|---|---|---|---|
| 27 | Run [lab 1.4](lab_04_competition_and_dynamics.ipynb) | Competitive response and lead lag tests, price wars, bandits, recovering demand that stockouts hid | Test whether a competitor leads or follows, and recover censored demand |

Then [stage 3](../03_defend_the_plan/).

## Where the ideas go

The elasticity you estimate here is only as good as the identification behind it,
and the naive estimate is wrong in a predictable direction. That is stage 2. The
channel economics feed the AOP in stage 3. The production versions of these models
live in [engine](../engine/), which the panel notebooks import rather than
reimplement, and panel notebooks N2, N5, N7 and N8 are the interview-grade versions
of this stage.
