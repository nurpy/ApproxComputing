from pycparser import c_parser, c_ast, parse_file, c_generator
import re

def getParseSections(file_name):
    fileConts=""
    with open(file_name,"r") as file:
            fileConts = file.read()
    sectionsToParse = []
    parsedText = ""
    parseText_flag = False
    for line in fileConts.splitlines():
        if(line.find("//StopParse") != -1):
            parseText_flag= False
            if bool(parsedText.strip()):# section has text
                sectionsToParse.append(parsedText)
                parsedText = ""
        if parseText_flag:
            if(line.find("//Exclude") == -1):
                parsedText += line + "\n"
        if(line.find("//Parse") != -1):
            parseText_flag= True
        
    #sectionsToParse = [ "DUMMYFUNC {\n" + section + "\n}" for section in sectionsToParse]

    return sectionsToParse

def preProcessText(file_name):
    #strings = re.findall(r"(?:for|if|while)\s*\([^\)]*\)\s*\{([\s\S]*?)\}",text)
    fileConts=""
    with open(file_name,"r") as file:
        fileConts = file.read()
    countLineNumber = 0
    parseTextFlag = False
    for line in fileConts.splitlines():
        countLineNumber+=1
        if parseTextFlag:        
            if(line.find("if") != -1 and line.find("(") != -1  and line.find(")") != -1 and line.find("//") == -1 and line.find("/*") == -1 and line.find("{") == -1):
                print(line)
                raise Exception("All iff statements should be of form \nif(xxx){\ndata\n} \noccured at line " + str(countLineNumber))
            if line.find("for") != -1 and line.find("(") != -1 and line.count(";") > 1 and line.find("{") == -1:
                print(line)
                raise Exception("All loops should be of the form \nfor(xxx){\ndata\n} \noccured at line " + str(countLineNumber))
        if line.find("Parse") != -1:
            parseTextFlag=True
        if line.find("StopParse") != -1:
            parseTextFlag=False
        

    


