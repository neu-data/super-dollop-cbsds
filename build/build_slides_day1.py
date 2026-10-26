"""Day 1 slides: Understanding data and making comparisons.
Run from the project folder:  python build/build_slides_day1.py
All numbers come from the R scripts (see instructor/outputs/*.log).
"""
import os
from slide_helpers import Deck, ROOT

d = Deck()

d.title_slide(
    "Concepts of Biostatistics and Data Science",
    "A two-day crash course with practical analysis in R\nDay 1: Understanding data and making comparisons",
    "Date: DD-MM-YYYY",
    notes="Welcome participants. Introduce yourself and ask each person for one sentence: their work and one thing "
          "they want from the course. Point out that the course has two strands each day: two hours of ideas, then "
          "two hours of practice in R. Reassure beginners: the aim is understanding, not memorising commands.")

d.table("Plan for today", [
    ["Time", "Session", "Focus"],
    ["09:00 to 09:10", "Welcome", "Aims, data, how the course works"],
    ["09:10 to 09:30", "Theory 1", "Questions, observations, variables, data quality"],
    ["09:30 to 09:55", "Theory 2", "Describing data: summaries and plots"],
    ["09:55 to 10:20", "Theory 3", "Samples, variability, effect sizes, CIs, tests"],
    ["10:20 to 10:42", "Theory 4", "Comparing groups: continuous outcomes"],
    ["10:42 to 11:00", "Theory 5", "Categorical associations; first look at confounding"],
    ["11:00 to 11:30", "Break", "(not counted in teaching time)"],
    ["11:30 to 13:30", "Practical", "Import, inspect, describe, compare in R"],
], col_w=[2.2, 1.8, 6], size=19,
    notes="Clock times are an example; adapt to your venue. Teaching time is exactly 4 hours: 2 hours theory and "
          "2 hours practical. If the group is slow, the categorical section can be shortened because the practical "
          "revisits it with the script 04_categorical.R.")

d.bullets("By the end of today you will be able to", [
    "Describe a dataset in terms of observations, variables and variable types",
    "Check a dataset for missing values, impossible values and coding problems",
    "Choose and calculate suitable summaries: counts, proportions, mean (SD), median (IQR)",
    "Choose a suitable plot: bar chart, histogram or boxplot",
    "Explain what a confidence interval and a p-value do and do not tell you",
    "Compare two or more groups with a t-test, ANOVA or a rank-based test, and say why",
    "Analyse a contingency table and explain proportions, risks, odds, RR and OR",
    "Recognise paired data and avoid analysing it as independent groups",
], size=22, notes="These are the measurable outcomes listed in the course overview. Each is practised in the workbook "
                  "exercises 1.1 to 1.11.")

d.two_col("Our data: the Healthy Hearts District Study (simulated)", [
    "480 adults aged 30 to 74 from four districts",
    "Baseline: age, sex, education, smoking, activity, diet score, BMI, blood pressure, CRP",
    "Randomised: standard advice or a lifestyle programme",
    "12-month follow-up: blood pressure, satisfaction, adverse events, clinic visits",
], [
    "Simulated with known rules, so results are for teaching only",
    "Realistic problems built in: missing values, a -99 code, skewed variables, people who left early",
    "Data dictionary: data/data_dictionary.csv",
    "One dataset all course: you learn the methods, not new data each time",
], heads=["What it contains", "Why we use it"],
    notes="Stress that this is not real data. Because we simulated it, we know the truth behind it, which lets us "
          "check whether methods recover it (for example, clustering on Day 2). Show the data dictionary briefly.")

# ------------------------------------------------------------------ Section 1
d.section("Part 1", "Questions, observations and variables",
          "Analysis starts with a question, not with a test")

