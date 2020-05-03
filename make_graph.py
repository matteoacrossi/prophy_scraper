import json

import networkx as nx
import argparse


def main(args):
    articles = json.load(args.articles)
    links = json.load(args.links)

    graph = nx.DiGraph()

    graph.add_edges_from([(link['source'], link['target']) for link in links])

    graphattrs = {}
    for article in articles:
        key = article.pop('paperId')
        graphattrs[key] = article

    nx.set_node_attributes(graph, graphattrs)

    nx.write_graphml(graph, args.output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse output of prophy_scraper into a GraphML file')
    parser.add_argument('articles', type=argparse.FileType('r'),
                        default='articles.json',
                        help='JSON file with articles (default articles.json)')
    parser.add_argument('links', type=argparse.FileType('r'), default='links.json',
                        help='JSON file with links (default links.json)')
    parser.add_argument('--output', '-o', type=argparse.FileType('wb'),
                        default='citation_graph.graphml',
                        help='Output file (default citation_graph.graphml)')
    main(parser.parse_args())
