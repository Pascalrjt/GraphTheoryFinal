## Graph Class: 
This class represents a graph with methods to add edges (add_edge), find the shortest path using Dijkstra's algorithm (dijkstra), and color the graph using the Welsh-Powell algorithm (welsh_powell_coloring).

## Dijkstra's Algorithm:
The Dijkstra method in the Graph class performs Dijkstra's algorithm to find the shortest paths from a given starting node to all other nodes in the graph.
It returns two values:
- distances: Stores the shortest distance from the start node to each node.
- previous_nodes: Stores the previous node in the shortest path to each node.

## Welsh-Powell Graph Coloring:
The welsh_powell_coloring method assigns colors to the nodes based on the Welsh-Powell graph coloring algorithm.
It sorts the nodes based on their distances (calculated by Dijkstra's algorithm) in descending order.
Then, it assigns colors to the nodes so adjacent nodes have different colors.

- Initisalization:
```py
sorted_vertices = sorted(self.graph.keys(), key=lambda x: distances[x], reverse=True)
colors = {}
current_color = 0
```
- `sorted_vertices`: The vertices (nodes) of the graph are sorted in descending order based on their distances from the starting node (as computed by Dijkstra's algorithm). Sorting the vertices in this way is a common heuristic to improve the performance of graph coloring algorithms.
- `colors`: A dictionary to store the assigned colors for each vertex. Initially empty.
- `current_color`: A variable to keep track of the current color being assigned.

- Main loop:
```py
for vertex in sorted_vertices:
    if vertex not in colors:
        colors[vertex] = current_color
        current_color += 1
```
- The algorithm iterates through the vertices in the order determined by sorted_vertices.
- For each vertex, if it has not been assigned a color (vertex not in colors), it assigns a new color `current_color` to it. The `current_color` is then incremented for the next vertex.

- Coloring Nodes in the shortest path:
```py
# Assign the same color to nodes in the shortest path
current_node = vertex
while previous_nodes[current_node] is not None:
    previous_node = previous_nodes[current_node]
    colors[previous_node] = colors[vertex]
    current_node = previous_node
```
- After assigning a color to the current vertex, the algorithm proceeds to assign the same color to all nodes in its shortest path.
- It starts with the current vertex `vertex` and iterates through the nodes in the shortest path until it reaches the starting node. For each node in the path, it assigns the same color as the current vertex.

## Visualize Graph Function (visualize_graph): 
This function uses the networkx and matplotlib libraries to visualize the graph. Nodes are colored based on the Welsh-Powell coloring.

- Initialization:
```py
G = nx.Graph()
```
- This line creates an empty undirected graph using the NetworkX library.

- Adding Edges to the Graph:
```py
for source, destinations in graph.items():
    for destination, cost in destinations.items():
        G.add_edge(source, destination, weight=cost)
```
- The function takes a graph `graph` as input, where vertices are keys, and values are dictionaries representing neighboring vertices and edge costs.
- It iterates through each vertex `source` and its neighboring vertices `destination` with associated edge costs `cost`.
- For each edge, it adds it to the NetworkX graph `G` with the corresponding weight.

- Node Positions:
```py
pos = nx.spring_layout(G)
```
- This line computes the layout positions of the nodes using the spring layout algorithm from NetworkX. The positions are stored in the `pos` variable.

- Color Mapping:
```py
unique_colors = list(set(coloring.values()))
color_mapping = {color: f'C{i}' for i, color in enumerate(unique_colors)}
```
- It extracts the unique colors from the `coloring` dictionary.
- `color_mapping` is a dictionary that maps each unique color to a distinct color code. The color codes are generated using the `C{i}` format, where `i` is an index.

- Drawing the Graph:
```py
nx.draw(G, pos, with_labels=True, node_size=700, node_color=[color_mapping[coloring[node]] for node in G.nodes], font_size=8, font_color="black", font_weight="bold", edge_color="gray", linewidths=1, alpha=0.7)
```
- `nx.draw` is used to draw the graph.
- `pos`: The layout positions of the nodes.
- `with_labels=True`: Display node labels.
- `node_size=700`: Set the size of the nodes.
- `node_color=[color_mapping[coloring[node]] for node in G.nodes]`: Assign colors to nodes based on the provided `coloring` dictionary.
- `font_size=8`: Set the font size for node labels.
- `font_color="black"`: Set the font color for node labels.
- `font_weight="bold"`: Set the font weight for node labels.
- `edge_color="gray"`: Set the color for edges.
- `linewidths=1`: Set the width of the edges.
- `alpha=0.7`: Set the transparency level.

- Drawing Edge Labels:
```py
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
```
- `nx.get_edge_attributes` extracts edge attributes (in this case, weights) from the graph.
- `nx.draw_networkx_edge_labels` is used to draw the edge labels on the graph.

- Displaying the Plot:
```py
plt.show()
```
- Finally, `plt.show()` displays the graph plot using Matplotlib.

## Generate Schedule Function (generate_schedule): 
This function generates a schedule based on the coloring of the graph. Each color corresponds to a day of the week, and the function assigns locations to days based on their color.

- Initialization:
```py
schedule = {}
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
```
- `schedule`: A dictionary that will store the schedule for each day of the week.
- `days_of_week`: A list containing the names of the days of the week.

- Iterating Over Coloring Information:
```py
for location, color in coloring.items():
    if location != start_node:
        day = days_of_week[color]
        if day not in schedule:
            schedule[day] = []
```
- The function iterates over each location in the coloring information.
- It skips the start node `the initial location / start node` because it's not part of the schedule.
- It determines the day of the week `day` based on the color assigned to the location.
- If the day is not already present in the schedule, it initializes an empty list for that day.

- Constructing Shortest Paths Information:
```py
# Using the shortest paths information
shortest_path_to_location = []
current_node = location
while previous_nodes[current_node] is not None:
    shortest_path_to_location.insert(0, current_node)
    current_node = previous_nodes[current_node]
```
- The function constructs the shortest path to the current location.
- It initializes an empty list `shortest_path_to_location` to store the sequence of nodes in the shortest path.
- Starting from the current location `location`, it follows the previous nodes obtained from Dijkstra's algorithm until it reaches the start node, inserting each node at the beginning of the list.

- Updating the Schedule Dictionary:
```py
schedule[day].append({
    'location': location,
    'color': color,
    'shortest_path': shortest_path_to_location,
    'distance': distances[location]
})
```
- The function appends information about the current location to the schedule for the corresponding day.
- The information includes the location name, assigned color, shortest path to the location, and the distance from the start node to the location.

4. On Run Button Click Function (on_run_button_click): 
This function is triggered when the "Run" button in the GUI is clicked. It reads the adjacency list and start location from the GUI, creates a Graph object, and applies Dijkstra's algorithm and Welsh-Powell coloring. It then updates the GUI with the coloring, shortest paths, and schedule.

- Reversing the Order of Locations Within Each Day:
```py
# Reverse the order of locations within each day
for day, locations in schedule.items():
    schedule[day] = list(reversed(locations))
```
- After constructing the initial schedule, the function reverses the order of locations within each day. This is done as the given route is originally from the destination to the origin which will needed to be reversed to show the proper route.

- Returning the Final Schedule:
```py
return schedule
```

## on_run_button_click (when run button is clicked):
The `on_run_button_click` function, which is called when the `Run` button in the GUI is clicked. This function is responsible for processing user input, rerunning the graph algorithms `Dijkstra's algorithm` and `Welsh-Powell coloring`, generating a new schedule, and updating the GUI with the results with the updated parameters.

- Getting the user input
```py
adjacency_list_str = adjacency_entry.get()
start_location = start_entry.get()
```
- It retrieves the user input from the GUI entry fields.
- `adjacency_list_str`: The user-provided string representing the adjacency list of the graph.
- `start_location`: The user-provided starting location.

- Initializing the Supply Chain Graph:
```py
supply_chain = Graph()
```
- Creates an instance of the Graph class to represent the supply chain.

- Parsing and Setting Up the Graph:
```py
# Convert the input strings to dictionary and set the default graph
adjacency_list = eval(adjacency_list_str)
for source, destinations in adjacency_list.items():
    supply_chain.graph.setdefault(source, {})

# Add bidirectional edges to the graph so that travel can be done both ways
for source, destinations in adjacency_list.items():
    for destination, cost in destinations.items():
        supply_chain.add_edge(source, destination, cost)
```
- Converts the user-provided string `adjacency_list_str` to a dictionary `adjacency_list`.
- Sets the default graph structure in the `supply_chain` instance using the `setdefault` method.
- Adds bidirectional edges to the graph based on the parsed adjacency list.

- Running Dijkstra's Algorithm and Graph Coloring:
```py
distances, previous_nodes = supply_chain.dijkstra(start_location)
coloring = supply_chain.welsh_powell_coloring(distances, previous_nodes)
```
- Runs Dijkstra's algorithm on the supply chain graph to compute the shortest distances and previous nodes from the start location.
- Runs the Welsh-Powell graph coloring algorithm on the supply chain graph to obtain a coloring scheme for the vertices.

- Updating the GUI Output Text:
```py
# Output text
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
```
- Updates the GUI output text with information about node colors and the shortest routes from the start location.
- Iterates over the coloring information and the distances dictionary to display node colors and shortest routes.

- Generating and Displaying the Schedule:
```py
schedule = generate_schedule(coloring, start_location, distances, previous_nodes)
output_text.set(output_text.get() + f"\nSchedule:\n")
for day, locations in schedule.items():
    output_text.set(output_text.get() + f"{day}:\n")
    for location_info in locations:
        output_text.set(output_text.get() + f"  {location_info['location']} (Color {location_info['color']}) - Route: {location_info['shortest_path']}, Distance: {location_info['distance']}km\n")
```
- Calls the `generate_schedule` function to create a schedule based on the coloring, distances, and previous nodes information.
- Updates the GUI output text with information about the generated schedule.

- Visualizing the Graph:
```py
# Visualize the graph with colors
visualize_graph(supply_chain.graph, coloring)
```
- Calls the `visualize_graph` function to display the graph with colors using Matplotlib and NetworkX.

## Create GUI Function (create_gui): 
This function creates the GUI using the `tkinter library`. It includes an entry for the adjacency list and start location, a "Run" button, and a label to display the output.

- GUI initialization:
```py
root = tk.Tk()
root.title("Global Supply Chain Optimization")
```
- Creates the main window `root` for the GUI using `tk.Tk()`.
- Sets the title of the window to "Global Supply Chain Optimization" using `root.title()`.

- Labels and Entry Fields:
```py
adjacency_label = ttk.Label(root, text="Enter adjacency list (in dictionary format):")
adjacency_label.pack(pady=5)

adjacency_entry = ttk.Entry(root, width=50)
adjacency_entry.pack(pady=5)

start_label = ttk.Label(root, text="Enter start location:")
start_label.pack(pady=5)

start_entry = ttk.Entry(root, width=20)
start_entry.pack(pady=5)
```
- Creates labels and entry fields for user input.
- `adjacency_label`: Label prompting the user to enter the adjacency list in dictionary format.
- `adjacency_entry`: Entry field for the user to input the adjacency list.
- `start_label`: Label prompting the user to enter the start location.
- `start_entry`: Entry field for the user to input the start location.

- Run button:
```py
run_button = ttk.Button(root, text="Run", command=lambda: on_run_button_click(adjacency_entry, start_entry, output_text))
run_button.pack(pady=10)
```
- Creates a "Run" button using `ttk.Button`.
- Associates the button with the `on_run_button_click` function using the `command` parameter.
- The `lambda` function is used to pass arguments `adjacency_entry`, `start_entry`, and `output_text` to the `on_run_button_click` function when the button is clicked.
- Packs the button into the GUI window.

- Output Text Variable and Label:
```py
output_text = tk.StringVar()
output_label = ttk.Label(root, textvariable=output_text, font=("Courier", 10), justify="left")
output_label.pack(pady=10)
```
- Creates a `StringVar` named `output_text` to store text that will be displayed in the GUI.
- `output_label`: Label that will display the content of `output_text`.
- The font is set to "Courier" with a font size of 10.
- The `justify` parameter is set to "left" to align the text to the left.
- Packs the label into the GUI window.

- Main Event Loop:
```py
root.mainloop()
```
- Enters the Tkinter main event loop, allowing the GUI to respond to user interactions and events.

## Main Section: 
```py
if __name__ == "__main__":
    create_gui()
```
If the script is run as the main program (not imported as a module), it calls the `create_gui` function to start the GUI.

The script also includes a sample input in the comments at the end. This input is a dictionary representing an adjacency list of a graph, where the keys are the nodes and the values are dictionaries with the neighboring nodes and the cost to reach them. The start location is also provided.
