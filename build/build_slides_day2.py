"""Day 2 slides: Regression and an introduction to data science.
Run from the project folder:  python build/build_slides_day2.py
All numbers come from the R scripts (see instructor/outputs/*.log).
"""
import os
from slide_helpers import Deck, ROOT

d = Deck()

d.title_slide(
    "Concepts of Biostatistics and Data Science",
    "A two-day crash course with practical analysis in R\nDay 2: Regression and an introduction to data science",
    "Date: DD-MM-YYYY",
    notes="Welcome back. Ask for one thing from Day 1 that was unclear; note it and return to it during the recap "
          "or the practical.")

d.table("Plan for today", [
    ["Time", "Session", "Focus"],
    ["09:00 to 09:10", "Theory 1", "Recap; four purposes of analysis"],
    ["09:10 to 09:25", "Theory 2", "Scatterplots, correlation, association and causation"],
    ["09:25 to 09:45", "Theory 3", "Simple linear regression"],
    ["09:45 to 10:10", "Theory 4", "Multiple regression, confounding and mediators"],
    ["10:10 to 10:20", "Theory 5", "Model checks and plots of fitted relationships"],
    ["10:20 to 10:40", "Theory 6", "Introduction to logistic and Poisson regression"],
    ["10:40 to 11:00", "Theory 7", "Prediction, train/test, and clustering"],
    ["11:00 to 11:30", "Break", "(not counted in teaching time)"],
    ["11:30 to 13:30", "Practical", "Regression in R, guided demos, final exercise"],
], col_w=[2.2, 1.8, 6], size=19,
    notes="Linear regression is the main practical today. Logistic regression, Poisson regression and clustering "
          "are introductions: participants run guided code and learn to read the output, not to master the methods.")

d.bullets("By the end of today you will be able to", [
    "Explain the difference between describing, estimating associations, predicting and discovering groups",
    "Use a scatterplot and correlation to describe a relationship, and explain why association is not causation",
    "Fit and interpret simple and multiple linear regression models in R",
    "Explain confounding and mediation, and interpret an adjusted association",
    "Check a linear regression model using residual plots, and plot fitted relationships",
    "Read the output of a logistic and a Poisson regression (OR, aOR, IRR) at an introductory level",
    "Describe what k-means clustering does, why scaling matters, and why clusters need checking",
], size=22, notes="Outcomes 1 to 5 are practised fully. Outcomes 6 and 7 are introductory and supported by "
                  "guided demonstrations.")

d.bullets("Recap of Day 1", [
    "Start from the question, the outcome type and the design (independent or paired)",
    "Describe first: counts with denominators, mean (SD) or median (IQR), plots",
    "Report an effect size with a 95% CI; a p-value alone is not enough",
    "Welch's t-test and ANOVA by default; rank-based tests answer a different question",
    "Proportions, risks and odds differ; the design decides which you can interpret",
    "Crude associations can be confounded: smoking OR 3.4 fell to 2.6 after stratifying by age",
], notes="Use this to answer questions left over from Day 1.")

d.table("Four purposes of analysis", [
    ["Purpose", "Example question (our data)", "Typical tools", "Judged by"],
    ["Describe", "What is the distribution of SBP?", "Summaries, plots", "Accuracy, clarity"],
    ["Estimate associations", "Is activity associated with lower SBP, at the same age and sex?", "Regression with adjustment", "Bias, CI, design"],
    ["Predict", "Can we predict a person's SBP from routine data?", "Regression, machine learning", "Error on new data"],
    ["Discover groups", "Are there distinct lifestyle profiles?", "Clustering", "Usefulness, stability"],
], col_w=[2.3, 4.6, 2.8, 2.3], size=18, row_h=0.65,
    box="The same model can serve different purposes, but each purpose asks different things of it.",
    notes="Explaining (estimating an association, often with a causal question in mind) needs careful choice of "
          "confounders and design. Prediction needs good performance on new data and does not require coefficients "
          "to be causal. Clustering has no outcome at all.")

# ------------------------------------------------------------------ Section 1
d.section("Part 1", "Relationships between continuous variables",
          "Scatterplots, correlation, association and causation")

