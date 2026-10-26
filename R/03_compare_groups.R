# =============================================================================
# 03_compare_groups.R                            DAY 1 PRACTICAL, PART C (35 min)
# Comparing a continuous or ordinal outcome between groups
#
# Data: simulated Healthy Hearts District Study (teaching data only).
# Workbook exercises 1.7 to 1.9 and extensions E1.1 to E1.3 refer to this script.
#
# Before running any test, write down:
#   1. the question,  2. the outcome and its type,  3. the groups,
#   4. whether observations are independent or paired,
#   5. the effect you will report (difference, ratio...) with its 95% CI.
# =============================================================================

library(dplyr)
library(ggplot2)
source("R/theme_neudata.R")   # Neudata colours and plot theme

hearts <- readRDS("data/hearts.rds")

# =============================================================================
# A. TWO INDEPENDENT GROUPS, CONTINUOUS OUTCOME
# Question: Does mean baseline systolic BP differ between women and men?
# =============================================================================

# Always look first
hearts |>
  group_by(sex) |>
  summarise(n = n(), mean = mean(sbp_0), sd = sd(sbp_0))

ggplot(hearts, aes(x = sex, y = sbp_0)) +
  geom_boxplot(fill = neudata_mist, outlier.shape = NA, width = 0.5) +
  geom_jitter(width = 0.12, alpha = 0.3) +
  labs(x = NULL, y = "Systolic BP at baseline (mmHg)")

# Welch's t-test (R's default). It does not assume equal variances in the
# two groups, so it is a sensible default.
t.test(sbp_0 ~ sex, data = hearts)

# Reading the output:
#  * "mean in group Female / Male": the two sample means.
#  * 95% CI: for the difference Female minus Male (R uses the order of the
#    factor levels). A negative CI means women have lower mean SBP.
#  * p-value: how surprising a difference this large would be if the true
#    means were equal. It is NOT the probability that the null hypothesis is true.
# Assumptions: independent observations; the outcome is continuous; the
# sample means are approximately normally distributed. With large groups this
# holds even if the data are moderately skewed. With small groups, look at the
# data: strong skew or outliers matter more.

# Student's t-test assumes equal variances. Only use it if you have a reason.
t.test(sbp_0 ~ sex, data = hearts, var.equal = TRUE)

# =============================================================================
# B. A SKEWED OUTCOME: CRP in smokers and non-smokers
# =============================================================================

hearts |>
  group_by(smoker) |>
  summarise(n = sum(!is.na(crp)),
            median = median(crp, na.rm = TRUE),
            q1 = quantile(crp, 0.25, na.rm = TRUE),
            q3 = quantile(crp, 0.75, na.rm = TRUE))

# Option 1: Wilcoxon rank-sum test (also called Mann-Whitney U test).
# It compares the whole distributions using ranks. It asks whether values in one
# group tend to be higher than in the other. It is NOT assumption-free (it
# assumes independent observations) and it is NOT, in general, a test of medians.
# conf.int = TRUE gives the Hodges-Lehmann estimate: the median of all
# differences between a smoker and a non-smoker. It is not the difference in medians.
wilcox.test(crp ~ smoker, data = hearts, conf.int = TRUE)

# Option 2: analyse log(CRP) with a t-test, then back-transform.
# exp(difference in mean logs) = ratio of geometric means.
tt_log <- t.test(log(crp) ~ smoker, data = hearts)
tt_log
exp(tt_log$conf.int)          # CI for ratio No / Yes
1 / exp(tt_log$conf.int)      # CI for ratio Yes / No (smokers relative to non-smokers)
# Interpretation: the geometric mean CRP in smokers is about 1.6 times that in
# non-smokers (95% CI 1.3 to 2.0), because exp(1.110 - 0.621) = 1.63.
# Both approaches answer slightly different questions. Choose before you look.

# =============================================================================
# C. PAIRED OBSERVATIONS: the same people measured twice
# Question: In the lifestyle programme group, did SBP change from baseline to 12 months?
# =============================================================================

prog <- hearts |>
  filter(programme == "Lifestyle programme", !is.na(sbp_12))
nrow(prog)

# Each person's change is the unit of analysis
prog <- prog |> mutate(change = sbp_12 - sbp_0)
summary(prog$change)

