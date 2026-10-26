"""Participant workbook and stand-alone final exercise.
Run from the project folder:  python build/build_workbook.py
Appendices embed the reference PDFs (cheat sheet, diagrams, method guide) as page images,
so the workbook always matches the reference pack. Rebuild after changing reference/.
"""
import os, csv
import fitz  # PyMuPDF
from PIL import Image
from docx_helpers import Doc, ROOT, GREY

REF = os.path.join(ROOT, "reference")
PAGES = os.path.join(ROOT, "build", "page_images")
os.makedirs(PAGES, exist_ok=True)


def pdf_pages(pdf_name, dpi=170):
    """Render each page of a reference PDF to PNG and return the paths (landscape flag too)."""
    path = os.path.join(REF, pdf_name)
    out = []
    if not os.path.exists(path):
        return out
    doc = fitz.open(path)
    for i, page in enumerate(doc):
        if "All property rights and copyright" in page.get_text():
            continue  # skip each PDF's copyright page inside the workbook
        png = os.path.join(PAGES, f"{os.path.splitext(pdf_name)[0]}_p{i + 1}.png")
        page.get_pixmap(dpi=dpi).save(png)
        landscape = page.rect.width > page.rect.height
        if landscape:  # rotate so the page fills a portrait workbook page
            Image.open(png).rotate(90, expand=True).save(png)
        out.append((png, landscape))
    return out


def exercise(doc, num, title, task, code=None, questions=(), lines=4, ext=False):
    doc.h3(f"{'Extension' if ext else 'Exercise'} {num}. {title}")
    doc.p(task)
    if code:
        doc.code(code)
    for q in questions:
        doc.p(q)
        doc.answer_box(lines)


def final_exercise(doc):
    doc.h1("Final exercise: choose, plot, conclude (25 minutes)")
    doc.p("Work alone or in pairs. Pick ONE question. Use the cheat sheet and decision diagrams, and the template "
          "script `R/08_final_exercise.R`. There is more than one defensible analysis for each question; what "
          "matters is that you can justify yours.")
    doc.table([
        ["", "Question"],
        ["F1", "Were participants in the lifestyle programme more satisfied with their care at 12 months than those given standard advice?"],
        ["F2", "Do men and women differ in C-reactive protein (CRP) at baseline?"],
        ["F3", "Is a healthier diet score associated with lower baseline systolic blood pressure, after allowing for age and sex?"],
        ["F4", "Was high blood pressure at 12 months less common in the lifestyle programme group than in the standard advice group?"],
    ], widths=[1, 15.4], size=10)
    doc.p("Step 1. Write your question and the outcome, its type, the groups or exposure, and the design "
          "(independent or paired; any confounders).")
    doc.answer_box(4)
    doc.p("Step 2. Which analysis did you choose, and why? Name one alternative and say why you did not choose it.")
    doc.answer_box(4)
    doc.p("Step 3. Describe the data: give the numbers you will report (with denominators or n).")
    doc.answer_box(3)
    doc.p("Step 4. Produce one plot that shows the answer. Paste it here or sketch it.")
    doc.answer_box(9, "Plot")
    doc.p("Step 5. Results: the effect estimate with its 95% CI (and p-value if you wish). What did you check?")
    doc.answer_box(4)
    doc.p("Step 6. Conclusion in plain language (3 to 5 sentences) for a reader with no statistical training. "
          "Include the size of the effect, the uncertainty, whether it matters in practice, and one limitation.")
    doc.answer_box(8, "Conclusion")


