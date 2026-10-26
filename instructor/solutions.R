# =============================================================================
# solutions.R                                         INSTRUCTOR ONLY
# Model solutions for the participant workbook exercises (Day 1, Day 2,
# extensions and the final exercise). Run from the project folder.
# Output from the latest run is in instructor/outputs/solutions.log
# Data are simulated for teaching.
# =============================================================================

library(readr)
library(dplyr)
library(ggplot2)
library(broom)
source("R/theme_neudata.R")   # Neudata colours and plot theme

# ============================== DAY 1 ========================================

# --- 1.1 Import -------------------------------------------------------------
raw <- read_csv("data/hearts_raw.csv", show_col_types = FALSE)
dim(raw)                                   # 480 participants, 19 variables

# --- 1.2 Missing values -----------------------------------------------------
colSums(is.na(raw))
sum(raw$activity_min == -99, na.rm = TRUE) # 7 coded as -99
hearts <- readRDS("data/hearts.rds")       # identical to the cleaned data
colSums(is.na(hearts))[colSums(is.na(hearts)) > 0]

# --- 1.3 Variable types: see answer key (no code) ---------------------------

# --- 1.4 Frequencies ---------------------------------------------------------
count(hearts, smoker) |> mutate(percent = round(100 * n / sum(n), 1))
hearts |> filter(!is.na(education)) |> count(education) |>
  mutate(percent = round(100 * n / sum(n), 1))

# --- 1.5 Summaries -----------------------------------------------------------
summ <- function(x) c(n = sum(!is.na(x)), mean = mean(x, na.rm = TRUE), sd = sd(x, na.rm = TRUE),
                      median = median(x, na.rm = TRUE), q1 = unname(quantile(x, 0.25, na.rm = TRUE)),
                      q3 = unname(quantile(x, 0.75, na.rm = TRUE)))
round(rbind(sbp_0 = summ(hearts$sbp_0), crp = summ(hearts$crp)), 2)

# --- 1.6 Plots ----------------------------------------------------------------
ggplot(hearts, aes(bmi)) + geom_histogram(binwidth = 1, fill = neudata_cols[["teal"]], colour = "white")
ggplot(hearts, aes(smoker, crp)) + geom_boxplot(fill = neudata_mist) + scale_y_log10()
summ(hearts$bmi)

# --- 1.7 BMI by sex: Welch t-test --------------------------------------------
hearts |> group_by(sex) |> summarise(n = sum(!is.na(bmi)), mean = mean(bmi, na.rm = TRUE),
                                     sd = sd(bmi, na.rm = TRUE))
t.test(bmi ~ sex, data = hearts)

# --- 1.8 Paired change in the Standard advice group ----------------------------
std <- hearts |> filter(programme == "Standard advice", !is.na(sbp_12))
nrow(std)
t.test(std$sbp_12, std$sbp_0, paired = TRUE)

# --- 1.9 BMI by district -----------------------------------------------------
hearts |> group_by(district) |> summarise(n = sum(!is.na(bmi)), mean = mean(bmi, na.rm = TRUE),
                                          sd = sd(bmi, na.rm = TRUE))
oneway.test(bmi ~ district, data = hearts)
pairwise.t.test(hearts$bmi, hearts$district, pool.sd = FALSE, p.adjust.method = "holm")

# --- 1.10 Sex and high BP (2 x 2) -------------------------------------------
tab_sex <- table(hearts$sex, hearts$high_bp_0)
addmargins(tab_sex)
round(prop.table(tab_sex, 1), 3)
p_m <- tab_sex["Male", "Yes"] / sum(tab_sex["Male", ])
p_f <- tab_sex["Female", "Yes"] / sum(tab_sex["Female", ])
c(prev_male = p_m, prev_female = p_f, PR = p_m / p_f,
  OR = (p_m / (1 - p_m)) / (p_f / (1 - p_f)))
chisq.test(tab_sex)
fisher.test(tab_sex)$conf.int     # an exact CI for the OR, for reference

# --- 1.11 High BP by district (4 x 2) ----------------------------------------
tab_d <- table(hearts$district, hearts$high_bp_0)
addmargins(tab_d)
round(prop.table(tab_d, 1), 3)
chisq.test(tab_d)