d.table("Start with the question", [
    ["Question", "Purpose", "What we will need"],
    ["What proportion of participants smoke?", "Describe", "Count and proportion"],
    ["Is mean blood pressure higher in men than in women?", "Compare groups", "Difference in means with CI"],
    ["Is smoking associated with high blood pressure?", "Association", "Table, RR or OR with CI"],
    ["Did blood pressure change after the programme?", "Compare paired measurements", "Mean change with CI"],
], col_w=[5, 2.4, 3.6], size=19,
    box="The method follows from the question, the type of outcome and the study design.",
    notes="Ask the group to suggest a question of their own that these data could answer. Write two or three on a "
          "flip chart and return to them in the practical. Emphasise that the shape of the data alone never "
          "decides the analysis.")

d.bullets("Observations and variables", [
    "An observation is one unit we measured: here, one participant (one row)",
    "A variable is one characteristic recorded for every observation (one column)",
    "Before analysing, ask: what does one row represent?",
    ("If a person is measured twice, the two values are linked (paired)", 1),
    ("If people come from the same clinic or family, they may be more alike (clustered)", 1),
    "Standard methods assume each observation is independent of the others",
], notes="Independence is the assumption most often violated and least visible in the output. Here each row is a "
         "different person, and baseline and 12-month blood pressure are two columns in the same row, so they are "
         "paired by design.")

d.table("Types of variables", [
    ["Type", "Meaning", "Example in our data"],
    ["Continuous", "Any value on a scale", "sbp_0, bmi, crp, age"],
    ["Count (discrete)", "Whole numbers 0, 1, 2 ...", "clinic_visits"],
    ["Binary", "Two categories", "smoker, high_bp_0, adverse_event"],
    ["Nominal", "Categories without order", "district"],
    ["Ordinal", "Ordered categories; gaps may not be equal", "education, satisfaction (1 to 5)"],
    ["Time-to-event", "Time until something happens, often censored", "not in our data (further learning)"],
], col_w=[2.2, 4.4, 4.4], size=19,
    notes="The type of the OUTCOME is one of the main things that decides the method. Note that satisfaction is "
          "stored as numbers but is ordinal: the difference between 1 and 2 need not equal that between 4 and 5. "
          "Censoring means we know only that the event had not happened by the end of follow-up.")

d.bullets("Check data quality before any analysis", [
    "Range: are values possible? (activity of -99 minutes is a code, not a value)",
    "Missing values: how many, in which variables, and why?",
    ("41 people have no 12-month blood pressure because they left the study early", 1),
    "Categories: consistent spelling and labels (\"North\", \"north\", \"N\")",
    "Duplicates and identifiers: one row per person?",
    "Types: is each variable stored as a number or a category, as intended?",
], box="Most R functions silently drop rows with missing values. Always report how many observations each result uses.",
    notes="Missing data are not just a nuisance. If people who left the study differ from those who stayed, "
          "complete-case results can be biased. Do not replace missing values with the mean; it makes the data look "
          "less variable than they are. Multiple imputation is the usual remedy and is beyond this course.")

# ------------------------------------------------------------------ Section 2
d.section("Part 2", "Describing data", "Summaries and plots that suit the variable")

d.bullets("Categorical variables: counts and proportions", [
    "A proportion is a count divided by a denominator: always say what the denominator is",
    ("Smokers: 79 / 480 = 16.5% of all participants", 1),
    ("Tertiary education: 134 / 474 = 28.3% of those with education recorded (6 missing)", 1),
    "Percentages without counts can mislead when groups are small",
    "Plot with a bar chart: one bar per category, bars separated by gaps",
], notes="Ask: if 6 people have no education recorded, should they be in the denominator? Either choice can be "
         "right; what matters is saying which. Show count() in R during the practical.")

