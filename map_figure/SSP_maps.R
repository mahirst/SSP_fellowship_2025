setwd("Downloads/")

library(ggplot2)
library(maps)
library(mapdata)
library(readr)
library(dplyr)

# load data for u.s.
data <- read_csv("complete_university_coordinates.csv") %>%
  filter(!is.na(Latitude), !is.na(Longitude))

# u.s. state outlines
states_map <- map_data("state")

# north america outlines
world_map <- map_data("world")
north_america <- world_map %>%
  filter(region %in% c("Canada", "Mexico", "USA"))

# plot
ggplot() +
  # canada and mexico
  geom_polygon(data = north_america, aes(x = long, y = lat, group = group),
               fill = "gray95", color = "gray40", size = 0.2) +
  
  # bold state borders
  geom_polygon(data = states_map, aes(x = long, y = lat, group = group),
               fill = NA, color = "gray40", size = 0.2) +
  
  # data points
  geom_point(data = data, aes(x = Longitude, y = Latitude),
             color = "blue", size = 1.3, alpha = 0.8) +
  
  # full bounding box to include AK + HI
  coord_fixed(xlim = c(-180, -50), ylim = c(10, 75), expand = FALSE) +
  theme_void() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 14)
  )


##############
#plot just michigan

# load data
institutions <- read_csv("institution_coordinates.csv")

# map data for just Michigan
states_map <- map_data("state")
michigan_map <- filter(states_map, region == "michigan")

# plot map
ggplot() +
  geom_polygon(data = michigan_map, aes(x = long, y = lat, group = group),
               fill = "gray95", color = "gray40", size = 0.3) +
  geom_point(data = institutions, aes(x = Longitude, y = Latitude),
             color = "blue", size = 3, alpha = 0.9) +
  coord_fixed(1.3) +
  theme_void() +
  
  theme(plot.title = element_text(hjust = 0.5, size = 14))
