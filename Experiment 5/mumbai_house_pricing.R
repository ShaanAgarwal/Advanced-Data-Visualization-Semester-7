library(tidyverse)
library(ggplot2)
library(wordcloud)
library(RColorBrewer)
library(plotly)
library(scales)

data <- read.csv("mumbai_house_pricing.csv")

print("Column names in the dataset:")
print(names(data))

names(data) <- make.names(names(data))

print("Column names after renaming:")
print(names(data))

# Open a PDF device
pdf("visualizations.pdf", width = 8, height = 6)

# Box and Whisker Plot - Price by Number of Bedrooms
box_whisker_plot <- ggplot(data, aes(x = factor(No..of.Bedrooms), y = Price)) +
  geom_boxplot(fill = "lightblue") +
  labs(title = "Box and Whisker Plot of Price by Number of Bedrooms", x = "Number of Bedrooms", y = "Price") +
  scale_y_continuous(labels = scales::comma) +
  theme_minimal()
print(box_whisker_plot)

# Violin Plot - Price by Number of Bedrooms
violin_plot <- ggplot(data, aes(x = factor(No..of.Bedrooms), y = Price)) +
  geom_violin(fill = "lightblue", alpha = 0.6) +
  geom_boxplot(width = 0.1, alpha = 0.3, outlier.size = 1.5) +
  labs(title = "Violin Plot of Price by Number of Bedrooms", x = "Number of Bedrooms", y = "Price") +
  scale_y_continuous(labels = scales::comma) +
  scale_x_discrete(labels = function(x) paste0("Bedrooms: ", x)) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) 

print(violin_plot)

# Linear Regression Plot - Price vs Area
linear_regression_plot <- ggplot(data, aes(x = Area, y = Price)) +
  geom_point(color = "blue") +
  geom_smooth(method = "lm", color = "red") +
  labs(title = "Linear Regression of Price vs Area", x = "Area", y = "Price") +
  scale_y_continuous(labels = scales::comma) +
  theme_minimal()
print(linear_regression_plot)

# Nonlinear Regression Plot - Price vs Area with a Polynomial Fit
nonlinear_regression_plot <- ggplot(data, aes(x = Area, y = Price)) +
  geom_point(color = "blue") +
  geom_smooth(method = "lm", formula = y ~ poly(x, 2), color = "green") +
  labs(title = "Nonlinear Regression of Price vs Area (Polynomial Fit)", x = "Area", y = "Price") +
  scale_y_continuous(labels = scales::comma) +
  theme_minimal()
print(nonlinear_regression_plot)

unique_locations <- unique(data$Location)
selected_locations <- unique_locations[seq(1, length(unique_locations), length.out = 10)] 

# Jitter Plot - Price by Location with Limited x-axis Labels
jitter_plot <- ggplot(data, aes(x = factor(Location), y = Price)) +
  geom_jitter(color = "darkorange", alpha = 0.6, size = 2, width = 0.2) +  
  labs(title = "Jitter Plot of Price by Location", x = "Location", y = "Price") +
  scale_y_continuous(labels = scales::comma) + 
  scale_x_discrete(breaks = selected_locations, labels = selected_locations) + 
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 10))  

print(jitter_plot)

# Word Cloud Chart - Locations
location_freq <- table(data$Location)
wordcloud(names(location_freq), freq = location_freq, min.freq = 1, 
          scale = c(4, 0.5), colors = brewer.pal(8, "Dark2"), random.order = FALSE)
dev.off()

# 3D Scatter Plot - Area vs Price vs Number of Bedrooms
plot_3d <- plot_ly(data, x = ~Area, y = ~Price, z = ~No..of.Bedrooms, 
                   type = 'scatter3d', mode = 'markers', 
                   marker = list(size = 5, color = ~Price, colorscale = 'Viridis'))

plot_3d <- plot_3d %>% layout(title = "3D Scatter Plot of Area vs Price vs Number of Bedrooms",
                              scene = list(xaxis = list(title = 'Area'),
                                           yaxis = list(title = 'Price'),
                                           zaxis = list(title = 'Number of Bedrooms')))

htmlwidgets::saveWidget(plot_3d, "3d_scatter_plot.html")