d.table("Centre and spread for continuous variables", [
    ["Summary", "What it describes", "SBP at baseline (n = 480)"],
    ["Mean", "Average value; sensitive to extreme values", "129.3 mmHg"],
    ["Standard deviation (SD)", "Typical distance of values from the mean", "15.6 mmHg"],
    ["Median", "Middle value when sorted", "129 mmHg"],
    ["Interquartile range (IQR)", "Range of the middle 50% (25th to 75th percentile)", "118 to 140 mmHg"],
], col_w=[3, 5, 3], size=19,
    items_after=["Symmetric distribution: mean (SD) and median (IQR) tell a similar story",
                 "Skewed distribution: report median (IQR), or analyse on a log scale"],
    notes="For roughly symmetric data about two thirds of values lie within one SD of the mean. That rule does not "
          "hold for skewed data, which is why the median and IQR are preferred there.")

d.text_image("Skewed data: C-reactive protein", [
    "Most values are low; a few are very high",
    "Mean 3.0 mg/L, median 1.9 mg/L",
    "SD (3.4) is larger than the mean: a sign of right skew",
    "Report median (IQR): 1.9 (1.2 to 3.7) mg/L",
    "On a log scale the distribution is roughly symmetric",
], "f_hist_crp.png", split=0.36,
    notes="Many biological measurements (CRP, viral load, income, costs) are right-skewed. Taking logs is often "
          "natural because effects act multiplicatively. We will use this on the CRP comparison.")

d.text_image("Choosing a plot", [
    "One categorical variable: bar chart",
    "One continuous variable: histogram (shape) or boxplot (summary)",
    "Continuous by group: boxplots with the points shown",
    "Two continuous variables: scatterplot (Day 2)",
    ("Box: IQR; line: median; whiskers: up to 1.5 IQR", 1),
], "f_box_district.png", split=0.4,
    notes="Showing the individual points stops a boxplot hiding small groups or odd distributions. Avoid bar charts "
          "of means (\"dynamite plots\"); they hide the data. Avoid pie charts and 3D effects.")

# ------------------------------------------------------------------ Section 3
d.section("Part 3", "From a sample to a population",
          "Variability, effect sizes, confidence intervals and tests")

d.bullets("Samples and populations", [
    "Population: everyone we want to draw conclusions about",
    "Sample: the people we actually measured",
    "A statistic (e.g. a sample mean) estimates a population value",
    "A different sample would give a different estimate: this is sampling variability",
    "Statistics quantifies that uncertainty; it cannot remove bias from a poor sample",
], notes="A large but unrepresentative sample gives a precise estimate of the wrong thing. Random sampling or "
         "random allocation is what lets us use these methods to generalise or to compare fairly.")

d.image("The same study repeated 20 times", "f_sampling_cis.png",
        caption="Each line is one sample of 30 people with its 95% CI. 19 of the 20 intervals include the true mean.",
        notes="We treated our 480 participants as a population and drew 20 random samples of 30. Each sample gives a "
              "different mean and interval. Over many samples about 95% of intervals contain the true value. For "
              "any single interval we do not know whether it is one of the lucky ones.")

d.bullets("Standard error and confidence interval", [
    "SD describes how individuals vary; the standard error (SE) describes how an estimate varies",
    "For a mean:  SE = SD / √n.  Larger samples give smaller SEs",
    "95% confidence interval ≈ estimate ± 2 × SE",
    "Interpretation: the range of population values reasonably compatible with the data",
    ("Strictly: the method captures the true value in 95% of repeated samples", 1),
    "Example: mean SBP 129.3 mmHg, SE = 15.6 / √480 = 0.71, 95% CI about 127.9 to 130.7",
], notes="Avoid saying \"there is a 95% probability the true value is in this interval\" for one particular "
         "interval; in this framework the true value is fixed. In practice, read the CI as a range of plausible "
         "values and look at both ends.")

d.bullets("Effect sizes: how big is the difference?", [
    "An effect size measures the size of a difference or association in meaningful units",
    ("Difference in means: men's SBP is 6.1 mmHg higher than women's", 1),
    ("Ratio of geometric means: smokers' CRP is 1.6 times that of non-smokers", 1),
    ("Difference or ratio of proportions, odds ratio", 1),
    "Always report an effect size with its 95% CI",
    "A p-value alone says nothing about the size of an effect",
], notes="Standardised effect sizes (such as Cohen's d) exist but are harder to interpret than differences in the "
         "original units. Prefer the original units when they are meaningful, as mmHg is here.")

