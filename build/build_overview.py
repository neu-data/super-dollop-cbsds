"""Course overview, prerequisites, learning outcomes, timetable and pre-course preparation.
Run from the project folder:  python build/build_overview.py
"""
import os
from docx_helpers import Doc, ROOT

doc = Doc("Concepts of Biostatistics and Data Science",
          "A two-day crash course with practical analysis in R: overview, timetable and pre-course preparation",
          header_text="Concepts of Biostatistics and Data Science  |  Crash course overview",
          byline="Neudata Consulting Ltd  ·  Version 1.0  ·  26-10-2026")

doc.h1("About the crash course")
doc.p("Concepts of Biostatistics and Data Science is a two-day crash course for teaching the core ideas of "
      "biostatistics and the first steps of data science. It is designed to be delivered as a short, intensive "
      "course: each day has two hours of explanation and two hours of guided analysis in R. The emphasis is on "
      "choosing a method for a stated question, checking its assumptions and interpreting the result in plain "
      "language. R commands are taught as the means to that end.")
doc.p("As a crash course it covers the essentials and points to further learning rather than trying to teach "
      "every method in depth. Trainers can use the slides, workbook, scripts and reference pack as a complete "
      "package, or take individual sessions for shorter teaching.")
doc.p("Day 1 covers understanding data and making comparisons: research questions, variables and data quality, "
      "descriptive statistics and plots, sampling variability, confidence intervals and tests, comparisons of "
      "two or more groups, and associations between categorical variables. Day 2 moves from relationships "
      "between variables to simple and multiple linear regression, confounding and mediation, model checking, "
      "and short introductions to logistic regression, Poisson regression, prediction and clustering.")
doc.note("All examples use one simulated dataset, the Healthy Hearts District Study. It was generated with known "
         "rules so that results can be checked. Any finding from it applies only to the simulation and is for "
         "teaching.")

doc.h2("Who it is for")
doc.bullets([
    "People with little statistical training who need to understand or carry out basic analyses",
    "Data enthusiasts who want a sound statistical footing for working with data",
    "Participants with some working knowledge who want to strengthen their understanding and practical "
    "skills. Optional extension exercises are provided for them.",
])

doc.h2("Prerequisites")
doc.bullets([
    "Comfort with basic arithmetic, percentages and reading a simple graph",
    "No previous statistics course is required",
    "No previous R experience is required, but completing the pre-course preparation (below) is essential",
    "A laptop on which you can install software (Windows, macOS or Linux)",
])

doc.h1("Learning outcomes")
doc.p("By the end of the course participants will be able to:")
doc.table([
    ["#", "Outcome", "Day", "How it is practised"],
    ["1", "Identify observations, variables and variable types in a dataset, and state a research question in terms of an outcome, exposure or groups, and design", "1", "Workbook 1.1 to 1.3"],
    ["2", "Import a CSV file into R, check for missing and implausible values, and recode a missing-value code", "1", "Workbook 1.1 to 1.2"],
    ["3", "Calculate and report counts with denominators, proportions, mean (SD) and median (IQR), and justify the choice", "1", "Workbook 1.4 to 1.5"],
    ["4", "Produce and describe a bar chart, histogram and boxplot", "1", "Workbook 1.6"],
    ["5", "Interpret a 95% confidence interval and a p-value correctly, and distinguish statistical significance from practical importance", "1", "Workbook 1.7 to 1.9"],
    ["6", "Compare two or more independent groups with Welch's t-test, ANOVA, Wilcoxon rank-sum or Kruskal-Wallis tests, and explain what each compares", "1", "Workbook 1.7, 1.9, E1.1"],
    ["7", "Recognise paired data and analyse it with a paired method", "1", "Workbook 1.8, E1.4"],
    ["8", "Analyse a contingency table: proportions with explicit denominators, risk or prevalence ratio, odds ratio, chi-square and Fisher's exact tests", "1", "Workbook 1.10 to 1.11"],
    ["9", "Describe a relationship with a scatterplot and correlation, and explain why association is not causation", "2", "Workbook 2.1"],
    ["10", "Fit, interpret and check simple and multiple linear regression models, including adjusted associations", "2", "Workbook 2.2 to 2.4"],
    ["11", "Explain confounding and mediation with a causal diagram, and decide what to adjust for", "2", "Workbook 2.3"],
    ["12", "Read and interpret the output of a logistic regression (OR, aOR) and a Poisson regression with an offset (IRR), including a check for overdispersion", "2", "Workbook 2.5 to 2.6 (guided)"],
    ["13", "Explain the difference between describing, estimating associations, predicting and discovering groups, including train/test separation and data leakage", "2", "Slides; extension E2.2"],
    ["14", "Run and interpret a k-means clustering with scaled variables, and explain why clusters need checking", "2", "Workbook 2.7 (guided)"],
    ["15", "Choose an analysis for a stated question, produce a suitable plot and write a plain-language conclusion", "2", "Final exercise"],
], widths=[0.8, 10, 1, 4.6], size=9)

