import numpy as np
import sympy as sym
from   scipy import linalg

def Solve(circuit):
    identity = sym.Symbol("Id")
    symbols = {node.name:sym.Symbol(node.name) for node in circuit.nodes.values()}
    currents_symbols = {node.name:sym.Symbol('i'+node.name) for node in circuit.nodes.values()}
    rank = len(circuit.nodes) - 1 # Excluding reference Node 0
    admittances = np.zeros([rank, rank], dtype=complex)
    currents = [0 for _ in range(rank)]
    source_voltages = []
    for key, node in circuit.nodes.items():
        if key != "0":
            expression = 0
            for branch in node.branches:
                other_node = branch.neg_node if key == branch.pos_node else branch.pos_node
                if branch.element_type == "R":
                    expression += (symbols[key] - symbols[other_node]) * branch.admittance
                    # print(key)
                    # print(expression)
                    # print("N:",other_node)
                elif branch.element_type == "V":
                    #print("V:", branch.pos_node, branch.neg_node, "\n\n")
                    source_voltages.append((branch.pos_node, branch.neg_node, branch.voltage))
            
            for pos, neg, voltage in source_voltages:
                if key not in (pos, neg):
                    expression = expression.subs(symbols[pos], symbols[neg] + identity * voltage)
                    
            expression = expression.subs("0", 0) # Substitute 0 into reference Node 0
            expression = expression.expand() # This is necessary because complex numbers do not get automatically expanded in Sympy
            currents[int(key) - 1] += - expression.coeff(identity) # Fill up the admittance matrix
            for key2 in circuit.nodes.keys():
                if key2 != "0":
                    admittances[int(key) - 1, int(key2) - 1]  = expression.coeff(symbols[key2]) # Get coefficient of each symbol
    
    while True:
        substituted = False
        for key in circuit.nodes.keys():
            if key == "0":
                continue
            for key2 in circuit.nodes.keys():
                if key2 == "0":
                    continue
                expression = currents[int(key) - 1]
                if key != key2 and expression.coeff(currents_symbols[key2]) != 0:
                    currents[int(key) - 1] = expression.subs(currents_symbols[key2], currents[int(key2) - 1])
                    substituted = True
        if not substituted:
            break

    #print("\n", "-"*30, "\nAdmittances\n", admittances)
    inverse = linalg.inv(admittances)
    voltages = np.matmul(inverse, currents)
    voltages = [complex(float(sym.re(v)), float(sym.im(v))) for v in voltages]
    
    # Check for contradictions among source_voltages
    for pos, neg, voltage in source_voltages:
        pos_v = voltages[int(pos) - 1] if int(pos) > 0 else complex(0, 0)
        neg_v = voltages[int(neg) - 1] if int(neg) > 0 else complex(0, 0)
        diff_v = pos_v - neg_v
        if not np.isclose(diff_v.real, voltage.real) or not np.isclose(diff_v.imag, voltage.imag):
            #print("\nVoltage contradiction at V {}-{}", pos, neg)
            voltages[int(pos) - 1] = neg_v + voltage
    
    # Update values of currents
    for key, value in enumerate(currents):
        pos = str(key + 1)
        pos_node = circuit.nodes[pos]
        neg = str(key)
        for branch in pos_node.branches:
            if {pos, neg} == {branch.pos_node, branch.neg_node}:
                chosen_branch = branch
                if chosen_branch.element_type == "R":
                    
                    pos_v = voltages[int(pos) - 1] if int(pos) > 0 else complex(0, 0)
                    neg_v = voltages[int(neg) - 1] if int(neg) > 0 else complex(0, 0)
                    currents[key] = (pos_v - neg_v) / chosen_branch.impedance
                else:
                    currents[key] = "Voltage source"
                break
    
    #print("\n", "-"*30, "\nInverse\n", inverse, "\n\nCurrents\n", currents, "\n\nVoltages\n", voltages)
    return voltages, currents