d.text_image("Always start with a scatterplot", [
    "Each point is one person",
    "Look for direction, form (straight or curved), spread and outliers",
    "SBP rises with age, fairly linearly",
    "Line: least-squares fit with 95% confidence band",
], "f_scatter_age.png", split=0.36,
    notes="The scatterplot shows what a single number cannot: curvature, clusters, outliers, unequal spread.")

d.bullets("Correlation coefficients", [
    "Pearson's r: strength of a straight-line association, from -1 to +1",
    ("Age and SBP: r = 0.50 (95% CI 0.43 to 0.57)", 1),
    "Spearman's rho: uses ranks; measures a monotonic association, less affected by skew and outliers",
    ("Activity and CRP: rho = -0.15, p = 0.001", 1),
    "r has no units and does not tell you how much y changes per unit of x",
    "r near 0 does not mean no relationship: it may be curved",
], notes="R: cor.test(~ sbp_0 + age, data = hearts) and method = \"spearman\". A correlation of 0.5 means age and "
         "SBP share a moderate linear association; it does not mean half of SBP is caused by age.")

d.image("Why we always plot", "f_correlation_examples.png",
        caption="Simulated examples. The curved relationship is strong but r is close to 0; one outlier creates r = 0.68.",
        notes="Anscombe made this point in 1973 with four datasets that have the same correlation but very different "
              "plots.")

d.bullets("Association is not causation", [
    "An association between X and Y can arise because:",
    ("X causes Y", 1),
    ("Y causes X (reverse causation)", 1),
    ("A third variable causes both (confounding)", 1),
    ("Chance, or how participants were selected or measured (bias)", 1),
    "More active people have lower SBP in our data, but they are also younger",
    "Randomised trials remove confounding by design; observational studies must adjust for it",
], notes="In our data the lifestyle programme was randomised, so the difference between programme groups can be "
         "read causally (within the limits of the trial). The activity-SBP association is observational.")

# ------------------------------------------------------------------ Section 2
d.section("Part 2", "Simple linear regression", "One outcome, one predictor")

d.bullets("The regression line", [
    "Model: SBP = b0 + b1 × age + error",
    "b1 (slope): difference in mean SBP for a 1-unit difference in age",
    "b0 (intercept): predicted mean SBP when age = 0 (anchors the line; often not meaningful)",
    "Error: how far each person is from the line (the residual)",
    "R chooses b0 and b1 to make the squared residuals as small as possible (least squares)",
], box="R:  fit1 <- lm(sbp_0 ~ age, data = hearts);  summary(fit1);  confint(fit1)",
    notes="The model describes how the MEAN of the outcome changes with the predictor. Individuals vary around that "
          "mean; the residual standard error tells us by how much.")

d.table("Reading the output", [
    ["Term", "Estimate", "95% CI", "Meaning"],
    ["Intercept", "95.2", "89.8 to 100.6", "Predicted mean SBP at age 0 (outside the data)"],
    ["age", "0.66", "0.56 to 0.76", "Mean SBP 0.66 mmHg higher per year of age"],
    ["age10 (per 10 years)", "6.6", "5.6 to 7.6", "Mean SBP 6.6 mmHg higher per decade"],
], col_w=[2.6, 1.6, 2.2, 6], size=19,
    items_after=["R² = 0.25: age accounts for a quarter of the variation in SBP",
                 "Residual standard error 13.5 mmHg: typical distance of a person from the line",
                 "Rescale predictors (e.g. per 10 years) so the slope is a meaningful difference"],
    notes="A low R-squared does not make an association unimportant, and a high R-squared does not make it causal. "
          "The p-value for the slope (< 0.001) tests whether the slope is zero.")

d.bullets("Assumptions of linear regression", [
    "Independent observations: comes from the design, not from a plot",
    "Linearity: the mean outcome changes in a straight line with each predictor",
    "Constant spread: residuals have similar variance across fitted values",
    "Approximately normal residuals: matters least with large samples",
    "The OUTCOME does not need to be normally distributed; the residuals are what we check",
    "Watch for single points with large influence on the fit",
], notes="Order of importance: independence and linearity first. Non-normal residuals mainly affect prediction "
         "intervals and small-sample inference. If spread increases with the mean, a log transformation of the "
         "outcome often helps.")

