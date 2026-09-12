# 0.4 · The Travel Money Card, its P&L and the migration

The role profile gives this job two responsibilities the rest of the track does not
cover: own the P&L for the Travel Money Card, and lead the card's roadmap and
migration project. This file is the commercial view of both. It is written from
public sources and from how card programmes generally work, because First Rate has
not published details of the migration. Treat the specifics as things to confirm in
week one, not things to assert in the interview.

## What the card is

The Post Office Travel Money Card is a prepaid Mastercard issued by First Rate
Exchange Services, which has been a principal member of Mastercard and an authorised
e-money institution since 2016. It launched in 2006 as a blank card sold only in
branch and is now a multi-currency product holding up to about 22 currencies, with
an app for loading and managing balances and support for Apple Pay and Google Pay.
First Rate says it is used for a purchase every 1.5 seconds across 197 countries and
territories, and it won Best Prepaid Card at the Card & Payments Awards in 2012,
2020 and 2025.

The fee shape, as reported by comparison sites (the official fee table is Section 11
of the card terms on the Post Office travel money site, and you should read that
version before quoting any number): no fee to spend in a currency you hold; a 3%
charge when the card is used in a currency you do not hold; a per-withdrawal ATM fee
that varies by currency, on the order of £1.50 or €2; a 1.5% fee on sterling
top-ups with a minimum of £3 and a maximum of £50; a £2 monthly inactivity fee
after twelve months without use; and a closure fee. Load limits reported are a £50
minimum, £5,000 per transaction, £10,000 balance and £30,000 a year.

That structure is the whole pricing problem in miniature. The visible price is the
exchange rate on the load. The margin also lives in the cross-border fee, the ATM
fee and, most sensitively, the inactivity fee on balances customers forgot. The
customer sees the rate; the regulator sees the total cost over the life of the card.

## The P&L you would own

The profile names the three revenue lines, and each has its own driver.

**New card sales.** Cards sold, times the FX margin on the first load, less what it
costs to put a card in a hand: the card itself from the manufacturing bureau, the
KYC check, fulfilment, and from April 2026 a £5 commission to the postmaster for
every card sold in a Post Office branch, up from 40p. That change alone moves the
economics of a branch-sold card and is worth knowing cold.

**Reloads.** Active cards, times reloads per active card, times the FX margin on
each reload, plus the sterling top-up fee where it applies. This is the recurring
engine and the line most sensitive to the rate the customer sees in the app against
what Wise or Revolut show in the next tab.

**In-life revenue.** Spend abroad earns FX margin where the customer converts on the
card, a cross-border fee where they spend in an unsupported currency, ATM fees,
interchange paid by the merchant's bank on every purchase, and inactivity fees on
dormant balances. Breakage, the balances that are never spent, sits here too and is
the line the fair value assessment will look at first.

Below revenue sit the costs a pricing manager has to hold in the same spreadsheet:
scheme fees to Mastercard, the issuer processor's per-card and per-transaction
charges, the bureau's card production and delivery, KYC per applicant, fraud and
chargebacks, customer service, the cost of holding and safeguarding customer money,
and the cost of hedging the currency balances the company is short. Owning the P&L
means a monthly bridge across all of that, by line, against the plan.

Two metrics to define on day one, because most arguments about the card will be
definition disputes: what counts as an active card, and what counts as revenue per
active card. Everything else follows from those two.

## What a migration is

An issuer's card programme has moving parts that are usually supplied by different
companies. The **scheme** (Mastercard) sets the rules and moves the money between
banks. The **issuer processor** runs the accounts: it authorises each transaction in
real time, keeps the balances, applies the fees, handles disputes and produces the
data. The **card bureau** manufactures, personalises and posts the physical cards.
The **KYC partner** checks identity when a card is applied for. The **app and
tokenisation** layer puts the card in Apple Pay and Google Pay. The profile lists an
existing and a current processing partner, the bureaux, the KYC partner and the
scheme as your external relationships, which is the list of parties in a processor
migration.

Companies migrate for a few reasons: the contract is ending, the unit cost per
transaction is too high, the old platform cannot do what the roadmap needs (instant
issuance, better tokenisation, richer data, multi-currency at the scheme level), or
resilience and regulatory expectations have moved. The technical project manager
runs the cutover. The pricing and revenue manager runs the commercial workstream,
and that is the part to be able to describe.

## The pricing decisions inside a migration

**The unit cost model, old against new.** Before anything else, a per-card and
per-transaction cost stack for both processors, because the new platform's pricing
is usually a different shape (a platform fee plus lower per-transaction, or the
reverse). The break-even depends on volume mix, so it runs through the same P&L
above, not through a procurement spreadsheet.

**The fee schedule review.** A migration is the moment fees get looked at, and every
change has to pass fair value. The FCA's October 2024 review of Consumer Duty in
payments firms found that many fair value assessments leaned on benchmarking against
competitors and did not analyse costs, benefits or how different customer groups
were affected. If you change the inactivity fee, the ATM fee or the top-up fee, you
need the reassessment, the customer notice period the terms require, and a view of
who is affected by group. Grandfather where the harm of change outweighs the gain.

