import heapq
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

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

def on_run_button_click(adjacency_entry, start_entry, output_text):
    adjacency_list_str = adjacency_entry.get()
    start_location = start_entry.get()

    supply_chain = Graph()

    # Convert the input strings to dictionary and set default graph
    adjacency_list = eval(adjacency_list_str)
    for source, destinations in adjacency_list.items():
        supply_chain.graph.setdefault(source, {})

    # Add bidirectional edges to the graph
    for source, destinations in adjacency_list.items():
        for destination, cost in destinations.items():
            supply_chain.add_edge(source, destination, cost)

    distances, previous_nodes = supply_chain.dijkstra(start_location)
    coloring = supply_chain.welsh_powell_coloring(distances, previous_nodes)

    # Prepare the output text
    output_text.set("\nLocation\t\tColor\n")
    for location, color in coloring.items():
        output_text.set(output_text.get() + f"{location}\t\t{color}\t\t\t\t\t\t\n")

    output_text.set(output_text.get() + f"\nShortest Routes from {start_location}\n")
    for destination, distance in distances.items():
        if destination != start_location:
            path = []
            current_node = destination
            while previous_nodes[current_node] is not None:
                path.insert(0, current_node)
                current_node = previous_nodes[current_node]
            path.insert(0, start_location)
            output_text.set(output_text.get() + f"To {destination}: {path} (Distance: {distance}km)\n")

    schedule = generate_schedule(coloring, start_location, distances, previous_nodes)
    output_text.set(output_text.get() + f"\nSchedule:\n")
    for day, locations in schedule.items():
        output_text.set(output_text.get() + f"{day}:\n")
        for location_info in locations:
            output_text.set(output_text.get() + f"  {location_info['location']} (Color {location_info['color']}) - Route: {location_info['shortest_path']}, Distance: {location_info['distance']}km\n")

    # Visualize the graph with colors
    visualize_graph(supply_chain.graph, coloring)


def create_gui():
    root = tk.Tk()
    root.title("Global Supply Chain Optimization")

    adjacency_label = ttk.Label(root, text="Enter adjacency list (in dictionary format):")
    adjacency_label.pack(pady=5)

    adjacency_entry = ttk.Entry(root, width=50)
    adjacency_entry.pack(pady=5)

    start_label = ttk.Label(root, text="Enter start location:")
    start_label.pack(pady=5)

    start_entry = ttk.Entry(root, width=20)
    start_entry.pack(pady=5)

    run_button = ttk.Button(root, text="Run", command=lambda: on_run_button_click(adjacency_entry, start_entry, output_text))
    run_button.pack(pady=10)

    output_text = tk.StringVar()
    output_label = ttk.Label(root, textvariable=output_text, font=("Courier", 10), justify="left")
    output_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()

# Sample input
# {'FactoryA': {'WarehouseX': 1, 'WarehouseY': 3, 'DistributionCenter1': 5},'FactoryB': {'DistributionCenter1': 2, 'DistributionCenter2': 4},'WarehouseX': {'RetailStore1': 1},'WarehouseY': {'RetailStore2': 7},'DistributionCenter1': {'RetailStore1': 3},'DistributionCenter2': {'RetailStore2': 2},'RetailStore1': {},'RetailStore2': {}}
# FactoryA