d.image("Checking residuals", "f_residuals.png",
        caption="Left: SBP on age, no pattern. Right: a curved relationship forced into a straight line leaves a clear pattern.",
        notes="In R: par(mfrow = c(2, 2)); plot(fit1). Explain each panel briefly. Participants will do this in "
              "exercise 2.2.")

d.bullets("Categorical predictors: t-tests and ANOVA are regressions", [
    "A binary predictor gives the difference in means: same as a Student t-test",
    "A predictor with k categories becomes k - 1 indicator (dummy) variables",
    ("Each coefficient is a difference from the reference level", 1),
    "SBP by district, adjusted for age and sex (reference North):",
    ("South +5.7 mmHg (2.3 to 9.1); East +2.0 (-1.3 to 5.3); West -1.6 (-4.9 to 1.7)", 1),
    "Regression lets us compare groups while adjusting for other variables",
], notes="anova(lm(sbp_0 ~ district)) gives exactly the F-test from Day 1 (F = 7.3). Changing the reference "
         "level with relevel() or factor(levels = ...) changes the coefficients but not the model.")

# ------------------------------------------------------------------ Section 3
d.section("Part 3", "Multiple regression and confounding",
          "Adjusted associations, confounders and mediators")

d.bullets("Why adjust?", [
    "Question: is physical activity associated with lower SBP?",
    "Crude: each extra hour of activity per week, SBP 2.1 mmHg lower",
    "But older people are less active (r = -0.19) and have higher SBP",
    "Part of the crude association may reflect age",
    "Multiple regression compares people with the same values of the other variables",
], box="Model: SBP = b0 + b1 × activity + b2 × age + b3 × male + error",
    notes="b1 is now the difference in mean SBP per hour of activity among people of the same age and sex. This is "
          "what \"adjusted for\" means.")

d.text_image("Confounder: a common cause", [
    "Age affects activity and affects SBP",
    "It is not on the path from activity to SBP",
    "Ignoring it mixes the effect of age into the activity estimate",
    "Adjust for confounders to estimate the activity association",
], "dag_confounder.png", split=0.45,
    notes="A causal diagram (directed acyclic graph, DAG) makes assumptions explicit. Arrows show assumed causal "
          "directions. Draw the diagram from subject knowledge before the analysis, not from the data.")

d.text_image("Mediator: on the causal path", [
    "Activity may lower BMI, and BMI raises SBP",
    "BMI carries part of the effect of activity",
    "Adjusting for BMI removes that part",
    "The result is a different quantity: the association not through BMI",
], "dag_mediator.png", split=0.45,
    notes="Whether to adjust for a mediator depends on the question. For the total effect of being more active, do "
          "not adjust for BMI. Mediation analysis is a specialised topic; this is the intuition only.")

d.image("Crude, adjusted and mediator-adjusted estimates", "f_crude_adjusted.png",
        caption="Activity coefficient (mmHg per hour/week) with 95% CI. Models 1 and 2 use 473 people, model 3 uses 463.",
        notes="Model 1: -2.08 (-2.62 to -1.53). Model 2: -1.60 (-2.08 to -1.12). Model 3: -0.86 (-1.36 to -0.37). "
              "Interpretation of model 2: among people of the same age and sex, each extra hour of activity per week "
              "is associated with a mean SBP 1.6 mmHg lower. Model 3 is not \"more adjusted and therefore better\"; it "
              "answers a different question. The models also differ slightly in sample size because of missing BMI.")

d.bullets("Choosing what to adjust for", [
    "Use subject knowledge and a causal diagram, not p-values or automatic stepwise selection",
    "Adjust for confounders: common causes of exposure and outcome",
    "Do not adjust for mediators if you want the total effect",
    "Do not adjust for consequences of the outcome, or for colliders (common effects)",
    "Keep enough data: as a rough guide, at least 10 to 20 observations per coefficient",
    "Adjustment cannot fix unmeasured or poorly measured confounders",
], notes="A collider is a variable caused by both exposure and outcome. Adjusting for it can create a spurious "
         "association. Mention briefly; it is further learning. Residual confounding remains in all observational "
         "studies.")

