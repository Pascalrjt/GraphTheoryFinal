import networkx as nx
import matplotlib.pyplot as plt
import datetime

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
        print(f"{class_name}: Color {color}")

    for class_name, students in input_data.items():
        for student in students:
            for other_class in input_data:
                if other_class != class_name and student in input_data[other_class]:
                    G.add_edge(class_name, other_class)

    node_colors = [schedule[class_name] for class_name in G.nodes]

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.rainbow)
    plt.show()

class ScheduleAllocator:
    def __init__(self, schedule, class_duration=3, start_time=datetime.time(11, 0), end_time=datetime.time(16, 0)):
        self.schedule = schedule
        self.class_duration = class_duration
        self.start_time = start_time
        self.end_time = end_time
        self.num_periods = 0  # Add a new attribute to store the number of periods

    def allocate_schedule(self):
        allocated_schedule = {}
        current_time = datetime.datetime.combine(datetime.date.today(), self.start_time)

        for class_name, color in self.schedule.items():
            allocated_schedule[class_name] = current_time.strftime("%I:%M %p")
            current_time += datetime.timedelta(hours=self.class_duration)
            if current_time.time() > self.end_time:
                current_time = datetime.datetime.combine(datetime.date.today(), self.start_time)
                self.num_periods += 1  # Increment the number of periods

        return allocated_schedule, self.num_periods  # Return the allocated schedule and the number of periods


# Example input data
input_data = {
    'Physics': ['Arnold', 'Ingrid', 'Fred', 'Bill', 'Jack'],
    'Mathematics': ['Eleanor', 'Arnold', 'Herb'],
    'English': ['Arnold', 'David'],
    'Geology': ['Carol', 'Bill', 'Fred', 'Herb'],
    'Business': ['George', 'Eleanor', 'Carol'],
    'Statistics': ['David', 'Ingrid', 'George'],
    'Economics': ['Ingrid', 'Jack']
}

# Get the schedule
graph_instance = Graph()
for class_name, students in input_data.items():
    graph_instance.add_class(class_name, students)

result_schedule = graph_instance.color_classes()

# Visualize the colored graph
visualize_schedule(result_schedule, input_data)

print(result_schedule)

# Example usage
schedule_allocator = ScheduleAllocator(result_schedule)
allocated_schedule = schedule_allocator.allocate_schedule()
print(allocated_schedule)