# --- E1.1 Kruskal-Wallis: activity by education -------------------------------
hearts |> group_by(education) |>
  summarise(n = sum(!is.na(activity_min)), median = median(activity_min, na.rm = TRUE),
            q1 = quantile(activity_min, 0.25, na.rm = TRUE), q3 = quantile(activity_min, 0.75, na.rm = TRUE))
kruskal.test(activity_min ~ education, data = hearts)

# --- E1.2 Satisfaction by sex --------------------------------------------------
hearts |> filter(!is.na(satisfaction)) |> count(sex, satisfaction) |>
  group_by(sex) |> mutate(pct = round(100 * n / sum(n), 1))
wilcox.test(satisfaction ~ sex, data = hearts)

# --- E1.3 Student vs Welch for SBP by district --------------------------------
summary(aov(sbp_0 ~ district, data = hearts))
oneway.test(sbp_0 ~ district, data = hearts)

# --- E1.4 McNemar in the Standard advice group --------------------------------
tab_std <- table(Baseline = std$high_bp_0, Month12 = std$high_bp_12)
tab_std
mcnemar.test(tab_std)

# --- E1.5 Stratify smoking and high BP by age group -------------------------
hearts <- hearts |> mutate(age_group = cut(age, c(29, 49, 74), labels = c("30-49", "50-74")))
round(prop.table(table(hearts$age_group, hearts$smoker), 1), 3)   # smokers are older
for (g in levels(hearts$age_group)) {
  t <- with(filter(hearts, age_group == g), table(smoker, high_bp_0))
  cat("\nAge", g, "\n"); print(addmargins(t))
  cat("OR =", round(t[2, 2] * t[1, 1] / (t[2, 1] * t[1, 2]), 2), "\n")
}
mantelhaen.test(table(hearts$smoker, hearts$high_bp_0, hearts$age_group))

# --- E1.6 Fisher in older participants: see 04_categorical.R ------------------

# ============================== DAY 2 ========================================
hearts <- hearts |> mutate(age10 = age / 10, bmi5 = bmi / 5, activity_hr = activity_min / 60)

# --- 2.1 Correlation ---------------------------------------------------------
ggplot(hearts, aes(bmi, sbp_0)) + geom_point(alpha = 0.4)
cor.test(~ sbp_0 + bmi, data = hearts)
cor.test(~ sbp_0 + bmi, data = hearts, method = "spearman", exact = FALSE)

# --- 2.2 Simple linear regression: SBP on BMI --------------------------------
fit_bmi <- lm(sbp_0 ~ bmi, data = hearts)
tidy(fit_bmi, conf.int = TRUE)
glance(fit_bmi)[, c("r.squared", "sigma", "nobs")]
tidy(lm(sbp_0 ~ bmi5, data = hearts), conf.int = TRUE)   # per 5 kg/m2
par(mfrow = c(2, 2)); plot(fit_bmi); par(mfrow = c(1, 1))

# --- 2.3 Smoking and SBP: crude and adjusted --------------------------------
fit_s0 <- lm(sbp_0 ~ smoker, data = hearts)
fit_s1 <- lm(sbp_0 ~ smoker + age + sex, data = hearts)
bind_rows(tidy(fit_s0, conf.int = TRUE) |> mutate(model = "crude"),
          tidy(fit_s1, conf.int = TRUE) |> mutate(model = "adjusted age, sex")) |>
  filter(term == "smokerYes") |> select(model, estimate, conf.low, conf.high, p.value)

# --- 2.4 Fitted relationship plot -----------------------------------------
fit_b2 <- lm(sbp_0 ~ bmi + age + sex, data = hearts)
tidy(fit_b2, conf.int = TRUE)
new <- expand.grid(bmi = seq(18, 37, 0.5), age = 50,
                   sex = factor(c("Female", "Male"), levels = c("Female", "Male")))
new <- cbind(new, predict(fit_b2, newdata = new, interval = "confidence"))
ggplot(new, aes(bmi, fit, colour = sex, fill = sex)) +
  geom_ribbon(aes(ymin = lwr, ymax = upr), alpha = 0.2, colour = NA) + geom_line()

# --- 2.5 Logistic regression: BMI and high BP ------------------------------
fit_lb <- glm(high_bp_0 ~ bmi5 + age10 + sex, family = binomial, data = hearts)
tidy(fit_lb, conf.int = TRUE, exponentiate = TRUE)

