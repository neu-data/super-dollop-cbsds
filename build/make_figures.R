# =============================================================================
# build/make_figures.R          Figures for the slides and workbook (instructor)
# Run from the project folder:  Rscript build/make_figures.R
# Uses the course packages plus patchwork (only for side-by-side panels).
# All data are simulated for teaching.
# =============================================================================

library(dplyr)
library(ggplot2)
library(patchwork)
library(cluster)

hearts <- readRDS("data/hearts.rds") |>
  mutate(activity_hr = activity_min / 60, age10 = age / 10)

# Neudata palette (R/theme_neudata.R). Variable names describe the role:
# "blue" = main colour (Neudata teal), "orange" = contrast colour (Neudata blue)
source("R/theme_neudata.R")
blue <- neudata_cols[["teal"]]; orange <- neudata_cols[["blue"]]; green <- neudata_cols[["teal_light"]]
light <- neudata_mist; grey <- neudata_cols[["grey"]]
theme_set(theme_neudata(base_size = 16) +
            theme(plot.title = element_text(size = 16)))
out <- "figures"
dir.create(out, showWarnings = FALSE)
save <- function(p, name, w = 9, h = 5) ggsave(file.path(out, name), p, width = w, height = h, dpi = 200, bg = "white")

# --- Day 1: describing data ---------------------------------------------------
p <- ggplot(hearts, aes(district)) + geom_bar(fill = blue, width = 0.6) +
  geom_text(stat = "count", aes(label = after_stat(count)), vjust = -0.4, size = 5) +
  labs(x = "District", y = "Participants")
save(p, "f_bar_district.png", 7, 4.5)

p <- ggplot(hearts, aes(sbp_0)) + geom_histogram(binwidth = 5, fill = blue, colour = "white") +
  geom_vline(xintercept = mean(hearts$sbp_0), colour = orange, linewidth = 1) +
  annotate("text", x = mean(hearts$sbp_0) + 2, y = 55, hjust = 0, colour = orange, size = 5,
           label = sprintf("mean %.1f\nmedian %.0f", mean(hearts$sbp_0), median(hearts$sbp_0))) +
  labs(x = "Systolic BP at baseline (mmHg)", y = "Participants", title = "Roughly symmetric")
save(p, "f_hist_sbp.png", 8, 4.5)

crp_mean <- mean(hearts$crp, na.rm = TRUE); crp_med <- median(hearts$crp, na.rm = TRUE)
p1 <- ggplot(filter(hearts, !is.na(crp)), aes(crp)) +
  geom_histogram(binwidth = 1, fill = orange, colour = "white") +
  geom_vline(xintercept = crp_med, colour = blue, linewidth = 1) +
  geom_vline(xintercept = crp_mean, colour = neudata_cols[["navy"]], linewidth = 1, linetype = 2) +
  annotate("text", x = 8, y = 90, hjust = 0, size = 4.5,
           label = sprintf("median %.1f (solid)\nmean %.1f (dashed)", crp_med, crp_mean)) +
  labs(x = "CRP (mg/L)", y = "Participants", title = "Right-skewed")
p2 <- ggplot(filter(hearts, !is.na(crp)), aes(crp)) +
  geom_histogram(bins = 25, fill = orange, colour = "white") + scale_x_log10() +
  labs(x = "CRP (mg/L, log scale)", y = NULL, title = "Same data, log scale")
save(p1 + p2, "f_hist_crp.png", 11, 4.5)

p <- ggplot(hearts, aes(district, sbp_0)) +
  geom_boxplot(fill = light, outlier.shape = NA, width = 0.55) +
  geom_jitter(width = 0.15, alpha = 0.3, size = 1.3) +
  labs(x = "District", y = "Systolic BP (mmHg)")
save(p, "f_box_district.png", 8, 4.8)