def parseText(file_name,introtext):


    map_of_func_defs={}
    map_of_if_defs={}
    map_of_all_if_defs={}
    map_of_for_loop_unroll = {}

    generator = c_generator.CGenerator()
    
    class RvalueVariableVisitor(c_ast.NodeVisitor):
        def visit_Return(self,node):
            pass# you need to add a token here to show that this value can not be approximated
        def visit_FuncDef(self,node):
            pass# you need to add a token here to show that this value can not be approximated
            #print(node)
            map_of_func_defs[node.coord.line] = node.decl.name
    #        arr_of_funcs.append((node.coord.line,node.decl.name))
    #        print(f"Function {node.decl.name} starts at line {node.coord.line} and ends at line {node.body.coord.line}")
            self.generic_visit(node)  # Continue to traverse the AST
        def visit_For(self,node):
            if isinstance(node.init, c_ast.DeclList):  # If the initialization is a declaration
                for decl in node.init.decls:
                    pass

                    #map_of_for_loop_unroll[node.coord.line+1] = f"std::vector<int> INDEX_LOOP;INDEX_LOOP.push_back({decl.name})"
                    loop_text = generator.visit(node)  # Convert AST node back to C code
                    number_of_lines=1
                    for line in loop_text.splitlines():
                        if(line.find("{") != -1):# the new code always has { on a new line
                            continue
                        number_of_lines+=1
                    map_of_for_loop_unroll[node.coord.line] = decl.name

            elif isinstance(node.init, c_ast.Assignment):  # If the initialization is an assignment (e.g., i = 0
                
                loop_text = generator.visit(node)  # Convert AST node back to C code
                number_of_lines=0
                for line in loop_text.splitlines():
                    if(line.find("{") != -1):# the new code always has { on a new line
                        continue
                map_of_for_loop_unroll[node.coord.line] = node.init.lvalue.name


            if isinstance(node.stmt, c_ast.Compound):
                pass
            else:
                map_of_if_defs[node.coord.line] = 1
                map_of_if_defs[node.coord.line+1] = 2
                print(f"Found for loop without braces: {(node.coord.line)}")

            self.generic_visit(node)

        def visit_If(self, node):
            # Check if the 'iftrue' (body of the 'if') is a single statement, not a Compound node
            map_of_all_if_defs[node.coord.line] = True
            if node.iftrue:
                if isinstance(node.iftrue, c_ast.Compound):
                    pass
                else:
                    try:
                        operator=node.op
                        print(node.iftrue)
                        map_of_if_defs[node.coord.line] = 1
                        map_of_if_defs[node.coord.line+1] = 2
                    except:
                        pass

            # Check the 'else' part similarly
                
            if node.iffalse:
                if isinstance(node.iffalse, c_ast.Compound):
                    pass
                else:
                    print("Else block without braces found.")
                    map_of_if_defs[node.coord.line+2] = 1
                    map_of_if_defs[node.coord.line+3] = 2
            self.generic_visit(node)  # Continue to traverse the AST

        
            


    
    fileConts=""
    with open(file_name,"r") as file:
        fileConts = file.read()
    prevline=""
    preText = "" 


    comment_code = fileConts


    """
    for line in fileConts.splitlines():
        if line.find("if") != -1 and prevline.find("if") != -1 and line.find("{") == -1 and prevline.find("{") == -1:
            line = "\n" + line
        if(len(line) > 0):
            line = line.split("//")[0];
            
        preText += line + "\n"
        prevline = line
    """
    for line in fileConts.splitlines():
        if line.find("//Ignore") != -1:
            continue
        preText+=line+"\n"


    


    code = preText
    




    c_code = code
    c_code = c_code.replace(r"\\",r"\\\\")
    result = re.sub(r'#.*?["].*?["]', '', c_code)
    result = re.sub(r'#.*?[">]', '', result)
    result = re.sub(r'//.*', '', result)
    result = re.sub(r'/\*.*', '', result)
    result = re.sub(r'\*/.*', '', result)
    result = re.sub(r'\*\*.*', '', result)

    text=""
    line_number = 0
    map_of_declaratives = {}
    for line in result.splitlines():
        if  line.find("#ifdef") == -1 and line.find("#else") == -1 and line.find("#endif") == -1 and line.find("#define") == -1 and line.find("#pragma") == -1:

            if(len(line.strip()) > 0):
                if(line.strip()[0] == "*"):
                    line = ""
                    map_of_declaratives[line_number] = line
            text+=line + "\n"
        else:
            text+= "\n"
            map_of_declaratives[line_number] = line


    parser = c_parser.CParser()
    ast = parser.parse(text)
    visitor = RvalueVariableVisitor()
    visitor.visit(ast)
    # Visit all nodes in the AST
    visitor.visit(ast)
    text = "" 

    hashmap_of_lvalue_names = {}

    line_number=0
    parseText_flag = False
    #print(comment_code)
    for line in comment_code.splitlines():
        line_number+=1


        if(line.find("//StopParse") != -1) or line.find("/*Exclude") != -1:
            parseText_flag= False
            
        if parseText_flag and line.find("//Exclude") == -1:
            #parse text with extra code
            text += line 
            if line_number > min(map_of_func_defs.keys()): #make sure your not doing global variables
                curline = line.strip()
                curline = curline.split("//")[0]
                if not curline:
                    text += "\n"
                    continue
                if ";" == curline[len(curline)-1] and line_number not in map_of_all_if_defs: #valid line
                    #now perform checks to determin type
                    #if its an array or not
            #        Tokens_in_line = line.split("")
                    Tokens_in_line = re.split("= | \|= |\+= |\-=",line)
                    
                    if len(Tokens_in_line) > 1:
                        lvalue = Tokens_in_line[0]
                        lvalue = lvalue.strip()
                        lvalue = lvalue.split(" ")
                        lvalue = (lvalue[len(lvalue)-1])

                        if lvalue.find("[") == -1:
                            #text+= lvalue
                            text+=f"print(LOOPVARIABLE,\"{line_number}\" + CurrentFunctionName,{lvalue},\"{lvalue}_file\");"
                        else:
                            lvalue_elements = lvalue.split("[")
                            lvalue_name = lvalue_elements.pop(0)
                            arr_of_indexes=[]
                            for element in lvalue_elements:
                                index  = element.replace("]","").replace("[","")
                                text += f"{lvalue_name}_arr.push_back({index});"

                            text+=f"print(LOOPVARIABLE,{lvalue_name}_arr,\"{line_number}\" + CurrentFunctionName,{lvalue},\"{lvalue_name}_file\");"
                            text+=f"{lvalue_name}_arr.clear();"

                            hashmap_of_lvalue_names[lvalue_name] = line_number
            text+="\n"


        else:
            #add line normally
            if line.find("/*Exclude") == -1 and line.find("*/Exclude") == -1:
                text+=line + "\n"
            
        if(line.find("//Parse") != -1 or line.find("*/Exclude") != -1):
            parseText_flag= True


        

                    



    line_number = 1
    actual_line_number = 1
    map_of_lvalues={}
    file_text = ""
    for line in text.splitlines():
        




        if line_number not in map_of_func_defs:
            """
            if line_number in map_of_if_defs:
                if map_of_if_defs[line_number] == 1:
                    pattern = r"if\s*\(\s*[^()]*\s*(?:\([^)]*\))*\s*[^)]*\s*\)"
                    line = re.sub(pattern, r'\g<0> {',line)
                    pattern = r"for\s*\(\s*[^()]*\s*(?:\([^)]*\))*\s*[^)]*\s*\)"
                    line = re.sub(pattern, r'\g<0> {',line)
                    pattern = "else"
                    line = line.replace("else","else{")
                elif map_of_if_defs[line_number] == 2:
                    line += "}"
            """
            if(line.find("//UNROLL") != -1 and line.find("for ") != -1):
                forLoopVariable = map_of_for_loop_unroll[line_number] 
                line = line+"\n"+f"LOOPVARIABLE.push_back({forLoopVariable});"
            if(line.find("//STOPUNROLL") != -1):
                line = f"LOOPVARIABLE.pop_back();\n" + line 
            file_text+=line + "\n"
            line_number+=1
            actual_line_number+=1
            continue
        else:
            func_name = map_of_func_defs[line_number]
            func_name = func_name.capitalize()
            if line.find("{") == -1:
                file_text += line + "\n"
                map_of_func_defs[line_number+1] = func_name
                line_number+=1
                actual_line_number+=1
                continue


            file_text += line + "\n"
            file_text+= f"std::string CurrentFunctionName = \"{func_name}_FUNCNAME\";" + "\n"
            actual_line_number+=1
            for lvalue_name,line in hashmap_of_lvalue_names.items():
                file_text+= f"std::vector<int> {lvalue_name}_arr;" + "\n"
                #file_text+= f"std::vector<int> {lvalue_name}_arr;" + "\n"

                actual_line_number+=1
            file_text+="std::vector<int> LOOPVARIABLE;\n"
            actual_line_number+=1


            line_number+=1
            actual_line_number+=1


    file_text = introtext+file_text
    return file_text

