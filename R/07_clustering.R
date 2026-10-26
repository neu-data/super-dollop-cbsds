# =============================================================================
# 07_clustering.R                        DAY 2 PRACTICAL, PART C (20 min, guided)
# Unsupervised learning: k-means and hierarchical clustering
#
# Data: simulated Healthy Hearts District Study (teaching data only).
# Workbook exercise 2.7 and extension E2.4 refer to this script.
#
# Clustering has no outcome. It looks for groups of people who are similar
# on the variables we CHOOSE. Different variables, scaling or k give
# different clusters. Clusters are a description to be checked, not a discovery
# to be believed.
# =============================================================================

library(dplyr)
library(ggplot2)
library(cluster)     # silhouette(); comes with R
source("R/theme_neudata.R")   # Neudata colours and plot theme

hearts <- readRDS("data/hearts.rds")

# --- 1. Choose variables (a substantive decision) ---------------------------
# Question: are there distinct lifestyle profiles?
# We use three lifestyle measures and deliberately leave out the outcomes (BP),
# so that we can later ask whether the profiles differ in BP.
life <- hearts |>
  select(id, activity_min, diet_score, bmi) |>
  filter(!is.na(activity_min), !is.na(bmi))      # k-means needs complete data
nrow(life)

summary(life[, -1])
# activity_min ranges over hundreds, diet_score over 0 to 10. Distances would
# be dominated by activity unless we put the variables on a common scale.

# --- 2. Scale: each variable to mean 0, SD 1 --------------------------------
life_scaled <- scale(life[, c("activity_min", "diet_score", "bmi")])
round(apply(life_scaled, 2, sd), 2)

# --- 3. How many clusters? --------------------------------------------------
# k-means needs k in advance. Two common aids (neither is decisive):
#  * Elbow: total within-cluster sum of squares falls as k rises; look for a bend.
#  * Average silhouette width: how well each point sits in its own cluster
#    compared with the next nearest (higher is better, maximum 1).
set.seed(2024)
k_values <- 1:8
wss <- sapply(k_values, function(k) kmeans(life_scaled, centers = k, nstart = 25)$tot.withinss)
sil <- sapply(2:8, function(k) {
  km <- kmeans(life_scaled, centers = k, nstart = 25)
  mean(silhouette(km$cluster, dist(life_scaled))[, "sil_width"])
})

ggplot(data.frame(k = k_values, wss = wss), aes(k, wss)) +
  geom_line(colour = "grey50") + geom_point(size = 2.5, colour = neudata_cols[["teal"]]) +
  scale_x_continuous(breaks = k_values) +
  labs(x = "Number of clusters (k)", y = "Total within-cluster sum of squares",
       title = "Elbow plot")
data.frame(k = 2:8, avg_silhouette = round(sil, 3))
# Here the elbow is gradual and every average silhouette is below 0.35, with
# k = 2 slightly highest. That is weak structure: the data do not clearly
# favour one k. We look at k = 3 because three profiles are easy to describe,
# and compare it with k = 2 in the workbook. Say this openly when reporting.

# --- 4. Fit k-means with the chosen k ---------------------------------------
set.seed(2024)
km3 <- kmeans(life_scaled, centers = 3, nstart = 25)   # nstart: try 25 random starts
life$cluster <- factor(km3$cluster)
table(life$cluster)

# Describe the clusters on the ORIGINAL scale, then give them names
life |>
  group_by(cluster) |>
  summarise(n = n(),
            activity_median = median(activity_min),
            diet_mean = round(mean(diet_score), 1),
            bmi_mean = round(mean(bmi), 1))

ggplot(life, aes(x = activity_min, y = bmi, colour = cluster)) +
  geom_point(alpha = 0.6) +
  scale_x_log10() +
  scale_colour_manual(values = unname(neudata_cols[c("teal", "blue", "teal_light")])) +
  labs(x = "Physical activity (min/week, log scale)", y = "BMI (kg/m2)",
       colour = "Cluster", title = "k-means clusters (k = 3, scaled variables)")

# --- 5. What happens without scaling? ----------------------------------------
set.seed(2024)
km3_raw <- kmeans(life[, c("activity_min", "diet_score", "bmi")], centers = 3, nstart = 25)
life |>
  mutate(cluster_raw = factor(km3_raw$cluster)) |>
  group_by(cluster_raw) |>
  summarise(n = n(), activity_min = paste(range(activity_min), collapse = " to "),
            diet_mean = round(mean(diet_score), 1), bmi_mean = round(mean(bmi), 1))
# Unscaled clusters are just bands of activity minutes; diet and BMI barely matter.

# --- 6. Do the clusters relate to anything outside the clustering? ---------
# A useful check: compare clusters on a variable NOT used to build them.
life <- life |> left_join(select(hearts, id, sbp_0, age), by = "id")
life |>
  group_by(cluster) |>
  summarise(n = n(), mean_age = round(mean(age), 1), mean_sbp = round(mean(sbp_0), 1))
# Caution: we should not then "test" whether clusters differ on the variables
# used to create them. They were built to differ on those.

# --- 7. Hierarchical clustering (demonstration) -----------------------------
# Builds a tree by repeatedly merging the two closest groups.
# Ward's method merges the groups that least increase within-group variation.
d <- dist(life_scaled)
hc <- hclust(d, method = "ward.D2")
plot(hc, labels = FALSE, hang = -1, main = "Hierarchical clustering (Ward)",
     xlab = "", sub = "")
rect.hclust(hc, k = 3, border = unname(neudata_cols[c("teal", "blue", "teal_light")]))

life$hc3 <- factor(cutree(hc, k = 3))
table(kmeans = life$cluster, hierarchical = life$hc3)
# Cluster numbers are arbitrary labels. Look for agreement in the pattern.

# -----------------------------------------------------------------------------
# Your turn: Workbook exercise 2.7 and extension E2.4.
# -----------------------------------------------------------------------------

