"""
This program will produce a visualization of an
undirected network graph.

Code largely copied from:
https://plot.ly/ipython-notebooks/network-graphs/

author: Colin Williams
last updated: Feb 2017
"""

#from parsing import buildGraph
import pickle
import os

import plotly.plotly as py
from plotly.graph_objs import *
import matplotlib.pyplot as plt
import networkx as nx

def renderAsPlotly(G = nx.Graph(), weights = {}):

    pos = nx.spring_layout(G)

    nx.set_node_attributes(G, 'pos', pos)
    nx.set_node_attributes(G, 'weight', weights)

    dmin=1
    ncenter=0
    for n in pos:
        x,y=pos[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d

    p=nx.single_source_shortest_path_length(G,ncenter)

    edge_trace = Scatter(
        x=[],
        y=[],
        line=Line(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    node_trace = Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=Marker(
            showscale=True,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale='YIGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'].append(x)
        node_trace['y'].append(y)

        node_info = str(node)
        node_trace['text'].append(node_info)
        node_trace['marker']['size'].append(node['weight'])

    for node, adjacencies in enumerate(G.adjacency_list()):
        node_trace['marker']['color'].append(len(adjacencies))
        #node_info = '# of connections: '+str(len(adjacencies))
        #node_trace['text'].append(node_info)

    fig = Figure(data=Data([edge_trace, node_trace]),
                 layout=Layout(
                    title='<br>Keywords in Williams Economics Research',
                    titlefont=dict(size=16),
                    showlegend=False,
                    width=650,
                    height=650,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Python code inspiration: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

    py.plot(fig, filename='networkx')

def renderAsMatPlot(G = nx.Graph()):

    nx.draw_spring(G, node_size=75, node_color='c', edge_color='k') #with_labels=True, font_size=11

    plt.show()

def main():
    field = 'keywords'
    G = pickle.load( open("pickled-graphs" + os.sep + field + ".p", "rb"))
    weights = pickle.load( open("pickled-graphs"+os.sep+field+"-weights.p", "rb"))

    renderAsPlotly(G, weights)

if __name__ == '__main__':
    main()