# --- Day 1: sampling variability and confidence intervals ---------------------
# Treat the 480 participants as a "population" and draw 20 samples of 30
set.seed(7)
pop_mean <- mean(hearts$sbp_0)
samp <- lapply(1:20, function(i) {
  x <- sample(hearts$sbp_0, 30)
  tt <- t.test(x)
  data.frame(sample = i, mean = mean(x), lo = tt$conf.int[1], hi = tt$conf.int[2])
}) |> bind_rows() |> mutate(covers = lo <= pop_mean & hi >= pop_mean)
p <- ggplot(samp, aes(y = factor(sample), x = mean, xmin = lo, xmax = hi, colour = covers)) +
  geom_vline(xintercept = pop_mean, colour = grey, linetype = 2) +
  geom_errorbar(orientation = "y", width = 0.3, linewidth = 0.8) + geom_point(size = 2.5) +
  scale_colour_manual(values = c(`TRUE` = blue, `FALSE` = orange), guide = "none") +
  labs(x = "Mean SBP and 95% CI (mmHg)", y = "Sample (n = 30 each)",
       title = sprintf("20 samples from the same population (true mean %.1f, dashed)", pop_mean)) +
  theme(axis.text.y = element_blank())
save(p, "f_sampling_cis.png", 9, 5.5)

# Statistical vs practical significance (hypothetical studies, illustration)
ill <- data.frame(study = factor(c("A: large study, tiny effect", "B: small study, uncertain",
                                   "C: clear, important effect", "D: no evidence, precise"),
                                 levels = rev(c("A: large study, tiny effect", "B: small study, uncertain",
                                                "C: clear, important effect", "D: no evidence, precise"))),
                  est = c(1, 6, 9, 0.3), lo = c(0.4, -2, 6.5, -1.2), hi = c(1.6, 14, 11.5, 1.8))
p <- ggplot(ill, aes(y = study, x = est, xmin = lo, xmax = hi)) +
  annotate("rect", xmin = -Inf, xmax = 5, ymin = -Inf, ymax = Inf, fill = light) +
  geom_vline(xintercept = 0, colour = grey) +
  geom_vline(xintercept = 5, colour = orange, linetype = 2) +
  geom_errorbar(orientation = "y", width = 0.25, linewidth = 1, colour = blue) + geom_point(size = 3, colour = blue) +
  annotate("text", x = 5.2, y = 4.45, hjust = 0, colour = orange, size = 4.5,
           label = "smallest difference that matters (5 mmHg)") +
  labs(x = "Difference in mean SBP (mmHg) with 95% CI", y = NULL,
       title = "Illustration: what the CI tells you that a p-value does not")
save(p, "f_significance_vs_importance.png", 10, 4.8)

# --- Day 1: comparing groups -------------------------------------------------
tt <- t.test(sbp_0 ~ sex, data = hearts)
p <- hearts |> group_by(sex) |>
  summarise(m = mean(sbp_0), lo = t.test(sbp_0)$conf.int[1], hi = t.test(sbp_0)$conf.int[2]) |>
  ggplot(aes(sex, m)) +
  geom_jitter(data = hearts, aes(sex, sbp_0), width = 0.15, alpha = 0.2, colour = grey) +
  geom_errorbar(aes(ymin = lo, ymax = hi), width = 0.15, linewidth = 1, colour = blue) +
  geom_point(size = 4, colour = blue) +
  labs(x = NULL, y = "Systolic BP (mmHg)",
       title = sprintf("Men - women: %.1f mmHg (95%% CI %.1f to %.1f)",
                       diff(tt$estimate), -tt$conf.int[2], -tt$conf.int[1]))
save(p, "f_ttest_sex.png", 7, 5)

prog <- filter(hearts, programme == "Lifestyle programme", !is.na(sbp_12))
set.seed(1)
s40 <- slice_sample(prog, n = 40)
long <- bind_rows(data.frame(id = s40$id, time = "Baseline", sbp = s40$sbp_0),
                  data.frame(id = s40$id, time = "12 months", sbp = s40$sbp_12)) |>
  mutate(time = factor(time, levels = c("Baseline", "12 months")))
p1 <- ggplot(long, aes(time, sbp, group = id)) + geom_line(colour = "grey70") +
  geom_point(colour = blue) + labs(x = NULL, y = "Systolic BP (mmHg)", title = "Each line is one person")
tp <- t.test(prog$sbp_12, prog$sbp_0, paired = TRUE)
ti <- t.test(prog$sbp_12, prog$sbp_0)
ci <- data.frame(analysis = factor(c("Paired (correct)", "Independent (wrong)"),
                                   levels = c("Independent (wrong)", "Paired (correct)")),
                 est = c(tp$estimate, diff(rev(ti$estimate))), lo = c(tp$conf.int[1], ti$conf.int[1]),
                 hi = c(tp$conf.int[2], ti$conf.int[2]))
