import sys
import glob
import os

import simple_parser
import simple_solver

from rich.console import Console
from rich.table import Table

import schemdraw
import schemdraw.elements as elm

schematics_folder = "schematics"

def Print_Table(voltages, currents):
    console = Console()
    v_table = Table(show_header=True, header_style="bold purple")
    v_table.add_column("Node")
    v_table.add_column("Voltage")
    v_table.add_row("0 (Reference)", "0")
    for key, value in enumerate(currents):
        v_table.add_row(str(key + 1), str(voltages[key]))
    
    console.print(v_table)
    
    i_table = Table(show_header=True, header_style="bold red")
    i_table.add_column("+ node")
    i_table.add_column("- node")
    i_table.add_column("Current")
    for key, value in enumerate(currents):
        i_table.add_row(str(key + 1), str(key), str(currents[key]))
    
    console.print(i_table)

def Save_Schematic(circuit, voltages, currents, file_name):

    
    d = schemdraw.Drawing()
    elements = {}
    elements["0"] = d.add(elm.Ground)
    drawn = []
    directions = ["up", "right", "down", "left"]
    direc = 0
    for key, node in circuit.nodes.items():
        if key != "0":
            for i, branch in enumerate(node.branches):
                if branch not in drawn:
                    pos, neg = branch.pos_node, branch.neg_node
                    el = None
                    i = int(key) - 1
                    if branch.element_type == "R":                        
                        el = elm.Resistor(directions[direc], lblofst = 1,
                                          label="Ω={z.real:+0.02f} {z.imag:+0.02f}j\nV={v.real:+0.02f} {v.imag:+0.02f}j"
                                                 .format(z=branch.impedance, v=voltages[i]),
                                          to = elements[neg].start if neg in elements else None)
                    else:
                        el = elm.SourceV(label="V = {}".format(str(branch.voltage)))
                    d.add(el)
                    other_node = neg if key == pos else pos
                    new_node = None
                    if key not in elements:
                        new_node = key
                    elif other_node not in elements:
                        new_node = other_node
                    if new_node is not None:
                        label = "Node {}\nI=".format(new_node)
                        c = currents[int(new_node) - 1]
                        label += "{c.real:+0.02f} {c.imag:+0.02f}j".format(c=c) if isinstance(c, complex) else "V-source"
                        if  directions[direc] in ("up", "bottom"):
                            elements[new_node] =  d.add(elm.Dot(lblofst = 1, lftlabel=label))
                        else:
                            elements[new_node] =  d.add(elm.Dot(lblofst = 1, botlabel=label))
                        
                    if neg == "0" and i == len(node.branches) - 1:
                        d.add(elm.Ground)
                    drawn.append(branch)
            direc = (direc + 1) % 4

    #d.draw()
    d.save('schematics/{}.png'.format(file_name.split("\\")[-1]))
    
if __name__ == "__main__":
    args = sys.argv
    file_name = ""
    if len(args) < 2:
        # If no args, look inside "examples" folder
        files = []
        for file in glob.glob("examples/*"):
            files.append(file)
        if len(files) == 0: 
            print("\nNo files to parse")
            sys.exit()
        else:
            file_name = files[0]
    else:
        file_name = args[1].replace("/", "\\")

    circuit = simple_parser.Parse(file_name)
    if not os.path.exists(schematics_folder):
        os.makedirs(schematics_folder)
    voltages, currents = simple_solver.Solve(circuit)
    Print_Table(voltages, currents)
    Save_Schematic(circuit, voltages, currents, file_name)