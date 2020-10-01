import sys
from classes import element_identifiers, Branch, Circuit

num_of_args = 5

def Quit(message):
    print(message)
    sys.exit()

def ParseError(line_num, lines, order, extra_info="", offset=0):
    #print(order, "\n", line[order], "\n")
    message = "\nParsing error at line no. {}\n".format(line_num + 1)
    if extra_info:
        message += "({})\n".format(extra_info)
    if line_num > 0:
        message += "\n    {}    ".format(lines[line_num - 1])
    else:
        message += "\nBegining of file\n" + "-" * 16 + "\n"
        
    message += "\n--> {} <--\n".format(lines[line_num])
    if order > -1:
        line = lines[line_num].split(" ")
        space = 4 + sum([len(line[i]) + 1 for i in range(order)]) + offset
        message += " " * space + "^"
        
    if line_num + 1 < len(lines):
        message += "\n    {}    ".format(lines[line_num + 1])
    else:
        message += "\n" + "-" * 11 + "\nEnd of file"
    Quit(message)

def Parse(file_location):
    try:
        f = open(file_location, "r")
    except Exception as e:
        Quit("{} not found\n".format(file_location))
    
    circuit = Circuit()
    lines = [l.strip() for l in f.readlines()]
    f.close()
    
    for line_num, line in enumerate(lines):
        line = line.split()
        length = len(line)
        if length != num_of_args:
            ParseError(line_num, lines, -1, extra_info = "Too many arguments" if length > num_of_args else "Too few arguments")

        # 0: Element type & branch name
        element_type = None
        branch_name = line[0]
        if line[0][0] in element_identifiers:
            element_type = line[0][0]
        else:
            ParseError(line_num, lines, 0, extra_info = "Expected a valid identifier")
        try:
            int(line[0][1:])
        except:
            ParseError(line_num, lines, 0, extra_info = "Expected an integer value", offset = 1)
        
        # 1,2: pos_node, neg_node
        pos_node, neg_node = None, None
        for i in range(2):
            try:
                value = int(line[i + 1])
                if i == 0:
                    pos_node = value
                else:
                    neg_node = value
            except:
                ParseError(line_num, lines, i + 1, extra_info = "Expected an integer value")
        
        # 3, 4: magnitude, angle
        magnitude, angle = None, None
        for i in range(2):
            try:
                value = float(line[i + 3])
                if i == 0:
                    magnitude = value
                else:
                    angle = value
            except:
                ParseError(line_num, lines, i + 3, extra_info = "Expected a float value")
        
        branch = Branch(branch_name, element_type, pos_node, neg_node, magnitude, angle)
        if not circuit.add_branch_to_node(branch):
            # A duplicate branch name exists if False value is returned
            ParseError(line_num, lines, 0, extra_info = "Element name already exists. Please specify a unique one.")
            
    if "0" not in circuit.nodes.keys():
        ParseError(len(lines) - 1, lines, -1, extra_info = "Reference Node 0 is not specified at all. ")
    
    return circuit