p2 <- ggplot(ci, aes(y = analysis, x = est, xmin = lo, xmax = hi)) +
  geom_vline(xintercept = 0, colour = grey) +
  geom_errorbar(orientation = "y", width = 0.2, linewidth = 1, colour = c(blue, orange)) +
  geom_point(size = 3, colour = c(blue, orange)) +
  labs(x = "Mean change (mmHg), 95% CI", y = NULL, title = "Same mean, different precision")
save(p1 + p2 + plot_layout(widths = c(1, 1.3)), "f_paired.png", 11, 4.8)

p <- hearts |> group_by(district) |>
  summarise(m = mean(sbp_0), lo = t.test(sbp_0)$conf.int[1], hi = t.test(sbp_0)$conf.int[2]) |>
  ggplot(aes(district, m)) +
  geom_jitter(data = hearts, aes(district, sbp_0), width = 0.15, alpha = 0.2, colour = grey) +
  geom_errorbar(aes(ymin = lo, ymax = hi), width = 0.15, linewidth = 1, colour = blue) +
  geom_point(size = 4, colour = blue) +
  coord_cartesian(ylim = c(110, 150)) +
  labs(x = "District", y = "Mean SBP with 95% CI (mmHg)", title = "Points: individuals (axis cropped)")
save(p, "f_anova_district.png", 8, 5)

# --- Day 1: categorical ----------------------------------------------------
pr <- hearts |> count(smoker, high_bp_0) |> group_by(smoker) |>
  mutate(N = sum(n), prop = n / N) |> filter(high_bp_0 == "Yes")
p <- ggplot(pr, aes(smoker, prop)) + geom_col(fill = blue, width = 0.5) +
  geom_text(aes(label = sprintf("%d / %d = %.0f%%", n, N, 100 * prop)), vjust = -0.5, size = 5) +
  scale_y_continuous(labels = scales::percent, limits = c(0, 0.6)) +
  labs(x = "Smoker", y = "Prevalence of high BP")
save(p, "f_prev_smoking.png", 6.5, 4.8)

# How the OR relates to the RR as the outcome becomes common
or_rr <- expand.grid(p0 = seq(0.01, 0.6, 0.01), RR = c(1.5, 2, 3)) |>
  filter(p0 * RR < 0.99) |>
  mutate(p1 = p0 * RR, OR = (p1 / (1 - p1)) / (p0 / (1 - p0)))
p <- ggplot(or_rr, aes(p0, OR, colour = factor(RR))) + geom_line(linewidth = 1.2) +
  geom_hline(aes(yintercept = RR, colour = factor(RR)), linetype = 2) +
  scale_colour_manual(values = c(blue, orange, green), name = "True RR") +
  scale_x_continuous(labels = scales::percent) +
  coord_cartesian(ylim = c(1, 10)) +
  labs(x = "Risk in the unexposed group", y = "Odds ratio",
       title = "OR is close to RR only when the outcome is rare (dashed = RR)")
save(p, "f_or_vs_rr.png", 9, 5)

# --- Day 2: correlation and regression ------------------------------------
p <- ggplot(hearts, aes(age, sbp_0)) + geom_point(alpha = 0.35, colour = grey) +
  geom_smooth(method = "lm", formula = y ~ x, colour = blue, fill = green) +
  labs(x = "Age (years)", y = "Systolic BP (mmHg)", title = "r = 0.50; slope 6.6 mmHg per 10 years")
save(p, "f_scatter_age.png", 8, 5)

set.seed(3)
x <- rnorm(150)
cex <- bind_rows(
  data.frame(x = x, y = 0.3 * x + rnorm(150), panel = "Weak linear"),
  data.frame(x = x, y = 0.9 * x + rnorm(150, sd = 0.4), panel = "Strong linear"),
  data.frame(x = x, y = x^2 + rnorm(150, sd = 0.3), panel = "Curved"),
  data.frame(x = c(rnorm(29), 6), y = c(rnorm(29), 6), panel = "One outlier")
) |> group_by(panel) |> mutate(lab = sprintf("r = %.2f", cor(x, y))) |> ungroup() |>
  mutate(panel = factor(panel, levels = c("Weak linear", "Strong linear", "Curved", "One outlier")))
