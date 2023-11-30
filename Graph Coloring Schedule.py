import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.graph = {}

    def add_class(self, class_name, students):
        if class_name not in self.graph:
            self.graph[class_name] = set(students)
        else:
            self.graph[class_name].update(students)

    def color_classes(self):
        sorted_classes = sorted(self.graph.keys(), key=lambda x: len(self.graph[x]), reverse=True)
        color_map = {}
        color = 1

        for class_name in sorted_classes:
            if class_name not in color_map:
                color_map[class_name] = color

                for adjacent_class in self.graph[class_name]:
                    if adjacent_class not in color_map:
                        color_map[adjacent_class] = color

                color += 1

        return color_map


def visualize_schedule(schedule, input_data):
    G = nx.Graph()

    for class_name, color in schedule.items():
        G.add_node(class_name, color=color)

    for class_name, students in input_data.items():
        for student in students:
            for other_class in input_data:
                if other_class != class_name and student in input_data[other_class]:
                    G.add_edge(class_name, other_class)

    node_colors = [schedule[class_name] for class_name in G.nodes]

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.rainbow)
    plt.show()


def get_user_input():
    input_data = {}
    num_courses = int(input("Enter the number of courses: "))
    
    for _ in range(num_courses):
        course = input("Enter course name: ")
        students = input("Enter students (comma-separated): ").split(',')
        input_data[course] = [student.strip() for student in students]
    
    return input_data


# Get user input for courses and students
user_input_data = get_user_input()

# Get the schedule
graph_instance = Graph()
for class_name, students in user_input_data.items():
    graph_instance.add_class(class_name, students)

result_schedule = graph_instance.color_classes()

# Visualize the colored graph
visualize_schedule(result_schedule, user_input_data)