doc.h2("What is practised, demonstrated or left for further reading")
doc.p("Eight hours is enough to build sound foundations, not to master every method. The table sets realistic "
      "expectations.")
doc.table([
    ["Level", "Topics"],
    ["Practised in R (core pathway)", "Importing and checking data; descriptive statistics and plots; Welch t-test; paired t-test; one-way ANOVA with pairwise comparisons; chi-square and Fisher's exact tests; risks, odds, RR and OR; correlation; simple and multiple linear regression; residual checks; plotting fitted values"],
    ["Guided demonstration (run the code, interpret the output)", "Wilcoxon and Kruskal-Wallis tests; Mantel-Haenszel adjustment; logistic regression and aOR; Poisson regression with offset and overdispersion; k-means clustering"],
    ["Short demonstration or extension", "McNemar's test; ANCOVA for a trial; train/test split and RMSE; negative binomial regression; hierarchical clustering; interaction terms"],
    ["Further learning (signposted only)", "Ordinal and multinomial regression; survival analysis; mixed models and GEE for repeated or clustered data; multiple imputation; formal causal inference; machine learning beyond the basics"],
], widths=[4.5, 11.9], size=9.5)

doc.h1("Timetable")
doc.p("Each day has 240 minutes of teaching: 120 minutes of theory and 120 minutes of practical work. The break "
      "is listed separately and is not counted in teaching time. Clock times are an example and can be shifted.")
doc.h2("Day 1: Understanding data and making comparisons")
doc.table([
    ["Time", "Minutes", "Session", "Content", "Materials"],
    ["09:00", "10", "Theory", "Welcome, aims, the course dataset, how the days work", "Day 1 slides 1 to 4"],
    ["09:10", "20", "Theory", "Questions, observations, variables and types; data quality and missing values", "Slides, Part 1"],
    ["09:30", "25", "Theory", "Counts and proportions; mean, SD, median, IQR; skewness; bar charts, histograms, boxplots", "Slides, Part 2"],
    ["09:55", "25", "Theory", "Samples and populations; variability; SE and CIs; effect sizes; p-values; significance vs importance", "Slides, Part 3"],
    ["10:20", "22", "Theory", "Independent vs paired; Welch t-test; skewed outcomes; paired t-test; ANOVA, pairwise comparisons, Kruskal-Wallis", "Slides, Part 4"],
    ["10:42", "18", "Theory", "Contingency tables; risks, odds, RR, OR; design and measures; chi-square, Fisher; first look at confounding; McNemar", "Slides, Part 5"],
    ["11:00", "(30)", "Break", "Not counted in teaching time", ""],
    ["11:30", "25", "Practical A", "Import, inspect, recode -99, missing values, factor levels", "01_import_and_inspect.R; workbook 1.1 to 1.3"],
    ["11:55", "30", "Practical B", "Frequencies, summaries, histograms, boxplots", "02_describe_and_plot.R; 1.4 to 1.6"],
    ["12:25", "35", "Practical C1", "t-tests, log scale, Wilcoxon, paired t-test, ANOVA", "03_compare_groups.R; 1.7 to 1.9"],
    ["13:00", "20", "Practical C2", "2 x 2 tables, RR and OR, chi-square, Fisher", "04_categorical.R; 1.10 to 1.11"],
    ["13:20", "10", "Review", "Questions, common mistakes, preview of Day 2", ""],
    ["", "240", "Total", "120 theory + 120 practical", ""],
], widths=[1.3, 1.5, 2.1, 7.6, 3.9], size=9)

