import math

# Node 0 is regarded as the reference node

element_identifiers = {"R", "V"}

class Node:
    def __init__(self, name):
        self.name = str(name)
        self.branches = []
    def add_branch(self, branch):
        self.branches.append(branch)

class Branch:
    def __init__(self, name, element_type, pos_node, neg_node, magnitude, angle):
        self.name = name
        self.element_type = element_type            
        self.pos_node = str(pos_node)
        self.neg_node = str(neg_node)
        self.magnitude = magnitude
        self.angle = angle # degrees
        if element_type == "R":
            self.impedance = self.expand_complex()
            self.admittance = 1 / self.impedance
        elif element_type == "V":
            self.voltage = self.expand_complex()
    
    def expand_complex(self):
        angle = (self.angle / 180) * math.pi
        return self.magnitude * (math.cos(angle) + math.sin(angle) * 1j)

# class Impedance(Branch):
#     def __init__(self, name, pos_node, neg_node, magnitude, angle):
#         Branch.__init__(self, name, pos_node, neg_node, magnitude, angle)

# class VoltageSource(Branch):
#     def __init__(self, name, pos_node, neg_node, magnitude, angle):
#         Branch.__init__(self, name, pos_node, neg_node, magnitude, angle)

class Circuit():
    def __init__(self):
        self.nodes = {}
        self.elements = set()
        
    def add_branch_to_node(self, branch):
        if branch.name in self.elements:
            return False
        self.elements.add(branch.name)
        for node_name in [branch.pos_node, branch.neg_node]:
            if node_name not in self.nodes:
                self.nodes[node_name] = Node(node_name)
            #print(node_name, "\n\n")
            self.nodes[node_name].add_branch(branch)
            #print(self.nodes[node_name].branches)
        return True