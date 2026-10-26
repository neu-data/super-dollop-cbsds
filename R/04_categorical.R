# =============================================================================
# 04_categorical.R                               DAY 1 PRACTICAL, PART C (20 min)
# Contingency tables, proportions, risks, odds, RR, OR, chi-square, Fisher
#
# Data: simulated Healthy Hearts District Study (teaching data only).
# Workbook exercises 1.10 to 1.11 and extensions E1.4 to E1.6 refer to this script.
# =============================================================================

library(dplyr)
library(ggplot2)
source("R/theme_neudata.R")   # Neudata colours and plot theme

hearts <- readRDS("data/hearts.rds")

# A small helper that prints a 2 x 2 table with every measure we discuss.
# Rows = exposure (first level = unexposed), columns = outcome (No, Yes).
# CIs use the usual large-sample formulas on the log scale.
two_by_two <- function(exposure, outcome) {
  tab <- table(exposure, outcome)
  a <- tab[2, 2]; b <- tab[2, 1]   # exposed:   outcome yes, outcome no
  c <- tab[1, 2]; d <- tab[1, 1]   # unexposed: outcome yes, outcome no
  p1 <- a / (a + b); p0 <- c / (c + d)
  rr <- p1 / p0
  se_log_rr <- sqrt(1 / a - 1 / (a + b) + 1 / c - 1 / (c + d))
  or <- (a * d) / (b * c)
  se_log_or <- sqrt(1 / a + 1 / b + 1 / c + 1 / d)
  print(addmargins(tab))
  cat(sprintf("\nProportion with outcome, exposed:   %d / %d = %.3f", a, a + b, p1))
  cat(sprintf("\nProportion with outcome, unexposed: %d / %d = %.3f", c, c + d, p0))
  cat(sprintf("\nDifference in proportions: %.3f", p1 - p0))
  cat(sprintf("\nOdds, exposed:   %d / %d = %.3f", a, b, a / b))
  cat(sprintf("\nOdds, unexposed: %d / %d = %.3f", c, d, c / d))
  cat(sprintf("\nRatio of proportions (RR or PR): %.2f (95%% CI %.2f to %.2f)",
              rr, exp(log(rr) - 1.96 * se_log_rr), exp(log(rr) + 1.96 * se_log_rr)))
  cat(sprintf("\nOdds ratio (OR):                 %.2f (95%% CI %.2f to %.2f)\n",
              or, exp(log(or) - 1.96 * se_log_or), exp(log(or) + 1.96 * se_log_or)))
  invisible(tab)
}

# =============================================================================
# A. A 2 x 2 TABLE: smoking and high blood pressure at baseline
# Design note: baseline data are CROSS-SECTIONAL (measured at one time), so
# the proportions are PREVALENCES, and the ratio is a PREVALENCE RATIO (PR).
# "Risk" strictly means the proportion who develop the outcome over a period
# of follow-up, as in a cohort study or a trial.
# =============================================================================

tab_smk <- table(hearts$smoker, hearts$high_bp_0,
                 dnn = c("Smoker", "High BP (SBP >= 140)"))
tab_smk
addmargins(tab_smk)

# Row proportions: denominator = everyone in that smoking group
round(prop.table(tab_smk, margin = 1), 3)
# Column proportions answer a different question (of those with high BP,
# what proportion smoke?). Always state which denominator you used.
round(prop.table(tab_smk, margin = 2), 3)

two_by_two(hearts$smoker, hearts$high_bp_0)
# The OR (3.4) is further from 1 than the PR (2.2). This happens whenever the
# outcome is common (here 21% and 48%). Do not describe an OR of 3.4 as
# "3.4 times the risk": the prevalence is about 2.2 times higher.

# Plot the proportions, not the counts, when groups differ in size
hearts |>
  count(smoker, high_bp_0) |>
  group_by(smoker) |>
  mutate(prop = n / sum(n)) |>
  filter(high_bp_0 == "Yes") |>
  ggplot(aes(x = smoker, y = prop)) +
  geom_col(fill = neudata_cols[["teal"]], width = 0.5) +
  scale_y_continuous(labels = scales::percent, limits = c(0, 0.5)) +
  labs(x = "Smoker", y = "Proportion with high BP",
       title = "Prevalence of high BP by smoking status")

# Chi-square test of association.
# For 2 x 2 tables R applies Yates' continuity correction by default.
chisq.test(tab_smk)
chisq.test(tab_smk)$expected   # all expected counts should be reasonably large (about 5 or more)

# =============================================================================
# B. RARE OUTCOMES AND SMALL COUNTS: Fisher's exact test
# Question: Were adverse events (minor injuries) more common in the programme?
# Design: randomised trial with 12-month follow-up, so these ARE risks.
# =============================================================================

tab_ae <- table(hearts$programme, hearts$adverse_event,
                dnn = c("Group", "Adverse event"))
addmargins(tab_ae)
chisq.test(tab_ae)$expected    # smallest expected count is 8.5
# The chi-square approximation is usually adequate when all expected counts
# are about 5 or more. Fisher's exact test does not rely on that approximation,
# so it is the usual choice when expected counts are small.
fisher.test(tab_ae)            # gives a (conditional) odds ratio and exact CI
two_by_two(hearts$programme, hearts$adverse_event)
# Risk: 14/240 = 5.8% vs 3/240 = 1.2%. With only 17 events the CI for the RR
# is very wide (about 1.4 to 16): the size of the increase is uncertain.

# Older participants only: here the expected counts fall below 5
older <- filter(hearts, age >= 65)
tab_ae_older <- table(older$programme, older$adverse_event)
addmargins(tab_ae_older)
chisq.test(tab_ae_older)$expected   # R warns that the approximation may be incorrect
fisher.test(tab_ae_older)

# =============================================================================
# C. LARGER TABLES: education and smoking (3 x 2)
# =============================================================================
tab_edu <- table(hearts$education, hearts$smoker, dnn = c("Education", "Smoker"))
addmargins(tab_edu)
round(prop.table(tab_edu, margin = 1), 3)   # proportion smoking within each education level
chisq.test(tab_edu)
# A significant chi-square says the smoking proportion is not the same in all
# education groups. Look at the row proportions to see where the differences are.

# =============================================================================
# D. A FIRST LOOK AT CONFOUNDING (taken further on Day 2)
# Men smoke more than women AND have higher BP in these data. Some of the
# crude smoking-BP association may be due to sex.
# =============================================================================
round(prop.table(table(hearts$sex, hearts$smoker), 1), 3)

# Stratify: look at the smoking-BP association separately in women and men
for (s in levels(hearts$sex)) {
  cat("\n=====", s, "=====\n")
  with(filter(hearts, sex == s), two_by_two(smoker, high_bp_0))
}

# Mantel-Haenszel: one OR for smoking, adjusted for sex
mantelhaen.test(table(hearts$smoker, hearts$high_bp_0, hearts$sex))

# =============================================================================
# E. PAIRED BINARY DATA: McNemar's test (extension)
# Same people, high BP yes/no at baseline and at 12 months (programme group).
# A chi-square test would wrongly treat the two time points as independent groups.
# =============================================================================
prog <- filter(hearts, programme == "Lifestyle programme", !is.na(high_bp_12))
tab_paired <- table(Baseline = prog$high_bp_0, Month12 = prog$high_bp_12)
tab_paired
mcnemar.test(tab_paired)
# Only the discordant cells (changed status) carry information about change.

# -----------------------------------------------------------------------------
# Your turn: Workbook exercises 1.10 to 1.11 and extensions E1.4 to E1.6.
# -----------------------------------------------------------------------------

