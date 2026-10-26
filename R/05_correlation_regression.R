# =============================================================================
# 05_correlation_regression.R                     DAY 2 PRACTICAL, PART A (50 min)
# Scatterplots, correlation, simple and multiple linear regression,
# confounding, mediators, model checks and plots of fitted relationships
#
# Data: simulated Healthy Hearts District Study (teaching data only).
# Workbook exercises 2.1 to 2.4 and extensions E2.1 to E2.2 refer to this script.
# =============================================================================

library(dplyr)
library(ggplot2)
library(broom)
source("R/theme_neudata.R")   # Neudata colours and plot theme

hearts <- readRDS("data/hearts.rds") |>
  mutate(activity_hr = activity_min / 60,   # hours of activity per week
         age10       = age / 10)            # age in decades

# =============================================================================
# A. SCATTERPLOTS AND CORRELATION
# =============================================================================

ggplot(hearts, aes(x = age, y = sbp_0)) +
  geom_point(alpha = 0.4, colour = neudata_cols[["teal"]]) +
  labs(x = "Age (years)", y = "Systolic BP at baseline (mmHg)")

# Pearson's r measures the strength of a LINEAR association (-1 to +1)
cor.test(~ sbp_0 + age, data = hearts)

# Spearman's rho uses ranks: it measures a MONOTONIC association
# (one variable tends to rise as the other rises), and is less affected by
# outliers and skew. Useful for CRP and activity, which are both skewed.
ggplot(hearts, aes(x = activity_hr, y = crp)) +
  geom_point(alpha = 0.4, colour = neudata_cols[["teal"]]) +
  labs(x = "Physical activity (hours/week)", y = "CRP (mg/L)")
cor.test(~ crp + activity_hr, data = hearts, method = "spearman", exact = FALSE)

# Correlation is not causation, and r says nothing about the SIZE of the
# change in y per unit of x. For that we need regression.

# =============================================================================
# B. SIMPLE LINEAR REGRESSION: SBP and age
#    sbp_0 = b0 + b1 * age + error
# =============================================================================

fit1 <- lm(sbp_0 ~ age, data = hearts)
summary(fit1)
confint(fit1)
tidy(fit1, conf.int = TRUE)     # the same numbers as a tidy table

# Reading the output:
#  * (Intercept) b0: predicted mean SBP at age 0. Not meaningful on its own
#    because nobody in the data is under 30. It anchors the line.
#  * age b1: the difference in mean SBP for each 1-year difference in age.
#  * Residual standard error: typical distance of points from the line (mmHg).
#  * R-squared: proportion of the variation in SBP explained by age.

# A slope per decade is easier to talk about
fit1b <- lm(sbp_0 ~ age10, data = hearts)
tidy(fit1b, conf.int = TRUE)

# The fitted line with its 95% confidence band (uncertainty about the MEAN)
ggplot(hearts, aes(x = age, y = sbp_0)) +
  geom_point(alpha = 0.35, colour = "grey45") +
  geom_smooth(method = "lm", formula = y ~ x, colour = neudata_cols[["teal"]], fill = neudata_cols[["teal_light"]]) +
  labs(x = "Age (years)", y = "Systolic BP at baseline (mmHg)")

# =============================================================================
# C. MODEL CHECKS: look at the residuals (observed minus fitted)
# Assumptions of linear regression, in order of importance:
#   1. Independent observations (comes from the design, not from a plot)
#   2. Linearity: the mean of y changes linearly with x
#   3. Constant spread of residuals (homoscedasticity)
#   4. Residuals approximately normal (matters least in large samples,
#      mainly for prediction intervals and small-sample CIs)
# The outcome itself does NOT need to be normally distributed.
# =============================================================================

par(mfrow = c(2, 2))
plot(fit1)
par(mfrow = c(1, 1))
# Top left (Residuals vs Fitted): look for curves or a funnel shape.
# Top right (Q-Q): points near the line suggest approximately normal residuals.
# Bottom left (Scale-Location): spread constant across fitted values?
# Bottom right (Residuals vs Leverage): any single point with a big influence?

# =============================================================================
# D. MULTIPLE LINEAR REGRESSION: adjusted associations and confounding
# Question: Is physical activity associated with lower SBP?
# =============================================================================

# Crude (unadjusted) association
fit_crude <- lm(sbp_0 ~ activity_hr, data = hearts)

# Older people are less active AND have higher SBP. Age could be a
# CONFOUNDER: a common cause of activity and SBP. Sex too.
cor.test(~ activity_hr + age, data = hearts)

fit_adj <- lm(sbp_0 ~ activity_hr + age + sex, data = hearts)
summary(fit_adj)

