# =============================================================================
# 01_import_and_inspect.R                        DAY 1 PRACTICAL, PART A (25 min)
# Importing data, inspecting variables and handling basic missing values
#
# Data: the Healthy Hearts District Study. These data are SIMULATED for
# teaching. Any "finding" is a property of the simulation, not of real people.
#
# How to use: run one line at a time with Ctrl+Enter and read the comments.
# Workbook exercises 1.1 to 1.3 refer to this script.
# =============================================================================

library(readr)
library(dplyr)

# --- 1. Import ---------------------------------------------------------------
# read_csv() reads a comma-separated file into a data frame (a "tibble").
# Each row is one participant (an observation); each column is a variable.
raw <- read_csv("data/hearts_raw.csv")

# Fallback if readr is not installed:  raw <- read.csv("data/hearts_raw.csv")

# --- 2. First look -----------------------------------------------------------
dim(raw)          # number of rows (participants) and columns (variables)
glimpse(raw)      # each variable, its type and the first few values
head(raw, 10)     # first 10 rows

# Ask: what does one row represent? What type is each variable?
#   <chr> = text, <dbl> = number. R does not yet know that "district" is a
#   category or that "satisfaction" (1 to 5) is an ordered rating.

# --- 3. Look for problems before analysing ----------------------------------
summary(raw)

# activity_min has a minimum of -99. Minutes of activity cannot be negative:
# -99 is a code the data-entry team used for "not recorded".
raw |> filter(activity_min < 0) |> select(id, activity_min)

# How many values are missing (NA) in each variable?
colSums(is.na(raw))

# --- 4. Clean ---------------------------------------------------------------
# (a) Recode -99 to NA so R treats it as missing, not as a real number.
# (b) Turn text categories into factors with a sensible order of levels.
#     The first level is the reference group in later comparisons.
hearts <- raw |>
  mutate(
    activity_min  = na_if(activity_min, -99),
    district      = factor(district, levels = c("North", "South", "East", "West")),
    sex           = factor(sex, levels = c("Female", "Male")),
    education     = factor(education, levels = c("Primary or less", "Secondary", "Tertiary")),
    smoker        = factor(smoker, levels = c("No", "Yes")),
    high_bp_0     = factor(high_bp_0, levels = c("No", "Yes")),
    high_bp_12    = factor(high_bp_12, levels = c("No", "Yes")),
    programme     = factor(programme, levels = c("Standard advice", "Lifestyle programme")),
    adverse_event = factor(adverse_event, levels = c("No", "Yes"))
  )

# Check the recoding worked: activity_min should now have 7 NAs and no -99
summary(hearts$activity_min)
colSums(is.na(hearts))

# Check ranges are plausible
range(hearts$age)
range(hearts$bmi, na.rm = TRUE)
range(hearts$sbp_0)

# Check categories (look for typing variants such as "north" or "N")
count(hearts, district)
count(hearts, education)

# --- 5. Missing values: what R does and what you should report --------------
# Most R functions drop rows with a missing value in the variables they use
# ("complete-case analysis"). That is acceptable for this course, but:
#   * always report how many observations each result is based on;
#   * ask WHY values are missing. 38 participants have no 12-month blood
#     pressure because they left the study early. If those who left differ
#     from those who stayed, complete-case results may be biased.
#   * do not replace missing values with the mean. It makes the data look
#     less variable than they are. (Multiple imputation is the usual remedy;
#     it is beyond this course.)
hearts |> summarise(n_total = n(), n_with_sbp_12 = sum(!is.na(sbp_12)))

# Compare those with and without 12-month data on baseline characteristics
hearts |>
  group_by(missing_sbp_12 = is.na(sbp_12)) |>
  summarise(n = n(), mean_age = mean(age), mean_sbp_0 = mean(sbp_0))

# --- 6. Save your cleaned data (optional) -----------------------------------
# The course provides the same cleaned file as data/hearts.rds, which the
# later scripts load. Saving your own copy lets you compare.
# saveRDS(hearts, "data/my_hearts_clean.rds")

# -----------------------------------------------------------------------------
# Your turn: Workbook exercises 1.1 to 1.3. Write your code below.
# -----------------------------------------------------------------------------

