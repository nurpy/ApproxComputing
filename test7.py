
from pycparser import c_parser, c_ast
import numpy as np
import scipy.stats
import argparse

import re
import sys
import subprocess
import os
from queue import PriorityQueue


import ProcessFile
import DataGenerator
import parseInputs
import textModification












file_name,save_file,v2c,v2v,compiler_flags = parseInputs.understand_command()




introtext = """
#include<iostream>
#include<vector>
#include<fstream>
#include <memory>
#include <string>
#include <stdexcept>
std::string DIRNAME="out/";

void deleteFirstLine(const std::string& filename) {
    std::ifstream inFile(filename);
    if (!inFile) {
        std::cerr << "Error opening file!" << std::endl;
        return;
    }

    std::ofstream tempFile("temp.txt");
    if (!tempFile) {
        std::cerr << "Error creating temp file!" << std::endl;
        return;
    }

    std::string line;
    bool firstLineSkipped = false;

    while (std::getline(inFile, line)) {
        if (!firstLineSkipped) {
            firstLineSkipped = true; // Skip the first line
            continue;
        }
        tempFile << line << '\\n'; // Write the rest to temp file
    }

    inFile.close();
    tempFile.close();

    // Replace the original file with the temp file
    std::remove(filename.c_str());
    std::rename("temp.txt", filename.c_str());
}
template<typename ... Args>
std::string string_format( const std::string& format, Args ... args )
{
    int size_s = std::snprintf( nullptr, 0, format.c_str(), args ... ) + 1; // Extra space for 
    if( size_s <= 0 ){ throw std::runtime_error( "Error during formatting." ); }
    auto size = static_cast<size_t>( size_s );
    std::unique_ptr<char[]> buf( new char[ size ] );
    std::snprintf( buf.get(), size, format.c_str(), args ... );
    return std::string( buf.get(), buf.get() + size - 1 ); // We don't want the  inside
}
template <typename T>
void print(std::vector<int> loopIndexes, std::vector<int> indexes, std::string CurrentFunctionName, const T& value,std::string FILENAME){
std::ofstream mainbuffer_file;
std::string INDEXNAME = "";
std::string LOOPINDEXNAME = "";
for(auto& loopindex: loopIndexes){
    LOOPINDEXNAME += "^" + std::to_string(loopindex) + "^";
}
for(auto& index: indexes){
    INDEXNAME += "#" + std::to_string(index) + "#";
}
mainbuffer_file.open(DIRNAME+  LOOPINDEXNAME + CurrentFunctionName + FILENAME+INDEXNAME+ ".txt",std::ios_base::app);
mainbuffer_file <<  string_format("%d",value) << '\\n';
mainbuffer_file.close();
}
template <typename T>
void print(std::vector<int> loopIndexes, std::string CurrentFunctionName, const T& value,std::string FILENAME){
std::ofstream mainbuffer_file;
std::string INDEXNAME = "";
std::string LOOPINDEXNAME = "";
for(auto& loopindex: loopIndexes){
    LOOPINDEXNAME += "^" + std::to_string(loopindex) + "^";
}
mainbuffer_file.open( DIRNAME+ LOOPINDEXNAME + CurrentFunctionName + FILENAME+INDEXNAME+ ".txt",std::ios_base::app);
mainbuffer_file <<  string_format("%d",value) << '\\n';
mainbuffer_file.close();
}


int readValue(std::string CurrentFunctionName,std::string FILENAME, std::unique_ptr<std::vector<std::string>>& buffer){

if(buffer->empty()){


}
if(!buffer->empty()){
    //std::string str = 

    int num =  std::stoi(buffer->back());
    buffer->pop_back();
    return num;

}


std::string INDEXNAME = "";
std::ifstream mainbuffer_file(DIRNAME+CurrentFunctionName + FILENAME+INDEXNAME+ ".itxt");
//mainbuffer_file.open(  CurrentFunctionName + FILENAME+INDEXNAME+ ".itxt",std::ios_base::app);
std::string first_value_in_file;
//std::getline(mainbuffer_file, first_value_in_file);

while(std::getline(mainbuffer_file, first_value_in_file)){

    //buffer->push_back(first_value_in_file);
    buffer->insert(buffer->begin(),first_value_in_file);

}

mainbuffer_file.close();
//deleteFirstLine(DIRNAME+CurrentFunctionName + FILENAME+INDEXNAME+ ".itxt");
/*
if (first_value_in_file == ""){
	  throw std::invalid_argument( "file: " + DIRNAME +CurrentFunctionName + FILENAME+INDEXNAME+ ".itxt" +  " ran out of values" );
}
*/

int num =  std::stoi(buffer->back());
buffer->pop_back();
return num;

}

int readValue(std::string CurrentFunctionName,std::string FILENAME,std::vector<int> loopindex, std::unique_ptr<std::vector<std::string>>& buffer){

if(buffer->empty()){


}
if(!buffer->empty()){
    //std::string str = 

    int num =  std::stoi(buffer->back());
    buffer->pop_back();
    return num;

}

std::string INDEXNAME = "";
std::string LOOPNAME = "";
for(auto& index: loopindex){
    LOOPNAME += "^" + std::to_string(index) + "^";
}
std::ifstream mainbuffer_file(DIRNAME+LOOPNAME+CurrentFunctionName + FILENAME+INDEXNAME+ ".itxt");
//mainbuffer_file.open(  CurrentFunctionName + FILENAME+INDEXNAME+ ".itxt",std::ios_base::app);
std::string first_value_in_file;
//std::getline(mainbuffer_file, first_value_in_file);
while(std::getline(mainbuffer_file, first_value_in_file)){

    //buffer->push_back(first_value_in_file);
    buffer->insert(buffer->begin(),first_value_in_file);

}
mainbuffer_file.close();
/*
//deleteFirstLine(DIRNAME+LOOPNAME+CurrentFunctionName + FILENAME+INDEXNAME+ ".itxt");
if (first_value_in_file == ""){
	  throw std::invalid_argument( "file: " + DIRNAME +LOOPNAME+CurrentFunctionName + FILENAME+INDEXNAME+ ".itxt" +  " ran out of values" );
}
*/
int num =  std::stoi(buffer->back());
buffer->pop_back();
return num;


}

int readValue(std::vector<int> indexes, std::string CurrentFunctionName, std::string FILENAME, std::unique_ptr<std::vector<std::string>>& buffer){

if(buffer->empty()){


}
if(!buffer->empty()){
    //std::string str = 

    int num =  std::stoi(buffer->back());
    buffer->pop_back();
    return num;

}

std::string INDEXNAME = "";
for(auto& index: indexes){
    INDEXNAME += "#" + std::to_string(index) + "#";
}
std::ifstream mainbuffer_file(DIRNAME+CurrentFunctionName + FILENAME+INDEXNAME+ ".itxt");
//mainbuffer_file.open(  CurrentFunctionName + FILENAME+INDEXNAME+ ".itxt",std::ios_base::app);
std::string first_value_in_file;
//std::getline(mainbuffer_file, first_value_in_file);

while(std::getline(mainbuffer_file, first_value_in_file)){

    //buffer->push_back(first_value_in_file);
    buffer->insert(buffer->begin(),first_value_in_file);

}

mainbuffer_file.close();

/*
deleteFirstLine(DIRNAME+CurrentFunctionName + FILENAME+INDEXNAME+ ".itxt");
if (first_value_in_file == ""){
	  throw std::invalid_argument( "file: " + DIRNAME+CurrentFunctionName + FILENAME+INDEXNAME+ ".itxt" +  " ran out of values" );
}
*/

int num =  std::stoi(buffer->back());
buffer->pop_back();
return num;


}

int readValue(std::vector<int> indexes, std::string CurrentFunctionName, std::string FILENAME,std::vector<int> loopindex, std::unique_ptr<std::vector<std::string>>& buffer){

if(buffer->empty()){


}
if(!buffer->empty()){
    //std::string str = 

    int num =  std::stoi(buffer->back());
    buffer->pop_back();
    return num;

}

std::string INDEXNAME = "";
for(auto& index: indexes){
    INDEXNAME += "#" + std::to_string(index) + "#";
}
std::string LOOPNAME = "";
for(auto& index: loopindex){
    LOOPNAME += "^" + std::to_string(index) + "^";
}
std::ifstream mainbuffer_file(DIRNAME+LOOPNAME+CurrentFunctionName + FILENAME+INDEXNAME+ ".itxt");
//mainbuffer_file.open(  CurrentFunctionName + FILENAME+INDEXNAME+ ".itxt",std::ios_base::app);
std::string first_value_in_file;
//std::getline(mainbuffer_file, first_value_in_file);

while(std::getline(mainbuffer_file, first_value_in_file)){

    //buffer->push_back(first_value_in_file);
    buffer->insert(buffer->begin(),first_value_in_file);

}

mainbuffer_file.close();

/*
deleteFirstLine(DIRNAME+LOOPNAME+CurrentFunctionName + FILENAME+INDEXNAME+ ".itxt");
if (first_value_in_file == ""){
	  throw std::invalid_argument( "file: " + DIRNAME+LOOPNAME+CurrentFunctionName + FILENAME+INDEXNAME+ ".itxt" +  " ran out of values" );
}
*/

int num =  std::stoi(buffer->back());
buffer->pop_back();
return num;


}
    """
