# coding=utf-8
import AST
from AST import addToClass
from threader import thread


# chaque opération correspond à son instruction d'exécution de la machine SVM
operations = {
	'+' : 'ADD',
	'-' : 'SUB',
	'*' : 'MUL',
	'/' : 'DIV',
	'<' : 'NEGCOMP',
	'>' : 'POSCOMP'
}

inLoop = None
counter =0
cpt = 0

from threader import dict_variables
used_variables = []


@addToClass(AST.ProgramNode)
def compile(self):
	bytecode = ""
	for c in self.children:
		bytecode += c.compile()
	return bytecode


@addToClass(AST.TokenNode)
def compile(self):
	bytecode = ""
	bytecode += "%s" % self.tok
	return bytecode

@addToClass(AST.AssignNode)
def compile(self):
	bytecode = ""
	global cpt
	if counter==1:
		bytecode +="\t"
	elif counter==2:
		bytecode +="\t\t"
	elif counter==3:
		bytecode +="\t\t\t"
	else:
		pass

	
	if self.children[0].tok not in bytecode and self.children[0].tok not in used_variables:
		bytecode += str(dict_variables.get(self.children[0].tok))+" "
		bytecode += self.children[0].tok + " = "
		used_variables.append(self.children[0].tok)
	else:
		bytecode += self.children[0].tok + " = "

	bytecode += self.children[1].compile()
	bytecode +=";\n"
	return bytecode
	

@addToClass(AST.PrintNode)
def compile(self):
	bytecode = ""
	if counter==1:
		bytecode +="\t"
	elif counter==2:
		bytecode +="\t\t"
	elif counter==3:
		bytecode +="\t\t\t"
	else:
		pass
	bytecode += "cout << "
	bytecode += self.children[0].compile()+";\n"

	return bytecode


@addToClass(AST.OpNode)
def compile(self):
	bytecode = ""	
	bytecode += str(self.children[0].tok)
	for key,value in operations.items():
		if value == operations[self.op]:
			bytecode += key
	bytecode += str(self.children[1].tok)


	return bytecode

	
@addToClass(AST.WhileNode)
def compile(self):
	global inLoop
	global counter
	bytecode = ""

	if counter==1 and inLoop:
		bytecode +="\t"
	elif counter==2 and inLoop:
		bytecode +="\t\t"
	elif counter==3 and inLoop:
		bytecode +="\t\t\t"
	else:
		pass
	bytecode += "while(%s) {" % self.children[0].compile()
	counter +=1
	bytecode +="\n"
	inLoop=True
	bytecode += self.children[1].compile()
	if counter==3:
		bytecode +="\t\t}\n"
	elif counter==2:
		bytecode +="\t}\n"
	else:
		bytecode +="}\n"
	counter -=1
	inLoop = False

	return bytecode

@addToClass(AST.IfNode)
def compile(self):
	global inLoop
	global counter
	bytecode = ""


	if counter==1:
		bytecode +="\t"
	elif counter==2:
		bytecode +="\t\t"
	elif counter==3:
		bytecode="\t\t\t"
	else:
		pass
	bytecode += "if(%s) {" % self.children[0].compile()
	counter +=1
	bytecode +="\n"
	inLoop=True
	bytecode += self.children[1].compile()
	if counter==3:
		bytecode +="\t\t}\n"
	elif counter==2:
		bytecode +="\t}\n"
	else:
		bytecode +="}\n"

	counter -=1
	inLoop = False

	return bytecode

@addToClass(AST.FunctionNode)
def compile(self):
	global counter
	bytecode=""
	bytecode += "public void "
	bytecode +=  " %s" % self.children[0].tok
	bytecode +="()\n{"
	counter +=1
	bytecode +="\n"+self.children[1].compile()
	if counter==3:
		bytecode +="\t\t}\n"		
	elif counter==2:
		bytecode +="\t}\n"
	else:
		bytecode +="}\n"
	return bytecode

if __name__ == "__main__":
    from parser4 import parse
    import sys, os.path
    from os import path
    prog = open(sys.argv[1]).read()


    if path.exists(os.path.splitext(sys.argv[1])[0]+'.vm'):
        open(os.path.splitext(sys.argv[1])[0]+'.vm', 'w').close()
    ast = parse(prog)
    entry = thread(ast)
    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0]+'.vm'    
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()
    print ("Wrote output to", name)