doc.h2("Day 2: Regression and an introduction to data science")
doc.table([
    ["Time", "Minutes", "Session", "Content", "Materials"],
    ["09:00", "10", "Theory", "Recap; describing, estimating associations, predicting, discovering groups", "Day 2 slides 1 to 6"],
    ["09:10", "15", "Theory", "Scatterplots; Pearson and Spearman correlation; association and causation", "Slides, Part 1"],
    ["09:25", "20", "Theory", "Simple linear regression: the line, output, assumptions, residuals, categorical predictors", "Slides, Part 2"],
    ["09:45", "25", "Theory", "Multiple regression; confounders and mediators; choosing adjustment variables; interpreting coefficients", "Slides, Part 3"],
    ["10:10", "10", "Theory", "Plotting fitted relationships; effect modification", "Slides, Part 3"],
    ["10:20", "20", "Theory", "Logistic regression (OR, aOR, probabilities); Poisson regression (rates, offsets, overdispersion)", "Slides, Part 4"],
    ["10:40", "20", "Theory", "Explaining vs predicting; train/test and leakage; k-means, scaling, choosing k, hierarchical clustering; further learning", "Slides, Part 5"],
    ["11:00", "(30)", "Break", "Not counted in teaching time", ""],
    ["11:30", "50", "Practical A", "Correlation, simple and multiple regression, confounding, model checks, fitted plots", "05_correlation_regression.R; 2.1 to 2.4"],
    ["12:20", "20", "Practical B", "Guided: logistic and Poisson regression", "06_logistic_poisson.R; 2.5 to 2.6"],
    ["12:40", "20", "Practical C", "Guided: k-means clustering", "07_clustering.R; 2.7"],
    ["13:00", "25", "Final exercise", "Choose an analysis, plot, conclusion", "08_final_exercise.R"],
    ["13:25", "5", "Close", "Reporting checklist; resources for further learning", ""],
    ["", "240", "Total", "120 theory + 120 practical", ""],
], widths=[1.3, 1.5, 2.1, 7.6, 3.9], size=9)
doc.p("If the group is slower than planned, shorten Day 1 Part 5 (the practical revisits it) and turn Day 2 "
      "Practical C into a five-minute demonstration. Do not cut the final exercise.", italic=True)

doc.h1("Pre-course preparation (about 30 minutes)")
doc.p("Please complete these steps before Day 1. Installation problems are the most common way to lose "
      "teaching time.")
doc.numbered([
    "Install R (version 4.1 or later) from CRAN: https://cran.r-project.org/ . Choose the download for your "
    "operating system and accept the default options. R is the program that does the calculations.",
    "Install RStudio Desktop (free, open source) from Posit: https://docs.posit.co/ide/user/download.html . "
    "RStudio is the window you work in: it shows your script, the console, plots and data side by side. "
    "Install R first.",
    "Unzip the course folder to a location you can find, for example Documents.",
    "Double-click `Concepts-of-Biostatistics-and-Data-Science.Rproj`. RStudio opens with the course folder as the working "
    "folder, so paths such as `data/hearts.csv` work.",
    "In RStudio, open `R/00_install_and_check.R` and click Source. It installs the four course packages "
    "(readr, dplyr, ggplot2, broom) and checks that the data can be read.",
    "Check that the last line in the console says: Your computer is ready for the course.",
])
doc.p("Links checked on 26 October 2026. Software websites change; if a link has moved, search for "
      "\"CRAN R download\" or \"RStudio Desktop download\".", italic=True, size=9.5)

doc.h2("If installation fails")
doc.bullets([
    "Bring the laptop anyway: the instructor will help at the start of Day 1, or you can pair with a neighbour.",
    "The cleaned data are supplied ready to use as `data/hearts.csv` and `data/hearts.rds`, so no download is "
    "needed during the course.",
    "If packages cannot be installed, all tests and models still run in base R. Use `read.csv()` instead of "
    "`read_csv()`; ggplot2 plots can be replaced by `hist()`, `boxplot()` and `plot()`.",
    "If the data files are missing or damaged, `source(\"data/make_hearts_data.R\")` rebuilds them using base R only.",
    "As a last resort, Posit Cloud (https://posit.cloud) runs RStudio in a web browser. Check its current account options before the course.",
])

doc.h2("R and RStudio in one paragraph")
doc.p("R is a free programming language for statistics. You give it instructions (commands) and it returns "
      "results, tables and plots. Commands are saved in a script (a text file ending in .R) so that the whole "
      "analysis can be repeated exactly. RStudio is a free program that makes R easier to use: the script is in "
      "the top-left pane, the console where results appear is below it, the data and objects you have created "
      "are listed top-right, and plots and help appear bottom-right. Run the current line with Ctrl+Enter "
      "(Cmd+Enter on a Mac). Add-on packages extend R; we use four of them.")

doc.h1("Crash course materials")
doc.table([
    ["Material", "File(s)"],
    ["Slides with speaker notes", "slides/Day1_*.pptx, slides/Day2_*.pptx (and PDF copies)"],
    ["Participant workbook (includes cheat sheet and decision diagrams)", "workbook/Participant_workbook.docx (and PDF)"],
    ["Final exercise", "workbook/Final_exercise.docx; R/08_final_exercise.R"],
    ["R scripts in teaching order", "R/00 to R/08"],
    ["Data and data dictionary", "data/hearts_raw.csv, data/hearts.csv, data/hearts.rds, data/data_dictionary.csv"],
    ["Cheat sheet, decision diagrams, method-selection guide", "reference/ (PDF and editable LaTeX sources)"],
    ["Instructor answer key and solutions", "instructor/ (answer key, solutions.R, output logs)"],
], widths=[7, 9.4], size=9.5)

doc.save(os.path.join(ROOT, "course", "Course_overview_and_timetable.docx"))