d.table("Interpreting a multiple regression", [
    ["Term", "Estimate", "95% CI", "Interpretation"],
    ["activity_hr", "-1.60", "-2.08 to -1.12", "Per extra hour/week, same age and sex"],
    ["age", "0.59", "0.49 to 0.69", "Per year of age, same activity and sex"],
    ["sexMale", "6.0", "3.7 to 8.3", "Men vs women, same age and activity"],
], col_w=[2.3, 1.6, 2.4, 6], size=19,
    items_after=["Each coefficient is adjusted for the others in the model",
                 "Adjusted R² = 0.34; 7 people excluded because activity was missing",
                 "These are associations: causal interpretation depends on design and assumptions"],
    notes="Coefficients for the adjustment variables (age, sex) are not themselves adjusted for their own "
          "confounders, so be careful about interpreting them causally (the \"Table 2 fallacy\").")

d.text_image("Plotting a fitted relationship", [
    "Choose values for the other variables (here age 50)",
    "Predict the mean outcome over a range of the exposure",
    "Show the 95% confidence band",
    "Parallel lines: the model assumes the same activity slope for both sexes",
], "f_fitted_activity.png", split=0.38,
    notes="R: predict(fit_adj, newdata = new, interval = \"confidence\"). If we thought the slope differed by sex, we "
          "would add an interaction term (activity_hr * sex) and the lines could diverge.")

d.bullets("Effect modification (interaction): different from confounding", [
    "Confounding: a third variable distorts the overall association. Remedy: adjust",
    "Effect modification: the association genuinely differs between subgroups",
    ("Example question: is the smoking-BP association stronger in men?", 1),
    "Fit an interaction term, e.g. lm(sbp_0 ~ smoker * sex + age, data = hearts)",
    "Interactions need much larger samples to estimate well; pre-specify them",
], notes="In the Day 1 stratified table the smoking ORs were 2.75 (women) and 3.28 (men), with wide overlapping "
         "CIs: no clear evidence of effect modification. Looking at many subgroups invites false findings.")

# ------------------------------------------------------------------ Section 4
d.section("Part 4", "Beyond continuous outcomes",
          "An introduction to logistic and Poisson regression")

d.table("Matching the model to the outcome", [
    ["Outcome", "Model", "Effect measure", "In this course"],
    ["Continuous", "Linear regression", "Difference in means", "Practised"],
    ["Binary", "Logistic regression", "Odds ratio (OR, aOR)", "Introduced, guided demo"],
    ["Count, with exposure time", "Poisson regression (offset)", "Incidence rate ratio (IRR)", "Introduced, guided demo"],
    ["Ordinal", "Ordinal (proportional odds) regression", "Cumulative OR", "Further learning"],
    ["Nominal, > 2 categories", "Multinomial regression", "Relative risk ratios", "Further learning"],
    ["Time-to-event", "Cox regression, Kaplan-Meier", "Hazard ratio", "Further learning"],
    ["Repeated / clustered", "Mixed models, GEE", "Depends on outcome", "Further learning"],
], col_w=[2.8, 3.6, 3, 2.6], size=17,
    notes="Logistic and Poisson regression are generalised linear models: a linear predictor on a transformed scale "
          "(log-odds or log-rate). The R syntax looks almost the same as lm(), which makes it easy to run them and "
          "easy to misread them. Hence the emphasis on interpretation.")

d.bullets("Logistic regression for a binary outcome", [
    "Models the log-odds of the outcome as a linear function of the predictors",
    "exp(coefficient) = odds ratio; with other variables in the model, an adjusted OR (aOR)",
    "High BP and smoking: crude OR 3.39 (2.05 to 5.61)",
    "Adjusted for age and sex: aOR 2.04 (95% CI 1.17 to 3.54)",
    "Age: aOR 2.29 per 10 years (1.84 to 2.87); men vs women: aOR 2.06 (1.30 to 3.30)",
], box="glm(high_bp_0 ~ smoker + age10 + sex, family = binomial, data = hearts)  then  tidy(fit, conf.int = TRUE, exponentiate = TRUE)",
    notes="Interpretation: among people of the same age and sex, the odds of high BP were about twice as high in "
          "smokers. The crude OR reflected partly that smokers were older and more often male. Note: ORs are not "
          "collapsible, so a crude and adjusted OR can differ slightly even without confounding; the large change "
          "here reflects real confounding by age. Check: enough events (124 here), linear log-odds for continuous "
          "predictors, independence.")

