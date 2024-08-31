FROM rocker/tidyverse:latest
WORKDIR /app
COPY crime_data.csv /app/
COPY generate_charts.R /app/
CMD ["Rscript", "generate_charts.R"]