introtext=""
with open("introtext.cpp",'r') as file:
    introtext=file.read()




def parseText():

    map_of_func_defs={}
    map_of_if_defs={}
    map_of_all_if_defs={}

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
    for line in fileConts.splitlines():
        if line.find("if") != -1 and prevline.find("if") != -1 and line.find("{") == -1 and prevline.find("{") == -1:
            line = "\n" + line
        if(len(line) > 0):
            line = line.split("//")[0];
            
        preText += line + "\n"
        prevline = line

    code = preText
    print(code)





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
        if line.find("#ifdef") == -1 and line.find("#else") == -1 and line.find("#endif") == -1 and line.find("#define") == -1 and line.find("#pragma") == -1:

            if(len(line.strip()) > 0):
                if(line.strip()[0] == "*"):
                    line = ""
                    map_of_declaratives[line_number] = line
            text+=line + "\n"
        else:
            print(line)
            text+= "\n"
            map_of_declaratives[line_number] = line


    parser = c_parser.CParser()
    print(text)
    ast = parser.parse(text)
    visitor = RvalueVariableVisitor()
    visitor.visit(ast)

    # Visit all nodes in the AST
    visitor.visit(ast)
    text = "" 

    hashmap_of_lvalue_names = {}

    line_number=0
    for line in code.splitlines():
        line_number+=1
        text+=line 
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
                        text+=f"print(CurrentFunctionName,{lvalue},\"{lvalue}_file\");"
                    else:
                        lvalue_elements = lvalue.split("[")
                        lvalue_name = lvalue_elements.pop(0)
                        arr_of_indexes=[]
                        for element in lvalue_elements:
                            index  = element.replace("]","").replace("[","")
                            text += f"{lvalue_name}_arr.push_back({index});"

                        text+=f"print({lvalue_name}_arr,CurrentFunctionName,{lvalue},\"{lvalue_name}_file\");"
                        text+=f"{lvalue_name}_arr.clear();"

                        hashmap_of_lvalue_names[lvalue_name] = line_number



                    
        text+="\n"



    line_number = 1
    actual_line_number = 1
    map_of_lvalues={}
    file_text = ""
    for line in text.splitlines():
        




        if line_number not in map_of_func_defs:
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


            line_number+=1
            actual_line_number+=1


    file_text = introtext+file_text
    return file_text
