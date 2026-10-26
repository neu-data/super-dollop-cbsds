# =============================================================================
# 02_describe_and_plot.R                         DAY 1 PRACTICAL, PART B (30 min)
# Frequencies, proportions, centre and spread; bar charts, histograms, boxplots
#
# Data: simulated Healthy Hearts District Study (teaching data only).
# Workbook exercises 1.4 to 1.6 refer to this script.
# =============================================================================

library(dplyr)
library(ggplot2)

hearts <- readRDS("data/hearts.rds")   # cleaned data (same result as script 01)

# A plain, readable look for all plots in the course
source("R/theme_neudata.R")   # Neudata colours and plot theme
course_teal <- neudata_cols[["teal"]]
course_blue <- neudata_cols[["blue"]]

# --- 1. Categorical variables: counts and proportions -----------------------
# A proportion always has a denominator. Say what it is.
count(hearts, district) |>
  mutate(percent = round(100 * n / sum(n), 1))

count(hearts, smoker) |>
  mutate(percent = round(100 * n / sum(n), 1))

# Missing values are a category of their own when you count. Here 6 people
# have no education recorded. Decide whether the denominator should include them.
count(hearts, education) |>
  mutate(percent_all = round(100 * n / sum(n), 1),
         percent_known = ifelse(is.na(education), NA,
                                round(100 * n / sum(n[!is.na(education)]), 1)))

# Bar chart: one bar per category, height = count
ggplot(hearts, aes(x = district)) +
  geom_bar(fill = course_teal, width = 0.6) +
  labs(x = "District", y = "Number of participants",
       title = "Participants by district")

# --- 2. Continuous variables: centre and spread -----------------------------
# Mean and SD describe symmetric distributions well.
# Median and IQR (25th to 75th percentile) are better for skewed data,
# because a few extreme values pull the mean and SD.
hearts |>
  summarise(n      = sum(!is.na(sbp_0)),
            mean   = mean(sbp_0),
            sd     = sd(sbp_0),
            median = median(sbp_0),
            q1     = quantile(sbp_0, 0.25),
            q3     = quantile(sbp_0, 0.75))

# na.rm = TRUE tells R to ignore missing values. Without it the result is NA.
mean(hearts$crp)
mean(hearts$crp, na.rm = TRUE)

hearts |>
  summarise(n      = sum(!is.na(crp)),
            mean   = mean(crp, na.rm = TRUE),
            sd     = sd(crp, na.rm = TRUE),
            median = median(crp, na.rm = TRUE),
            q1     = quantile(crp, 0.25, na.rm = TRUE),
            q3     = quantile(crp, 0.75, na.rm = TRUE))
# CRP: the mean is above the median and the SD is large relative to the mean.
# Both signal right skew. Report median (IQR) for CRP.

# Summaries by group
hearts |>
  group_by(district) |>
  summarise(n = n(), mean_sbp = mean(sbp_0), sd_sbp = sd(sbp_0),
            median_sbp = median(sbp_0))

# --- 3. Plots for one continuous variable -----------------------------------
# Histogram: the shape of the distribution. Try changing binwidth.
ggplot(hearts, aes(x = sbp_0)) +
  geom_histogram(binwidth = 5, fill = course_teal, colour = "white") +
  labs(x = "Systolic blood pressure at baseline (mmHg)", y = "Number of participants")

ggplot(hearts, aes(x = crp)) +
  geom_histogram(binwidth = 1, fill = course_blue, colour = "white") +
  labs(x = "C-reactive protein (mg/L)", y = "Number of participants",
       title = "CRP is right-skewed: most values are low, a few are high")
# (R warns that 14 rows were removed. These are the missing CRP values.)

# On a log scale the skewed CRP distribution looks roughly symmetric
ggplot(hearts, aes(x = crp)) +
  geom_histogram(bins = 25, fill = course_blue, colour = "white") +
  scale_x_log10() +
  labs(x = "C-reactive protein (mg/L, log scale)", y = "Number of participants")

# --- 4. Comparing a distribution across groups ------------------------------
# Boxplot: the line is the median, the box is the IQR, whiskers reach to
# the most extreme points within 1.5 x IQR, and dots beyond are drawn separately.
# Adding the raw points shows how many observations sit behind each box.
ggplot(hearts, aes(x = district, y = sbp_0)) +
  geom_boxplot(fill = neudata_mist, outlier.shape = NA, width = 0.55) +
  geom_jitter(width = 0.15, alpha = 0.35, size = 1.2) +
  labs(x = "District", y = "Systolic BP at baseline (mmHg)")

# Saving a plot for a report
dir.create("outputs", showWarnings = FALSE)
ggsave("outputs/sbp_by_district.png", width = 6, height = 4, dpi = 200)

# -----------------------------------------------------------------------------
# Your turn: Workbook exercises 1.4 to 1.6. Write your code below.
# -----------------------------------------------------------------------------

