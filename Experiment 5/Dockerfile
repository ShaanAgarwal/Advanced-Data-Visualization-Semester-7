# Use the latest rocker/tidyverse image as the base
FROM rocker/tidyverse:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the dataset and R script into the container
COPY mumbai_house_pricing.csv /app/
COPY mumbai_house_pricing.R /app/

# Install additional R packages required for the word cloud, 3D chart, and saving the 3D plot as an HTML file
RUN R -e "install.packages(c('wordcloud', 'RColorBrewer', 'plotly', 'htmlwidgets'), repos='http://cran.rstudio.com/')"

# Set the command to run the R script
CMD ["Rscript", "mumbai_house_pricing.R"]
