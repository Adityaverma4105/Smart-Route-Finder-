import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import json
import os

class GraphRouteFinder:
    def __init__(self):
        self.graph = {}
        self.load_default_graph()
        self.create_gui()

    def load_default_graph(self):
        """Load default graph or from file if exists"""
        default_graph = {
            'A': {'B': 4, 'C': 2},
            'B': {'A': 4, 'C': 1, 'D': 5},
            'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
            'D': {'B': 5, 'C': 8, 'E': 2, 'F': 6},
            'E': {'C': 10, 'D': 2, 'F': 2},
            'F': {'D': 6, 'E': 2}
        }
        
        # Check if there's a saved graph
        if os.path.exists("graph_data.json"):
            try:
                with open("graph_data.json", "r") as f:
                    self.graph = json.load(f)
            except:
                self.graph = default_graph
        else:
            self.graph = default_graph

    def save_graph(self):
        """Save current graph to file"""
        with open("graph_data.json", "w") as f:
            json.dump(self.graph, f)

    def dijkstra(self, start, end):
        """Find shortest path using Dijkstra's algorithm"""
        if start not in self.graph or end not in self.graph:
            return float('inf'), []
            
        pq = [(0, start)]
        dist = {node: float('inf') for node in self.graph}
        dist[start] = 0
        parent = {node: None for node in self.graph}
        visited = set()

        while pq:
            curr_dist, node = heapq.heappop(pq)
            
            if node in visited:
                continue
                
            visited.add(node)
            
            if node == end:
                break
                
            for neighbor, weight in self.graph[node].items():
                if neighbor not in visited:
                    new_dist = curr_dist + weight
                    if new_dist < dist[neighbor]:
                        dist[neighbor] = new_dist
                        parent[neighbor] = node
                        heapq.heappush(pq, (new_dist, neighbor))

        # Reconstruct path
        path = []
        step = end
        while step is not None:
            path.append(step)
            step = parent[step]
        path.reverse()
        
        if dist[end] == float('inf'):
            return float('inf'), []
        return dist[end], path

    def add_edge(self, node1, node2, weight):
        """Add edge to the graph"""
        if node1 not in self.graph:
            self.graph[node1] = {}
        if node2 not in self.graph:
            self.graph[node2] = {}
            
        self.graph[node1][node2] = weight
        self.graph[node2][node1] = weight  # Assuming undirected graph

    def remove_edge(self, node1, node2):
        """Remove edge from the graph"""
        if node1 in self.graph and node2 in self.graph[node1]:
            del self.graph[node1][node2]
        if node2 in self.graph and node1 in self.graph[node2]:
            del self.graph[node2][node1]

    def get_nodes(self):
        """Get all nodes in the graph"""
        return list(self.graph.keys())

    def visualize_graph(self, path=None):
        """Visualize the graph with matplotlib"""
        G = nx.Graph()
        
        # Add edges to networkx graph
        for node, neighbors in self.graph.items():
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)
        
        pos = nx.spring_layout(G)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Draw all edges
        nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5, ax=ax)
        
        # Draw path edges if provided
        if path and len(path) > 1:
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, ax=ax)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=700, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=16, font_weight='bold', ax=ax)
        
        # Draw edge labels
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
        
        ax.set_title("Graph Visualization")
        ax.axis('off')
        
        return fig

    def create_gui(self):
        """Create the main GUI"""
        self.root = tk.Tk()
        self.root.title("Advanced Smart Route Finder")
        self.root.geometry("1000x700")
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Advanced Route Finder", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Route finder section
        route_frame = ttk.LabelFrame(main_frame, text="Find Route", padding="10")
        route_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(route_frame, text="Start Node:").grid(row=0, column=0, padx=(0, 5))
        self.start_var = tk.StringVar()
        self.start_menu = ttk.Combobox(route_frame, textvariable=self.start_var, values=self.get_nodes(), width=10)
        self.start_menu.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(route_frame, text="End Node:").grid(row=0, column=2, padx=(0, 5))
        self.end_var = tk.StringVar()
        self.end_menu = ttk.Combobox(route_frame, textvariable=self.end_var, values=self.get_nodes(), width=10)
        self.end_menu.grid(row=0, column=3, padx=(0, 20))
        
        find_btn = ttk.Button(route_frame, text="Find Shortest Path", command=self.find_route)
        find_btn.grid(row=0, column=4, padx=(0, 10))
        
        # Graph editor section
        editor_frame = ttk.LabelFrame(main_frame, text="Graph Editor", padding="10")
        editor_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Add edge controls
        ttk.Label(editor_frame, text="Node 1:").grid(row=0, column=0, padx=(0, 5))
        self.node1_var = tk.StringVar()
        ttk.Entry(editor_frame, textvariable=self.node1_var, width=10).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(editor_frame, text="Node 2:").grid(row=0, column=2, padx=(0, 5))
        self.node2_var = tk.StringVar()
        ttk.Entry(editor_frame, textvariable=self.node2_var, width=10).grid(row=0, column=3, padx=(0, 10))
        
        ttk.Label(editor_frame, text="Weight:").grid(row=0, column=4, padx=(0, 5))
        self.weight_var = tk.StringVar()
        ttk.Entry(editor_frame, textvariable=self.weight_var, width=10).grid(row=0, column=5, padx=(0, 10))
        
        add_btn = ttk.Button(editor_frame, text="Add Edge", command=self.add_edge_handler)
        add_btn.grid(row=0, column=6, padx=(0, 10))
        
        remove_btn = ttk.Button(editor_frame, text="Remove Edge", command=self.remove_edge_handler)
        remove_btn.grid(row=0, column=7, padx=(0, 10))
        
        refresh_btn = ttk.Button(editor_frame, text="Refresh Nodes", command=self.refresh_node_menus)
        refresh_btn.grid(row=0, column=8, padx=(0, 10))
        
        save_btn = ttk.Button(editor_frame, text="Save Graph", command=self.save_graph)
        save_btn.grid(row=0, column=9)
        
        # Results section
        result_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        result_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        # Text widget for results
        self.result_text = tk.Text(result_frame, height=8, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Visualization section
        viz_frame = ttk.LabelFrame(main_frame, text="Graph Visualization", padding="10")
        viz_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        viz_frame.columnconfigure(0, weight=1)
        viz_frame.rowconfigure(0, weight=1)
        
        # Matplotlib figure
        self.fig = self.visualize_graph()
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Visualize button
        viz_btn = ttk.Button(main_frame, text="Visualize Current Graph", command=self.update_visualization)
        viz_btn.grid(row=5, column=0, columnspan=3, pady=(0, 10))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E))

    def find_route(self):
        """Handle find route button click"""
        start = self.start_var.get()
        end = self.end_var.get()
        
        if not start or not end:
            messagebox.showwarning("Input Error", "Please select both start and end nodes")
            return
            
        if start not in self.graph or end not in self.graph:
            messagebox.showerror("Node Error", "Selected nodes do not exist in the graph")
            return
        
        distance, path = self.dijkstra(start, end)
        
        if distance == float('inf'):
            result_msg = f"No path found from {start} to {end}"
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result_msg)
            self.status_var.set("No path found")
            self.update_visualization([])  # Update visualization with no path
        else:
            result_msg = f"Shortest path from {start} to {end}:\n"
            result_msg += f"Path: {' -> '.join(path)}\n"
            result_msg += f"Distance: {distance} units\n\n"
            
            # Detailed breakdown
            result_msg += "Path Details:\n"
            total = 0
            for i in range(len(path)-1):
                node1, node2 = path[i], path[i+1]
                weight = self.graph[node1][node2]
                total += weight
                result_msg += f"{node1} -> {node2}: {weight} units (Total: {total})\n"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result_msg)
            self.status_var.set(f"Found path with distance {distance}")
            self.update_visualization(path)  # Update visualization with path

    def add_edge_handler(self):
        """Handle add edge button click"""
        node1 = self.node1_var.get().strip().upper()
        node2 = self.node2_var.get().strip().upper()
        weight_str = self.weight_var.get().strip()
        
        if not node1 or not node2:
            messagebox.showwarning("Input Error", "Please enter both node names")
            return
            
        try:
            weight = float(weight_str)
        except ValueError:
            messagebox.showerror("Input Error", "Weight must be a number")
            return
            
        if weight <= 0:
            messagebox.showerror("Input Error", "Weight must be positive")
            return
            
        self.add_edge(node1, node2, weight)
        self.refresh_node_menus()
        self.status_var.set(f"Added edge {node1}-{node2} with weight {weight}")
        messagebox.showinfo("Success", f"Edge {node1}-{node2} added successfully")

    def remove_edge_handler(self):
        """Handle remove edge button click"""
        node1 = self.node1_var.get().strip().upper()
        node2 = self.node2_var.get().strip().upper()
        
        if not node1 or not node2:
            messagebox.showwarning("Input Error", "Please enter both node names")
            return
            
        if node1 not in self.graph or node2 not in self.graph:
            messagebox.showerror("Node Error", "One or both nodes do not exist")
            return
            
        if node2 not in self.graph[node1]:
            messagebox.showerror("Edge Error", f"No edge exists between {node1} and {node2}")
            return
            
        self.remove_edge(node1, node2)
        self.refresh_node_menus()
        self.status_var.set(f"Removed edge {node1}-{node2}")
        messagebox.showinfo("Success", f"Edge {node1}-{node2} removed successfully")

    def refresh_node_menus(self):
        """Refresh the node selection menus"""
        nodes = self.get_nodes()
        self.start_menu['values'] = nodes
        self.end_menu['values'] = nodes

    def update_visualization(self, path=None):
        """Update the graph visualization"""
        # Clear the previous canvas
        self.canvas.get_tk_widget().destroy()
        
        # Create new figure
        self.fig = self.visualize_graph(path)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas.get_tk_widget().master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = GraphRouteFinder()
    app.run()