# BMI is different. Activity may lower BMI, and BMI raises SBP:
#   activity -> BMI -> SBP.  BMI is (partly) a MEDIATOR on the path.
# Adjusting for a mediator removes part of the effect we want to estimate.
fit_med <- lm(sbp_0 ~ activity_hr + age + sex + bmi, data = hearts)

# Compare the activity coefficient across the three models
bind_rows(
  tidy(fit_crude, conf.int = TRUE) |> mutate(model = "1. Crude"),
  tidy(fit_adj,   conf.int = TRUE) |> mutate(model = "2. Adjusted for age and sex"),
  tidy(fit_med,   conf.int = TRUE) |> mutate(model = "3. Also adjusted for BMI (mediator)")
) |>
  filter(term == "activity_hr") |>
  select(model, estimate, conf.low, conf.high, p.value)

# Interpretation of model 2: "Among people of the same age and sex, each extra
# hour of activity per week was associated with a mean SBP about 1.6 mmHg lower."
# Model 2 targets the TOTAL association of activity (not via confounders).
# Model 3 estimates the part NOT passing through BMI. Neither is "more correct";
# they answer different questions. Choose adjustment variables from your
# understanding of the causes (draw a diagram), not from p-values.
# NB: The models use different numbers of people because of missing values.
nobs(fit_crude); nobs(fit_adj); nobs(fit_med)

# A categorical predictor: district. R creates indicator (dummy) variables;
# each coefficient is a difference from the reference level (North).
fit_district <- lm(sbp_0 ~ district + age + sex, data = hearts)
tidy(fit_district, conf.int = TRUE)
# Without age and sex this model gives the same F-test as one-way ANOVA (Day 1):
anova(lm(sbp_0 ~ district, data = hearts))

# Check the multiple regression model as before
par(mfrow = c(2, 2)); plot(fit_adj); par(mfrow = c(1, 1))

# =============================================================================
# E. PLOTTING A FITTED RELATIONSHIP FROM A MULTIPLE REGRESSION
# Predicted mean SBP across activity, for women and men aged 50
# =============================================================================
new <- expand.grid(activity_hr = seq(0, 10, by = 0.25), age = 50,
                   sex = factor(c("Female", "Male"), levels = c("Female", "Male")))
pred <- predict(fit_adj, newdata = new, interval = "confidence")
new <- cbind(new, pred)

ggplot(new, aes(x = activity_hr, y = fit, colour = sex, fill = sex)) +
  geom_ribbon(aes(ymin = lwr, ymax = upr), alpha = 0.2, colour = NA) +
  geom_line(linewidth = 1) +
  scale_colour_manual(values = unname(neudata_cols[c("teal", "blue")])) +
  scale_fill_manual(values = unname(neudata_cols[c("teal", "blue")])) +
  labs(x = "Physical activity (hours/week)", y = "Predicted mean SBP (mmHg)",
       colour = NULL, fill = NULL, title = "Fitted SBP at age 50, with 95% CI")

# =============================================================================
# F. EXTENSION: estimating the programme effect with baseline adjustment
# In a randomised trial, adjusting the follow-up value for its baseline value
# (often called ANCOVA) usually gives a more precise estimate than comparing
# change scores.
# =============================================================================
fit_trial <- lm(sbp_12 ~ programme + sbp_0, data = hearts)
tidy(fit_trial, conf.int = TRUE)

# =============================================================================
# G. EXTENSION: prediction and train/test separation
# For PREDICTION, judge a model on data it has not seen. Split first, fit on the
# training set, evaluate once on the test set.
# Leakage: any information from the test set (or from the future) used while
# building the model, e.g. choosing variables using all the data, or using
# sbp_12 to predict high_bp_12. It makes performance look better than it is.
# =============================================================================
set.seed(42)
train_rows <- sample(nrow(hearts), size = round(0.7 * nrow(hearts)))
train <- hearts[train_rows, ]
test  <- hearts[-train_rows, ]

m_small <- lm(sbp_0 ~ age, data = train)
m_big   <- lm(sbp_0 ~ age + sex + bmi + activity_hr + smoker + district, data = train)

rmse <- function(model, data) {
  pred <- predict(model, newdata = data)
  sqrt(mean((data$sbp_0 - pred)^2, na.rm = TRUE))
}
c(train_small = rmse(m_small, train), test_small = rmse(m_small, test),
  train_big   = rmse(m_big, train),   test_big   = rmse(m_big, test))
# RMSE = typical prediction error in mmHg. Test error is the honest one.

# -----------------------------------------------------------------------------
# Your turn: Workbook exercises 2.1 to 2.4 and extensions E2.1 to E2.2.
# -----------------------------------------------------------------------------

