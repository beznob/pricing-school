# 04 · Satisfy the regulator

Charging different people different prices is normal and useful. It is also watched.
Under the FCA Consumer Duty a firm has to show that the price a customer paid was
reasonable against the benefit they received, and to show it for groups of customers
rather than only on average. This stage is how you evidence that.

Steps are numbered as in the [track](../README.md). This stage comes before stage 3
in the sequence, because the competition and operating model labs build on the
fairness lab here.

## The steps

| Step | Do this | What it teaches | Done when you can |
|---|---|---|---|
| 24 | Read [4.1 Segments and fairness](01_segments_and_fairness.md) | Segments, differential pricing and where the fairness line sits, the check that passes while the harm is real, the captive customer | Describe the fairness check that passes while the harm is real |
| 25 | Run [lab 4.1](lab_01_segmentation_and_fairness.ipynb) | Price discrimination and fences, Simpson's paradox, a fairness audit that finds a real age gap, Consumer Duty, the cost of a policy cap | Run a fairness audit and cost a cap |
| 26 | Read [4.2 Fair value assessment](02_fair_value_assessment.md), then regenerate it with `python ../engine/fair_value.py` | A worked price against value assessment for the prepaid card, with differential outcome testing for vulnerable customers and the remediation that follows | Explain the assessment to a compliance colleague, including what you would change |

Then loop back to [stage 1](../01_set_the_rate/) for step 27, lab 1.4.

File 4.2 is generated, not written by hand. `run_role_case_study.py` regenerates it
too. Competition law and the governance cycle that sits around this work are in §4
and §5 of [file 3.3](../03_defend_the_plan/03_operating_model_and_governance.md).

## The trap worth memorising

A fairness check run inside each channel can pass everywhere and still hide real
harm, because the mix of customers differs between channels. In the worked portfolio
the vulnerable customer premium is invisible within channels and is 1.33 percentage
points once you look across them. The same arithmetic that moves profit through mix
in [file 1.4](../01_set_the_rate/04_price_volume_mix_and_leakage.md) quietly moves
who pays. Panel notebook N6 is the interview-grade version.

## Where the ideas go

Regulation also constrains how you learn. Once a model sets prices you still need
variation to keep identifying elasticity, and an unconstrained bandit is not
defensible to a regulator. Panel notebook N9 works the safe exploration problem and
shows a fee corridor that costs little and out-learns the unconstrained version.
