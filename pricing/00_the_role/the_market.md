# 0.2 · Travel Money & Prepaid — the domain deep-dive

The real product, economics, players and rules of UK travel money and prepaid FX
cards, grounded in public sources as of September 2026. Figures are quoted as the
sources give them and should be checked before you say them in the room. The
[sources](#sources) are listed at the end.

## First Rate Exchange Services in facts

First Rate began in 1994 when Bank of Ireland started supplying foreign exchange to
the Post Office. It pioneered 0% commission for consumers in 2001, and became a
formal 50/50 joint venture between Post Office and Bank of Ireland in 2002. When the
two partners ended their Post Office branded loans and mortgages in December 2023,
they extended the wider financial services partnership to 2031 and said the foreign
exchange joint venture continues under the same terms and remains the largest
provider of consumer foreign exchange in the UK.

The company is an authorised electronic money institution regulated by the FCA
(reference 900412), a money service business supervised by HMRC, and since 2016 a
principal member of Mastercard, which is why it issues the Travel Money Card itself
rather than through a bank. It moved to a new head office at Botanica, Datchet in
2025 and rebranded. Companies House number 04287490; the latest accounts are made up
to 31 March 2026, and reading them is a sensible evening before the interview.

First Rate describes itself as a wholesale provider to financial services, travel
and retail companies as well as the Post Office's partner. It names TUI, John Lewis
Finance, Hays Travel and Jersey Post among its partners, acquired American Express
Wholesale Currency Services in 2017, and says that one in four outbound travellers
leaving the UK with foreign currency are supplied by First Rate. It offers over 60
currencies.

## The products

**Foreign currency cash** is sold in Post Office branches, online for home delivery
(since 2006), and online for collection in branch, which launched in 2014 and now
offers same-day collection at around 3,000 branches, with main currencies available
in as little as two hours. First Rate says the online service supports over 500,000
foreign currency transactions a year. The price is the FX margin, the gap between the
wholesale rate and the rate on the board.

**The Travel Money Card** is the prepaid multi-currency Mastercard, holding up to
about 22 currencies, managed in an app with Apple Pay and Google Pay. Revenue comes
across the card's life rather than from one sale. In the role profile this product is
what **TMC** means, and [file 0.4](the_card_and_the_migration.md) is devoted to it.

**Wholesale supply** to partner brands, who retail currency under their own name at
their own prices. Contracted, negotiated, and usually indexed to the wholesale rate.

Adjacent to all three sit the fintech travel cards and app-based FX from Wise,
Revolut, Monzo and Starling, with low or transparent margins.

## The revenue model

Cash earns FX margin, and where offered a delivery fee. The card earns FX margin on
loads and reloads, a sterling top-up fee, a cross-border fee in unsupported
currencies, ATM fees, interchange on purchases, inactivity fees on dormant balances,
and breakage on balances never spent. Its P&L splits into new card sales, reloads and
in-life revenue, each with its own margin, growth and risk, and each of those is a
line the role owns. Wholesale earns a contracted margin per unit of currency
supplied.

## Why FX margin is a hard price to set

Customers find it hard to compare spreads, unlike a stated fee, so this is where the
margin lives and also where conduct risk concentrates. At the same time the
reference rate is public: anyone can see the interbank rate on their phone, so the
spread is benchmarkable by anyone who cares to look, and the digital channel is
elastic for exactly that reason. Margin tends to be pushed up in peak season, when
demand is already high, so a naive elasticity estimate is badly biased
([file 1.3](../01_set_the_rate/03_elasticity.md) §6). And the wholesale cost moves
every day, which is a natural instrument for identification and the reason wholesale
contracts are indexed.

## The channels and their economics

| Channel | Character | Elasticity in the case study | Economics |
|---|---|---|---|
| Post Office branches, over 11,500 of them, 97% run by postmasters on an agency or franchise basis | The biggest retail network in the UK; walk-in, trusted, convenience | Inelastic, about minus 1.0 | The network is paid a share of income, so the biggest gross channel is a middling net one |
| Directly managed branches | Same counter, different cost structure | Moderate, about minus 1.3 | High cost to serve: rent, cash handling, staff |
| Online: home delivery and click and collect | Price-transparent, self-serve, the rate is compared in another tab | Most elastic, about minus 2.2 | Low cost to serve; compete hard |
| Agency partners such as travel agents | Currency bundled with the holiday | Fairly inelastic, about minus 1.2 | Agency payaway; cross-sell |
| Wholesale partners who retail under their own brand | Contracted, negotiated, indexed | Least elastic, about minus 0.7 | The partner sets the consumer price; First Rate earns a contracted margin |

The elasticities are the simulator's, not First Rate's. The mapping of the engine's
`retail` and `post_office` channels onto directly managed and postmaster-run
branches is illustrative; the point it makes is real, that the same FX margin earns
very different net contribution depending on who is paid to sell it.

## The Postmaster layer

The payaway has two layers. First Rate pays the Post Office for distribution through
the network, on terms that are not public. The Post Office then pays postmasters.
The second layer changed in April 2026: banking and travel products now deliver a
minimum 55% revenue share to postmasters, the commission on a Travel Money Card
sold in branch rose from 40p to £5 for all branches, and the Post Office has said it
aims to increase postmaster remuneration by £250 million by 2030. The engine's
assumption of 45% paid away on the Post Office channel is an illustration of the
first layer, not a fact about it.

Two consequences for pricing. The network now has a much stronger incentive to sell
cards, so card volume from branches is likely to rise and the acquisition cost of a
branch-sold card has risen with it. And any margin move on the branch channel is a
move in the postmasters' income, which makes the Post Office both a shareholder and
a stakeholder with its own arithmetic ([file 1.7](../01_set_the_rate/07_channels_promotions_revenue_management.md) §1
treats partner commission as a two-sided lever).

## The competitors and the 2025 consolidation

Travelex remains the other national specialist. The supermarkets sell currency in
store and online, often with loyalty-scheme rates: Tesco, M&S, Asda. No1 Currency
has a large store estate. Two 2025 transactions reshaped the high street. Western
Union completed its purchase of eurochange in April 2025 for about £60 million,
bringing roughly 230 stores into a global remittance group. Sainsbury's Bank
announced in July 2025 the sale of its travel money business to Fexco Group, which
will run the 220 or so bureaux under the Sainsbury's brand; the estate was described
as almost 10% of the UK market. Fexco's Irish currency business is also listed as a
First Rate wholesale client since 2022, a reminder that partners and competitors
overlap in this market.

The structural threat is the fintechs. Wise charges an explicit fee on the mid-market
rate; Revolut, Monzo and Starling offer near-interbank spending within limits. They
move the market towards transparent, near-zero FX margin, which squeezes the spread
model. The defence is convenience, cash access, network reach, bundling and trust,
serving the less price-sensitive segments well, and possibly a transparent or
subscription tier for the price-sensitive
([file 1.6](../01_set_the_rate/06_strategy_and_offer_design.md) §8).

The market is still growing. Mintel's 2025 report puts UK consumer spending on
overseas holidays at £59.8 billion in 2025, up around 12%, and says cash remains the
most popular spending method among UK holidaymakers abroad, especially older ones,
with cards preferred for larger purchases.

Directional market levels to quote as directional, from the
[master prompt](../../interview/FRES_MASTER_PREP_PROMPT.md): high street rates a
few percent below interbank on major currencies; online typically beats branch
walk-up by 1 to 3%; buyback markedly worse than sell; airport worse again.

## The regulatory frame

The FCA Consumer Duty applies to First Rate as an e-money institution, and the price
and value outcome is the one that binds on pricing: a firm has to show that the
total price over the life of a product is reasonable against the benefits, and to
show it for groups of customers, with particular attention to vulnerable customers.
The FCA's multi-firm review of Consumer Duty in payments firms, published on 9
October 2024, found that many fair value assessments relied on benchmarking prices
against competitors rather than analysing costs and benefits, that several did not
clearly conclude whether fair value was being delivered, and that firms with tiered
pricing often did not analyse how different fee arrangements affected different
customer groups. Good practice had clear conclusions, analysis by customer group,
consideration of non-financial benefits such as customer support, and documented
remediation. That is the standard [file 4.2](../04_satisfy_the_regulator/02_fair_value_assessment.md)
is built to meet.

E-money and payments rules sit underneath: the Electronic Money Regulations 2011,
including safeguarding of customer funds, and the Payment Services Regulations 2017.
Consumer protection law requires all-in pricing to be clear, with no drip-revealed
margins and genuine rate claims. Competition law, including the rules on information
exchange and resale price maintenance, is in
[file 3.3](../03_defend_the_plan/03_operating_model_and_governance.md) §4.

## The senior pricing agenda for this business

Estimate channel FX margin elasticity causally, with cost-shock instruments and
regional tests, and refresh it on a cadence. Price the net contribution per channel:
harvest where demand is inelastic, compete where it is elastic. Defend the spread
against the fintechs through differentiation, segmentation, bundling and possibly a
transparent tier. Run the fair value process to the FCA's 2024 standard: total
lifecycle cost, customer groups, vulnerable outcomes, inactivity fee remediation,
annual governance. Own the AOP by revenue line and channel with elasticity-consistent
scenarios and a bridge Finance can follow. And, specific to this role, own the card's
three revenue lines through the migration without letting the fee schedule drift
away from fair value ([file 0.4](the_card_and_the_migration.md)).

## Connecting to the case study

Realised in code in [the engine](../engine/README.md): `travel_money_simulator.py`
(five channels including the Post Office network and wholesale partners, FX margin,
the card lifecycle, competitors), `elasticity_models.py` (causal channel
elasticity), `distribution_economics.py` (channel net economics and margin support),
`fair_value.py` (Consumer Duty) and `aop_scenario.py` (plan, scenarios, competitor
index). See [file 0.1](the_job_and_the_evidence.md) for the map to the role profile.

## Red flags

One FX margin across channels with very different elasticity and economics. Ranking
the Post Office channel on gross revenue while the payaway hides the net. Inactivity
or breakage revenue with no fair value justification. Ignoring the fintech spread
squeeze until the margin has already gone. Wholesale contracts with no FX index.
Treating TMC as anything other than the card.

## Check yourself

Try these before you look at the answers below.

1. Name the three revenue lines the card is planned on, and the fee that is the
   textbook Consumer Duty harm.
2. Why is the online channel the most price sensitive and the wholesale channel the
   least?
3. The Post Office channel has the highest gross FX revenue. Why is it not the best
   channel by contribution, and what changed in April 2026?

**Answers.** (1) New card sales, reloads, and in-life revenue. The harm is the
inactivity fee that erodes balances customers have forgotten, which shows up as
breakage. (2) Online customers can see the interbank rate, compare in another tab
and switch at no cost. Wholesale partners buy on a contract indexed to the wholesale
rate and set their own consumer prices, so First Rate's rate board is not what
decides their volume. (3) A share of the channel's income is paid away to the
network, so net contribution is middling even though gross is the largest. From
April 2026 postmasters receive at least 55% of travel product income and £5 per card
sold, which strengthens the network's incentive to sell and raises the acquisition
cost of a branch-sold card.

## Sources

[First Rate Exchange Services, front page](https://www.firstrate.co.uk/), for
ownership, regulatory references, partners, the one in four claim and the currency
count.
[First Rate, our history](https://www.firstrate.co.uk/about-us/history/), for the
timeline from 1994 to the 2025 move to Botanica.
[First Rate, Post Office Travel Money Online](https://www.firstrate.co.uk/post-office-travel-money-online/),
for the 2006 launch, click and collect, branch count and transaction volume.
[First Rate, the Travel Money Card](https://www.firstrate.co.uk/post-office-travel-money-card/),
for the card's evolution, usage claim and awards.
[Companies House, company 04287490](https://find-and-update.company-information.service.gov.uk/company/04287490).
[Post Office, December 2023, partnership with Bank of Ireland extended](https://corporate.postoffice.co.uk/blogs/2023_12/post-office-extends-financial-services-partnership-with-bank-of-ireland-with-flexibility-to-strike-new-deals-with-other-financial-providers/),
for the 50/50 joint venture continuing on the same terms and the largest provider claim.
[Post Office, April 2026, remuneration uplift for postmasters](https://www.mynewsdesk.com/uk/post-office/pressreleases/post-office-confirms-major-remuneration-uplift-for-postmasters-from-april-2026-3443592),
for the 55% share, the £5 card commission, the £250 million by 2030 and the network figures.
[FCA, Payments Consumer Duty multi-firm review, 9 October 2024](https://www.fca.org.uk/publications/multi-firm-reviews/payments-consumer-duty).
[Western Union acquires eurochange, April 2025](https://www.businesswire.com/news/home/20250408366869/en/Corsair-Completes-Sale-of-eurochange-to-The-Western-Union-Company-Finalizes-Exit-from-NoteMachine).
[Sainsbury's Bank sells travel money business to Fexco Group, 30 July 2025](https://corporate.sainsburys.co.uk/news/press-releases/sainsbury-s-bank-announces-sale-of-travel-money-business-to-fexco-group/).
[Mintel, UK Travel Money Market Report 2025](https://store.mintel.com/report/uk-travel-money-market-report).
Card fees as reported by [Exiap](https://exiap.co.uk/reviews/post-office-travel-card)
and [Wise](https://wise.com/gb/blog/best-prepaid-travel-card-with-no-fees); the
authoritative table is Section 11 of the card terms linked from
[postoffice.travelmoneyonline.co.uk](https://postoffice.travelmoneyonline.co.uk/terms-and-conditions/).