p <- ggplot(cex, aes(x, y)) + geom_point(alpha = 0.5, colour = blue) +
  geom_text(data = distinct(cex, panel, lab), aes(x = -Inf, y = Inf, label = lab),
            hjust = -0.1, vjust = 1.3, size = 5) +
  facet_wrap(~panel, nrow = 1, scales = "free") +
  labs(x = NULL, y = NULL, title = "Always plot: r summarises only straight-line association (simulated)") +
  theme(axis.text = element_blank())
save(p, "f_correlation_examples.png", 12, 3.8)

fit1 <- lm(sbp_0 ~ age, data = hearts)
set.seed(5)
xc <- runif(200, 0, 10); yc <- 2 + 0.2 * (xc - 5)^2 + rnorm(200, sd = 0.8)
fitc <- lm(yc ~ xc)
rd <- bind_rows(data.frame(fitted = fitted(fit1), resid = resid(fit1), panel = "SBP ~ age: no pattern"),
                data.frame(fitted = fitted(fitc), resid = resid(fitc), panel = "Curved relationship fitted as a line (simulated)"))
p <- ggplot(rd, aes(fitted, resid)) + geom_hline(yintercept = 0, colour = grey) +
  geom_point(alpha = 0.4, colour = blue) +
  geom_smooth(method = "loess", formula = y ~ x, se = FALSE, colour = orange) +
  facet_wrap(~panel, scales = "free") + labs(x = "Fitted values", y = "Residuals")
save(p, "f_residuals.png", 11, 4.5)

m1 <- lm(sbp_0 ~ activity_hr, data = hearts)
m2 <- lm(sbp_0 ~ activity_hr + age + sex, data = hearts)
m3 <- lm(sbp_0 ~ activity_hr + age + sex + bmi, data = hearts)
co <- bind_rows(lapply(list(m1, m2, m3), function(m) {
  ci <- confint(m)["activity_hr", ]
  data.frame(est = coef(m)["activity_hr"], lo = ci[1], hi = ci[2])
})) |> mutate(model = factor(c("1. Crude", "2. + age, sex (confounders)", "3. + BMI (mediator)"),
                             levels = rev(c("1. Crude", "2. + age, sex (confounders)", "3. + BMI (mediator)"))))
p <- ggplot(co, aes(y = model, x = est, xmin = lo, xmax = hi)) +
  geom_vline(xintercept = 0, colour = grey) +
  geom_errorbar(orientation = "y", width = 0.2, linewidth = 1, colour = blue) + geom_point(size = 3.5, colour = blue) +
  geom_text(aes(label = sprintf("%.2f", est)), vjust = -1.1, size = 5) +
  labs(x = "Difference in mean SBP per extra hour of activity/week (mmHg), 95% CI", y = NULL)
save(p, "f_crude_adjusted.png", 10, 4.2)

new <- expand.grid(activity_hr = seq(0, 10, 0.25), age = 50,
                   sex = factor(c("Female", "Male"), levels = c("Female", "Male")))
new <- cbind(new, predict(m2, newdata = new, interval = "confidence"))
p <- ggplot(new, aes(activity_hr, fit, colour = sex, fill = sex)) +
  geom_ribbon(aes(ymin = lwr, ymax = upr), alpha = 0.2, colour = NA) + geom_line(linewidth = 1.2) +
  scale_colour_manual(values = c(blue, orange)) + scale_fill_manual(values = c(blue, orange)) +
  labs(x = "Physical activity (hours/week)", y = "Predicted mean SBP (mmHg)", colour = NULL, fill = NULL,
       title = "Fitted SBP at age 50 (model 2), with 95% CI")
save(p, "f_fitted_activity.png", 8.5, 5)

lr <- glm(high_bp_0 ~ smoker + age10 + sex, family = binomial, data = hearts)
nl <- expand.grid(age10 = seq(3, 7.5, 0.05), smoker = factor(c("No", "Yes"), levels = c("No", "Yes")),
                  sex = factor("Female", levels = c("Female", "Male")))
