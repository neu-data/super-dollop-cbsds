# =============================================================================
# 00_install_and_check.R          PRE-COURSE PREPARATION (do this before Day 1)
# Concepts of Biostatistics and Data Science: a two-day crash course in R
#
# 1. Open the file "Concepts-of-Biostatistics-and-Data-Science.Rproj" in RStudio.
#    (This sets the working folder so that paths such as "data/hearts.csv" work.)
# 2. Open this script and click "Source" (top right of the script pane),
#    or select all lines and press Ctrl+Enter (Cmd+Enter on a Mac).
# 3. The last line printed should say "Your computer is ready for the course."
# =============================================================================

# The course uses four add-on packages. Everything else (t-tests, regression,
# clustering) is in base R or in packages that come with R (stats, MASS, cluster).
course_packages <- c("readr", "dplyr", "ggplot2", "broom")

# Install only the packages you do not already have
to_install <- course_packages[!course_packages %in% rownames(installed.packages())]
if (length(to_install) > 0) {
  install.packages(to_install)
}

# Load each package and report its version
for (p in course_packages) {
  library(p, character.only = TRUE)
  cat(sprintf("%-8s version %s loaded\n", p, as.character(packageVersion(p))))
}
for (p in c("MASS", "cluster")) {
  cat(sprintf("%-8s version %s available (comes with R)\n", p, as.character(packageVersion(p))))
}

# Check that the course data can be read
stopifnot(file.exists("data/hearts_raw.csv"), file.exists("data/hearts.rds"))
hearts <- readRDS("data/hearts.rds")
cat("Course data found:", nrow(hearts), "rows and", ncol(hearts), "columns\n")

cat("R version:", R.version.string, "\n")
cat("Your computer is ready for the course.\n")

# -----------------------------------------------------------------------------
# If something goes wrong
# - "there is no package called ..."  Run install.packages("name") and retry.
# - "cannot open file 'data/...'"     You did not open the .Rproj file first, so
#                                     R is looking in the wrong folder.
# - No internet during the course     The cleaned data are in data/hearts.csv and
#                                     data/hearts.rds. If even these are missing,
#                                     run source("data/make_hearts_data.R"), which
#                                     rebuilds them using base R only.
# -----------------------------------------------------------------------------
