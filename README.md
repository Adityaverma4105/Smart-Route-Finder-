# Smart-Route-Finder
#Algorithm Used – Dijkstra’s Algorithm
Algorithm Steps:
1.	Assign a tentative distance value to every node: 0 for the start node and ∞ for all others.
2.	Set the start node as current.
3.	For the current node, consider all unvisited neighbors and calculate their tentative distances.
4.	If the newly calculated distance is smaller, update it.
5.	Mark the current node as visited.
6.	Select the unvisited node with the smallest tentative distance as the new current node.
7.	Repeat until all nodes are visited or the destination is reached.
Time Complexity:
O(E log V) using a min-heap (where E = edges, V = vertices)
