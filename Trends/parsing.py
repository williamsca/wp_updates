"""
Various functions related to parsing the papers.rdf file

author: Colin Williams
last updated: Feb 2017
"""

import os
import csv
import networkx as nx

# TODO: build Graph
# TODO: draw Graph

def parseRDF(path, field = "Keywords"):
    with open(path, 'r') as f:
        with open(os.getcwd() + os.sep + field + ".csv", "w", newline='') as d:
            writer = csv.writer(d)
            variables = ["number", "date", field]
            writer.writerow(variables)

            lines = f.readlines()
            errors = 0
            for i in range(0, len(lines), 1):
                if lines[i].startswith(field + ":"):
                    keywords = lines[i][lines[i].find(":") +1:-1].lower().split(', ')

                    num = ''
                    date = ''
                    for j in range(i-15, i+8, 1):
                        if lines[j].startswith("Number:"):
                            num = lines[j][lines[j].find(":")+1:-1]
                        if lines[j].lower().startswith("creation-date"):
                            date = lines[j][lines[j].find(":")+1:-1]

                    # Five failures where it doesn't find either the number or the creation date... why?

                    for word in keywords:
                        if not num or not date or not keywords[0]:
                            break
                        entry = [num.strip(), date.strip(), word.strip()]
                        writer.writerow(entry)
                        #print(entry)

def buildGraph(field="keywords"):
    G = nx.Graph()

    path = os.getcwd() + os.sep + field + ".csv"
    with open(path, 'r') as f:
        reader = csv.reader(f)
        num = 0
        nodes = []
        for row in reader:
            G.add_node(row[2])
            if row[0] == num:
                nodes.append(row[2])
            else:
                connectNodes(nodes, G)

                # reset
                nodes = []
                nodes.append(row[2])
                num = row[0]

        print(G['china'])
    f.close()

def connectNodes(nodes=[], G=nx.Graph()):
    if len(nodes) > 1:
        for i in range(0, len(nodes)-1):
            #print("Len: " + str(len(nodes)))
            #print(str(i))
            G.add_edge(nodes[-1], nodes[i])
            if 'weight' in G[nodes[-1]][nodes[i]]:
                G[nodes[-1]][nodes[i]]['weight']+=1
            else:
                G[nodes[-1]][nodes[i]]['weight']=1
        nodes.pop()
        connectNodes(nodes, G)
    return G

def main():
    path = os.path.dirname(os.getcwd()) + os.sep + "RePEc" + os.sep + "papers.rdf"
    #parseRDF(path)
    buildGraph()

if __name__ == '__main__':
    main()

#G=nx.Graph()
#links = [1, 2]
#G.add_nodes_from([1, 2, 3])
