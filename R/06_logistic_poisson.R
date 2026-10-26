# =============================================================================
# 06_logistic_poisson.R                 DAY 2 PRACTICAL, PART B (20 min, guided demo)
# Introduction to logistic regression (binary outcome) and
# Poisson regression (count outcome with exposure time)
#
# Data: simulated Healthy Hearts District Study (teaching data only).
# Workbook exercises 2.5 to 2.6 and extension E2.3 refer to this script.
# This is an introduction. Using these models well takes further study.
# =============================================================================

library(dplyr)
library(ggplot2)
library(broom)
source("R/theme_neudata.R")   # Neudata colours and plot theme

hearts <- readRDS("data/hearts.rds") |>
  mutate(age10 = age / 10)

# =============================================================================
# A. LOGISTIC REGRESSION
# Outcome: high_bp_0 (Yes/No). The model is linear on the LOG-ODDS scale:
#   log(odds of high BP) = b0 + b1*smoker + b2*age10 + b3*sex
# exp(coefficient) = odds ratio (OR).
# R models the probability of the SECOND factor level ("Yes").
# =============================================================================

# Crude model: reproduces the 2 x 2 table OR from Day 1 (about 3.4)
fit_lr0 <- glm(high_bp_0 ~ smoker, family = binomial, data = hearts)
tidy(fit_lr0, conf.int = TRUE, exponentiate = TRUE)

# Adjusted model: OR for smoking among people of the same age and sex
fit_lr1 <- glm(high_bp_0 ~ smoker + age10 + sex, family = binomial, data = hearts)
tidy(fit_lr1, conf.int = TRUE, exponentiate = TRUE)
# Columns: estimate = OR (or aOR when adjusted), conf.low/conf.high = 95% CI.
# Smokers in these data are older and more often male, and age and sex both
# raise BP. Adjusting moves the OR from about 3.4 towards 2.
# aOR for age10 = multiplicative change in the odds per 10 years of age.

# Predicted probabilities are easier to explain than odds ratios
new <- expand.grid(age10 = seq(3, 7.5, by = 0.1),
                   smoker = factor(c("No", "Yes"), levels = c("No", "Yes")),
                   sex = factor("Female", levels = c("Female", "Male")))
new$prob <- predict(fit_lr1, newdata = new, type = "response")

ggplot(new, aes(x = age10 * 10, y = prob, colour = smoker)) +
  geom_line(linewidth = 1) +
  scale_colour_manual(values = unname(neudata_cols[c("teal", "blue")])) +
  scale_y_continuous(labels = scales::percent, limits = c(0, 1)) +
  labs(x = "Age (years)", y = "Predicted probability of high BP",
       colour = "Smoker", title = "Women: predicted probability of high BP")

# Checks to mention (not covered in depth):
#  * independent observations; enough events (a rough guide is at least about
#    10 events per coefficient, a heuristic, not a law); linearity of continuous
#    predictors on the log-odds scale.
#  * An OR is not a risk ratio when the outcome is common (as here).

# =============================================================================
# B. POISSON REGRESSION FOR COUNTS WITH DIFFERENT FOLLOW-UP TIMES
# Outcome: clinic_visits = number of unplanned clinic visits.
# People were followed for different lengths of time (followup_months), so
# compare RATES (visits per person-month), not raw counts.
# The OFFSET log(followup_months) tells the model about each person's exposure time.
#   log(expected visits) = log(months) + b0 + b1*programme + ...
# exp(coefficient) = incidence rate ratio (IRR).
# =============================================================================

hearts |>
  group_by(programme) |>
  summarise(people = n(), visits = sum(clinic_visits),
            person_months = sum(followup_months),
            rate_per_100_pm = 100 * visits / person_months)

fit_pois <- glm(clinic_visits ~ programme + age10 + high_bp_0 + offset(log(followup_months)),
                family = poisson, data = hearts)
tidy(fit_pois, conf.int = TRUE, exponentiate = TRUE)

# Overdispersion check: in a Poisson model the variance equals the mean.
# Real counts often vary more. Ratio of Pearson chi-square to residual df:
dispersion <- sum(residuals(fit_pois, type = "pearson")^2) / df.residual(fit_pois)
dispersion
# A value well above 1 (here about 2) means the Poisson SEs and CIs are too narrow.

# Two common remedies (give similar IRRs, wider CIs):
fit_qp <- glm(clinic_visits ~ programme + age10 + high_bp_0 + offset(log(followup_months)),
              family = quasipoisson, data = hearts)
tidy(fit_qp, conf.int = TRUE, exponentiate = TRUE)

# Extension: negative binomial regression (MASS package, comes with R)
fit_nb <- MASS::glm.nb(clinic_visits ~ programme + age10 + high_bp_0 + offset(log(followup_months)),
                       data = hearts)
tidy(fit_nb, conf.int = TRUE, exponentiate = TRUE)

# -----------------------------------------------------------------------------
# Your turn: Workbook exercises 2.5 to 2.6 and extension E2.3.
# -----------------------------------------------------------------------------