d.text_image("From odds ratios to probabilities", [
    "Predicted probabilities are easier to communicate",
    "At 60 years, a woman who smokes has a higher predicted probability than a non-smoker",
    "The OR is constant; the difference in probability is not",
    "With a common outcome, OR overstates the risk ratio",
], "f_logistic_curve.png", split=0.38,
    notes="R: predict(fit, newdata = new, type = \"response\"). For risk ratios or differences from a binary outcome, "
          "other approaches exist (log-binomial or modified Poisson regression, marginal effects); further learning.")

d.text_image("Poisson regression for counts and rates", [
    "Outcome: number of unplanned clinic visits",
    "People were followed for 2 to 12 months",
    "Compare rates: visits per person-month",
    "Offset log(follow-up months) puts exposure time in the model",
    "exp(coefficient) = incidence rate ratio (IRR)",
], "f_poisson_rates.png", split=0.4,
    notes="Without the offset, people followed for 12 months would look like heavy users compared with those "
          "followed for 3 months. The offset is the log of the exposure, entered with a fixed coefficient of 1.")

d.table("Rate ratios and overdispersion", [
    ["Model", "IRR: programme vs standard", "95% CI"],
    ["Poisson", "0.91", "0.82 to 1.02"],
    ["Quasi-Poisson", "0.91", "0.78 to 1.06"],
    ["Negative binomial (extension)", "0.93", "0.79 to 1.08"],
], col_w=[4, 4, 3], size=19,
    items_after=["Poisson assumes variance = mean. Here the dispersion ratio is 2.0",
                 "Overdispersion makes Poisson CIs too narrow; quasi-Poisson or negative binomial widen them",
                 "Adjusted for age and baseline high BP. Conclusion: no clear evidence that visit rates differ"],
    notes="Dispersion ratio = sum of squared Pearson residuals / residual degrees of freedom. Values well above 1 "
          "suggest overdispersion. Excess zeros, very long follow-up differences or clustered data need further "
          "methods.")

# ------------------------------------------------------------------ Section 5
d.section("Part 5", "Prediction and discovering groups",
          "Train/test separation, leakage and clustering")

d.two_col("Explaining versus predicting", [
    "Goal: estimate an association, ideally a causal one",
    "Choose variables from a causal diagram",
    "Report effect sizes with CIs",
    "Bias matters more than accuracy",
], [
    "Goal: accurate predictions for new people",
    "Variables chosen for predictive value, not causal role",
    "Report prediction error on new data",
    "Coefficients need not have a causal meaning",
], heads=["Explaining (estimation)", "Predicting"],
    notes="A good predictor of hospital use might be the number of past visits, which explains nothing causally. "
          "A good causal estimate may predict poorly. Be clear which goal you have.")

d.bullets("Train/test separation and data leakage", [
    "A model always fits the data it was built on better than new data",
    "Split the data: fit on a training set (e.g. 70%), evaluate once on a test set (30%)",
    "Example: predicting SBP. Error (RMSE) in mmHg:",
    ("Age only: 13.4 training, 13.7 test", 1),
    ("Age, sex, BMI, activity, smoking, district: 11.4 training, 12.3 test", 1),
    "Leakage: information from the test set or the future enters model building",
    ("Choosing variables using all the data; using 12-month SBP to predict 12-month high BP", 1),
], notes="RMSE = root mean squared error, the typical size of a prediction error. Cross-validation repeats the split "
         "several times. Leakage makes models look better than they will perform in practice.")

d.bullets("Discovering groups: clustering", [
    "Unsupervised learning: no outcome variable",
    "Groups people who are similar on the variables we choose",
    "Similarity is measured by a distance (usually Euclidean)",
    "k-means: choose k; assign each person to the nearest centre; move centres to the mean; repeat",
    "Hierarchical: merge the closest groups step by step, giving a tree (dendrogram)",
    "Our example: activity, diet score and BMI",
], notes="Clustering is descriptive. It always returns clusters, even from data with no real groups. Our data were "
         "simulated with three hidden lifestyle profiles, which lets us check how well the clusters recover them "
         "(answer key).")