# --- 2.6 Poisson: smoking and clinic visits --------------------------------
fit_ps <- glm(clinic_visits ~ smoker + age10 + offset(log(followup_months)),
              family = poisson, data = hearts)
tidy(fit_ps, conf.int = TRUE, exponentiate = TRUE)
sum(residuals(fit_ps, type = "pearson")^2) / df.residual(fit_ps)
fit_qs <- update(fit_ps, family = quasipoisson)
tidy(fit_qs, conf.int = TRUE, exponentiate = TRUE)

# --- 2.7 Clustering: k = 2 versus k = 3 -------------------------------------
life <- hearts |> select(id, activity_min, diet_score, bmi) |>
  filter(!is.na(activity_min), !is.na(bmi))
z <- scale(life[, 2:4])
set.seed(2024); km2 <- kmeans(z, 2, nstart = 25)
set.seed(2024); km3 <- kmeans(z, 3, nstart = 25)
life$k2 <- factor(km2$cluster); life$k3 <- factor(km3$cluster)
life |> group_by(k2) |> summarise(n = n(), act = median(activity_min),
                                  diet = mean(diet_score), bmi = mean(bmi))
table(k2 = life$k2, k3 = life$k3)

# Instructor only: compare with the hidden simulated profile
truth <- read.csv("instructor/hearts_truth.csv")
life <- left_join(life, truth, by = "id")
table(kmeans_k3 = life$k3, true_profile = life$profile)

# --- E2.1 Programme effect: change score vs ANCOVA -------------------------
t.test(I(sbp_12 - sbp_0) ~ programme, data = hearts)$conf.int
tidy(lm(sbp_12 ~ programme + sbp_0, data = hearts), conf.int = TRUE)[2, ]

# --- E2.2 Train/test with an extra model -----------------------------------
set.seed(42)
train_rows <- sample(nrow(hearts), size = round(0.7 * nrow(hearts)))
train <- hearts[train_rows, ]; test <- hearts[-train_rows, ]
rmse <- function(m, d) sqrt(mean((d$sbp_0 - predict(m, newdata = d))^2, na.rm = TRUE))
m_mid <- lm(sbp_0 ~ age + sex + bmi, data = train)
c(train = rmse(m_mid, train), test = rmse(m_mid, test))

# --- E2.3 Negative binomial: see 06_logistic_poisson.R ------------------------

# --- E2.4 Hierarchical clustering with average linkage --------------------
hc_avg <- hclust(dist(z), method = "average")
table(average_k3 = cutree(hc_avg, 3))       # typically very unequal groups
hc_w <- hclust(dist(z), method = "ward.D2")
table(ward_k3 = cutree(hc_w, 3))

# ========================== FINAL EXERCISE ===================================
# F1 Satisfaction by programme (ordinal): see 03_compare_groups.R section E

# F2 CRP by sex (skewed continuous)
hearts |> group_by(sex) |> summarise(n = sum(!is.na(crp)), median = median(crp, na.rm = TRUE),
                                     q1 = quantile(crp, .25, na.rm = TRUE), q3 = quantile(crp, .75, na.rm = TRUE))
wilcox.test(crp ~ sex, data = hearts, conf.int = TRUE)
tt <- t.test(log(crp) ~ sex, data = hearts); exp(-diff(tt$estimate)); 1 / exp(tt$conf.int)

# F3 Diet score and SBP, adjusted for age and sex
tidy(lm(sbp_0 ~ diet_score, data = hearts), conf.int = TRUE)[2, ]
tidy(lm(sbp_0 ~ diet_score + age + sex, data = hearts), conf.int = TRUE)[2, ]

# F4 High BP at 12 months by programme (randomised; 41 missing)
tab12 <- table(hearts$programme, hearts$high_bp_12)
addmargins(tab12); round(prop.table(tab12, 1), 3)
chisq.test(tab12)
p <- prop.table(tab12, 1)[, "Yes"]; c(RR = p[2] / p[1], RD = p[2] - p[1])
tidy(glm(high_bp_12 ~ programme + high_bp_0, family = binomial, data = hearts),
     conf.int = TRUE, exponentiate = TRUE)
