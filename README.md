# Prophy.science crawler

This scrapy spider crawls recursively the [Prophy.science](https://prophy.science) API for all articles
citing a given set of articles.

To crawl from a list of seed papers `seed_papers.json` use the command:

```
scrapy crawl prophy -a seed_papers.json
```

A maximum depth can be specified with `-s DEPTH_LIMIT=n`. If not specified, run until all citations have been scraped recursively.

```
scrapy crawl prophy -a seed_papers.json -s DEPTH_LIMIT=2
```

The output of the scraper consists of two files `articles.json` and `links.json`. In order to parse them into a GraphML graph, use

```
python make_graph.py [articles.json] [links.json] [-o citation_graph.graphml]
```

which will output
