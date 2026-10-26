<div align="center">

<img src="https://raw.githubusercontent.com/neu-data/.github/main/assets/banner.svg" alt="Neudata Consulting Ltd" width="100%" />

# Concepts of Biostatistics and Data Science

**A two-day crash course for teaching the concepts of biostatistics and data science, with practical analysis in R.**

`2 days` · `8 teaching hours` · `2 h theory + 2 h practical per day` · `R and RStudio` · `simulated teaching data`

![Neudata](https://img.shields.io/badge/Neudata-Consulting-055F56?style=flat)
![Status](https://img.shields.io/badge/status-active-0B376C?style=flat)
![R](https://img.shields.io/badge/R-%E2%89%A5%204.1-055F56?style=flat&logo=r&logoColor=white)
![Client](https://img.shields.io/badge/client-internal-04242F?style=flat)

*Neudata · #ClearDataClearImpact*

</div>

---

## About the crash course

This crash course gives participants a working understanding of the core ideas of biostatistics and the first steps of data science in two days. Each day has two hours of explanation and two hours of guided analysis in R. The emphasis is on choosing a method for a stated question, checking its assumptions and interpreting the result in plain language, rather than memorising R commands.

It is written for people with little statistical background, data enthusiasts, and participants with some working knowledge who want to strengthen their understanding. A guided core pathway is provided for beginners, with optional extensions for more experienced participants. As a crash course it covers the essentials and signposts further learning; it does not claim to make participants expert in every method.

| Day | Theme | Covers |
|:---:|---|---|
| **1** | Understanding data and making comparisons | Research questions, variables and data quality; descriptive statistics and plots; sampling variability, effect sizes, confidence intervals and tests; Welch t-test, paired t-test, ANOVA, Wilcoxon and Kruskal-Wallis tests; contingency tables, risks, odds, RR, OR, chi-square and Fisher's exact tests; a first look at confounding |
| **2** | Regression and an introduction to data science | Scatterplots and correlation; simple and multiple linear regression; confounders, mediators and adjusted associations (aOR); model checks; introductions to logistic regression and Poisson regression (offsets, overdispersion); prediction, train/test separation and data leakage; k-means and hierarchical clustering |

All examples use one **simulated** dataset, the Healthy Hearts District Study (480 adults, 19 variables). Its results are for teaching only.

## Getting started

1. Install R (4.1 or later) from <https://cran.r-project.org/> and RStudio Desktop from <https://docs.posit.co/ide/user/download.html>.
2. Clone or download this repository and open `Concepts-of-Biostatistics-and-Data-Science.Rproj` in RStudio.
3. Run `R/00_install_and_check.R`. It installs the four course packages (readr, dplyr, ggplot2, broom) and checks the data.

```bash
git clone https://github.com/neu-data/super-dollop-cbsds.git
```

Full pre-course instructions and fallbacks are in [`course/Course_overview_and_timetable.pdf`](course/Course_overview_and_timetable.pdf).

## Materials

| Folder / file | Contents | Audience |
|---|---|---|
| [`course/`](course) | Overview, prerequisites, 15 measurable learning outcomes, what is practised or demonstrated, timetables (240 min per day, break listed separately), pre-course setup | Everyone |
| [`slides/`](slides) | Day 1 and Day 2 decks on the Neudata PowerPoint template, with speaker notes (`.pptx` and `.pdf`) | Trainers |
| [`workbook/`](workbook) | Participant workbook with guided exercises, answer spaces, extensions, the final exercise and the full reference pack; stand-alone final exercise | Participants |
| [`R/`](R) | Commented scripts in teaching order (`00` to `08`) and the Neudata ggplot2 theme | Everyone |
| [`data/`](data) | Raw and cleaned simulated data, data dictionary, base-R script that rebuilds the data | Everyone |
| [`reference/`](reference) | Statistics and R cheat sheet, decision diagrams, method-selection guide (PDF and editable LaTeX) | Everyone |
| [`instructor/`](instructor) | Answer key, solutions script, output logs, hidden simulated profiles for checking the clustering | Trainers |
| [`figures/`](figures) | Figures used in the slides and workbook | Build output |
| [`build/`](build) | Scripts and Neudata templates that regenerate the figures, slides and Word documents | Maintainers |

> **Instructor materials are public.** This repository is public, so the answer key and solutions can be read by anyone. When running the course, give participants the `workbook/`, `slides/`, `R/`, `data/` and `reference/` folders rather than a link to the full repository if you want answers to stay hidden until the end.

### R scripts in teaching order

| Script | Session | Workbook |
|---|---|---|
| `00_install_and_check.R` | Pre-course | |
| `01_import_and_inspect.R` | Day 1 practical A | 1.1 to 1.3 |
| `02_describe_and_plot.R` | Day 1 practical B | 1.4 to 1.6 |
| `03_compare_groups.R` | Day 1 practical C1 | 1.7 to 1.9, E1.1 to E1.3 |
| `04_categorical.R` | Day 1 practical C2 | 1.10 to 1.11, E1.4 to E1.6 |
| `05_correlation_regression.R` | Day 2 practical A | 2.1 to 2.4, E2.1 to E2.2 |
| `06_logistic_poisson.R` | Day 2 practical B (guided) | 2.5 to 2.6, E2.3 |
| `07_clustering.R` | Day 2 practical C (guided) | 2.7, E2.4 |
| `08_final_exercise.R` | Day 2 final exercise | Final exercise |

## House style

Everything follows the Neudata templates:

- Slides: [neu-data/powerpoint-template](https://github.com/neu-data/powerpoint-template) (`build/templates/Neudata-Template.pptx`)
- Word documents: [neu-data/word-templates](https://github.com/neu-data/word-templates) (`build/templates/Neudata-Document.docx`)
- Reference pack: the `neudata` LaTeX class from [neu-data/latex-report-template](https://github.com/neu-data/latex-report-template)
- Figures: the Neudata palette in [`R/theme_neudata.R`](R/theme_neudata.R), from [neu-data/project-template](https://github.com/neu-data/project-template)

## Rebuilding

The Word files, slide decks and PDFs can be edited directly. To regenerate them from source, run from the project folder:

```bash
Rscript data/make_hearts_data.R
```

```bash
Rscript build/make_figures.R
```

```bash
python build/build_slides_day1.py
```

```bash
python build/build_slides_day2.py
```

```bash
python build/build_overview.py
```

```bash
python build/build_workbook.py
```

```bash
python build/build_answer_key.py
```

The reference pack is LaTeX: compile `reference/cheat_sheet.tex`, `reference/method_selection_guide.tex` and `reference/decision_diagrams.tex` with `pdflatex` (twice), and rebuild individual diagrams with `python build_diagrams.py` inside `reference/diagrams/`. Rebuild the workbook afterwards, because it embeds the reference pages. The Python builders need `python-pptx`, `python-docx`, `PyMuPDF` and `Pillow`; the figures also need the R package `patchwork`. PDF copies of the Word and PowerPoint files were exported with Microsoft Office.

If you change the data (for example the seed), every number in the slides, answer key and reference pack must be checked again against the new logs in `instructor/outputs/`.

## Testing status

Tested on Windows 11 with R 4.6.1 (26 October 2026):

- All scripts `R/00` to `R/08`, `instructor/solutions.R`, `data/make_hearts_data.R` and `build/make_figures.R` run without errors. Logs are in `instructor/outputs/`.
- Numbers quoted in the slides, answer key, cheat sheet, diagrams and method guide come from those logs.
- Every complete R command printed in the reference pack was run against the course data. Those that do not run on their own are deliberate fragments (placeholders such as `...`, package names, or one step of a pipeline).
- The decks and documents were rendered to PDF and inspected page by page.
- The `Run course scripts` GitHub Actions workflow repeats the script check on Linux with a fresh package installation on every push.

Not tested: macOS, R versions other than 4.6.1 (R 4.1 or later is required for the native pipe `|>`), and the base-R fallback for running without packages, which is described but not scripted.

---

<div align="center">

**Neudata Consulting Ltd** · *Insight. Impact. Innovation.*
[www.neu-data.com](https://www.neu-data.com) · [contact@neu-data.com](mailto:contact@neu-data.com)

Copyright © Neudata, 2026. All rights reserved.

</div>