def loopIterationToNumber(value):
    try:
        iteration = ''.join(value)
    except:
        return None
    try:
        iteration=int(iteration)
    except:
        iteration=None
    return iteration
def removeIndex(value):
    return value.replace("[","").replace("]","")
def test_varaible(file_name,introtext,varaiable_name,dataName):
    print(f"IMPORTANT {varaiable_name}")
    print(f"IMPORTANT {dataName}")
 
    loopiter=None
    lineNum=None
    #def getlineNume_and_varName():
    replacedLineNumber =dataName[dataName.find("/")+1:]
    replacedLineNumber = replacedLineNumber.split("^")[-1]
    lineNum=""
    v=0
    while(replacedLineNumber[v].isdigit()):
        lineNum+=replacedLineNumber[v]
        v+=1
    lineNum=int(lineNum)
    if(dataName.find("^") != -1):
        #has loops
        #loopiter = dataName.split("^")[1]
        loopiter = [x for x in dataName.split("^") if x.isdigit()]
    else:
        loopiter=None
        #no loops
    print(loopiter)


    map_of_func_defs={}
    map_of_if_defs={}
    map_of_all_if_defs={}
    map_of_for_loop_unroll = {}

    generator = c_generator.CGenerator()
    
    class RvalueVariableVisitor(c_ast.NodeVisitor):
        def visit_Return(self,node):
            pass# you need to add a token here to show that this value can not be approximated
        def visit_FuncDef(self,node):
            pass# you need to add a token here to show that this value can not be approximated
            #print(node)
            map_of_func_defs[node.coord.line] = node.decl.name
    #        arr_of_funcs.append((node.coord.line,node.decl.name))
    #        print(f"Function {node.decl.name} starts at line {node.coord.line} and ends at line {node.body.coord.line}")
            self.generic_visit(node)  # Continue to traverse the AST
        def visit_For(self,node):
            if isinstance(node.init, c_ast.DeclList):  # If the initialization is a declaration
                for decl in node.init.decls:
                    pass

                    #map_of_for_loop_unroll[node.coord.line+1] = f"std::vector<int> INDEX_LOOP;INDEX_LOOP.push_back({decl.name})"
                    loop_text = generator.visit(node)  # Convert AST node back to C code
                    number_of_lines=1
                    for line in loop_text.splitlines():
                        if(line.find("{") != -1):# the new code always has { on a new line
                            continue
                        number_of_lines+=1
                    map_of_for_loop_unroll[node.coord.line] = decl.name

            elif isinstance(node.init, c_ast.Assignment):  # If the initialization is an assignment (e.g., i = 0
                
                loop_text = generator.visit(node)  # Convert AST node back to C code
                number_of_lines=0
                for line in loop_text.splitlines():
                    if(line.find("{") != -1):# the new code always has { on a new line
                        continue
                map_of_for_loop_unroll[node.coord.line] = node.init.lvalue.name


            if isinstance(node.stmt, c_ast.Compound):
                pass
            else:
                map_of_if_defs[node.coord.line] = 1
                map_of_if_defs[node.coord.line+1] = 2
                print(f"Found for loop without braces: {(node.coord.line)}")

            self.generic_visit(node)

        def visit_If(self, node):
            # Check if the 'iftrue' (body of the 'if') is a single statement, not a Compound node
            map_of_all_if_defs[node.coord.line] = True
            if node.iftrue:
                if isinstance(node.iftrue, c_ast.Compound):
                    pass
                else:
                    try:
                        operator=node.op
                        print(node.iftrue)
                        map_of_if_defs[node.coord.line] = 1
                        map_of_if_defs[node.coord.line+1] = 2
                    except:
                        pass

            # Check the 'else' part similarly
                
            if node.iffalse:
                if isinstance(node.iffalse, c_ast.Compound):
                    pass
                else:
                    print("Else block without braces found.")
                    map_of_if_defs[node.coord.line+2] = 1
                    map_of_if_defs[node.coord.line+3] = 2
            self.generic_visit(node)  # Continue to traverse the AST

        
            


    fileConts=""
    with open(file_name,"r") as file:
        fileConts = file.read()
    prevline=""
    preText = ""

    #fileConts=file_name


    comment_code = fileConts


    """
    for line in fileConts.splitlines():
        if line.find("if") != -1 and prevline.find("if") != -1 and line.find("{") == -1 and prevline.find("{") == -1:
            line = "\n" + line
        if(len(line) > 0):
            line = line.split("//")[0];
            
        preText += line + "\n"
        prevline = line
    """
    for line in fileConts.splitlines():
        if line.find("//Ignore") != -1:
            continue
        preText+=line+"\n"


    


    code = preText
    




    c_code = code
    c_code = c_code.replace(r"\\",r"\\\\")
    result = re.sub(r'#.*?["].*?["]', '', c_code)
    result = re.sub(r'#.*?[">]', '', result)
    result = re.sub(r'//.*', '', result)
    result = re.sub(r'/\*.*', '', result)
    result = re.sub(r'\*/.*', '', result)
    result = re.sub(r'\*\*.*', '', result)

    text=""
    line_number = 0
    map_of_declaratives = {}
    for line in result.splitlines():
        if  line.find("#ifdef") == -1 and line.find("#else") == -1 and line.find("#endif") == -1 and line.find("#define") == -1 and line.find("#pragma") == -1:

            if(len(line.strip()) > 0):
                if(line.strip()[0] == "*"):
                    line = ""
                    map_of_declaratives[line_number] = line
            text+=line + "\n"
        else:
            text+= "\n"
            map_of_declaratives[line_number] = line


    parser = c_parser.CParser()
    ast = parser.parse(text)
    visitor = RvalueVariableVisitor()
    visitor.visit(ast)
    # Visit all nodes in the AST
    visitor.visit(ast)
    text = "" 

    hashmap_of_lvalue_names = {}

    line_number=0
    parseText_flag = False
    #print(comment_code)
    for line in comment_code.splitlines():
        line_number+=1


        if(line.find("//StopParse") != -1) or line.find("/*Exclude") != -1:
            parseText_flag= False
            
        if parseText_flag and line.find("//Exclude") == -1:
            #parse text with extra code
            text += line 
            if line_number > min(map_of_func_defs.keys()): #make sure your not doing global variables
                curline = line.strip()
                curline = curline.split("//")[0]
                if not curline:
                    text += "\n"
                    continue
                if ";" == curline[len(curline)-1] and line_number not in map_of_all_if_defs: #valid line
                    #now perform checks to determin type
                    #if its an array or not
            #        Tokens_in_line = line.split("")
                    Tokens_in_line = re.split("= | \|= |\+= |\-=",line)
                    def get_assignment_type(equation):
                        """
                        Finds the first compound assignment operator (+=, -=, *=, /=, etc.) in a string
                        and returns its type.

                        Args:
                            equation: The string containing the equation.

                        Returns:
                            A tuple containing the operator and its type, or None if no match is found.
                        """
                        pattern = r"([+\-*/%&|^]?=)"
                        match = re.search(pattern, equation)

                        if match:
                            operator = match.group(1)
                            if operator == '=':
                                return operator
                            elif operator == '+=':
                                return operator
                            elif operator == '-=':
                                return operator
                            elif operator == '*=':
                                return operator
                            elif operator == '/=':
                                return operator
                            elif operator == '%=':
                                return operator
                            elif operator == '&=':
                                return operator
                            elif operator == '|=':
                                return operator
                            elif operator == '^=':
                                return operator
                            else:
                                return operator
                        else:
                            return None
                    assignmentop = get_assignment_type(line.strip())
                    assignmentop = "="
                    
                    if len(Tokens_in_line) > 1:
                        lvalue = Tokens_in_line[0]
                        lvalue = lvalue.strip()
                        lvalue = lvalue.split(" ")
                        lvalue = (lvalue[len(lvalue)-1])
                        lvalue_true_name = lvalue.split("[")[0]
                        varaiable_true_name = varaiable_name.split("[")[0]

                        
                        if (lvalue == varaiable_name or lvalue_true_name == varaiable_true_name) and lineNum == line_number:
                            print(line_number)
                            if loopiter == None:
                                if varaiable_name.find("[") == -1:
                                #text+= lvalue
                                    text+=f"{lvalue} {assignmentop} readValue(\"{line_number}\" + CurrentFunctionName,\"{lvalue}_file\",{removeIndex(varaiable_name)}{loopIterationToNumber(loopiter)}_dataArr);"
                                #text+=f"print(LOOPVARIABLE,\"{line_number}\" + CurrentFunctionName,{lvalue},\"{lvalue}_file\");"
                                else:
                                    lvalue_elements = lvalue.split("[")
                                    lvalue_name = lvalue_elements.pop(0)
                                    arr_of_indexes=[]

                                    varaiable_name_chars = list(varaiable_name)
                                    indexArr=[ f"{[int(i)]}" for i in varaiable_name_chars if i.isdigit()] #variable indexes
                                    index_string = ''.join(indexArr)

                                    #original indexes 
                                    conditional=[]
                                    arrayindecies = ""
                                        
                                    for element,element2 in zip(indexArr,lvalue_elements):
                                        index  = element.replace("]","").replace("[","")
                                        index2  = element2.replace("]","").replace("[","")
                                        conditional.append(f"{index} == {index2}")
                                        arrayindecies += f"{lvalue_name}_arr.push_back({index});"
                                    if_statement = " && ".join(conditional)

                                    #text+=f"{lvalue_name}{index_string} = readValue({lvalue_name}_arr,CurrentFunctionName,\"{lvalue_name}_file\");"

                                    if_statement = f"if({if_statement})" +  "{"+ f"{arrayindecies} {lvalue_name}{index_string} {assignmentop} readValue({lvalue_name}_arr,\"{line_number}\"+CurrentFunctionName,\"{lvalue_name}_file\",{removeIndex(varaiable_name)}{loopIterationToNumber(loopiter)}_dataArr);"  
                                    text+=if_statement

                                    text+=f"{lvalue_name}_arr.clear();" + "}"
                                    hashmap_of_lvalue_names[lvalue_name] = line_number
                            else:
                                if varaiable_name.find("[") == -1:
                                    loop_conditional="if("
                                    count=0
                                    for i in loopiter:
                                        if(count > 0):
                                            loop_conditional+=" && "
                                        loop_conditional+=f"{i} == LOOPVARIABLE[{count}] "
                                        count+=1
                                    loop_conditional+=")"


                                    text+=f"{loop_conditional}" + "{" + f"{lvalue} {assignmentop} readValue( \"{line_number}\" + CurrentFunctionName,\"{lvalue}_file\",LOOPVARIABLE,{removeIndex(varaiable_name)}{loopIterationToNumber(loopiter)}_dataArr);" + "}"
                                #text+=f"print(LOOPVARIABLE,\"{line_number}\" + CurrentFunctionName,{lvalue},\"{lvalue}_file\");"
                                else:

                                    loop_conditional=""
                                    count=0
                                    for i in loopiter:
                                        if(count > 0):
                                            loop_conditional+=" && "
                                        loop_conditional+=f"{i} == LOOPVARIABLE[{count}] "
                                        count+=1
                                    loop_conditional+=""


                                    lvalue_elements = lvalue.split("[")
                                    lvalue_name = lvalue_elements.pop(0)
                                    arr_of_indexes=[]

                                    varaiable_name_chars = list(varaiable_name)
                                    indexArr=[ f"{[int(i)]}" for i in varaiable_name_chars if i.isdigit()] #variable indexes
                                    index_string = ''.join(indexArr)

                                    #original indexes 
                                    conditional=[]
                                    arrayindecies = ""
                                        
                                    for element,element2 in zip(indexArr,lvalue_elements):
                                        index  = element.replace("]","").replace("[","")
                                        index2  = element2.replace("]","").replace("[","")
                                        conditional.append(f"{index} == {index2}")
                                        arrayindecies += f"{lvalue_name}_arr.push_back({index});"
                                    if_statement = " && ".join(conditional)
                                    if_statement += f"&& {loop_conditional}"

                                    #text+=f"{lvalue_name}{index_string} = readValue({lvalue_name}_arr,CurrentFunctionName,\"{lvalue_name}_file\");"

                                    if_statement = f"if({if_statement})" +  "{"+ f"{arrayindecies} {lvalue_name}{index_string} {assignmentop} readValue({lvalue_name}_arr,\"{line_number}\"+CurrentFunctionName,\"{lvalue_name}_file\",LOOPVARIABLE,{removeIndex(varaiable_name)}{loopIterationToNumber(loopiter)}_dataArr);" 
                                    text+=if_statement

                                    text+=f"{lvalue_name}_arr.clear(); " + "}"
                                    hashmap_of_lvalue_names[lvalue_name] = line_number


            text+="\n"


        else:
            #add line normally
            if line.find("/*Exclude") == -1 and line.find("*/Exclude") == -1:
                text+=line + "\n"
            
        if(line.find("//Parse") != -1 or line.find("*/Exclude") != -1):
            parseText_flag= True


        

                    



    line_number = 1
    actual_line_number = 1
    map_of_lvalues={}
    file_text = ""
    for line in text.splitlines():
        




        if line_number not in map_of_func_defs:
            """
            if line_number in map_of_if_defs:
                if map_of_if_defs[line_number] == 1:
                    pattern = r"if\s*\(\s*[^()]*\s*(?:\([^)]*\))*\s*[^)]*\s*\)"
                    line = re.sub(pattern, r'\g<0> {',line)
                    pattern = r"for\s*\(\s*[^()]*\s*(?:\([^)]*\))*\s*[^)]*\s*\)"
                    line = re.sub(pattern, r'\g<0> {',line)
                    pattern = "else"
                    line = line.replace("else","else{")
                elif map_of_if_defs[line_number] == 2:
                    line += "}"
            """
            if(line.find("//UNROLL") != -1 and line.find("for ") != -1):
                forLoopVariable = map_of_for_loop_unroll[line_number] 
                line = line+"\n"+f"LOOPVARIABLE.push_back({forLoopVariable});"
            if(line.find("//STOPUNROLL") != -1):
                line = f"LOOPVARIABLE.pop_back();\n" + line 
            file_text+=line + "\n"
            line_number+=1
            actual_line_number+=1
            continue
        else:
            func_name = map_of_func_defs[line_number]
            func_name = func_name.capitalize()
            if line.find("{") == -1:
                file_text += line + "\n"
                map_of_func_defs[line_number+1] = func_name
                line_number+=1
                actual_line_number+=1
                continue


            file_text += line + "\n"
            file_text+= f"std::string CurrentFunctionName = \"{func_name}_FUNCNAME\";" + "\n"
            actual_line_number+=1
            for lvalue_nameitem in hashmap_of_lvalue_names.items():
                file_text+= f"std::vector<int> {lvalue_name}_arr;" + "\n"

                actual_line_number+=1

            file_text+= f"std::ifstream {removeIndex(varaiable_name)}{loopIterationToNumber(loopiter)}_dataArr;"
            #file_text+= f"std::unique_ptr<std::vector<std::string>> {removeIndex(varaiable_name)}{loopIterationToNumber(loopiter)}_dataArr =std::make_unique<std::vector<std::string>>();"
            file_text+= "std::vector<int> LOOPVARIABLE;\n"
            actual_line_number+=1


            line_number+=1
            actual_line_number+=1


    file_text = introtext+file_text
    return file_text


