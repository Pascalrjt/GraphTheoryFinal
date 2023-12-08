import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, source, destination, cost):
        if source not in self.graph:
            self.graph[source] = {}
        if destination not in self.graph:
            self.graph[destination] = {}

        self.graph[source][destination] = cost
        self.graph[destination][source] = cost  # Add the reverse edge

    def dijkstra(self, start):
        distances = {node: float('infinity') for node in self.graph}
        distances[start] = 0
        priority_queue = [(0, start)]
        previous_nodes = {node: None for node in self.graph}

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances, previous_nodes

    def welsh_powell_coloring(self, distances, previous_nodes):
        sorted_vertices = sorted(self.graph.keys(), key=lambda x: distances[x], reverse=True)
        colors = {}
        current_color = 0

        for vertex in sorted_vertices:
            if vertex not in colors:
                colors[vertex] = current_color
                current_color += 1

                # Assign the same color to nodes in the shortest path
                current_node = vertex
                while previous_nodes[current_node] is not None:
                    previous_node = previous_nodes[current_node]
                    colors[previous_node] = colors[vertex]
                    current_node = previous_node

        return colors


def visualize_graph(graph, coloring):
    G = nx.Graph()

    for source, destinations in graph.items():
        for destination, cost in destinations.items():
            G.add_edge(source, destination, weight=cost)

    pos = nx.spring_layout(G)

    unique_colors = list(set(coloring.values()))
    color_mapping = {color: f'C{i}' for i, color in enumerate(unique_colors)}

    nx.draw(G, pos, with_labels=True, node_size=700, node_color=[color_mapping[coloring[node]] for node in G.nodes], font_size=8, font_color="black", font_weight="bold", edge_color="gray", linewidths=1, alpha=0.7)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.show()


def generate_schedule(coloring, start_node, distances, previous_nodes):
    schedule = {}
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    for location, color in coloring.items():
        if location != start_node:
            day = days_of_week[color]  
            if day not in schedule:
                schedule[day] = []

            # Use the shortest paths information
            shortest_path_to_location = []
            current_node = location
            while previous_nodes[current_node] is not None:
                shortest_path_to_location.insert(0, current_node)
                current_node = previous_nodes[current_node]

            schedule[day].append({
                'location': location,
                'color': color,
                'shortest_path': shortest_path_to_location,
                'distance': distances[location]
            })

    # Reverse the order of locations within each day
    for day, locations in schedule.items():
        schedule[day] = list(reversed(locations))

    return schedule



def main():
    # Example usage for a Global Supply Chain Optimization scenario with named locations
    supply_chain = Graph()

    # Define edges representing bidirectional transportation routes between locations with costs
    adjacency_list = {
        'FactoryA': {'WarehouseX': 1, 'WarehouseY': 3, 'DistributionCenter1': 5},
        'FactoryB': {'DistributionCenter1': 2, 'DistributionCenter2': 4},
        'WarehouseX': {'RetailStore1': 1},
        'WarehouseY': {'RetailStore2': 7},
        'DistributionCenter1': {'RetailStore1': 3},
        'DistributionCenter2': {'RetailStore2': 2},
        'RetailStore1': {},  # Add an empty dictionary for 'RetailStore1'
        'RetailStore2': {}   # Add an empty dictionary for 'RetailStore2'
    }

    # Initialize all locations in the graph
    for source, destinations in adjacency_list.items():
        supply_chain.graph.setdefault(source, {})

    # Add bidirectional edges to the graph
    for source, destinations in adjacency_list.items():
        for destination, cost in destinations.items():
            supply_chain.add_edge(source, destination, cost)

    # Example shortest paths from 'FactoryA' to other locations
    start_location = 'FactoryA'
    distances, previous_nodes = supply_chain.dijkstra(start_location)

    # Perform graph coloring using Welsh-Powell algorithm
    coloring = supply_chain.welsh_powell_coloring(distances, previous_nodes)

    # Print the schedule
    print("\nLocation\tColor\tShortest Path\t\tDistance")
    for location, color in coloring.items():
        print(f"{location}\t\t{color}\t\t\t\t\t\t")

    # Specify the start node for the schedule
    start_node = 'FactoryA'

    # Generate and print the schedule (excluding the start node)
    schedule = generate_schedule(coloring, start_node, distances, previous_nodes)
    print("\nSchedule:")
    for day, locations in schedule.items():
        print(f"{day}:")
        for location_info in locations:
            print(f"  {location_info['location']} (Color {location_info['color']}) - Shortest Path: {location_info['shortest_path']}, Distance: {location_info['distance']}")

    # Visualize the graph with colors
    visualize_graph(supply_chain.graph, coloring)

if __name__ == "__main__":
    main()
