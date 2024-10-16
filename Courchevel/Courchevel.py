import networkx as nx
import matplotlib.pyplot as plt
import pickle
import os
from PIL import Image

# Define directory path to simplify file loading
here = os.path.dirname(os.path.abspath(__file__))

# Define file paths, so that even if you move the file, it will still work
filename_blackpickle = os.path.join(here, 'rotten_pickle.gpickle')
filename_redpickle = os.path.join(here, 'rotten_redpickle.gpickle')
filename_bluepickle = os.path.join(here, 'rotten_bluepickle.gpickle')
filename_greenpickle = os.path.join(here, 'rotten_greenpickle.gpickle')

# Load graphs objects from file
G_black = pickle.load(open(filename_blackpickle, 'rb'))
G_red = pickle.load(open(filename_redpickle, 'rb'))
G_blue = pickle.load(open(filename_bluepickle, 'rb'))
G_green = pickle.load(open(filename_greenpickle, 'rb'))

# Create list of graphs for each level of ski
G_list = [G_black, G_red, G_blue, G_green]

# Display graph
#img = Image.open(os.path.join(here, 'Graphe_Courchevel.png'))
#img.show()

# Ask questions to determine shortest path parameters, some aren't asked : I promise It's a democracy
print("Assurez-vous de ne pas vous coincer dans un endroit où vous n'avez pas le niveau, sinon nous ne pouvons rien pour vous et vous devrez faire la descente dangeureuse sur les fesses. Bonne chance !")

SOURCE = input("De quel point nommé du plan partez-vous ? Veuillez l'écrire en majuscule , par exemple : LOZE. A vous maintenant") # test 'LOZE'
TARGET = input("A quel point nommé du plan voulez-vous vous rendre ? Veuillez l'écrire en majuscule , par exemple : LA TANIA 1400M. A vous maintenant") # test 'LA TANIA 1400M'

WEIGHT = 'weight'

METHOD = 'dijkstra'

G_ind = int(input("Quel est votre niveau de ski ? Si expert, 0. Si confimé, 1. Si intermediaire, tapez 2. Si debutant, tapez 3. A vous maintenant."))  # test G_black

# Check if G_ind is valid
if G_ind != 0 and G_ind != 1 and G_ind != 2 and G_ind != 3:
    raise ValueError("Vous n'avez pas rentré un niveau de ski valide. Veuillez recommencer.")

# Define G as the graph that shortest path will use
G = G_list[G_ind]

# Draw graph G with NetworkX, but irrelevant for app's usage
#nx.draw(G, with_labels=True, font_weight='bold')
#plt.show()

# Find SOURCE and TARGET in G, their id because label can't be used
for node in G.nodes(data = True):
    if node[1]['label'] == SOURCE:
        # print(node)
        SOURCE = node[0]

for node in G.nodes(data = True):
    if node[1]['label'] == TARGET:
        # print(node)
        TARGET = node[0]

# Check if SOURCE and TARGET are valid
if SOURCE == TARGET:
    raise ValueError("Vous êtes déjà arrivé.e.s à destination.")
elif SOURCE not in G.nodes():
    raise ValueError("Il ne s'agit pas d'un point du domaine skiable. Pas le droit au bonheur snif.")
elif TARGET not in G.nodes():
    raise ValueError("Il ne s'agit pas d'un point du domaine skiable. Pas le droit au bonheur prout.")
elif nx.has_path(G, source=SOURCE, target=TARGET) == False:
    raise ValueError("Il n'existe pas de chemin entre ces deux points. Pas le droit au bonheur beeeh.")

# Shortest Path
Shortest_P = nx.shortest_path(G, source=SOURCE, target=TARGET, weight=WEIGHT, method=METHOD)
#print('Shortest Path',Shortest_P)

# Create a graph from 'Shortest_P'to get edges attributes
pathGraph = nx.path_graph(Shortest_P)  # does not pass edges attributes

# Read attributes from each edge => list of tuples for dev with every edge's attributes
# Useful to verify data and such but irrelevant for app's usage
for Edge_A in pathGraph.edges():
    #print from_node, to_node, edge's attributes
    All_Path = Edge_A, G.edges[Edge_A[0], Edge_A[1]]
    print('ALL_PATH',All_Path)

Chemin = []
# Add labels to Chemin
for Edge_A in pathGraph.edges():
    Chemin.append(G.edges[Edge_A[0], Edge_A[1]]['label'])
#print('Chemin', Chemin)



Time = 0
# Add weights to Time
for Edge_A in pathGraph.edges():
    Time += G.edges[Edge_A[0], Edge_A[1]]['weight']

for edge in range(len(Chemin)):
    if Chemin[edge].isupper():
        print("Prendre la remontée", Chemin[edge], "attention au décollageeee.")
    else:
        print("Prendre la piste", Chemin[edge], "jusqu'à l'intersection suivante. De préférence sans perdre de ski ou de bâton.")
print("Vous allez mettre", Time, "minutes. GL !")
print("Voici donc votre itinéraire à suivre. N'hésitez pas à utiliser le plan du domaine skiable pour vous repérer. Bonne chance !")