nl$prob <- predict(lr, newdata = nl, type = "response")
p <- ggplot(nl, aes(age10 * 10, prob, colour = smoker)) + geom_line(linewidth = 1.3) +
  scale_colour_manual(values = c(blue, orange), name = "Smoker") +
  scale_y_continuous(labels = scales::percent, limits = c(0, 1)) +
  labs(x = "Age (years)", y = "Predicted probability of high BP", title = "Women: logistic model with smoking, age and sex")
save(p, "f_logistic_curve.png", 8.5, 5)

pv <- hearts |> mutate(age_group = cut(age, c(29, 44, 59, 74), labels = c("30-44", "45-59", "60-74"))) |>
  group_by(age_group, high_bp_0) |>
  summarise(visits = sum(clinic_visits), pm = sum(followup_months), .groups = "drop") |>
  mutate(rate = 100 * visits / pm, lo = 100 * qchisq(0.025, 2 * visits) / 2 / pm,
         hi = 100 * qchisq(0.975, 2 * (visits + 1)) / 2 / pm)
p <- ggplot(pv, aes(age_group, rate, colour = high_bp_0)) +
  geom_pointrange(aes(ymin = lo, ymax = hi), position = position_dodge(0.4), size = 0.8, linewidth = 1) +
  scale_colour_manual(values = c(blue, orange), name = "High BP") +
  labs(x = "Age group", y = "Visits per 100 person-months (95% CI)", title = "Rates use person-time as the denominator")
save(p, "f_poisson_rates.png", 8.5, 5)

# --- Day 2: clustering --------------------------------------------------------
life <- hearts |> select(id, activity_min, diet_score, bmi) |> filter(!is.na(activity_min), !is.na(bmi))
z <- scale(life[, 2:4])
set.seed(2024); km <- kmeans(z, 3, nstart = 25)
set.seed(2024); kmr <- kmeans(life[, 2:4], 3, nstart = 25)
life$scaled <- factor(km$cluster); life$unscaled <- factor(kmr$cluster)
pal3 <- c(blue, orange, green)
pa <- ggplot(life, aes(activity_min, bmi, colour = unscaled)) + geom_point(alpha = 0.6) +
  scale_colour_manual(values = pal3, guide = "none") +
  labs(x = "Activity (min/week)", y = "BMI", title = "Unscaled: split by activity only")
pb <- ggplot(life, aes(activity_min, bmi, colour = scaled)) + geom_point(alpha = 0.6) +
  scale_colour_manual(values = pal3, guide = "none") +
  labs(x = "Activity (min/week)", y = "BMI", title = "Scaled: all three variables count")
save(pa + pb, "f_kmeans_scaling.png", 11, 4.8)

set.seed(2024)
wss <- sapply(1:8, function(k) kmeans(z, k, nstart = 25)$tot.withinss)
sil <- sapply(2:8, function(k) mean(silhouette(kmeans(z, k, nstart = 25)$cluster, dist(z))[, 3]))
pe <- ggplot(data.frame(k = 1:8, wss), aes(k, wss)) + geom_line(colour = grey) +
  geom_point(size = 3, colour = blue) + scale_x_continuous(breaks = 1:8) +
  labs(x = "k", y = "Within-cluster sum of squares", title = "Elbow: no sharp bend")
ps <- ggplot(data.frame(k = 2:8, sil), aes(k, sil)) + geom_line(colour = grey) +
  geom_point(size = 3, colour = blue) + scale_x_continuous(breaks = 2:8) +
  coord_cartesian(ylim = c(0, 0.6)) +
  labs(x = "k", y = "Average silhouette width", title = "Silhouette: all below 0.35")
save(pe + ps, "f_choose_k.png", 11, 4.5)

hc <- hclust(dist(z), method = "ward.D2")
png(file.path(out, "f_dendrogram.png"), width = 9, height = 4.8, units = "in", res = 200)
par(mar = c(1, 4, 3, 1))
plot(hc, labels = FALSE, hang = -1, main = "Hierarchical clustering (Ward), cut into 3 groups",
     xlab = "", sub = "", ylab = "Merge height", cex.main = 1.3)
rect.hclust(hc, k = 3, border = pal3)
dev.off()

message("Figures written to ", out)
