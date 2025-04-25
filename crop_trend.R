
library(ggplot2)
library(jsonlite)
library(base64enc)
library(dplyr)

args <- commandArgs(trailingOnly = TRUE)
if(length(args) < 1){
  stop("Crop name argument required")
}

crop_name <- tolower(args[1])

data <- read.csv("crop_production.csv", stringsAsFactors = FALSE)

names(data) <- trimws(names(data))
data$Crop <- tolower(data$Crop)
crop_data <- data[data$Crop == crop_name, ]

if(nrow(crop_data) == 0){
  result <- list(error = paste("No data found for crop:", crop_name))
  cat(toJSON(result))
  quit(save = "no", status = 0)
}

crop_data$Crop_Year <- as.numeric(crop_data$Crop_Year)
crop_data$Production <- as.numeric(crop_data$Production)

trend <- crop_data %>% 
  group_by(Crop_Year) %>% 
  summarise(total_production = sum(Production, na.rm = TRUE)) %>%
  arrange(Crop_Year)

p <- ggplot(trend, aes(x = Crop_Year, y = total_production)) +
  geom_line(color = "blue") +
  geom_point(color = "red") +
  ggtitle(paste("Production Trend for", toupper(crop_name))) +
  xlab("Year") +
  ylab("Total Production")

temp_file <- tempfile(fileext = ".png")
ggsave(filename = temp_file, plot = p, width = 6, height = 4, dpi = 150)

img_data <- dataURI(file = temp_file, mime = "image/png")

result <- list(plot_image = img_data)
cat(toJSON(result))
