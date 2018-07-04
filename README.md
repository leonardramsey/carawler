# carawler

# What is <i>carawler</i>?

Carawler is a web crawling tool used for quickly pulling data from Craigslist's car and trucks marketplaces.

It pulls this data with a single Python Scrapy spider and stores the data in a csv and xlsx spreadsheet.

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