def test_varaible(varaiable_name):
    map_of_func_defs={}
    map_of_if_defs={}
    map_of_all_if_defs={}

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
    for line in fileConts.splitlines():
        if line.find("if") != -1 and prevline.find("if") != -1 and line.find("{") == -1 and prevline.find("{") == -1:
            line = "\n" + line
        if(len(line) > 0):
            line = line.split("//")[0];
            
        preText += line + "\n"
        prevline = line

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
        if line.find("#ifdef") == -1 and line.find("#else") == -1 and line.find("#endif") == -1 and line.find("#define") == -1 and line.find("#pragma") == -1:

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
    for line in code.splitlines():
        line_number+=1
        text+=line 
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
                    lvalue_true_name = lvalue.split("[")[0]
                    varaiable_true_name = varaiable_name.split("[")[0]

                    if lvalue == varaiable_name or lvalue_true_name == varaiable_true_name:
                        if lvalue.find("[") == -1:
                            #text+= lvalue
                            #change the variable
                            #text+=f"print(CurrentFunctionName,{lvalue},\"{lvalue}_file\");"
                            text+=f"{lvalue} = readValue(CurrentFunctionName,\"{lvalue}_file\");"
                            

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

                            if_statement = f"if({if_statement})" +  "{"+ f"{arrayindecies} {lvalue_name}{index_string} = readValue({lvalue_name}_arr,CurrentFunctionName,\"{lvalue_name}_file\");"  + "}" 
                            text+=if_statement

                            text+=f"{lvalue_name}_arr.clear();"

                            hashmap_of_lvalue_names[lvalue_name] = line_number



                    
        text+="\n"

    line_number = 1
    actual_line_number = 1
    map_of_lvalues={}
    file_text = ""
    for line in text.splitlines():
        




        if line_number not in map_of_func_defs:
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


            line_number+=1
            actual_line_number+=1


    file_text = introtext+file_text

    return file_text