d.bullets("Hypothesis tests and p-values", [
    "Null hypothesis (H0): no difference or no association in the population",
    "p-value: if H0 were true, the probability of a result at least as extreme as ours",
    "A small p-value means the data are hard to reconcile with H0",
    "The p-value is NOT the probability that H0 is true",
    "p > 0.05 is NOT evidence of no difference: look at the CI",
    "0.05 is a convention, not a law. Report the actual p-value (e.g. p = 0.03)",
], notes="The purpose of a test is to judge whether chance alone is a reasonable explanation. Tests do not "
         "measure importance and do not establish cause. With many tests, some will be \"significant\" by chance.")

d.image("Statistical significance is not practical importance", "f_significance_vs_importance.png",
        caption="Hypothetical studies. Judge results by the estimate and both ends of the CI.",
        notes="A: very precise but trivial effect, statistically significant. B: not significant, but the data are "
              "compatible with an important benefit; we need more data. C: significant and important. D: not "
              "significant and precise, so we can rule out large differences. None of these establishes causation; "
              "that depends on design.")

# ------------------------------------------------------------------ Section 4
d.section("Part 4", "Comparing groups: continuous outcomes",
          "Two groups, more than two groups, and paired data")

d.text_image("First question: independent or paired?", [
    "Independent: different people in each group (men vs women)",
    "Paired: the same people measured twice, or matched pairs",
    "Paired designs remove between-person differences, so they are more precise",
    "Analysing paired data as independent gives the wrong CI and p-value",
], "f_paired.png", split=0.33,
    notes="Lifestyle group, 224 people with both measurements. The mean change is the same (-6.0 mmHg) in both "
          "analyses but the incorrect independent analysis gives a CI of -9.1 to -2.9 instead of -7.2 to -4.8. "
          "Repeated measurements over several time points or clustered data need other methods (further learning).")

d.text_image("Two independent groups: Welch's t-test", [
    "Question: does mean SBP differ between men and women?",
    "Difference (men - women): 6.1 mmHg, 95% CI 3.4 to 8.9, p < 0.001",
    "Welch's version does not assume equal variances: use it by default",
    "Assumptions: independent observations; sample means approximately normal",
    ("Holds for large groups even if data are moderately skewed", 1),
], "f_ttest_sex.png", split=0.48,
    notes="R command: t.test(sbp_0 ~ sex, data = hearts). R reports Female minus Male (-6.1, CI -8.9 to -3.4), "
          "following the order of the factor levels. Student's t-test (var.equal = TRUE) gives almost the same "
          "answer here because the SDs are similar (15.1 and 15.6).")

d.two_col("A skewed outcome: CRP in smokers and non-smokers", [
    "Analyse log(CRP) with a t-test, then back-transform",
    "Ratio of geometric means: 1.63 (95% CI 1.31 to 2.03)",
    "\"Typical CRP is about 60% higher in smokers\"",
], [
    "Wilcoxon rank-sum (Mann-Whitney) test, p < 0.001",
    "Asks whether values in one group tend to be larger",
    "Hodges-Lehmann shift 0.9 mg/L (0.5 to 1.4): not a difference in medians",
], heads=["Option 1: log scale", "Option 2: rank-based"],
    box="Rank tests still assume independent observations. They are not assumption-free and not, in general, tests of medians.",
    notes="Medians: 2.8 (smokers) and 1.8 (non-smokers). The Wilcoxon test compares medians only under the extra "
          "assumption that the two distributions have the same shape and differ only by a shift. Decide which "
          "question you want answered before you look at the p-values.")

