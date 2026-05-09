# Campus Navigation System (GUI + JSON + Visualization)
# Developed by Aryan

import json
import heapq
import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt

def load_campus_data(file_path="campus_data.json"):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "Campus data file not found!")
        return {}

def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    visited = set()

    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue

        path = path + [node]
        visited.add(node)

        if node == end:
            return cost, path

        for neighbor, distance in graph.get(node, {}).items():
            if neighbor not in visited:
                heapq.heappush(queue, (cost + distance, neighbor, path))

    return float("inf"), []

def show_graph(graph, path=None):
    G = nx.Graph()

    
    for node, edges in graph.items():
        for neighbor, weight in edges.items():
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8,6))

    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=1500, font_size=10)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    
    if path:
        edge_list = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edge_list, width=3, edge_color="red")

    plt.title("Campus Map Visualization", fontsize=14)
    plt.show()

class CampusNavigatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏫 Campus Navigation System")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        self.graph = load_campus_data()

        tk.Label(root, text="🏫 Campus Navigation System 🧭", font=("Arial", 16, "bold")).pack(pady=10)

        frame = tk.Frame(root)
        frame.pack(pady=20)

        locations = list(self.graph.keys())

        tk.Label(frame, text="Start Location:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        self.start_var = tk.StringVar()
        self.start_combo = ttk.Combobox(frame, textvariable=self.start_var, values=locations, width=20)
        self.start_combo.grid(row=0, column=1, padx=10)

        tk.Label(frame, text="Destination:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
        self.end_var = tk.StringVar()
        self.end_combo = ttk.Combobox(frame, textvariable=self.end_var, values=locations, width=20)
        self.end_combo.grid(row=1, column=1, padx=10)

        # Buttons
        tk.Button(root, text="Find Shortest Path", command=self.find_path,
                  font=("Arial", 12, "bold"), bg="#4CAF50", fg="white").pack(pady=10)

        tk.Button(root, text="Show Campus Map", command=self.show_map,
                  font=("Arial", 11, "bold"), bg="#2196F3", fg="white").pack(pady=5)

        # Result
        self.result_label = tk.Label(root, text="", font=("Arial", 12), wraplength=500, justify="center")
        self.result_label.pack(pady=20)

        # Exit
        tk.Button(root, text="Exit", command=root.destroy,
                  font=("Arial", 11, "bold"), bg="#E74C3C", fg="white").pack(pady=10)

    def find_path(self):
        start = self.start_var.get()
        end = self.end_var.get()

        if not start or not end:
            messagebox.showwarning("Input Error", "Please select both locations!")
            return
        if start == end:
            messagebox.showinfo("Same Location", "Start and destination cannot be the same.")
            return

        distance, path = dijkstra(self.graph, start, end)

        if distance == float("inf"):
            self.result_label.config(text="❌ No route found.")
        else:
            route = " → ".join(path)
            self.result_label.config(text=f"✅ Path: {route}\n📏 Distance: {distance} units.")
            show_graph(self.graph, path)

    def show_map(self):
        show_graph(self.graph)

if __name__ == "__main__":
    root = tk.Tk()
    app = CampusNavigatorApp(root)
    root.mainloop()