# Carawler_run.sh
# Original author: Leonard Ramsey
# 7-11-18

# --------------------------------------- (1) create output csv file --------------------------------------- #
echo "ID,Post Title,Price,Location,Post Time,URL" > carawler/output/cars.csv
# --------------------------------------- (2) run scrapy script --------------------------------------- #
scrapy crawl sales