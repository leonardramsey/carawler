# carawler

# What is <i>carawler</i>?

Carawler is a web crawling tool used for quickly pulling data from Craigslist's car and trucks marketplaces.

It pulls this data with a single Python Scrapy spider and stores the data in a csv and xlsx spreadsheet.

### Input files:

* car_filter.txt

<i>A list of all cars (e.g. year/manufacturer/model) to retain in the scraping. Delimited by newlines ('\n').</i> 

* price_filter.txt

<i>Contains the price range to use in scraping. The minimum price is specified in line 1 and maximum price in line 2. Read in and casted to python integers. Delimited by newlines ('\n').</i> 

In order to run the crawler from the command-line, make sure you are in the root project (not git) directory (where the scrapy.cfg file is located).

Activate the virtual environment:

```shell
source activate venv
```

To run the project, call the following command:

```shell
scrapy crawl sales
```

All output files are stored in the carawler/output directory.

### Output files:

* cars.csv

<i>A list of all post results from the Craigslist scraping in csv format. Columns delimited by ','.</i> 

* cars.xlsx

<i>A list of all post results from the Craigslist scraping in xlsx format.</i> 
