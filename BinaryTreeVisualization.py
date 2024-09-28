import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
import time

# Node class for the binary tree
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Function to create a larger binary tree
def create_large_tree():
    root = TreeNode(1)
    # Level 1
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    
    # Level 2
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)
    
    # Level 3
    root.left.left.left = TreeNode(8)
    root.left.left.right = TreeNode(9)
    root.left.right.left = TreeNode(10)
    root.left.right.right = TreeNode(11)
    root.right.left.left = TreeNode(12)
    root.right.left.right = TreeNode(13)
    root.right.right.left = TreeNode(14)
    root.right.right.right = TreeNode(15)
    
    # Level 4
    root.left.left.left.left = TreeNode(16)
    root.left.left.left.right = TreeNode(17)
    root.left.left.right.left = TreeNode(18)
    root.left.left.right.right = TreeNode(19)
    root.left.right.left.left = TreeNode(20)
    root.left.right.left.right = TreeNode(21)
    root.left.right.right.left = TreeNode(22)
    root.left.right.right.right = TreeNode(23)
    root.right.left.left.left = TreeNode(24)
    root.right.left.left.right = TreeNode(25)
    root.right.left.right.left = TreeNode(26)
    root.right.left.right.right = TreeNode(27)
    root.right.right.left.left = TreeNode(28)
    root.right.right.left.right = TreeNode(29)
    root.right.right.right.left = TreeNode(30)
    root.right.right.right.right = TreeNode(31)
    
    # Level 5 (adding 30 more values)
    root.left.left.left.left.left = TreeNode(32)
    root.left.left.left.left.right = TreeNode(33)
    root.left.left.left.right.left = TreeNode(34)
    root.left.left.left.right.right = TreeNode(35)
    root.left.left.right.left.left = TreeNode(36)
    root.left.left.right.left.right = TreeNode(37)
    root.left.left.right.right.left = TreeNode(38)
    root.left.left.right.right.right = TreeNode(39)
    root.left.right.left.left.left = TreeNode(40)
    root.left.right.left.left.right = TreeNode(41)
    root.left.right.left.right.left = TreeNode(42)
    root.left.right.left.right.right = TreeNode(43)
    root.left.right.right.left.left = TreeNode(44)
    root.left.right.right.left.right = TreeNode(45)
    root.left.right.right.right.left = TreeNode(46)
    root.left.right.right.right.right = TreeNode(47)
    root.right.left.left.left.left = TreeNode(48)
    root.right.left.left.left.right = TreeNode(49)
    root.right.left.left.right.left = TreeNode(50)
    root.right.left.left.right.right = TreeNode(51)
    root.right.left.right.left.left = TreeNode(52)
    root.right.left.right.left.right = TreeNode(53)
    root.right.left.right.right.left = TreeNode(54)
    root.right.left.right.right.right = TreeNode(55)

    return root

# Function to create a hierarchical position layout
def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    """If the graph is a tree, this gives a layout where the parents are centered
    above their children."""
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
    """Recursively compute positions of nodes in a tree structure."""
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
        
    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)  # prevent going back to parent
    
    if len(children) != 0:
        dx = width / len(children)
        nextx = xcenter - width/2 - dx/2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root, parsed=parsed)
    
    return pos

# Function to perform level-order traversal and visualize step by step
def level_order_traversal(root):
    if not root:
        return
    
    # Create a directed graph to represent the tree
    G = nx.DiGraph()
    labels = {}
    
    # BFS queue to explore nodes level by level
    queue = deque([root])
    
    # Set up plot
    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots(figsize=(15, 10))
    
    while queue:
        node = queue.popleft()
        
        # Add the current node to the graph
        G.add_node(node.value)
        labels[node.value] = str(node.value)
        
        # Explore children and add edges
        if node.left:
            G.add_edge(node.value, node.left.value)
            queue.append(node.left)
        if node.right:
            G.add_edge(node.value, node.right.value)
            queue.append(node.right)
        
        # Clear the plot for the next frame
        ax.clear()
        
        # Use the custom hierarchical layout for the positions
        pos = hierarchy_pos(G, root=1)  # 1 is the root node value
        
        # Draw the graph with the current set of nodes and edges
        nx.draw(G, pos, labels=labels, with_labels=True, node_size=500, font_size=8, node_color="lightblue", arrows=False, ax=ax)
        
        plt.title("Binary Tree Formation")
        plt.axis("off")  # Turn off the axis
        plt.draw()  # Draw the updated plot
        plt.pause(0.5)  # Pause to allow viewing the step (0.5 seconds per step)
        
    plt.ioff()  # Turn off interactive mode
    plt.show()  # Show the final plot

# Main function to run the visualization
def visualize_large_tree():
    root = create_large_tree()
    level_order_traversal(root)

visualize_large_tree()