def compile_and_run_file(out_file_name,compiler_flags):
    #compile and run file generated file
    bin_file_name = out_file_name.strip().split(".")[0]
    bin_file_name = f"{bin_file_name}"

    path = './out/'
    currentfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    compile_args = f"{out_file_name} -std=c++20 -o{bin_file_name}.o {compiler_flags}"
    os.system(f"./compile.sh {compile_args}")
    os.system(f"./{bin_file_name}.o")


    #new files indicate the variable files were made for
    path = '.'
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))] #finding all generated file
    new_files = [x for x in files if x not in currentfiles and x.find(".txt") != -1]
    return new_files





#find where you print variables

#file_text =  textModification.parseText(file_name,introtext)
#text_to_parse =  textModification.getParseSections(file_name)
textModification.preProcessText(file_name)
file_text = textModification.parseText(file_name,introtext)



#write to output file
dir="out/"
out_file_name = f"{dir}OUT_" + file_name
sourceFile = open(out_file_name, 'w')
print(file_text, file =sourceFile)
sourceFile.close()









#Generate the input data for the program
DataGenerator.ave8File()

#compile and run file
new_files = compile_and_run_file(out_file_name,compiler_flags)

#outputFile = "outdata.txt"
outputFile = "lenaout.bmp"
def saveOutputFile(outputFile):
    data = ""
    with open(outputFile,'rb') as file:
        data=file.read()
    with open("TemporaryOutput.bmp",'wb') as file:
        file.write(data)
saveOutputFile(outputFile) # save the original output




path = './out/'
new_files = [f"out/{f}" for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and (f.find(".txt") != -1)]

#perform some type of data processing on the data
#go through all the files if its a text file find average and standard deviation
#make sure to match the variable with being and array and a normal variable
file_data = []
for i in new_files:
    if i.find(".txt") != -1 and i.find("FUNCNAME") != -1:
        
        file_data.append(ProcessFile.avg_and_std_deviation_of_file(i))
        pass





#match the means and standard deviation with certain variable names


possible_V2C = []
for var_name,avg,std_dev,numbers in file_data:
    if std_dev < 5:
        possible_V2C.append((var_name,avg,numbers))
        print(f"made constant for {var_name}")



correlated_variables={}
correlated_variables_mean={}
for var_name,avg,std_dev,numbers in file_data:
    for var_name2,avg2,std_dev2,numbers2 in file_data:
        if var_name2 != var_name and len(numbers) == len(numbers2):
            try:
                correlation,p_value = scipy.stats.pearsonr(numbers, numbers2)
                #correlation, p_value = scipy.stats.spearmanr(numbers, numbers2)
                var1=var_name.split("FUNCNAME")[1]
                var2=var_name2.split("FUNCNAME")[1]
                print(f"correlation:{correlation} and pvalue:{p_value} | {var1} and {var2} ")

                if(abs(correlation) > 0.8 and abs(p_value) < 0.2):
                    #print(f"correlation:{correlation} and pvalue:{p_value}")

                    if var_name in correlated_variables:
                        correlated_variables[var_name].append(var_name2)
                        correlated_variables_mean[var_name].append((var_name2,avg,avg2))
                    else:
                        correlated_variables[var_name] = [var_name2]
                        correlated_variables_mean[var_name] = [(var_name2,avg,avg2)]

            except:
                pass

print(correlated_variables)
for key,data in correlated_variables.items():
    pass
    #print(f"variable {key} \correlated with: {data}")

for key,data in correlated_variables_mean.items():
    print(f"variable {key} \correlated with: {data} ") 
    #

    #


#remove all textfiles
#also remove a.out



##Dones?

##perform  the V2V or V2C substitutions or approximations
#V2V
files_to_simulate = []
file_text = ""
if v2v:
    for key,value in correlated_variables.items():
        print(f"key : {key}")
        if key.find(".txt") == -1:

            var_name = key.split("FUNCNAME")[1]
            file_text = textModification.test_varaible(file_name,introtext,var_name,key)
            print(f"************888{key}")
            files_to_simulate.append(("V2V",f"{key}_testFile.cpp"))

            sourceFile = open(f"{key}_testFile.cpp", 'w')
            print(file_text, file =sourceFile)
            sourceFile.close()