d.bullets("Choosing between t-tests and rank-based tests", [
    "Ask first: what summary answers the question? Mean, typical (geometric mean), or tendency to be larger?",
    "Look at plots of the data, not only a normality-test p-value",
    ("Normality tests reject trivial departures in large samples and miss big ones in small samples", 1),
    "A small sample does not automatically require a nonparametric test",
    ("With few observations every method has little information; rank tests can have very low power", 1),
    "For t-tests the normality assumption concerns the sampling distribution of the mean (or the residuals)",
], notes="This slide corrects common rules of thumb. The decision is a judgement based on the question, the scale "
         "of measurement, the plots and the sample size. Ordinal outcomes such as a 1 to 5 rating are a natural "
         "case for rank-based methods.")

d.bullets("Paired data: the paired t-test", [
    "Calculate each person's change, then analyse the changes",
    "Lifestyle group (n = 224): mean change -6.0 mmHg, 95% CI -7.2 to -4.8",
    "Standard advice group (n = 215): mean change -2.0 mmHg, 95% CI -3.2 to -0.8",
    "Rank-based alternative: Wilcoxon signed-rank test",
    "To compare the programme with standard advice, compare the changes between the two groups:",
    ("difference 4.0 mmHg, 95% CI 2.3 to 5.6 (Welch t-test on the changes)", 1),
], notes="A within-group change is not evidence that the programme works: the standard advice group also fell. "
         "Only the randomised comparison between groups estimates the programme effect. Day 2 shows the "
         "baseline-adjusted (ANCOVA) estimate as an extension.")

d.text_image("More than two groups: one-way ANOVA", [
    "Question: does mean SBP differ between the four districts?",
    "Welch's ANOVA: F = 6.8, p < 0.001",
    "The overall test says the means are not all equal",
    "It does not say which districts differ",
    "Assumptions: independence, similar spread (or use Welch), approximately normal residuals",
], "f_anova_district.png", split=0.45,
    notes="Means: North 126, South 134, East 131, West 126 mmHg. Classical ANOVA gives F = 7.3, p < 0.001. Residual "
          "plots are in the script. If one district had a much wider spread, Welch's version protects against that.")

d.table("Which groups differ? Pairwise comparisons", [
    ["Comparison (Tukey)", "Difference (mmHg)", "95% CI (adjusted)"],
    ["South - North", "7.6", "2.5 to 12.8"],
    ["East - North", "4.5", "-0.6 to 9.5"],
    ["West - North", "-0.3", "-5.4 to 4.7"],
    ["East - South", "-3.2", "-8.3 to 1.9"],
    ["West - South", "-8.0", "-13.1 to -2.8"],
    ["West - East", "-4.8", "-9.8 to 0.2"],
], col_w=[4, 3, 3], size=19,
    items_after=["Six comparisons: adjust for multiple testing (Tukey, or Holm with pairwise.t.test)",
                 "Better still: decide the comparisons that matter before seeing the data"],
    notes="Without adjustment, each extra comparison adds another chance of a false positive. A significant overall "
          "ANOVA followed by uncorrected t-tests on every pair is a common mistake.")

d.bullets("Kruskal-Wallis: a rank-based comparison of several groups", [
    "Extends the Wilcoxon rank-sum test to three or more independent groups",
    "Asks whether values tend to be larger in some groups than others",
    "CRP by district: medians 1.8 to 2.5 mg/L, Kruskal-Wallis p = 0.07",
    "A p-value above 0.05 is not proof of no difference: the data are inconclusive",
    "Like Wilcoxon, it assumes independence and is not generally a test of medians",
    "Follow-up: pairwise Wilcoxon tests with adjusted p-values, if justified",
], notes="Kruskal-Wallis is also a natural choice for ordinal outcomes with several groups. If you want an effect "
         "estimate for skewed data across several groups, analysing log values with ANOVA or regression often "
         "gives more useful answers (ratios of geometric means).")

