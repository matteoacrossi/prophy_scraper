# Prophy.science crawler

This scrapy spider crawls recursively the [Prophy.science](https://prophy.science) API for all articles
citing a given set of articles.

## Installation

```
git clone https://github.com/matteoacrossi/prophy_scraper.git
pip install scrapy networkx
```

## Usage

To crawl from a list of arXiv identifiers `seed_papers.json` use the command:

```
scrapy crawl prophy -a seedfile=example_seed_papers.json
```

A maximum depth can be specified with `-s DEPTH_LIMIT=n`. If not specified, run until all citations have been scraped recursively.

```
scrapy crawl prophy -a seedfile=example_seed_papers.json -s DEPTH_LIMIT=3
```

The output of the scraper consists of two files `articles.json` and `links.json`. In order to parse them into a GraphML graph, use

```
python make_graph.py [articles.json] [links.json] [-o citation_graph.graphml]
```
