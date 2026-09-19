"""Data for the paper pack. Edit here, then run build_paperpack.py.

Facts are taken from each paper's abstract and, where the paper was reachable, the publisher's full
text, read 18 September 2026. Anything that could
not be confirmed from those sources is marked as a check in the facilitator key, not stated.
"""

# The running order of the day. Each entry is (session number, session title,
# index into a paper's prompts list). The prompts lists below stay in topic
# order, so reordering the day means editing only this table.
SESSIONS = [
    ("1", "Where economic evidence enters policy", 0),
    ("2", "What economic evaluation is", 1),
    ("3", "Framing the question", 4),
    ("4", "Costing your own service", 3),
    ("5", "Outcomes, discounting and the ICER", 5),
    ("6", "Thresholds, opportunity cost, budget impact", 2),
    ("7", "Modelling in half an hour", 6),
    ("8", "Handling uncertainty", 7),
]

PAIRS = [
    (1, 2, "a well-built model with a favourable verdict, against one that concludes 'not cost-effective'"),
    (4, 3, "a conclusion that turns on a health-system assumption, against one that turns on clinical choices"),
    (5, 6, "a paper that is not really a cost-effectiveness analysis, against a technically competent one"),
    (7, 8, "an analysis that ends in a price to negotiate, against one that ends in a cost per DALY"),
]

Q_WHO = "Who funded or commissioned it, and who in India could act on its answer?"
Q_BOX = "Which of Drummond's six boxes is it in? If it is a full evaluation, which of the four types?"
Q_COST = "Where did the costs come from? Bottom up or top down? Whose costs are counted, and whose are not?"
Q_FRAME = "Is the comparator what actually happens now? Are the perspective and time horizon the ones India asks for?"
Q_UNC = "Which kinds of uncertainty were tested, and how? What is the probability that the conclusion is right?"