# ------------------------------------------------------------------ Section 5
d.section("Part 5", "Associations between categorical variables",
          "Contingency tables, risks, odds, chi-square and Fisher's exact test")

d.table("A 2 × 2 table: smoking and high blood pressure", [
    ["", "High BP: yes", "High BP: no", "Total", "Proportion with high BP"],
    ["Smoker", "38", "41", "79", "38 / 79 = 48.1%"],
    ["Non-smoker", "86", "315", "401", "86 / 401 = 21.4%"],
    ["Total", "124", "356", "480", "124 / 480 = 25.8%"],
], col_w=[2, 1.8, 1.8, 1.3, 3.5], size=19,
    items_after=["Row proportions answer: how common is high BP in each smoking group?",
                 "Column proportions answer a different question: what share of people with high BP smoke?",
                 "High BP here means SBP ≥ 140 mmHg at baseline (a cross-sectional measurement)"],
    notes="Always choose the direction of percentages to match the question. Rows are the exposure, columns the "
          "outcome. Dichotomising a continuous measurement loses information; we use it here because 140 mmHg is "
          "a recognised clinical threshold.")

d.text_image("Proportions, risks and odds", [
    "Proportion (prevalence): 38 / 79 = 0.48 vs 86 / 401 = 0.21",
    "Prevalence ratio (PR): 0.48 / 0.21 = 2.24 (95% CI 1.67 to 3.02)",
    "Odds: 38 / 41 = 0.93 vs 86 / 315 = 0.27",
    "Odds ratio (OR): 0.93 / 0.27 = 3.39 (95% CI 2.06 to 5.61)",
    "The OR is further from 1 than the PR because high BP is common",
], "f_or_vs_rr.png", split=0.45,
    box="Do not describe an OR of 3.4 as \"3.4 times the risk\". Here the prevalence is about 2.2 times higher.",
    notes="Risk = number with the outcome / number at risk. Odds = number with the outcome / number without. When "
          "the outcome is rare (under about 10%), odds and risks are similar and so are OR and RR. The figure shows "
          "how the OR moves away from the RR as the baseline risk increases.")

d.table("The study design decides which measure you can interpret", [
    ["Design", "What you can estimate", "Example"],
    ["Cohort or randomised trial", "Risks, risk difference, risk ratio (RR), OR", "Adverse events by programme"],
    ["Cross-sectional survey", "Prevalence, prevalence ratio (PR), OR", "High BP by smoking at baseline"],
    ["Case-control study", "Only the OR (cases and controls are sampled by outcome)", "(not in our data)"],
], col_w=[3, 5, 3.4], size=19,
    items_after=["\"Risk\" means new cases over a period among people initially free of the outcome",
                 "Logistic regression gives ORs whatever the design; interpret them with the design in mind"],
    notes="In a case-control study the investigator fixes the number of cases and controls, so the proportion with "
          "the outcome is meaningless; the OR is still valid. Adjusted ORs (aOR) come on Day 2.")

d.two_col("Chi-square and Fisher's exact test", [
    "Tests whether two categorical variables are associated",
    "Compares observed counts with the counts expected under no association",
    "Smoking and high BP: χ² = 23.1, p < 0.001",
    "Approximation works when expected counts are about 5 or more",
], [
    "Exact test: no large-sample approximation",
    "Adverse events: 14 / 240 (5.8%) vs 3 / 240 (1.3%)",
    "RR 4.67 (95% CI 1.36 to 16.0), Fisher p = 0.011",
    "Few events give a very wide CI: the size of the increase is uncertain",
], heads=["Chi-square test", "Fisher's exact test"],
    box="A significant chi-square for a larger table says the proportions differ somewhere. Look at the row proportions to see where.",
    notes="The adverse events table comes from the randomised comparison, so these are genuine risks. The expected "
          "count of events per group is 8.5, so chi-square would also be acceptable; in the subgroup aged 65 and over "
          "the expected counts fall to 2 to 3 and Fisher's test is the safer choice (see script 04).")