# Paired t-test = one-sample t-test on the differences
t.test(prog$sbp_12, prog$sbp_0, paired = TRUE)
t.test(prog$change)            # identical result

# WRONG: treating the two measurements as independent groups.
# The mean difference is the same but the CI is much wider, because it
# ignores that each person is compared with themselves.
t.test(prog$sbp_12, prog$sbp_0)

# Rank-based alternative for paired data: Wilcoxon signed-rank test
wilcox.test(prog$sbp_12, prog$sbp_0, paired = TRUE, conf.int = TRUE)

# Spaghetti plot of 40 random people: each line is one person
set.seed(1)
sample40 <- slice_sample(prog, n = 40)
long40 <- bind_rows(
  data.frame(id = sample40$id, time = "Baseline",  sbp = sample40$sbp_0),
  data.frame(id = sample40$id, time = "12 months", sbp = sample40$sbp_12)
) |>
  mutate(time = factor(time, levels = c("Baseline", "12 months")))

ggplot(long40, aes(x = time, y = sbp, group = id)) +
  geom_line(colour = "grey60") +
  geom_point(colour = neudata_cols[["teal"]]) +
  labs(x = NULL, y = "Systolic BP (mmHg)",
       title = "Paired data: each line joins one person's two measurements")

# Comparing the CHANGE between the two randomised groups (independent groups again)
hearts <- hearts |> mutate(change = sbp_12 - sbp_0)
hearts |>
  group_by(programme) |>
  summarise(n = sum(!is.na(change)), mean_change = mean(change, na.rm = TRUE),
            sd_change = sd(change, na.rm = TRUE))
t.test(change ~ programme, data = hearts)
# The CI is for Standard minus Lifestyle. A positive value means the
# lifestyle group's SBP fell further.

# =============================================================================
# D. MORE THAN TWO INDEPENDENT GROUPS
# Question: Does mean baseline SBP differ between the four districts?
# =============================================================================

hearts |>
  group_by(district) |>
  summarise(n = n(), mean = mean(sbp_0), sd = sd(sbp_0))

# Classical one-way ANOVA (assumes equal variances across groups)
fit_aov <- aov(sbp_0 ~ district, data = hearts)
summary(fit_aov)

# Welch's ANOVA does not assume equal variances. A sensible default.
oneway.test(sbp_0 ~ district, data = hearts)

# A small p-value says the four means are probably not all equal.
# It does NOT say which districts differ. For that, compare pairs and
# adjust for multiple comparisons:
pairwise.t.test(hearts$sbp_0, hearts$district, pool.sd = FALSE, p.adjust.method = "holm")
TukeyHSD(fit_aov)   # differences with adjusted 95% CIs (equal-variance ANOVA)

# Check assumptions with the residuals (each value minus its group mean)
par(mfrow = c(1, 2))
plot(fit_aov, which = 1)   # spread similar across groups?
plot(fit_aov, which = 2)   # residuals roughly on the line (approx. normal)?
par(mfrow = c(1, 1))

# Rank-based alternative: Kruskal-Wallis test. Like Wilcoxon, it compares
# distributions through ranks and assumes independent observations.
hearts |>
  group_by(district) |>
  summarise(n = sum(!is.na(crp)), median_crp = median(crp, na.rm = TRUE),
            q1 = quantile(crp, 0.25, na.rm = TRUE), q3 = quantile(crp, 0.75, na.rm = TRUE))
kruskal.test(crp ~ district, data = hearts)

# =============================================================================
# E. AN ORDINAL OUTCOME: satisfaction (1 = very dissatisfied ... 5 = very satisfied)
# =============================================================================
# The gap between 1 and 2 need not equal the gap between 4 and 5, so a mean
# can mislead. Show the distribution, then use a rank-based test.
hearts |>
  filter(!is.na(satisfaction)) |>
  count(programme, satisfaction) |>
  group_by(programme) |>
  mutate(percent = round(100 * n / sum(n), 1))

wilcox.test(satisfaction ~ programme, data = hearts)
# With only five possible values there are many ties. With groups this large,
# R uses a normal approximation that allows for ties (no exact p-value).

# -----------------------------------------------------------------------------
# Your turn: Workbook exercises 1.7 to 1.9 and extensions E1.1 to E1.3.
# -----------------------------------------------------------------------------