d.image("Scaling matters", "f_kmeans_scaling.png",
        caption="Activity is measured in hundreds of minutes, diet on a 0 to 10 scale. Without scaling, activity dominates the distances.",
        notes="scale() gives each variable mean 0 and SD 1. Scaling is a choice: it gives each variable equal weight. "
              "Variables measured on the same scale and units may not need it.")

d.image("How many clusters?", "f_choose_k.png",
        caption="No sharp elbow; average silhouette widths are all below 0.35. The data do not clearly favour one k.",
        notes="Silhouette: how well each person fits their own cluster compared with the nearest other one (maximum 1). "
              "Values of 0.25 to 0.5 suggest weak to moderate structure. Here k = 2 is slightly highest; we show k = 3 "
              "for interpretability and compare k = 2 in the workbook. Be honest about this uncertainty when reporting.")

d.image("Hierarchical clustering", "f_dendrogram.png",
        caption="Ward's method on the same scaled variables. Cutting the tree at three groups gives clusters similar to k-means.",
        notes="The linkage method matters: average linkage on these data gives one huge group and two tiny ones "
              "(workbook extension E2.4). Hierarchical clustering does not need k in advance, but you still choose "
              "where to cut.")

d.bullets("Are the clusters meaningful?", [
    "Clusters depend on the variables, the scaling, k and the algorithm",
    "Describe clusters on the original scale and name them carefully",
    ("Our k = 3: low activity / higher BMI; middle; high activity / good diet / lower BMI", 1),
    "Check stability: different seeds, subsets, methods",
    "Check usefulness: do clusters differ on variables NOT used to build them? (mean SBP 138, 127, 121 mmHg)",
    "Do not test for differences on the clustering variables: clusters were built to differ on them",
], notes="Clusters are a summary to be checked, not a discovery to be believed. In our simulation, k-means placed "
         "most Active people in one cluster and most Sedentary in another, but the middle cluster mixed profiles.")

d.table("Where to go next", [
    ["If your data have...", "Look into", "Starting point in R"],
    ["Ordered categories as outcome", "Ordinal (proportional odds) regression", "MASS::polr()"],
    ["Unordered categories (> 2)", "Multinomial regression", "nnet::multinom()"],
    ["Time to an event, with censoring", "Kaplan-Meier, Cox regression", "survival package"],
    ["Repeated measures or clusters", "Mixed models, GEE", "lme4, geepack"],
    ["Causal questions from observational data", "Causal diagrams, propensity scores", "dagitty, MatchIt"],
], col_w=[4, 4.2, 3], size=18,
    notes="These packages exist on CRAN; they are signposts, not course content. The reference pack's decision "
          "diagrams show these routes in dashed boxes.")

d.table("Practical session (2 hours)", [
    ["Part", "Script", "Workbook", "Time"],
    ["A. Correlation, simple and multiple regression, checks", "05_correlation_regression.R", "2.1 to 2.4", "50 min"],
    ["B. Logistic and Poisson regression (guided)", "06_logistic_poisson.R", "2.5 to 2.6", "20 min"],
    ["C. Clustering (guided)", "07_clustering.R", "2.7", "20 min"],
    ["Final exercise", "08_final_exercise.R", "Final exercise", "25 min"],
    ["Review and close", "", "", "5 min"],
], col_w=[5, 3.3, 1.8, 1.1], size=18,
    items_after=["Extensions E2.1 to E2.4 are for those who finish early",
                 "Keep the cheat sheet and decision diagrams open while you work"],
    notes="Protect the final exercise time. If the group is behind, shorten Part C to a demonstration.")

d.bullets("Reporting checklist", [
    "State the question, design and number of observations used (and why any were excluded)",
    "Describe the data before modelling",
    "Report effect sizes with 95% CIs, in meaningful units",
    "Say which variables were adjusted for, and why",
    "Report checks of assumptions",
    "Separate statistical significance from practical importance",
    "Do not claim causation unless the design supports it",
], notes="Close by thanking participants. Remind them the reference pack (cheat sheet, decision diagrams, "
         "method-selection guide) is designed for use after the course.")

out = os.path.join(ROOT, "slides", "Day2_Regression_and_data_science.pptx")
d.closing(notes="Thank participants. The materials, scripts and reference pack are theirs to keep. "
                 "All examples used simulated data and are for teaching only.")
d.save(out)
