setwd("~/Desktop/SSP_Fellowship/SSP_data_code/analysis/")

library(tidyverse)
library(lme4)
library(lmerTest)
library(car)
library(sjPlot)
# libraries for plots
library(broom)
library(broom.mixed)
library(dplyr)
library(ggplot2)
library(stringr)

data <- read.csv("Reshaped_University_Revenue_Data.csv")

# convert to proper types; need to set reference group: R1 (common), midwest (neutral region with a mix of institutions), white (more prevalent in the dataset, easier to contextualize).

data$type_1 <- relevel(as.factor(data$type_1), ref = "R1")
data$region <- relevel(as.factor(data$region), ref = "Midwest")
data$demogs_1_2012 <- relevel(as.factor(data$demogs_1_2012), ref = "White")
data$demogs_1_2022 <- relevel(as.factor(data$demogs_1_2022), ref = "White")
data$publishing_program <- as.factor(data$publishing_program)
data$press <- as.factor(data$press)
data$year <- as.factor(data$year)

# normalize revenue 
data$log_revenue <- log(data$revenue)

######################################
# longitudinal test (2012–2022)

# convert year to numeric for modeling trends
data$year_numeric <- as.numeric(as.character(data$year))

# lmm to test revenue over time by region, type of college, and publishing variables
model_long <- lmer(
  log_revenue ~ year_numeric * region + year_numeric * type_1 +
    publishing_program + press +
    (1 | university),
  data = data, REML = FALSE
)

summary(model_long)
plot(model_long)  # diagnostic residuals plot

# I cannot get my usual forest plot script to look good so I did ask ChatGPT 4o to help with this

# Tidy fixed effects from your model
coefs <- tidy(model_long, effects = "fixed", conf.int = TRUE)

# Filter out intercept to avoid axis distortion
coefs <- coefs %>% filter(term != "(Intercept)")

# Optional: clean and relabel variables for better readability
coefs$term <- coefs$term %>%
  str_replace_all("year_numeric", "Year") %>%
  str_replace_all("type_1", "") %>%
  str_replace_all("region", "") %>%
  str_replace_all("publishing_program1", "Publishing Program") %>%
  str_replace_all("press1", "University Press") %>%
  str_replace_all(":", " × ")  # Replace interaction symbol

# Optional: drop outliers with extreme CIs for better visual clarity
# coefs <- coefs %>% filter(estimate > -20, estimate < 20)

# Create the plot
ggplot(coefs, aes(x = estimate, y = reorder(term, estimate))) +
  geom_point(color = "steelblue", size = 2) +
  geom_errorbarh(aes(xmin = conf.low, xmax = conf.high),
                 height = 0.2, color = "steelblue") +
  geom_vline(xintercept = 0, linetype = "dashed", color = "red") +
  theme_minimal(base_size = 14) +
  theme(
    axis.text.y = element_text(size = 10),
    plot.title = element_text(hjust = 0.5, face = "bold")
  ) +
  labs(
    title = "Fixed Effects (95% Confidence Intervals)",
    x = "Estimate",
    y = NULL
  ) +
  coord_cartesian(xlim = c(-145, 120))  # Adjust as needed


# I want to only see the significant ones, for the sake of simplicity

#restrict to significant only
sig_coefs <- coefs %>% filter(p.value < 0.05)

ggplot(sig_coefs, aes(x = estimate, y = reorder(term, estimate))) +
  geom_point(color = "firebrick", size = 2.5) +
  geom_errorbarh(aes(xmin = conf.low, xmax = conf.high), height = 0.15, color = "firebrick") +
  geom_vline(xintercept = 0, linetype = "dashed", color = "gray50") +
  theme_minimal(base_size = 10) +  # Smaller base font
  theme(
    axis.text.y = element_text(size = 12, face = "bold"),  # Larger, bold y-axis labels
    axis.text.x = element_text(size = 10),
    plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
    axis.ticks.length.y = unit(0, "pt"),  # Remove y ticks for cleaner look
    panel.grid.major.y = element_blank(),  # Remove horizontal gridlines
    plot.margin = margin(10, 10, 10, 10)   # Tighter margins
  ) +
  labs()
    x = "Estimate",
    y = NULL
  )



######################################
# cross-year comparison: 2012 vs 2022
subset_data <- data %>% filter(year %in% c("2012", "2022"))

# convert year to factor again (for interaction terms)
subset_data$year <- as.factor(subset_data$year)

# linear model comparing revenue, demographics, and size by year
model_compare <- lm(
  log_revenue ~ year * type_1 + year * region +
    student_pop_size_2012_average + student_pop_size_2022_average +
    demogs_1_2012 + demogs_1_2022,
  data = subset_data
)

summary(model_compare)

# plot maybe

# Tidy the model
cross_coefs <- tidy(model_compare, conf.int = TRUE)

# Filter significant terms
cross_sig <- cross_coefs %>% filter(p.value < 0.05 & !is.na(estimate))

# Clean labels
cross_sig$term <- cross_sig$term %>%
  str_replace_all("type_1TCU", "Tribal College") %>%
  str_replace_all("regionSouth", "South Region") %>%
  str_replace_all("student_pop_size_2022_average", "Student Pop 2022") %>%
  str_replace_all("demogs_1_2022Hispanic/Latino", "2022: Hispanic/Latino") %>%
  str_replace_all("demogs_1_2012Asian", "2012: Asian")

# Plot
ggplot(cross_sig, aes(x = estimate, y = reorder(term, estimate))) +
  geom_point(color = "#800026", size = 3) +
  geom_errorbarh(aes(xmin = conf.low, xmax = conf.high), height = 0.15, color = "#800026") +
  geom_vline(xintercept = 0, linetype = "dashed", color = "gray50") +
  theme_minimal(base_size = 14) +
  theme(
    axis.text.y = element_text(face = "bold", size = 12),
    plot.title = element_text(face = "bold", hjust = 0.5),
    axis.text.x = element_text(size = 12)
  ) +
  labs(
    x = "Effect on Log Revenue",
    y = NULL
  )