**Dormant and expired cards.** A migration has to decide what happens to cards with
balances that have not been used, to cards that expire during the cutover, and to
balances on cards that will not be reissued. Safeguarded customer money moves with
the accounts. The commercial temptation is to let dormancy fees run; the Consumer
Duty answer is to make it easy to get the money back and to say so.

**The cutover risk to revenue.** Declined transactions during and after cutover are
lost FX margin and lost trust. The authorisation approval rate before and after is
the single number to watch, alongside reload volume per active card, which is where
a bad app experience shows up first.

**Postmaster incentives.** Card commission became £5 per card from April 2026. If
the migration changes how a card is sold in branch (instant issue against ordered),
the commission and the branch process move together, and the network needs to hear
about it from you before it happens.

## Vendor KPIs

The profile asks for experience developing KPIs for vendor management. A processor
scorecard a pricing manager would actually use:

| Measure | Why it matters to revenue |
|---|---|
| Authorisation approval rate, by channel and currency | Every wrongful decline is lost margin and a complaint |
| Platform availability and authorisation latency | Downtime at an airport ATM is a customer you do not get back |
| Cost per transaction and per active card, against contract | The migration's business case, tracked monthly |
| Card production lead time and fulfilment accuracy | Cards not in hands before travel do not get loaded |
| KYC pass rate and time to decision | Applicants who drop out at identity checks never become active cards |
| Dispute and chargeback turnaround | Regulatory clock and cost |
| Incident count and time to resolve | Resilience expectations for an e-money institution's critical supplier |
| Data delivery: completeness and timeliness of transaction files | Without it, none of the pricing above can be measured |

Pair each with a commercial KPI for the programme itself: cards in issue, active
cards, load volume, reloads per active card, revenue per active card, dormancy rate
and the fair value red-amber-green by customer group.

## Running the commercial workstream

The profile says communicate risk, issues and status on a regular basis, and act as
the primary liaison between internal teams, legal, finance and external vendors. In
a project that means a RAID log you keep current (risks that might happen, issues
that have, assumptions you are relying on, dependencies on other people), a weekly
status in the same shape every time (on track, at risk, off track, with the one
decision you need), and a habit of raising a risk before it becomes an issue.
Finance needs the business case tracked against actuals. Legal needs the contract
and the customer terms. Compliance needs the fair value reassessment and the
outsourcing paperwork. The vendors need one commercial owner who answers.

The procurement point in the profile is about compliance, not price. An e-money
institution that outsources a critical function stays responsible for it, so the
tender needs due diligence on the supplier's financial strength, security and
resilience, an exit plan, and Risk and Compliance in the room from the first
meeting rather than at sign-off.

## What to ask in week one

Which processor, which scheme products and which BIN ranges are moving, and by
when. What the contract cost shape is on both sides. Whether any customer fee is
changing, and whether a fair value reassessment has been started. How many cards are
dormant with a balance, and what the plan is for them. What the authorisation
approval rate is today, by channel. Who owns the app, and whether tokenisation moves
with the processor. Where the RAID log lives and who chairs the status meeting.

## Check yourself

Try these before you look at the answers below.

1. Name the three revenue lines the profile says you own on the card, and give the
   driver of each.
2. A migration proposal includes raising the inactivity fee from £2 to £3 a month to
   improve the business case. What has to happen before that can go ahead, and what
   would you say to the sponsor?
3. From April 2026 a postmaster earns £5 rather than 40p for each card sold in
   branch. What does that do to the economics of a branch-sold card, and what would
   you check?

**Answers.** (1) New card sales, driven by cards sold and the margin on the first
load. Reloads, driven by active cards and reloads per active card. In-life revenue,
driven by spend abroad, ATM use, cross-border use and dormancy. (2) A fair value
reassessment that looks at cost, benefit and the customers affected by group rather
than at what competitors charge, the customer notice the terms require, and a
Consumer Duty view on whether a fee that mainly falls on customers who have
forgotten a balance can ever be fair value. To the sponsor: the business case
should stand on unit cost and volume, and a fee rise on dormant customers is the
first thing the regulator will ask about. (3) It adds about £4.60 of acquisition
cost to every branch-sold card, so the break-even on a new card moves to the
reloads and in-life lines. Check the expected reloads per card and the dormancy
rate by channel, because a card that is sold and never reloaded is now a loss at
the point of sale.

## Sources

The card and First Rate's history:
[firstrate.co.uk, the Travel Money Card](https://www.firstrate.co.uk/post-office-travel-money-card/) and
[firstrate.co.uk, our history](https://www.firstrate.co.uk/about-us/history/).
Fees as reported by comparison sites, which should be checked against Section 11 of
the card terms on
[postoffice.travelmoneyonline.co.uk](https://postoffice.travelmoneyonline.co.uk/terms-and-conditions/):
[Exiap review](https://exiap.co.uk/reviews/post-office-travel-card) and
[Wise, best prepaid travel cards 2026](https://wise.com/gb/blog/best-prepaid-travel-card-with-no-fees).
Postmaster remuneration from April 2026:
[Post Office press release](https://www.mynewsdesk.com/uk/post-office/pressreleases/post-office-confirms-major-remuneration-uplift-for-postmasters-from-april-2026-3443592).
The FCA's findings on fair value in payments firms:
[Payments Consumer Duty multi-firm review, 9 October 2024](https://www.fca.org.uk/publications/multi-firm-reviews/payments-consumer-duty).
