# =============================================================================
# make_hearts_data.R
# Generates the SIMULATED "Healthy Hearts District Study" teaching dataset.
#
# Uses base R only, so it also works as a fallback if packages fail to install.
# All findings from these data are artefacts of the simulation and are for
# teaching only. They say nothing about real populations.
#
# Run from the project folder (the folder containing the .Rproj file):
#   source("data/make_hearts_data.R")
# Writes:
#   data/hearts_raw.csv         raw file with realistic data-entry problems
#   data/hearts.csv             cleaned file (fallback for the practicals)
#   data/hearts.rds             cleaned file with factor levels already set
#   instructor/hearts_truth.csv hidden simulated lifestyle profile (instructor only)
# =============================================================================

set.seed(15)
n <- 480

clip <- function(x, lo, hi) pmin(pmax(x, lo), hi)

# --- Baseline characteristics -------------------------------------------------
district <- sample(c("North", "South", "East", "West"), n, replace = TRUE,
                   prob = c(0.27, 0.24, 0.26, 0.23))
sex  <- sample(c("Female", "Male"), n, replace = TRUE, prob = c(0.53, 0.47))
male <- as.numeric(sex == "Male")
age  <- round(30 + 45 * rbeta(n, 1.3, 1.5))

edu_latent <- -0.03 * (age - 50) + rlogis(n)
education  <- as.character(cut(edu_latent, c(-Inf, -1.1, 0.9, Inf),
                               labels = c("Primary or less", "Secondary", "Tertiary")))
tertiary   <- as.numeric(education == "Tertiary")

smoker_p <- plogis(-2.2 + 1.0 * male + 0.045 * (age - 50) - 0.4 * tertiary)
smoker   <- ifelse(runif(n) < smoker_p, "Yes", "No")
smk      <- as.numeric(smoker == "Yes")

# Hidden lifestyle profile (drives activity, diet and BMI; used to check clustering)
prof_latent <- 0.035 * (age - 50) + 0.4 * smk + rlogis(n, scale = 0.9)
profile <- as.character(cut(prof_latent, quantile(prof_latent, c(0, 0.30, 0.75, 1)),
                            include.lowest = TRUE,
                            labels = c("Active", "Average", "Sedentary")))
pidx <- match(profile, c("Active", "Average", "Sedentary"))

activity_min <- round(rlnorm(n, log(c(320, 150, 45))[pidx], 0.45) / 5) * 5
diet_score   <- round(clip(rnorm(n, c(7.2, 5.5, 3.8)[pidx], 1.3), 0, 10))

didx <- match(district, c("North", "South", "East", "West"))
bmi  <- 26 + 0.04 * (age - 50) + c(-2.2, 0, 3.4)[pidx] +
        c(0, 0.8, 0.3, -0.5)[didx] + rnorm(n, 0, 3.2)
bmi  <- round(clip(bmi, 16.5, 48), 1)

sbp_0 <- 124 + 0.55 * (age - 50) + 0.8 * (bmi - 26) + 5 * male + 3 * smk -
         1.0 * (activity_min / 60 - 2.5) + c(0, 5, 2, -1)[didx] + rnorm(n, 0, 12)
sbp_0 <- round(sbp_0)
high_bp_0 <- ifelse(sbp_0 >= 140, "Yes", "No")

crp <- exp(log(1.8) + 0.08 * (bmi - 26) + 0.35 * smk + 0.005 * (age - 50) + rnorm(n, 0, 0.8))
crp <- round(pmax(crp, 0.1), 1)

# --- Randomised programme and 12-month follow-up -----------------------------
programme <- sample(rep(c("Standard advice", "Lifestyle programme"), each = n / 2))
prog <- as.numeric(programme == "Lifestyle programme")

sbp_12 <- round(sbp_0 - 2 - 5 * prog + rnorm(n, 0, 9))
dropout <- runif(n) < 0.08
followup_months <- ifelse(dropout, sample(2:11, n, replace = TRUE), 12)
sbp_12[dropout] <- NA
high_bp_12 <- ifelse(is.na(sbp_12), NA, ifelse(sbp_12 >= 140, "Yes", "No"))

sat_probs <- list(c(0.10, 0.20, 0.35, 0.25, 0.10), c(0.05, 0.12, 0.30, 0.33, 0.20))
satisfaction <- vapply(prog, function(p) sample(1:5, 1, prob = sat_probs[[p + 1]]), numeric(1))
satisfaction[dropout] <- NA

adverse_event <- ifelse(runif(n) < ifelse(prog == 1, 0.035, 0.01), "Yes", "No")

# Unplanned clinic visits: Poisson rate per month with extra-Poisson variation
rate   <- exp(log(0.22) + 0.015 * (age - 50) + 0.35 * (sbp_0 >= 140) + 0.2 * smk - 0.15 * prog)
frailty <- rgamma(n, shape = 3, rate = 3)
clinic_visits <- rpois(n, rate * followup_months * frailty)

hearts <- data.frame(
  id = sprintf("HH%03d", 1:n), district, sex, age, education, smoker,
  activity_min, diet_score, bmi, sbp_0, high_bp_0, crp, programme, sbp_12,
  high_bp_12, satisfaction, adverse_event, clinic_visits, followup_months,
  stringsAsFactors = FALSE
)

# --- Introduce realistic missing values --------------------------------------
hearts$bmi[sample(n, 10)]       <- NA
hearts$crp[sample(n, 14)]       <- NA
hearts$education[sample(n, 6)]  <- NA
miss_act <- sample(n, 7)
hearts$activity_min[miss_act]   <- NA

# Raw version: activity missing coded as -99, education missing as blank
raw <- hearts
raw$activity_min[miss_act] <- -99
dir.create("instructor", showWarnings = FALSE)
write.csv(raw, "data/hearts_raw.csv", row.names = FALSE, na = "")
write.csv(hearts, "data/hearts.csv", row.names = FALSE, na = "")

# Clean version with factor levels set in a sensible order
clean <- hearts
clean$district  <- factor(clean$district, levels = c("North", "South", "East", "West"))
clean$sex       <- factor(clean$sex, levels = c("Female", "Male"))
clean$education <- factor(clean$education, levels = c("Primary or less", "Secondary", "Tertiary"),
                          ordered = FALSE)
clean$smoker    <- factor(clean$smoker, levels = c("No", "Yes"))
clean$high_bp_0 <- factor(clean$high_bp_0, levels = c("No", "Yes"))
clean$high_bp_12 <- factor(clean$high_bp_12, levels = c("No", "Yes"))
clean$programme <- factor(clean$programme, levels = c("Standard advice", "Lifestyle programme"))
clean$adverse_event <- factor(clean$adverse_event, levels = c("No", "Yes"))
saveRDS(clean, "data/hearts.rds")

write.csv(data.frame(id = hearts$id, profile = profile),
          "instructor/hearts_truth.csv", row.names = FALSE)

message("Simulated Healthy Hearts data written: ", n, " participants, ",
        ncol(hearts), " variables.")