#V2C
if v2c:
    for var_name,avg,std_dev in possible_V2C:
        if var_name.find(".txt") == -1:
            var_name_with_method_signature = var_name
            print(var_name_with_method_signature)
            var_name = var_name.split("FUNCNAME")[1]
            print(f"variable name \n\n{var_name}\n\n")
            file_text = textModification.test_varaible(file_name,introtext,var_name,var_name_with_method_signature)
            print(var_name)
            print(f"file name: {var_name_with_method_signature}_testFile.cpp")

            files_to_simulate.append((avg,f"{var_name_with_method_signature}_testFile.cpp"))
            sourceFile = open(f"{var_name_with_method_signature}_testFile.cpp", 'w')
            print(file_text, file =sourceFile)
            sourceFile.close()






 
print(f"-------------------{files_to_simulate}")
print(new_files)
queue={}
for replacement_type,file in files_to_simulate:
    print(f"-------------{file}")

    
    #queue.update(DataGenerator.ave8FileOUT(file,new_files,compiler_flags,replacement_type))
    queue.update(DataGenerator.sobelFileOUT(file,new_files,compiler_flags,replacement_type))



substrings = set()  # To store unique substrings
listofkeys= list(queue.keys())
for i in range(len(listofkeys)):  # Starting index of substring
    for j in range(i + 1, len(listofkeys) + 1):  # Ending index (exclusive)
        substrings.add(frozenset(listofkeys[i:j]))  # Add substring to set
    
print(substrings)

print(queue)
highest_error=0.0
highest_error_text=""
largest_current_error=0.0
for i in substrings:
    i=list(i)
    var_map={}
    list_of_vars=[]
    list_of_error=[]
    for element in i:
        var_map[element.replace("_testFile.cpp","")]=queue[element][0][1]
        secondFileName = queue[element][0][1].replace(".txt",".txt")
        element = element.replace("_testFile.cpp","").replace("[","#").replace("]","#")
        element = element.split("#",1)
        var_file_name=""
        if(len(element) > 1):
            var_file_name = "_file#".join(element) + ".txt"
        else:
            var_file_name = element[0]+"_file.txt"

        #print(var_file_name)
        #print(secondFileName)
        compared_nums_avg = ProcessFile.avg_and_std_deviation_of_file(var_file_name)[1]
        compared_nums_avg2 = ProcessFile.avg_and_std_deviation_of_file(secondFileName)[1]

        DataGenerator.add_avg_toFile(compared_nums_avg-compared_nums_avg2,secondFileName.replace(".itxt",".txt"),var_file_name.replace(".txt",".itxt"))
        #print(secondFileName.replace(".txt",".itxt"))
        #print(var_file_name)
        #print(compared_nums_avg-compared_nums_avg2)
        list_of_vars.append(var_file_name)
        list_of_vars.append(secondFileName)
        list_of_error.append(compared_nums_avg-compared_nums_avg2)

        
    text_file=textModification.test_varaible2(file_name,introtext,var_map)
    with open("out/tempRUNFILE.cpp","w") as file:
        file.write(text_file)
    
    compile_and_run_file("out/tempRUNFILE.cpp","-DC -w")
    #new_numbers = ProcessFile.avg_and_std_deviation_of_file(outputFile)
    #normal_numbers = ProcessFile.avg_and_std_deviation_of_file("TemporaryOutput")

    psnr = DataGenerator.sobel_snr("TemporaryOutput.bmp",outputFile)

    #numbers_precentage_change = ProcessFile.mean_percentage_error(normal_numbers[-1],new_numbers[-1])
    numbers_precentage_change = abs(psnr)
    if(numbers_precentage_change > 20.0):
        print(numbers_precentage_change)
        print(list_of_vars)
        print(f"error gradient | {list_of_error}")
    #if highest_error < numbers_precentage_change:
    #    highest_error = numbers_precentage_change
    #    highest_error_text = text_file
    
    #    print(highest_error)
#print(highest_error_text)


#    print(file_name)
#    print(var_map)
    
    #print(text_file)
    #print(var_map)





"""
for i in substrings:
    if(len(i) ==2):
        for file in i:

            i=list(i)
            print(i)
            key = file[1][0]
            key=key.replace("_testFile.cpp","")
            var_name = key.split("FUNCNAME")[1]
            print(key)
            print(var_name)
            #file_text = textModification.test_varaible(file_name,"",var_name,key)   

            key = file[1][0]
            key=key.replace("_testFile.cpp","")
            var_name = key.split("FUNCNAME")[1]
            print(key)
            print(var_name)

            #print(file_text)
            break
        break
    
"""

#remove all the generated variable files
#print(new_files)
if(not save_file):
    os.system(f"rm out/*")

"""
if(not save_file):
    for i in new_files:
        print(f"Removed file {i}")
        os.system(f"rm {i}")
"""