d.table("A first look at confounding", [
    ["Analysis", "Odds ratio for smoking and high BP", "95% CI"],
    ["Crude (all participants)", "3.39", "2.06 to 5.61"],
    ["Women only", "2.75", "1.17 to 6.43"],
    ["Men only", "3.28", "1.73 to 6.23"],
    ["Combined, adjusted for sex (Mantel-Haenszel)", "3.09", "1.85 to 5.15"],
    ["Combined, adjusted for age group (Mantel-Haenszel)", "2.57", "1.51 to 4.37"],
], col_w=[5.5, 3.5, 2.5], size=19,
    items_after=["Smokers in these data are more often men and older; both raise blood pressure",
                 "Part of the crude association reflects age and sex, not smoking",
                 "Day 2: regression adjusts for several confounders at once"],
    notes="A confounder is a common cause of the exposure and the outcome. Stratifying compares like with like. Age "
          "matters more here than sex. Workbook extension E1.5 reproduces the age-stratified analysis.")

d.bullets("Paired categorical data: McNemar's test", [
    "Same people classified twice: high BP at baseline and at 12 months",
    "Lifestyle group: 28 changed from high to not high; 6 changed from not high to high",
    "Only these discordant pairs carry information about change",
    "McNemar's test: p < 0.001",
    "A chi-square test on these data would wrongly treat the time points as independent groups",
], notes="Concordant pairs (stayed high, stayed not high) tell us nothing about change. This mirrors the paired "
         "t-test: the design is paired, so the analysis must be paired.")

d.table("Summary: choosing a comparison", [
    ["Outcome", "2 independent groups", "> 2 independent groups", "Paired"],
    ["Continuous, mean meaningful", "Welch t-test", "Welch ANOVA (+ adjusted pairwise)", "Paired t-test"],
    ["Skewed, positive", "t-test on log scale, or Wilcoxon rank-sum", "ANOVA on logs, or Kruskal-Wallis", "Paired t on logs, or signed-rank"],
    ["Ordinal", "Wilcoxon rank-sum", "Kruskal-Wallis", "Wilcoxon signed-rank"],
    ["Binary", "Chi-square or Fisher; RR/OR with CI", "Chi-square (or Fisher)", "McNemar"],
], col_w=[2.6, 3.2, 3.4, 2.6], size=17, row_h=0.6,
    box="These are starting points, not automatic rules. The full decision diagrams are in the reference pack.",
    notes="Refer participants to reference/decision_diagrams.pdf and the cheat sheet. Emphasise that the design "
          "(independent or paired) is decided before looking at the numbers.")

d.table("Practical session (2 hours)", [
    ["Part", "Script", "Workbook", "Time"],
    ["A. Import and inspect, fix missing-value codes", "01_import_and_inspect.R", "1.1 to 1.3", "25 min"],
    ["B. Describe and plot", "02_describe_and_plot.R", "1.4 to 1.6", "30 min"],
    ["C1. Compare groups (continuous, paired)", "03_compare_groups.R", "1.7 to 1.9", "35 min"],
    ["C2. Categorical associations", "04_categorical.R", "1.10 to 1.11", "20 min"],
    ["Review and questions", "", "", "10 min"],
], col_w=[4.6, 3.2, 1.8, 1.2], size=19,
    items_after=["Open the .Rproj file first, then each script in turn",
                 "Extensions E1.1 to E1.6 are for those who finish early"],
    notes="Circulate during the practical. Typical problems: not opening the project (paths fail), forgetting "
          "na.rm = TRUE, running lines out of order. If installation failed, pair the participant with a neighbour "
          "or use data/hearts.csv with base R read.csv().")

out = os.path.join(ROOT, "slides", "Day1_Understanding_data_and_comparisons.pptx")
d.closing(notes="Thank participants. The materials, scripts and reference pack are theirs to keep. "
                 "All examples used simulated data and are for teaching only.")
d.save(out)
