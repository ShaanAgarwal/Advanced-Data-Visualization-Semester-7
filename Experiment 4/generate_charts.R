# Load necessary libraries
library(tidyverse)
library(ggplot2)

# Read the dataset
data <- read.csv("crime_data.csv")

# Print column names for debugging
print("Column names in the dataset:")
print(names(data))

# Rename columns to remove any extra characters and spaces
names(data) <- make.names(names(data))

# Verify column names after renaming
print("Column names after renaming:")
print(names(data))

# Open a PDF device
pdf("visualizations.pdf", width = 8, height = 6)

# Basic Bar Chart - Complaints Received by State
bar_chart <- ggplot(data, aes(x = Area_Name, y = CPA_._Cases_Registered)) +
  geom_bar(stat = "identity", fill = "steelblue") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  labs(title = "Complaints Received by State", x = "State", y = "Number of Complaints")
print(bar_chart)

# Pie Chart - Complaints Declared False by State with Labels for Top 5
pie_data <- data %>%
  group_by(Area_Name) %>%
  summarise(Total_False = sum(CPA_._Complaints.Cases_Declared_False.Unsubstantiated, na.rm = TRUE)) %>%
  arrange(desc(Total_False)) %>%
  mutate(Label = ifelse(row_number() <= 5, paste0(Area_Name, ": ", Total_False), NA))

pie_chart <- ggplot(pie_data, aes(x = "", y = Total_False, fill = Area_Name)) +
  geom_bar(width = 1, stat = "identity") +
  coord_polar("y") +
  labs(title = "Complaints Declared False by State") +
  theme_void() +
  geom_text(aes(label = Label), position = position_stack(vjust = 0.5), size = 3)
print(pie_chart)

# Histogram - Number of Cases Reported with Metrics
mean_cases <- mean(data$CPA_._Cases_Reported_for_Dept._Action, na.rm = TRUE)
median_cases <- median(data$CPA_._Cases_Reported_for_Dept._Action, na.rm = TRUE)
sd_cases <- sd(data$CPA_._Cases_Reported_for_Dept._Action, na.rm = TRUE)

histogram <- ggplot(data, aes(x = CPA_._Cases_Reported_for_Dept._Action)) +
  geom_histogram(binwidth = 10, fill = "steelblue", color = "black") +
  geom_vline(aes(xintercept = mean_cases), color = "red", linetype = "dashed") +
  geom_vline(aes(xintercept = median_cases), color = "green", linetype = "dashed") +
  annotate("text", x = mean_cases, y = Inf, label = paste("Mean: ", round(mean_cases, 2)), color = "red", vjust = -0.5) +
  annotate("text", x = median_cases, y = Inf, label = paste("Median: ", round(median_cases, 2)), color = "green", vjust = -1.5) +
  labs(title = "Histogram of Cases Reported", x = "Number of Cases Reported", y = "Frequency") +
  theme_minimal()
print(histogram)

# Time Line Chart - Cases Registered Over the Years for a Specific State
timeline_data <- filter(data, Area_Name == "Andhra Pradesh")
timeline_chart <- ggplot(timeline_data, aes(x = Year, y = CPA_._Cases_Registered)) +
  geom_line(color = "blue") +
  geom_point(color = "red") +
  labs(title = "Cases Registered Over the Years in Andhra Pradesh", x = "Year", y = "Number of Cases Registered")
print(timeline_chart)

# Scatter Plot - Cases Registered vs Complaints Received
scatter_plot <- ggplot(data, aes(x = CPA_._Cases_Registered, y = CPA_._Complaints_Received.Alleged)) +
  geom_point(aes(color = Area_Name)) +
  labs(title = "Cases Registered vs Complaints Received", x = "Cases Registered", y = "Complaints Received")
print(scatter_plot)

# Bubble Plot - Complaints Received vs Complaints Declared False
bubble_plot <- ggplot(data, aes(x = CPA_._Complaints_Received.Alleged, y = CPA_._Complaints.Cases_Declared_False.Unsubstantiated, size = CPA_._Cases_Registered, color = Area_Name)) +
  geom_point() +
  labs(title = "Complaints Received vs Complaints Declared False", x = "Complaints Received", y = "Complaints Declared False")
print(bubble_plot)

# Close the PDF device
dev.off()