def test_varaible2(file_name,introtext,swap_dict):

    varlist = list(swap_dict.keys())
    loopiter=None
    lineNum=None
    dict_of_replacements={}
    for var in  varlist:
    
        #def getlineNume_and_varName():
        replacedLineNumber =var[var.find("/")+1:]
        replacedLineNumber = replacedLineNumber.split("^")[-1]
        lineNum=""
        v=0
        while(replacedLineNumber[v].isdigit()):
            lineNum+=replacedLineNumber[v]
            v+=1
        lineNum=int(lineNum)
        if(var.find("^") != -1):
            #has loops
            #loopiter = dataName.split("^")[1]
            loopiter = [x for x in var.split("^") if x.isdigit()]
            #loopiter=int(loopiter[0])
        else:
            loopiter=None
            #no loops
        var_name = var.split("FUNCNAME")[1].replace("_file","").replace(".txt","")
        if(var_name.find("#") != -1):
            indexarr = ["["+x+"]" for x in var_name.split("#") if x.isdigit()]
            var_name = var_name + "".join(indexarr)
        if( lineNum in dict_of_replacements):
            dict_of_replacements[lineNum].append((var_name,lineNum,loopiter))
        else:
            dict_of_replacements[lineNum] = [(var_name,lineNum,loopiter)]

    print(dict_of_replacements)
    


    map_of_func_defs={}
    map_of_if_defs={}
    map_of_all_if_defs={}
    map_of_for_loop_unroll = {}

    generator = c_generator.CGenerator()
    
    class RvalueVariableVisitor(c_ast.NodeVisitor):
        def visit_Return(self,node):
            pass# you need to add a token here to show that this value can not be approximated
        def visit_FuncDef(self,node):
            pass# you need to add a token here to show that this value can not be approximated
            #print(node)
            map_of_func_defs[node.coord.line] = node.decl.name
    #        arr_of_funcs.append((node.coord.line,node.decl.name))
    #        print(f"Function {node.decl.name} starts at line {node.coord.line} and ends at line {node.body.coord.line}")
            self.generic_visit(node)  # Continue to traverse the AST
        def visit_For(self,node):
            if isinstance(node.init, c_ast.DeclList):  # If the initialization is a declaration
                for decl in node.init.decls:
                    pass

                    #map_of_for_loop_unroll[node.coord.line+1] = f"std::vector<int> INDEX_LOOP;INDEX_LOOP.push_back({decl.name})"
                    loop_text = generator.visit(node)  # Convert AST node back to C code
                    number_of_lines=1
                    for line in loop_text.splitlines():
                        if(line.find("{") != -1):# the new code always has { on a new line
                            continue
                        number_of_lines+=1
                    map_of_for_loop_unroll[node.coord.line] = decl.name

            elif isinstance(node.init, c_ast.Assignment):  # If the initialization is an assignment (e.g., i = 0
                
                loop_text = generator.visit(node)  # Convert AST node back to C code
                number_of_lines=0
                for line in loop_text.splitlines():
                    if(line.find("{") != -1):# the new code always has { on a new line
                        continue
                map_of_for_loop_unroll[node.coord.line] = node.init.lvalue.name


            if isinstance(node.stmt, c_ast.Compound):
                pass
            else:
                map_of_if_defs[node.coord.line] = 1
                map_of_if_defs[node.coord.line+1] = 2
                print(f"Found for loop without braces: {(node.coord.line)}")

            self.generic_visit(node)

        def visit_If(self, node):
            # Check if the 'iftrue' (body of the 'if') is a single statement, not a Compound node
            map_of_all_if_defs[node.coord.line] = True
            if node.iftrue:
                if isinstance(node.iftrue, c_ast.Compound):
                    pass
                else:
                    try:
                        operator=node.op
                        print(node.iftrue)
                        map_of_if_defs[node.coord.line] = 1
                        map_of_if_defs[node.coord.line+1] = 2
                    except:
                        pass

            # Check the 'else' part similarly
                
            if node.iffalse:
                if isinstance(node.iffalse, c_ast.Compound):
                    pass
                else:
                    print("Else block without braces found.")
                    map_of_if_defs[node.coord.line+2] = 1
                    map_of_if_defs[node.coord.line+3] = 2
            self.generic_visit(node)  # Continue to traverse the AST

        
            


    fileConts=""
    with open(file_name,"r") as file:
        fileConts = file.read()
    prevline=""
    preText = ""

    #fileConts=file_name


    comment_code = fileConts


    """
    for line in fileConts.splitlines():
        if line.find("if") != -1 and prevline.find("if") != -1 and line.find("{") == -1 and prevline.find("{") == -1:
            line = "\n" + line
        if(len(line) > 0):
            line = line.split("//")[0];
            
        preText += line + "\n"
        prevline = line
    """
    for line in fileConts.splitlines():
        if line.find("//Ignore") != -1:
            continue
        preText+=line+"\n"


    


    code = preText
    




    c_code = code
    c_code = c_code.replace(r"\\",r"\\\\")
    result = re.sub(r'#.*?["].*?["]', '', c_code)
    result = re.sub(r'#.*?[">]', '', result)
    result = re.sub(r'//.*', '', result)
    result = re.sub(r'/\*.*', '', result)
    result = re.sub(r'\*/.*', '', result)
    result = re.sub(r'\*\*.*', '', result)

    text=""
    line_number = 0
    map_of_declaratives = {}
    for line in result.splitlines():
        if  line.find("#ifdef") == -1 and line.find("#else") == -1 and line.find("#endif") == -1 and line.find("#define") == -1 and line.find("#pragma") == -1:

            if(len(line.strip()) > 0):
                if(line.strip()[0] == "*"):
                    line = ""
                    map_of_declaratives[line_number] = line
            text+=line + "\n"
        else:
            text+= "\n"
            map_of_declaratives[line_number] = line


    parser = c_parser.CParser()
    ast = parser.parse(text)
    visitor = RvalueVariableVisitor()
    visitor.visit(ast)
    # Visit all nodes in the AST
    visitor.visit(ast)
    text = "" 

    hashmap_of_lvalue_names = {}

    line_number=0
    parseText_flag = False
    #print(comment_code)
    for line in comment_code.splitlines():
        line_number+=1


        if(line.find("//StopParse") != -1) or line.find("/*Exclude") != -1:
            parseText_flag= False
            
        if parseText_flag and line.find("//Exclude") == -1:
            #parse text with extra code
            text += line 
            if line_number > min(map_of_func_defs.keys()): #make sure your not doing global variables
                curline = line.strip()
                curline = curline.split("//")[0]
                if not curline:
                    text += "\n"
                    continue
                if ";" == curline[len(curline)-1] and line_number not in map_of_all_if_defs: #valid line
                    #now perform checks to determin type
                    #if its an array or not
            #        Tokens_in_line = line.split("")
                    Tokens_in_line = re.split("= | \|= |\+= |\-=",line)

                    def get_assignment_type(equation):
                        """
                        Finds the first compound assignment operator (+=, -=, *=, /=, etc.) in a string
                        and returns its type.

                        Args:
                            equation: The string containing the equation.

                        Returns:
                            A tuple containing the operator and its type, or None if no match is found.
                        """
                        pattern = r"([+\-*/%&|^]?=)"
                        match = re.search(pattern, equation)

                        if match:
                            operator = match.group(1)
                            if operator == '=':
                                return operator
                            elif operator == '+=':
                                return operator
                            elif operator == '-=':
                                return operator
                            elif operator == '*=':
                                return operator
                            elif operator == '/=':
                                return operator
                            elif operator == '%=':
                                return operator
                            elif operator == '&=':
                                return operator
                            elif operator == '|=':
                                return operator
                            elif operator == '^=':
                                return operator
                            else:
                                return operator
                        else:
                            return None
                    assignmentop = get_assignment_type(line.strip())
                    
                    
                    if len(Tokens_in_line) > 1:
                        lvalue = Tokens_in_line[0]
                        lvalue = lvalue.strip()
                        lvalue = lvalue.split(" ")
                        lvalue = (lvalue[len(lvalue)-1])
                        lvalue_true_name = lvalue.split("[")[0]
                        #varaiable_true_name = varaiable_name.split("[")[0]

                        
                        #if (lvalue == varaiable_name or lvalue_true_name == varaiable_true_name) and lineNum == line_number:
                        if(line_number in dict_of_replacements):
                            varsToReplace = dict_of_replacements[line_number]
                            varNames = []
                            for data in varsToReplace:
                                varNames.append(data[0])

                            for varaiable_name,line_number,loopiter in varsToReplace:
                                if loopiter == None:
                                    if varaiable_name.find("[") == -1:
                                    #text+= lvalue
                                        text+=f"{lvalue} {assignmentop} readValue(\"{line_number}\" + CurrentFunctionName,\"{lvalue}_file\",{removeIndex(varaiable_name)}{loopIterationToNumber(loopiter)}_dataArr);"
                                    #text+=f"print(LOOPVARIABLE,\"{line_number}\" + CurrentFunctionName,{lvalue},\"{lvalue}_file\");"
                                    else:
                                        lvalue_elements = lvalue.split("[")
                                        lvalue_name = lvalue_elements.pop(0)
                                        arr_of_indexes=[]

                                        varaiable_name_chars = list(varaiable_name)
                                        indexArr=[ f"{[int(i)]}" for i in varaiable_name_chars if i.isdigit()] #variable indexes
                                        index_string = ''.join(indexArr)

                                        #original indexes 
                                        conditional=[]
                                        arrayindecies = ""
                                            
                                        for element,element2 in zip(indexArr,lvalue_elements):
                                            index  = element.replace("]","").replace("[","")
                                            index2  = element2.replace("]","").replace("[","")
                                            conditional.append(f"{index} == {index2}")
                                            arrayindecies += f"{lvalue_name}_arr.push_back({index});"
                                        if_statement = " && ".join(conditional)

                                        #text+=f"{lvalue_name}{index_string} = readValue({lvalue_name}_arr,CurrentFunctionName,\"{lvalue_name}_file\");"

                                        if_statement = f"if({if_statement})" +  "{"+ f"{arrayindecies} {lvalue_name}{index_string} {assignmentop} readValue({lvalue_name}_arr,\"{line_number}\"+CurrentFunctionName,\"{lvalue_name}_file\",{removeIndex(varaiable_name)}{loopIterationToNumber(loopiter)}_dataArr);"  
                                        text+=if_statement

                                        text+=f"{lvalue_name}_arr.clear();" + "}"
                                        hashmap_of_lvalue_names[lvalue_name] = line_number
                                else:
                                    if varaiable_name.find("[") == -1:
                                        loop_conditional="if("
                                        count=0
                                        for i in loopiter:
                                            if(count > 0):
                                                loop_conditional+=" && "
                                            loop_conditional+=f"{i} == LOOPVARIABLE[{count}] "
                                            count+=1
                                        loop_conditional+=")"


                                        text+=f"{loop_conditional}" + "{" + f"{lvalue} {assignmentop} readValue( \"{line_number}\" + CurrentFunctionName,\"{lvalue}_file\",LOOPVARIABLE,{removeIndex(varaiable_name)}{loopIterationToNumber(loopiter)}_dataArr);" + "}"
                                    #text+=f"print(LOOPVARIABLE,\"{line_number}\" + CurrentFunctionName,{lvalue},\"{lvalue}_file\");"
                                    else:

                                        loop_conditional=""
                                        count=0
                                        for i in loopiter:
                                            if(count > 0):
                                                loop_conditional+=" && "
                                            loop_conditional+=f"{i} == LOOPVARIABLE[{count}] "
                                            count+=1
                                        loop_conditional+=""


                                        lvalue_elements = lvalue.split("[")
                                        lvalue_name = lvalue_elements.pop(0)
                                        arr_of_indexes=[]

                                        varaiable_name_chars = list(varaiable_name)
                                        indexArr=[ f"{[int(i)]}" for i in varaiable_name_chars if i.isdigit()] #variable indexes
                                        index_string = ''.join(indexArr)

                                        #original indexes 
                                        conditional=[]
                                        arrayindecies = ""
                                            
                                        for element,element2 in zip(indexArr,lvalue_elements):
                                            index  = element.replace("]","").replace("[","")
                                            index2  = element2.replace("]","").replace("[","")
                                            conditional.append(f"{index} == {index2}")
                                            arrayindecies += f"{lvalue_name}_arr.push_back({index});"
                                        if_statement = " && ".join(conditional)
                                        if_statement += f"&& {loop_conditional}"

                                        #text+=f"{lvalue_name}{index_string} = readValue({lvalue_name}_arr,CurrentFunctionName,\"{lvalue_name}_file\");"

                                        if_statement = f"if({if_statement})" +  "{"+ f"{arrayindecies} {lvalue_name}{index_string} {assignmentop} readValue({lvalue_name}_arr,\"{line_number}\"+CurrentFunctionName,\"{lvalue_name}_file\",LOOPVARIABLE,{removeIndex(varaiable_name)}{loopIterationToNumber(loopiter)}_dataArr);" 
                                        text+=if_statement

                                        text+=f"{lvalue_name}_arr.clear(); " + "}"
                                        hashmap_of_lvalue_names[lvalue_name] = line_number


            text+="\n"


        else:
            #add line normally
            if line.find("/*Exclude") == -1 and line.find("*/Exclude") == -1:
                text+=line + "\n"
            
        if(line.find("//Parse") != -1 or line.find("*/Exclude") != -1):
            parseText_flag= True


        

                    



    line_number = 1
    actual_line_number = 1
    map_of_lvalues={}
    file_text = ""
    for line in text.splitlines():
        




        if line_number not in map_of_func_defs:
            """
            if line_number in map_of_if_defs:
                if map_of_if_defs[line_number] == 1:
                    pattern = r"if\s*\(\s*[^()]*\s*(?:\([^)]*\))*\s*[^)]*\s*\)"
                    line = re.sub(pattern, r'\g<0> {',line)
                    pattern = r"for\s*\(\s*[^()]*\s*(?:\([^)]*\))*\s*[^)]*\s*\)"
                    line = re.sub(pattern, r'\g<0> {',line)
                    pattern = "else"
                    line = line.replace("else","else{")
                elif map_of_if_defs[line_number] == 2:
                    line += "}"
            """
            if(line.find("//UNROLL") != -1 and line.find("for ") != -1):
                forLoopVariable = map_of_for_loop_unroll[line_number] 
                line = line+"\n"+f"LOOPVARIABLE.push_back({forLoopVariable});"
            if(line.find("//STOPUNROLL") != -1):
                line = f"LOOPVARIABLE.pop_back();\n" + line 
            file_text+=line + "\n"
            line_number+=1
            actual_line_number+=1
            continue
        else:
            func_name = map_of_func_defs[line_number]
            func_name = func_name.capitalize()
            if line.find("{") == -1:
                file_text += line + "\n"
                map_of_func_defs[line_number+1] = func_name
                line_number+=1
                actual_line_number+=1
                continue


            file_text += line + "\n"
            file_text+= f"std::string CurrentFunctionName = \"{func_name}_FUNCNAME\";" + "\n"
            actual_line_number+=1
            for lvalue_nameitem in hashmap_of_lvalue_names.items():
                file_text+= f"std::vector<int> {lvalue_name}_arr;" + "\n"

                actual_line_number+=1
            
            for key,value in dict_of_replacements.items():
                for values in value:
                    file_text+= f"std::ifstream {removeIndex(values[0])}{loopIterationToNumber(values[2])}_dataArr;"
                    #file_text+= f"std::unique_ptr<std::vector<std::string>> {removeIndex(values[0])}{loopIterationToNumber(values[2])}_dataArr =std::make_unique<std::vector<std::string>>();"


            file_text+="std::vector<int> LOOPVARIABLE;\n"
            actual_line_number+=1


            line_number+=1
            actual_line_number+=1


    file_text = introtext+file_text
    return file_text


