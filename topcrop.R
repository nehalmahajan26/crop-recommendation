library(dplyr)

# Read data
df <- read.csv("crop_production.csv")

# Find top 3 crops per State and District based on max production
top_3_crops <- df %>%
  group_by(State, District, Crop) %>%  
  summarise(Max_Production = max(Production, na.rm = TRUE), .groups = "drop") %>%  
  arrange(State, District, desc(Max_Production)) %>%  
  group_by(State, District) %>%  
  slice(1:3)  # Select the top 3 crops per State & District

print(top_3_crops)