def build_workbook():
    doc = Doc("Concepts of Biostatistics and Data Science",
              "Participant workbook for the two-day crash course with practical analysis in R",
              header_text="Concepts of Biostatistics and Data Science  |  Participant workbook",
              byline="Neudata Consulting Ltd  \u00b7  Version 1.0  \u00b7  26-10-2026")
    doc.p("Name: ______________________________        Date: ____________________")

    doc.h1("How to use this workbook")
    doc.p("This workbook accompanies the two-day crash course in the concepts of biostatistics and data science, and follows its practical sessions. Each exercise names the R script it belongs to. The "
          "scripts contain worked examples with comments; the exercises ask you to adapt that code to a new "
          "question and to interpret the result in words. Write your answers in the boxes.")
    doc.bullets([
        "Core exercises (numbered 1.1, 2.1 ...) form the guided pathway. Everyone should aim to complete them.",
        "Extensions (E1.1, E2.1 ...) are optional, for participants who finish early or have more experience.",
        "Always write the interpretation, not only the number. A good answer gives the estimate, its 95% CI, "
        "and what it means.",
        "The reference section at the end contains the cheat sheet, decision diagrams and method-selection guide.",
    ])
    doc.note("The Healthy Hearts District Study is simulated. Its results are for teaching only and must not be "
             "quoted as findings about real people.")

    doc.h2("Getting started in RStudio")
    doc.numbered([
        "Open `Concepts-of-Biostatistics-and-Data-Science.Rproj` (double-click). This sets the working folder.",
        "Open a script from the Files pane (bottom right), folder `R`.",
        "Put the cursor on a line and press Ctrl+Enter (Cmd+Enter on a Mac) to run it. Results appear in the "
        "Console (bottom left), plots in the Plots pane.",
        "Run lines in order from the top. If you get an error, read the message, check spelling and brackets, "
        "and check that earlier lines were run.",
        "Type your own code at the bottom of each script, under \"Your turn\". Save with Ctrl+S.",
    ])
    doc.table([
        ["Symbol", "Meaning", "Example"],
        ["<-", "Store a result under a name", "`fit <- lm(sbp_0 ~ age, data = hearts)`"],
        ["~", "\"is modelled by\" / \"by group\"", "`t.test(sbp_0 ~ sex, data = hearts)`"],
        ["|>", "Pass the result on to the next step", "`hearts |> count(district)`"],
        ["$", "One column of a data frame", "`hearts$age`"],
        ["na.rm = TRUE", "Ignore missing values", "`mean(hearts$crp, na.rm = TRUE)`"],
        ["?name", "Open the help page", "`?t.test`"],
    ], widths=[2.2, 5.4, 8.8], size=9.5)

    doc.h2("The data")
    doc.p("480 adults aged 30 to 74 from four districts were measured at baseline and randomly allocated to "
          "standard advice or a lifestyle programme. Blood pressure, satisfaction, adverse events and clinic "
          "visits were recorded over 12 months. Some participants left early.")
    rows = [["Variable", "Description", "Type", "Units or coding", "Missing"]]
    with open(os.path.join(ROOT, "data", "data_dictionary.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append([r["variable"], r["description"], r["type"], r["units_or_coding"], r["missing_values"]])
    doc.table(rows, widths=[2.9, 4.2, 3.3, 4.6, 1.4], size=8.5)

    # ===================================================================== DAY 1
    doc.page_break()
    doc.h1("Day 1 practical: understanding data and making comparisons")

    doc.h2("Part A. Import and inspect (script 01_import_and_inspect.R, 25 minutes)")
    exercise(doc, "1.1", "Import the raw data",
             "Run the first sections of the script to import `data/hearts_raw.csv`.",
             questions=["a) How many participants (rows) and variables (columns) are there?",
                        "b) What does one row represent? Which two variables are measurements of the same "
                        "thing on the same person at different times?"], lines=2)
    exercise(doc, "1.2", "Find and fix missing values",
             "Use `summary(raw)` and `colSums(is.na(raw))`.",
             questions=["a) Which variables have missing values, and how many?",
                        "b) What problem do you see in `activity_min`? How does the script fix it? How many "
                        "missing values does `activity_min` have after the fix?",
                        "c) 41 people have no 12-month blood pressure. Why might this matter for the results?"],
             lines=3)
    doc.h3("Exercise 1.3. Variable types")
    doc.p("Classify each variable. Use: continuous, count, binary, nominal, ordinal.")
    doc.table([["Variable", "Type", "Variable", "Type"],
               ["district", "", "satisfaction", ""],
               ["age", "", "clinic_visits", ""],
               ["education", "", "crp", ""],
               ["smoker", "", "high_bp_0", ""],
               ["sbp_0", "", "followup_months", ""]], widths=[4, 4.2, 4, 4.2], size=10)

    doc.h2("Part B. Describe and plot (script 02_describe_and_plot.R, 30 minutes)")
    exercise(doc, "1.4", "Counts and proportions",
             "Use `count()` and `mutate()` as in the script.",
             code="count(hearts, smoker) |> mutate(percent = round(100 * n / sum(n), 1))",
             questions=["a) What number and percentage of participants smoke? Write it as n / N (%).",
                        "b) What percentage have tertiary education? State your denominator and why."], lines=2)
    exercise(doc, "1.5", "Centre and spread",
             "Calculate the mean, SD, median and IQR of `sbp_0` and of `crp` (remember `na.rm = TRUE`).",
             questions=["a) Fill in: SBP mean ____ (SD ____), median ____ (IQR ____ to ____). "
                        "CRP mean ____ (SD ____), median ____ (IQR ____ to ____).",
                        "b) Which summary would you report for each variable, and why?"], lines=3)
    exercise(doc, "1.6", "Plots",
             "Make a histogram of `bmi` and a boxplot of `crp` by `smoker`. Try adding `scale_y_log10()` to the "
             "boxplot.",
             code="ggplot(hearts, aes(x = bmi)) + geom_histogram(binwidth = 1)\n"
                  "ggplot(hearts, aes(x = smoker, y = crp)) + geom_boxplot() + scale_y_log10()",
             questions=["Describe the shape of the BMI distribution, and what the boxplot suggests about CRP "
                        "in smokers and non-smokers. Why is the log scale helpful here?"], lines=4)

    doc.h2("Part C1. Compare groups (script 03_compare_groups.R, 35 minutes)")
    doc.p("For each comparison, first write the question, the outcome type, the groups, and whether the data are "
          "independent or paired.")
    exercise(doc, "1.7", "Two independent groups",
             "Does mean BMI differ between women and men? Adapt the t-test code from the script.",
             code="t.test(bmi ~ sex, data = hearts)",
             questions=["a) Report the mean BMI in each group, the difference and its 95% CI.",
                        "b) Interpret the result in one or two sentences. Does a p-value above 0.05 show that "
                        "men and women have the same mean BMI?"], lines=3)
    exercise(doc, "1.8", "Paired data",
             "Did systolic blood pressure change between baseline and 12 months in the Standard advice group?",
             code="std <- hearts |> filter(programme == \"Standard advice\", !is.na(sbp_12))\n"
                  "t.test(std$sbp_12, std$sbp_0, paired = TRUE)",
             questions=["a) Report the mean change and 95% CI. How many people does it use?",
                        "b) Compare with the Lifestyle programme group in the script (-6.0 mmHg). Why can we "
                        "not judge the programme from the within-group change alone? What comparison does?"],
             lines=3)
    exercise(doc, "1.9", "More than two groups",
             "Does mean BMI differ between the four districts? Summarise by district, then use Welch's ANOVA and "
             "Holm-adjusted pairwise comparisons.",
             code="oneway.test(bmi ~ district, data = hearts)\n"
                  "pairwise.t.test(hearts$bmi, hearts$district, pool.sd = FALSE, p.adjust.method = \"holm\")",
             questions=["a) What does the overall test tell you? What does it not tell you?",
                        "b) Which districts appear to differ? Why adjust the pairwise p-values?"], lines=3)

    doc.h2("Part C2. Categorical associations (script 04_categorical.R, 20 minutes)")
    exercise(doc, "1.10", "A 2 x 2 table",
             "Is high blood pressure at baseline (`high_bp_0`) associated with sex?",
             code="tab_sex <- table(hearts$sex, hearts$high_bp_0)\n"
                  "addmargins(tab_sex)\n"
                  "prop.table(tab_sex, margin = 1)\n"
                  "chisq.test(tab_sex)",
             questions=["a) Write the proportion with high BP in each sex as n / N (%).",
                        "b) Calculate the prevalence ratio and the odds ratio (men compared with women). "
                        "Why are they different? Which word should you use: risk or prevalence? Why?",
                        "c) Interpret the chi-square test."], lines=3)
    exercise(doc, "1.11", "A larger table",
             "Does the prevalence of high BP differ between districts? Make a 4 x 2 table, row proportions and a "
             "chi-square test.",
             questions=["Which districts have the highest and lowest prevalence? What does the chi-square test "
                        "tell you, and what does it not tell you?"], lines=3)

    doc.h2("Day 1 extensions (optional)")
    exercise(doc, "E1.1", "Kruskal-Wallis",
             "Compare `activity_min` across education levels with medians (IQR) and `kruskal.test()`. What does "
             "the test compare? Is it a test of medians?", ext=True, lines=3)
    exercise(doc, "E1.2", "An ordinal outcome",
             "Compare `satisfaction` between women and men. Show the percentage at each level, then use "
             "`wilcox.test()`. Why is a mean less suitable here?", ext=True, lines=3)
    exercise(doc, "E1.3", "Student or Welch?",
             "Compare `summary(aov(sbp_0 ~ district, data = hearts))` with `oneway.test(sbp_0 ~ district, data = "
             "hearts)`. When would the two disagree?", ext=True, lines=2)
    exercise(doc, "E1.4", "McNemar's test",
             "In the Standard advice group, cross-tabulate `high_bp_0` and `high_bp_12` and run `mcnemar.test()`. "
             "Which cells matter? Compare with the Lifestyle group in the script.", ext=True, lines=3)
    exercise(doc, "E1.5", "Confounding by age",
             "Create `age_group` (30-49, 50-74) with `cut(age, c(29, 49, 74))`. Estimate the smoking-high BP OR in "
             "each age group and the Mantel-Haenszel OR (`mantelhaen.test()`). Compare with the crude OR of 3.39. "
             "What do you conclude?", ext=True, lines=4)
    exercise(doc, "E1.6", "Small counts",
             "In the script, look at adverse events among participants aged 65 and over. Why is Fisher's exact "
             "test preferred here, and how would you describe the result?", ext=True, lines=3)

    # ===================================================================== DAY 2
    doc.page_break()
    doc.h1("Day 2 practical: regression and an introduction to data science")
    doc.h2("Part A. Correlation and linear regression (script 05_correlation_regression.R, 50 minutes)")
    exercise(doc, "2.1", "Scatterplot and correlation",
             "Plot `sbp_0` against `bmi` and calculate Pearson's and Spearman's correlations.",
             code="ggplot(hearts, aes(x = bmi, y = sbp_0)) + geom_point(alpha = 0.4)\n"
                  "cor.test(~ sbp_0 + bmi, data = hearts)\n"
                  "cor.test(~ sbp_0 + bmi, data = hearts, method = \"spearman\", exact = FALSE)",
             questions=["Describe the relationship (direction, form, strength). Report r with its 95% CI. Does "
                        "this show that BMI raises blood pressure?"], lines=4)
    exercise(doc, "2.2", "Simple linear regression",
             "Fit `lm(sbp_0 ~ bmi, data = hearts)`. Then create `bmi5 = bmi / 5` and refit.",
             code="hearts <- hearts |> mutate(bmi5 = bmi / 5)\n"
                  "fit_bmi <- lm(sbp_0 ~ bmi, data = hearts)\n"
                  "tidy(fit_bmi, conf.int = TRUE); glance(fit_bmi)\n"
                  "par(mfrow = c(2, 2)); plot(fit_bmi); par(mfrow = c(1, 1))",
             questions=["a) Interpret the slope per 1 kg/m2 and per 5 kg/m2, with 95% CIs.",
                        "b) What is R-squared and what does it mean here?",
                        "c) What do the residual plots show? Are the assumptions reasonable?"], lines=3)
    exercise(doc, "2.3", "Confounding",
             "Is smoking associated with SBP? Fit a crude model and one adjusted for age and sex.",
             code="fit_s0 <- lm(sbp_0 ~ smoker, data = hearts)\n"
                  "fit_s1 <- lm(sbp_0 ~ smoker + age + sex, data = hearts)\n"
                  "tidy(fit_s0, conf.int = TRUE); tidy(fit_s1, conf.int = TRUE)",
             questions=["a) Report the crude and adjusted differences in SBP for smokers. Why did the estimate "
                        "change?",
                        "b) Interpret the adjusted coefficient in one sentence starting \"Among people of the "
                        "same ...\".",
                        "c) A colleague suggests also adjusting for CRP, which smoking raises. Is CRP a confounder "
                        "or more like a mediator here? What would adjusting for it do? Draw a small diagram."],
             lines=3)
    exercise(doc, "2.4", "Plot a fitted relationship",
             "Fit `lm(sbp_0 ~ bmi + age + sex, data = hearts)` and plot predicted SBP against BMI for women and "
             "men aged 50, following section E of the script.",
             questions=["What does the plot show? What does the model assume about the BMI slope in women and men?"],
             lines=3)

    doc.h2("Part B. Logistic and Poisson regression (script 06_logistic_poisson.R, 20 minutes, guided)")
    exercise(doc, "2.5", "Logistic regression",
             "Model high BP at baseline using BMI (per 5 kg/m2), age (per 10 years) and sex.",
             code="hearts <- hearts |> mutate(age10 = age / 10, bmi5 = bmi / 5)\n"
                  "fit_lb <- glm(high_bp_0 ~ bmi5 + age10 + sex, family = binomial, data = hearts)\n"
                  "tidy(fit_lb, conf.int = TRUE, exponentiate = TRUE)",
             questions=["a) Interpret the aOR for `bmi5` with its 95% CI.",
                        "b) Why should this aOR not be described as \"times the risk\"?"], lines=3)
    exercise(doc, "2.6", "Poisson regression",
             "Compare the rate of unplanned clinic visits between smokers and non-smokers, adjusting for age, "
             "using an offset for follow-up time.",
             code="fit_ps <- glm(clinic_visits ~ smoker + age10 + offset(log(followup_months)),\n"
                  "              family = poisson, data = hearts)\n"
                  "tidy(fit_ps, conf.int = TRUE, exponentiate = TRUE)\n"
                  "sum(residuals(fit_ps, type = \"pearson\")^2) / df.residual(fit_ps)\n"
                  "tidy(update(fit_ps, family = quasipoisson), conf.int = TRUE, exponentiate = TRUE)",
             questions=["a) Interpret the IRR for smoking. Why is the offset needed?",
                        "b) What does the dispersion ratio show, and how does the quasi-Poisson CI differ?"],
             lines=3)

    doc.h2("Part C. Clustering (script 07_clustering.R, 20 minutes, guided)")
    exercise(doc, "2.7", "k-means: two or three clusters?",
             "Run the script, then fit k-means with k = 2 on the same scaled variables and describe both solutions.",
             code="set.seed(2024)\n"
                  "km2 <- kmeans(life_scaled, centers = 2, nstart = 25)\n"
                  "life$k2 <- factor(km2$cluster)\n"
                  "life |> group_by(k2) |> summarise(n = n(), act = median(activity_min),\n"
                  "                                  diet = mean(diet_score), bmi = mean(bmi))\n"
                  "table(life$k2, life$cluster)",
             questions=["a) Give each cluster a short descriptive name (k = 2 and k = 3).",
                        "b) Why were the variables scaled? What happened without scaling?",
                        "c) Give two reasons to be cautious before reporting these clusters as real groups."],
             lines=3)

    doc.h2("Day 2 extensions (optional)")
    exercise(doc, "E2.1", "Analysing a randomised trial",
             "Compare the programme effect estimated from change scores (Welch t-test on `sbp_12 - sbp_0`) with "
             "the baseline-adjusted estimate `lm(sbp_12 ~ programme + sbp_0)`. Which CI is narrower?",
             ext=True, lines=3)
    exercise(doc, "E2.2", "Train and test",
             "Using the split in section G of script 05, fit `lm(sbp_0 ~ age + sex + bmi)` on the training data and "
             "compare training and test RMSE. Why is test error the honest measure? Give one example of data "
             "leakage.", ext=True, lines=3)
    exercise(doc, "E2.3", "Negative binomial",
             "Fit the clinic visits model with `MASS::glm.nb()` (script 06). Compare the IRR and CI with Poisson "
             "and quasi-Poisson.", ext=True, lines=2)
    exercise(doc, "E2.4", "Linkage methods",
             "Repeat the hierarchical clustering with `method = \"average\"` and cut at 3 groups. Compare the "
             "group sizes with Ward's method. What does this tell you?", ext=True, lines=3)

    doc.page_break()
    final_exercise(doc)

    # ===================================================================== REFERENCE
    doc.page_break()
    doc.h1("Reference section")
    doc.p("The pages below are the same as the stand-alone reference pack in the `reference` folder (cheat sheet, "
          "decision diagrams and method-selection guide). Keep them for use after the course.")
    for title, pdf in (("Statistics and R cheat sheet", "cheat_sheet.pdf"),
                       ("Choosing an analysis: decision diagrams", "decision_diagrams.pdf"),
                       ("Method-selection guide", "method_selection_guide.pdf")):
        pages = pdf_pages(pdf)
        doc.h2(title)
        if not pages:
            doc.p(f"[{pdf} not found in reference/]", italic=True, color=GREY)
        for k, (png, landscape) in enumerate(pages):
            doc.image(png, width_cm=15.6 if landscape else 16.6)
            if not (pdf == "method_selection_guide.pdf" and k == len(pages) - 1):
                doc.page_break()

    doc.save(os.path.join(ROOT, "workbook", "Participant_workbook.docx"))


def build_final():
    doc = Doc("Final exercise", "Concepts of Biostatistics and Data Science: a two-day crash course in R",
              header_text="Concepts of Biostatistics and Data Science  |  Final exercise")
    doc.note("Data: the simulated Healthy Hearts District Study (teaching only). Template script: "
             "R/08_final_exercise.R. Use the cheat sheet and decision diagrams.")
    final_exercise(doc)
    doc.save(os.path.join(ROOT, "workbook", "Final_exercise.docx"))


if __name__ == "__main__":
    build_workbook()
    build_final()
