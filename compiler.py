# coding=utf-8
import AST
from AST import addToClass
from threader import thread
from pythonParser import parse

'''
Ce fichier sert à faire la partie arrière de ce projet. C'est ici que le code sera compilé vers notre langage target, qui est le c++.
Si le code choisi dans un fichier arrive à ce stade, cela veut dire qu'il a passé l'analyse lexicale,syntaxique et sémantique avec succès.
Si une erreur est détectée avant, aucune compilation sera effectuée.
Partie reprise des TPs réalisés en cours, adaptée à nos besoin et améliorée.

David da Silva
Robin Alfred
'''

# chaque opération correspond à son instruction d'exécution de la machine SVM
operations = {
	'+' : 'ADD',
	'-' : 'SUB',
	'*' : 'MUL',
	'/' : 'DIV',
	'<' : 'NEGCOMP',
	'>' : 'POSCOMP'
}

inLoop = None #pour savoir si on est dans une boucle
counter =0 #compteur pour savoir si on est dans une boucle

from threader import dict_variables
used_variables = [] # sera utilisé pour savoir si on a déjà utilisé la variable dans notre code

'''
Compile les ProgramNode.
Retourne la suite des enfants et les compile.
'''
@addToClass(AST.ProgramNode)
def compile(self):
	bytecode = ""
	for c in self.children:
		bytecode += c.compile()
	return bytecode

'''
Compile les TokenNode
'''
@addToClass(AST.TokenNode)
def compile(self):
	bytecode = ""
	bytecode += "%s" % self.tok
	return bytecode


'''
Compile les AssignNode.
Vérification de l'indentation actuelle
Vérifie si une variable a déjà été utilisée dans le code, pour n'afficher son type
que la première fois qu'elle est appelée.
'''
@addToClass(AST.AssignNode)
def compile(self):
	bytecode = ""
	#test pour vérifier le niveau d'indentaion
	if counter==1:
		bytecode +="\t"
	elif counter==2:
		bytecode +="\t\t"
	elif counter==3:
		bytecode +="\t\t\t"
	else:
		pass

	if self.children[0].tok not in bytecode and self.children[0].tok not in used_variables: #si la variable n'est pas encore utilisé
		bytecode += str(dict_variables.get(self.children[0].tok))+" " #on affiche son type
		bytecode += self.children[0].tok + " = " # et son nom
		used_variables.append(self.children[0].tok) # on ajoute la variable au tableau
	else:
		bytecode += self.children[0].tok + " = " #on ajoute seulement son nom

	bytecode += self.children[1].compile() #on compile le deuxieme enfant
	bytecode +=";\n"
	return bytecode
	
'''
Compile les PrintNode.
Vérification de l'indentation actuelle
'''
@addToClass(AST.PrintNode)
def compile(self):
	bytecode = ""
	#test pour vérifier le niveau d'indentation
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

'''
Compile les OpNode.
Vérifie l'opérateur choisi.
'''
@addToClass(AST.OpNode)
def compile(self):
	bytecode = ""	
	bytecode += str(self.children[0].tok)
	for key,value in operations.items():
		if value == operations[self.op]:
			bytecode += key
	bytecode += str(self.children[1].tok)
	return bytecode

	
'''
Compile les WhileNode.
Vérifie l'indentation.
Incrémentation/Décrementation quand on rentre/sort dans une boucle
'''
@addToClass(AST.WhileNode)
def compile(self):
	global counter
	bytecode = ""
	#vérification de l'indentation
	if counter==1:
		bytecode +="\t"
	elif counter==2:
		bytecode +="\t\t"
	elif counter==3:
		bytecode +="\t\t\t"
	else:
		pass
	bytecode += "while(%s) {" % self.children[0].compile()
	counter +=1 #on rentre dans un bloc
	bytecode +="\n"
	bytecode += self.children[1].compile()
	#vérification du niveau d'indentation nécessaire
	if counter==3:
		bytecode +="\t\t}\n"
	elif counter==2:
		bytecode +="\t}\n"
	else:
		bytecode +="}\n"
	counter -=1 #on sort du bloc

	return bytecode

'''
Compile les IfNode.
Vérifie l'indentation.
Incrémentation/Décrementation quand on rentre/sort dans une boucle
'''
@addToClass(AST.IfNode)
def compile(self):
	global counter
	bytecode = ""

	#vérification de l'indentation
	if counter==1:
		bytecode +="\t"
	elif counter==2:
		bytecode +="\t\t"
	elif counter==3:
		bytecode="\t\t\t"
	else:
		pass
	bytecode += "if(%s) {" % self.children[0].compile()
	counter +=1 #on rentre dans un bloc
	bytecode +="\n"
	bytecode += self.children[1].compile()
	if counter==3:
		bytecode +="\t\t}\n"
	elif counter==2:
		bytecode +="\t}\n"
	else:
		bytecode +="}\n"

	counter -=1 #on sort du bloc

	return bytecode

'''
Compile les FunctionNode
'''
@addToClass(AST.FunctionNode)
def compile(self):
	global counter
	bytecode=""
	bytecode += "public void "
	bytecode +=  "%s" % self.children[0].tok
	bytecode +="()\n{"
	counter +=1
	bytecode +="\n"+self.children[1].compile()
	#vérification de l'indentation
	if counter==3:
		bytecode +="\t\t}\n"		
	elif counter==2:
		bytecode +="\t}\n"
	else:
		bytecode +="}\n"
	return bytecode

if __name__ == "__main__":
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