PAPERS = [
# ---------------------------------------------------------------------------------------------
dict(
 n=1, partner=2, cluster="Oncology and surgery",
 short="Thiagarajan et al. 2026, sentinel node biopsy in early oral cancer",
 authors="Thiagarajan S, Sharda S, Chugh Y, Gupta N, Pramesh CS, Prinja S.",
 title="Sentinel lymph-node biopsy guided neck dissection versus elective neck dissection in the management of early-stage oral cancer: a cost-utility analysis.",
 journal="Cancer Med", vol="2026;15(2):e71571", pmid=41644818, pmcid="PMC12875840",
 doi="10.1002/cam4.71571", oa=True,
 summary=[
  "A <strong>Markov model</strong> follows a hypothetical cohort of patients in India with early oral squamous cell carcinoma, "
  "tracking disease-free survival, recurrence and overall survival. Three strategies are compared: "
  "<strong>sentinel lymph-node biopsy (SLNB) guided neck dissection</strong>; <strong>elective neck dissection (END) alone</strong>; "
  "and <strong>END with frozen section</strong>.",
  "Payer perspective, lifetime horizon, costs and QALYs discounted at 3%. One-way and probabilistic sensitivity analyses.",
  "SLNB costs <strong>INR 5,564</strong> more per patient than END alone and <strong>INR 2,507</strong> more than END with frozen section, "
  "and gains <strong>0.31</strong> and <strong>0.33</strong> QALYs respectively. The reported incremental cost-utility ratios are "
  "<strong>INR 8,088</strong> and <strong>INR 16,709</strong> per QALY. Judged against one times GDP per capita, SLNB has a "
  "<strong>94%</strong> probability of being cost-effective. The authors support its inclusion in the government insurance scheme.",
 ],
 prompts=[
  Q_WHO + " The authors name a specific scheme: which, and what would it need besides this paper?",
  Q_BOX,
  "They judge against <strong>one times GDP per capita</strong>. Would the verdict change against India's own estimate from Session 3?",
  "SLNB needs a gamma probe, a radiotracer and nuclear medicine time. Look for these in the costs. Were capital costs annuitised?",
  Q_FRAME,
  "Divide each incremental cost by its incremental QALYs. Do you get the ratios the paper reports? If not, find out why.",
  "Name the health states. How long is a cycle? Where did the recurrence probabilities come from?",
  Q_UNC,
 ],
 job="The <strong>well-built model</strong>, used to show that a sound analysis can still use a retired threshold rule, and that the abstract's own arithmetic needs checking.",
 grid=[
  ("Decision problem", "Early oral SCC; three neck-management strategies. Clear."),
  ("Comparator", "END alone and END with frozen section. Plausibly current practice in Indian cancer centres; ask the group whether END is what their own hospital does."),
  ("Perspective", "Payer. The Reference Case asks for abridged societal in the base case, with payer reported separately."),
  ("Outcomes", "QALYs. Check which utility source (Indian value set or borrowed)."),
  ("Horizon, discounting", "Lifetime; 3%. Meets the Reference Case."),
  ("Threshold", "One times GDP per capita."),
  ("Uncertainty", "One-way and PSA; 94% probability cost-effective."),
 ],
 teach=[
  "<strong>The threshold rule is wrong in principle but harmless here.</strong> The ratios are a few thousand to under twenty thousand rupees per QALY, "
  "far below GDP per capita and below India's willingness-to-pay estimate of ₹2,12,307 from Session 3. A good group says both things: "
  "the rule is retired, and it does not change this verdict. That is the mature position; the lazy one is to discard the paper for using it.",
  "<strong>The abstract's arithmetic does not reproduce.</strong> 5,564 ÷ 0.31 is about 17,950 and 2,507 ÷ 0.33 is about 7,600, "
  "not 8,088 and 16,709. The ratios look swapped, or computed from differently discounted figures. Send the group to the results table. "
  "Whatever the explanation, the lesson is: always recompute an ICER from the components.",
  "Payer perspective only. Out-of-pocket costs for travel to a centre with nuclear medicine may differ between strategies.",
 ],
 check="Open the full text and confirm (a) which utility weights were used and (b) the explanation for the ICER arithmetic, so the facilitator can answer when the group asks.",
),
# ---------------------------------------------------------------------------------------------
dict(
 n=2, partner=1, cluster="Oncology and surgery",
 short="Guleria et al. 2025, laparoscopic IPOM for ventral hernia",
 authors="Guleria C, Kumar D, Sahoo KC.",
 title="Review for cost-effectiveness analysis of laparoscopic Intra-peritoneal Onlay Mesh for ventral hernia repair in Indian settings.",
 journal="Cost Eff Resour Alloc", vol="2025;23(1):27", pmid=40495189, pmcid="",
 doi="10.1186/s12962-025-00638-4", oa=True,
 summary=[
  "A <strong>systematic review and meta-analysis of 10 randomised trials</strong> (1,204 patients) comparing "
  "<strong>laparoscopic intra-peritoneal onlay mesh (IPOM)</strong> repair with <strong>open ventral hernia repair</strong>, "
  "combined with a cost-effectiveness analysis from the <strong>Indian health system perspective</strong> over five years. "
  "Costs come from the National Health System Cost Database.",
  "Hernia recurrence, the primary outcome, did not differ (risk ratio <strong>1.28</strong>, 95% CI 0.81 to 2.04). "
  "Wound infection was lower with the laparoscopic repair (risk ratio <strong>0.31</strong>, 0.18 to 0.54).",
  "The ICER is <strong>INR 5,023 per wound infection averted</strong>, set against a threshold of <strong>INR 2,14,000</strong> "
  "based on India's per-capita income. In a probabilistic analysis of 10,000 simulations the laparoscopic repair was cost-effective in "
  "<strong>54.0%</strong>. The authors conclude it is not clinically effective for recurrence and less likely to be cost-effective.",
 ],
 prompts=[
  Q_WHO + " Look at the authors' affiliations.",
  Q_BOX,
  "The threshold is per-capita income. What unit of health is that threshold meant to buy? Is it the unit in this paper's ICER?",
  Q_COST,
  Q_FRAME + " Is five years long enough for hernia recurrence?",
  "The primary outcome was recurrence. Which outcome is in the ICER? Why might that choice matter?",
  "Is there a model at all, or is this a calculation on pooled trial results? Does it need one?",
  "54% of simulations favoured the laparoscopic repair. The authors call it 'less likely to be cost-effective'. Do you agree?",
 ],
 job="The paper that concludes <strong>not cost-effective</strong>, which is rare in print, and a clean example of a natural-unit ICER that cannot be judged against a per-QALY threshold.",
 grid=[
  ("Decision problem", "Laparoscopic IPOM vs open repair for ventral hernia, Indian health system."),
  ("Comparator", "Open repair. Probably still current practice in most public hospitals."),
  ("Effectiveness", "Meta-analysis of 10 RCTs. The strongest evidence source in the pack."),
  ("Costs", "NHSCD. Health system only; no out-of-pocket."),
  ("Outcomes", "Natural units: recurrence (primary), wound infection. No QALYs."),
  ("Horizon, discounting", "Five years. We could not find a discount rate on our read; ask the group to look."),
  ("Threshold", "INR 2,14,000, per-capita income."),
  ("Uncertainty", "PSA, 10,000 simulations; 54.0% cost-effective."),
 ],
 teach=[
  "<strong>Unit mismatch.</strong> A per-capita-income threshold is a (retired) rule of thumb for cost per DALY or QALY. "
  "Comparing <em>rupees per wound infection averted</em> against it has no meaning. A natural-unit ICER cannot enter a league table or meet a threshold.",
  "<strong>Outcome choice.</strong> Recurrence was primary and showed no difference; the ICER is built on a secondary outcome that did. "
  "Not necessarily wrong, but it must be justified, and the group should notice it.",
  "<strong>54% is a coin toss.</strong> 'Less likely to be cost-effective' is not what 54% says. The honest reading: the analysis cannot tell. "
  "Which fits Session 8's point that a probability of being cost-effective is not the probability of being right.",
  "A rare published negative. Ask the room how many 'not cost-effective' Indian evaluations they have read. Publication bias exists here too.",
 ],
 check="The handover describes this as an HTAIn study. On our read the paper mentions HTAIn and one author is at the Department of Health Research, but we did not confirm it was commissioned through HTAIn. Say 'HTAIn-linked' only if the full text confirms it.",
),
# ---------------------------------------------------------------------------------------------
dict(
 n=3, partner=4, cluster="Cardiology and medicine",
 short="Uy et al. 2021, surgery for rheumatic mitral valve disease",
 authors="Uy J, Ketkar AG, Portnoy A, Kim JJ.",
 title="Cost-utility analysis of heart surgeries for young adults with severe rheumatic mitral valve disease in India.",
 journal="Int J Cardiol", vol="2021;338:50-57", pmid=34090957, pmcid="",
 doi="10.1016/j.ijcard.2021.05.059", oa=False,
 summary=[
  "A <strong>Markov model</strong> of a hypothetical cohort of <strong>20-year-olds</strong> in India with severe rheumatic mitral valve disease, "
  "from an <strong>Indian public payer perspective</strong>, estimating lifetime costs and QALYs.",
  "Three strategies: <strong>valve repair</strong>; <strong>mechanical valve replacement</strong>; <strong>bioprosthetic valve replacement</strong>. "
  "The comparator is a <strong>standard-of-care mix</strong> approximating Indian practice: 32% repair, 33% mechanical, 35% bioprosthetic.",
  "Results per patient (US dollars): repair <strong>$2,530, 9.7 QALYs</strong>; standard of care <strong>$2,990, 8.7 QALYs</strong>; "
  "mechanical <strong>$3,220, 6.2 QALYs</strong>; bioprosthetic <strong>$3,190, 10.1 QALYs</strong>.",
  "Repair is cheaper and more effective than both standard of care and mechanical replacement. Bioprosthetic replacement against repair costs "
  "<strong>$1,590 per QALY</strong>, which the authors say may be cost-effective against India's GDP per capita ($2,005). They conclude that repair "
  "is optimal, mechanical replacement should not be recommended for this group, and bioprosthetic replacement may be cost-effective where repair "
  "quality is not assured, newer valves are used, or valve prices fall.",
 ],
 prompts=[
  Q_WHO + " Where are the authors based?",
  Q_BOX,
  "Against what threshold is repair 'optimal' rather than bioprosthetic replacement? Try India's own estimate from Session 3.",
  "Costs are in US dollars. What would you want to know about the conversion and the cost year?",
  Q_FRAME + " Is a 'standard-of-care mix' a real comparator?",
  "Put the four strategies in order of QALYs. Which are dominated? Recompute the bioprosthetic vs repair ratio.",
  "A Markov model over a lifetime from age 20. What has to be assumed about valve durability and re-operation?",
  "The abstract does not describe the sensitivity analyses. What would you most want tested?",
 ],
 job="The <strong>clinically driven</strong> conclusion: the answer turns on which operation is chosen, and repair dominates current practice, yet current practice has not moved.",
 grid=[
  ("Decision problem", "Young adults, severe RMVD, choice of operation. Clear and clinically framed."),
  ("Comparator", "A modelled practice mix (32/33/35). Defensible, but its source should be checked."),
  ("Perspective", "Indian public payer only."),
  ("Outcomes", "QALYs, lifetime."),
  ("Costs", "Reported in US dollars."),
  ("Threshold", "India's GDP per capita, $2,005."),
  ("Uncertainty", "Not described in the abstract. The planning notes list one-way and probabilistic analysis; confirm."),
 ],
 teach=[
  "<strong>Dominance is not the whole answer.</strong> Repair dominates standard of care and mechanical replacement. But bioprosthetic replacement "
  "gains 0.4 QALY more than repair at $1,590 per QALY. So 'repair is optimal' holds only if the threshold is below $1,590. "
  "At the GDP rule the authors cite, bioprosthetic would be preferred. The conclusion depends on a threshold the abstract leaves ambiguous. A good group spots this.",
  "Check the arithmetic: $660 ÷ 0.4 QALY is $1,650, close to the reported $1,590 once QALYs are unrounded.",
  "<strong>The practice gap.</strong> If repair dominates, why do centres not do it? Surgical skill, learning curve, durability in rheumatic valves, "
  "follow-up access. These are real constraints the model may not carry; the ICER does not tell a surgeon how to acquire the skill.",
  "Mechanical valves at 6.2 QALYs: ask what drives that. Anticoagulation monitoring in young Indian adults, probably. A structural assumption worth naming.",
 ],
 check="This paper is not open access and the abstract does not describe the sensitivity analysis. If anyone on the faculty has access, confirm what uncertainty analysis was done and the cost year before the report-back.",
),
# ---------------------------------------------------------------------------------------------
dict(
 n=4, partner=3, cluster="Cardiology and medicine",
 short="Kaur et al. 2022, population screening for diabetes and hypertension",
 authors="Kaur G, Chauhan AS, Prinja S, Teerawattananon Y, Muniyandi M, Rastogi A, Jyani G, Nagarajan K, Lakshmi P, Gupta A, Selvam JM, Bhansali A, Jain S.",
 title="Cost-effectiveness of population-based screening for diabetes and hypertension in India: an economic modelling study.",
 journal="Lancet Public Health", vol="2022;7(1):e65-e73", pmid=34774219, pmcid="",
 doi="10.1016/S2468-2667(21)00199-7", oa=True,
 summary=[
  "A <strong>hybrid decision tree and Markov model</strong> of a cohort aged 30, over a <strong>lifetime</strong>, from a <strong>societal perspective</strong> "
  "that includes health-system and out-of-pocket costs, discounted at 3%. Population-based screening at different ages, frequencies and tests is compared "
  "with <strong>current practice</strong>, where diabetes and hypertension are detected opportunistically.",
  "Costs come from primary data in Haryana and Tamil Nadu, the National Health System Cost Database, the Costing of Health Services in India study, "
  "national survey data and insurance package rates. Quality of life was measured with <strong>EQ-5D-5L in 962 patients</strong>. Funded by the "
  "Department of Health Research.",
  "Judged against one times GDP per capita, <strong>no screening strategy was cost-effective at current levels of health-care use</strong>; even screening "
  "once in 20 years had only a 60% probability. But if <strong>20%</strong> of newly diagnosed patients were treated through Health and Wellness Centres, "
  "screening people aged 30 to 65 every three or five years became cost-effective, and at <strong>70%</strong> annual screening became cost saving.",
 ],
 prompts=[
  Q_WHO,
  Q_BOX,
  "Which threshold? And the programme is population-wide: what would its budget impact be, and does the paper say?",
  "This paper collected its own cost and quality-of-life data. What did that buy that a database could not?",
  Q_FRAME,
  "Find the ICER for one strategy you think is realistic. Is the utility weight from the Indian value set?",
  "Why a decision tree <em>and</em> a Markov model? What does each part do?",
  "The verdict flips on one number. Which is it, and is it clinical?",
 ],
 job="The <strong>best paper in the pack</strong> for showing where an ICER really comes from: the conclusion flips on a health-system assumption, not a clinical one.",
 grid=[
  ("Decision problem", "Population screening for diabetes and hypertension: ages, frequencies, tests. Carefully specified."),
  ("Comparator", "Current opportunistic detection. Exactly what the Reference Case asks for."),
  ("Perspective", "Societal, including out-of-pocket."),
  ("Costs", "Primary Indian data plus NHSCD, CHSI, national survey, package rates."),
  ("Outcomes", "QALYs, EQ-5D-5L in 962 Indian patients."),
  ("Horizon, discounting", "Lifetime from 30; 3%."),
  ("Threshold", "One times GDP per capita."),
  ("Uncertainty", "PSA, and a scenario analysis on treatment coverage that decides the result."),
 ],
 teach=[
  "<strong>The flip.</strong> Screening that finds people who are then not treated produces cost and no health. The ICER is a statement about the "
  "health system downstream of the test, not the test. This is the single most transferable lesson in the pack.",
  "Against the Uy paper: there the answer turns on the surgeon's choice; here on whether a Health and Wellness Centre dispenses the drugs.",
  "It uses the retired GDP rule too. Here, unlike Thiagarajan, it matters: the ICERs sit near the threshold, so the rule is doing work.",
  "Near-model Reference Case compliance: comparator, perspective, Indian utilities, primary costing, PSA. Use it as the 'what good looks like' exhibit.",
 ],
 check="Confirm open access at the journal site before telling the group they can download it.",
),
# ---------------------------------------------------------------------------------------------
dict(
 n=5, partner=6, cluster="Critical care, anaesthesia, neonatology",
 short="Sharma et al. 2016, Kangaroo Ward Care for very low birth weight infants",
 authors="Sharma D, Murki S, Oleti TP.",
 title="To compare cost effectiveness of 'Kangaroo Ward Care' with 'Intermediate intensive care' in stable very low birth weight infants (birth weight < 1100 grams): a randomized control trial.",
 journal="Ital J Pediatr", vol="2016;42:64", pmid=27412638, pmcid="",
 doi="10.1186/s13052-016-0274-3", oa=True,
 summary=[
  "A <strong>randomised trial</strong> in a tertiary neonatal unit in Hyderabad. <strong>141</strong> stable very low birth weight infants "
  "(71 and 70) were randomised to <strong>Kangaroo Ward Care</strong>, moving to the kangaroo ward with the mother at 1,150 g, or "
  "<strong>Intermediate Intensive Care</strong> in an incubator or warmer until 1,250 g.",
  "Hospital costs were estimated top down and parents' out-of-pocket costs bottom up, from randomisation to discharge.",
  "Mean cost was <strong>INR 41,592</strong> per infant with Kangaroo Ward Care and <strong>INR 75,389</strong> with intermediate care, a saving of "
  "about <strong>INR 33,800 (US$512)</strong> per infant. NICU and hospital stays were shorter. The authors conclude that early transfer to the "
  "kangaroo ward is a cost-effective intervention.",
 ],
 prompts=[
  Q_WHO,
  "Drummond's two questions: are both costs <em>and</em> consequences compared? Which box is it in?",
  "Is any threshold used? Could one be?",
  "Top down for the hospital, bottom up for the parents. What is the difference, and what does each risk missing?",
  Q_FRAME + " When does the horizon end?",
  "What is the outcome measure? Is there an ICER? If the babies do equally well, what kind of analysis is this, and what must be shown first?",
  "Is there a model? Would a longer horizon need one?",
  Q_UNC,
 ],
 job="<strong>The deliberately weak paper.</strong> Titled a cost-effectiveness analysis; actually a cost comparison inside a trial. A good group takes it apart in fifteen minutes.",
 grid=[
  ("Decision problem", "Early kangaroo ward vs intermediate care, stable VLBW infants. Clear."),
  ("Comparator", "Intermediate intensive care. Reasonable current practice."),
  ("Costs", "Hospital top down, parents bottom up. Promising, and a useful link to the costing session."),
  ("Outcomes", "Cost and length of stay. No QALY, no DALY, no ICER."),
  ("Horizon", "Ends at discharge."),
  ("Discounting", "Not reported; not needed at this horizon."),
  ("Uncertainty", "No sensitivity analysis reported."),
 ],
 teach=[
  "<strong>Not a cost-effectiveness analysis.</strong> With no health outcome in the ratio it is a cost analysis (Session 2, box 4). If the claim is 'same outcome, lower cost', "
  "it is a <strong>cost-minimisation</strong> argument, which is legitimate only if equivalence of outcomes is <em>demonstrated</em>. "
  "Ask what the paper shows about neonatal outcomes, and whether the trial was designed to show equivalence.",
  "The title is the teaching point: a word in a title is not a method. Link to Session 2's 'three errors we will keep catching'.",
  "Credit where due: a randomised design, and patient-side costs collected bottom up, which many better-known papers omit.",
  "Horizon at discharge misses readmission, growth and neurodevelopment; the outcomes that would matter over a lifetime are not in scope.",
 ],
 check="",
),
# ---------------------------------------------------------------------------------------------
dict(
 n=6, partner=5, cluster="Critical care, anaesthesia, neonatology",
 short="Patel et al. 2015, ward-based NIV for COPD respiratory failure",
 authors="Patel SP, Pena ME, Babcock CI.",
 title="Cost-effectiveness of noninvasive ventilation for chronic obstructive pulmonary disease-related respiratory failure in Indian hospitals without ICU facilities.",
 journal="Lung India", vol="2015;32(6):549-556", pmid=26664158, pmcid="PMC4663855",
 doi="10.4103/0970-2113.168137", oa=True,
 summary=[
  "A <strong>decision-analytic model</strong> comparing <strong>ward-based non-invasive ventilation (NIV) with standard treatment</strong> against "
  "<strong>standard treatment alone</strong> for COPD-related respiratory failure in Indian hospitals that have no ICU.",
  "All parameters come from the published literature. <strong>Societal perspective, lifetime horizon</strong>, future costs discounted at 3%, "
  "costs in 2012 US dollars. One-way, two-way and probabilistic sensitivity analyses.",
  "NIV gave 17.7% more survival, cost <strong>$101</strong> more and gained <strong>1.67 QALYs</strong>. The paper reports cost per QALY of "
  "<strong>$78</strong> for standard care ($535.02 ÷ 6.82) and <strong>$75</strong> for NIV ($636.33 ÷ 8.49), and an ICER of "
  "<strong>$61 per QALY</strong>, far below India's GDP per capita ($1,489). NIV was preferred in 100% of simulations at a willingness to pay above $250.",
 ],
 prompts=[
  Q_WHO + " Where are the authors based?",
  Q_BOX,
  "Against GDP per capita the answer is obvious. Would any plausible threshold change it? Then what is the real question for a hospital?",
  "Every parameter is from the literature. Which of them would you most want replaced with Indian data from your own ward?",
  Q_FRAME,
  "The paper reports $78 and $75 per QALY, and also $61. Which of these is the ICER, and what are the other two? Are QALYs discounted?",
  "What kind of model? What happens to a patient after discharge in it?",
  "100% probability of being cost-effective. What does PSA <em>not</em> capture here?",
 ],
 job="The <strong>technically competent</strong> paper. Right structure, lifetime, discounting, three kinds of sensitivity analysis; its weakness is where the numbers come from.",
 grid=[
  ("Decision problem", "Ward NIV vs standard care, COPD respiratory failure, hospitals without ICU. Well defined."),
  ("Comparator", "Standard treatment without NIV. Genuinely current practice in such hospitals."),
  ("Perspective", "Societal."),
  ("Effectiveness", "Published literature, not Indian data. Much likely from ICU or high-income settings."),
  ("Outcomes", "QALYs; survival."),
  ("Horizon, discounting", "Lifetime; 3% stated for future costs. Check whether QALYs were discounted."),
  ("Threshold", "GDP per capita, $1,489 (2012)."),
  ("Uncertainty", "One-way, two-way, probabilistic. 100% preferred above $250 per QALY."),
 ],
 teach=[
  "<strong>Average versus incremental,</strong> live. The $78 and $75 figures are average cost-effectiveness ratios, total cost over total QALYs, "
  "which Session 6 calls meaningless for a decision. The ICER is $101 ÷ 1.67 = about $61. Ask the group which number a decision-maker should read.",
  "<strong>Transferability.</strong> Every input is borrowed. NIV effectiveness on a general ward in an Indian district hospital, with its staffing, "
  "may be far from the trial settings. PSA varies parameters inside their borrowed ranges; it cannot test whether the ranges apply here. That is structural "
  "and transferability uncertainty, which Session 8 says PSA does not handle.",
  "<strong>When the answer is obvious, the question moves.</strong> At $61 per QALY no threshold matters. The real barrier is feasibility: staff, masks, "
  "monitoring on a ward. The economics says 'yes'; implementation is the open question.",
  "2012 US dollars against 2012 GDP. Ask how they would update it for a decision today.",
 ],
 check="",
),
# ---------------------------------------------------------------------------------------------
dict(
 n=7, partner=8, cluster="Paediatrics, infectious disease, nephrology",
 short="Gupta et al. 2022, peritoneal dialysis first",
 authors="Gupta D, Jyani G, Ramachandran R, Bahuguna P, Ameel M, Dahiya BB, Kohli HS, Prinja S, Jha V.",
 title="Peritoneal dialysis-first initiative in India: a cost-effectiveness analysis.",
 journal="Clin Kidney J", vol="2022;15(1):128-135", pmid=35035943, pmcid="PMC8757426",
 doi="10.1093/ckj/sfab126", oa=True,
 summary=[
  "A <strong>Markov model</strong> with one-year cycles compares starting kidney replacement therapy with <strong>peritoneal dialysis (PD first)</strong> "
  "against starting with <strong>haemodialysis (HD first)</strong> in people with kidney failure in India, over their lifetime, with complications such as "
  "peritonitis, vascular access problems and blood-borne infections.",
  "Two scenarios: a <strong>real-world</strong> one, using current costs and patterns of use; and a <strong>public programme</strong> one, following the "
  "Pradhan Mantri National Dialysis Programme. Health system costs, patients' out-of-pocket spending and indirect costs are all included; 3% discounting.",
  "Mean QALYs were <strong>3.3 with PD and 1.6 with HD</strong>. From a societal perspective PD first is <strong>cost-saving</strong> in both scenarios. "
  "If only costs directly attributable to care are counted, PD first is cost-effective only if PD consumables cost <strong>INR 70 per unit</strong>, "
  "65% below the recommended price of INR 200. The authors conclude the government should negotiate the price of PD consumables under the programme.",
 ],
 prompts=[
  Q_WHO + " The conclusion is addressed to someone specific: who?",
  Q_BOX,
  "Which threshold? And the conclusion is a price, not a verdict: what kind of answer is that?",
  "Health system, out-of-pocket and indirect costs are all in the base case. Which of those does the Indian Reference Case put in the base case, and which only in sensitivity analysis?",
  Q_FRAME + " Is 'HD first' what happens now?",
  "Where do the quality-of-life weights come from? Is it the Indian value set?",
  "Name the health states and the cycle length. Which complications are modelled?",
  "The answer changes with one perspective choice and one price. Which, and by how much?",
 ],
 job="The analysis that <strong>ends in a negotiating position</strong>: a price at which the policy pays, rather than a yes or no.",
 grid=[
  ("Decision problem", "PD first vs HD first for kidney failure; real-world and PMNDP scenarios. Policy-framed."),
  ("Comparator", "HD first. Current practice in India."),
  ("Perspective", "Societal, including indirect (productivity) costs in the base case."),
  ("Costs", "PMNDP data and micro-costing; out-of-pocket from patient interviews; indirect costs by the human capital approach."),
  ("Outcomes", "QALYs and life years. EQ-5D in 192 patients, valued with the Thai tariff because no Indian value set existed then."),
  ("Horizon, discounting", "Lifetime; 3%. One-year cycles."),
  ("Threshold", "Per-capita GDP, INR 1,48,171 (2019)."),
  ("Uncertainty", "PSA, 1,000 iterations, gamma for costs and beta for probabilities; threshold analysis on consumable price."),
 ],
 teach=[
  "<strong>The perspective decides the verdict.</strong> Cost-saving from the societal perspective, which includes productivity costs. On direct costs only, "
  "cost-effective only at INR 70 per unit. The Indian Reference Case (2023, after this paper) puts indirect costs in <em>sensitivity analysis only</em>. "
  "A good group sees that the headline would be weaker under today's rules.",
  "<strong>A price, not a verdict.</strong> The threshold analysis tells a purchaser what to negotiate for. That is often the most useful output an "
  "economic evaluation can give, and it links to the costing session: prices are not costs, and prices can move.",
  "<strong>Borrowed utilities.</strong> Thai tariff, because India had no EQ-5D value set at the time. Now it does (Session 6). Legitimate then; a flaw if repeated now.",
  "Against Srinivasan: both are Indian, both real-world, but this one ends in a number a ministry can act on, the other in a cost per DALY that cannot be compared with anything else in the pack.",
 ],
 check="",
),
# ---------------------------------------------------------------------------------------------
dict(
 n=8, partner=7, cluster="Paediatrics, infectious disease, nephrology",
 short="Srinivasan et al. 2024, childhood AML at a tertiary centre",
 authors="Srinivasan S, Bolous NS, Batra A, Bharti S, Singh N, Shaikh T, Yadav A, Kanwar V.",
 title="Cost-effectiveness of treating childhood acute myeloid leukemia at a tertiary care center in North India.",
 journal="Pediatr Blood Cancer", vol="2024;71(11):e31242", pmid=39126354, pmcid="",
 doi="10.1002/pbc.31242", oa=True,
 summary=[
  "A <strong>retrospective study</strong> of children under 15 with acute myeloid leukaemia treated at one tertiary cancer centre in North India. "
  "Outcomes, complications, deaths and costs were taken from the electronic medical record and the hospital database.",
  "Of <strong>59</strong> children, <strong>43</strong> received intensive therapy. Treatment-related mortality reached <strong>30%</strong>, mostly from sepsis; "
  "abandonment and limited access to bone marrow transplantation were also problems. Three-year event-free survival was <strong>24.5%</strong> and overall "
  "survival <strong>27.9%</strong> in those treated intensively.",
  "The total cost per newly diagnosed child treated with curative intent was <strong>US$4,454</strong>. Cost-effectiveness was measured as cost per "
  "<strong>DALY averted</strong>, which came to <strong>24% of GDP per capita</strong>; the authors judge treatment cost-effective even against a stringent "
  "threshold, and call for reducing treatment-related deaths.",
  "A <strong>published Comment</strong> on this paper appeared in the same journal (Sra, Bakhshi, Ganguly, <em>Pediatr Blood Cancer</em> 2025;72(1):e31305, PMID 39228042).",
 ],
 prompts=[
  Q_WHO,
  Q_BOX + " What is the comparator, even if the paper does not name one?",
  "Cost per DALY averted at 24% of GDP per capita. Which threshold is 'stringent', and would it pass India's own estimate?",
  "Costs come from the hospital database. Whose costs are these, and what does a family pay that is not in them?",
  Q_FRAME + " How are children who abandoned treatment counted?",
  "DALYs, not QALYs. Can this result be set beside any other paper in the pack? What does the Reference Case allow for children?",
  "Is there a model, or is this observed data? What happens to survival after three years?",
  "Is any uncertainty reported? Then read the published Comment: did its authors find what you found?",
 ],
 job="The <strong>real-world, DALY-based</strong> paper: honest data from one centre, a ratio that cannot be compared with the QALY papers, and a published peer appraisal to check the group against.",
 grid=[
  ("Decision problem", "Treating childhood AML with curative intent at one centre. The alternative is implicit."),
  ("Comparator", "Not stated in the abstract; in effect no curative treatment. Ask the group whether that is current practice."),
  ("Perspective", "Hospital costs from the database. Out-of-pocket and family costs unclear."),
  ("Effectiveness", "Observed outcomes in 59 children, one centre, retrospective."),
  ("Outcomes", "DALYs averted. The Reference Case permits DALYs only under age 4; these are children up to 15."),
  ("Horizon", "Three-year survival observed; DALYs imply extrapolation to a lifetime. Check how."),
  ("Threshold", "Cost per DALY averted as a share of GDP per capita (24%)."),
  ("Uncertainty", "None described in the abstract."),
 ],
 teach=[
  "<strong>Not comparable.</strong> A cost per DALY averted cannot sit in a league table beside cost per QALY gained. Paired with Gupta, "
  "which ends in a price a ministry can act on, this one ends in a ratio that answers 'is treatment worth offering at all?', which is a real and "
  "important question, but a different one.",
  "<strong>An implicit comparator.</strong> 'Cost-effective' compared with what? Almost certainly no curative treatment, where DALYs averted are measured "
  "against near-certain death. That makes the ratio favourable almost by construction.",
  "<strong>Denominators.</strong> With abandonment and 30% treatment-related mortality, whether the cost per patient includes the children who died "
  "early or left treatment changes the answer. Ask the group what the paper divides by.",
  "Credit: real Indian costs and outcomes, and the authors judge against a stringent threshold rather than the GDP rule.",
  "<strong>The Comment.</strong> The group can compare its appraisal with a published one. Treat it as a model of peer critique, not an answer key.",
 ],
 check="(a) Read the published Comment (Sra, Bakhshi, Ganguly, <em>Pediatr Blood Cancer</em> 2025;72(1):e31305, PMID 39228042) before the day, so you can say what it argued. "
       "(b) The paper is open access (CC BY-NC-ND): print the full text for Group 8.",
),
]
