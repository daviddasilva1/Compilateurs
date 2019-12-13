import ply.yacc as yacc

from lex4 import tokens

import AST


vars = {}

def p_programme_statement(p):
	''' programme : statement  '''
	p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
	''' programme : statement ENTER programme '''
	p[0] = AST.ProgramNode([p[1]]+p[3].children)

def p_statement(p):
	''' statement : assignation
						| expression '''
	p[0] = p[1]
	
def p_expression_num_or_var(p):
	'''expression : INT
		| FLOAT 
		| IDENTIFIER'''
	p[0] = AST.TokenNode(p[1])

def p_statement_print(p):
    ''' statement : PRINT expression '''
    p[0] = AST.PrintNode(p[2])
	
def p_expression_paren(p):
	'''expression : '(' expression ')' '''
	p[0] = p[2]
	
def p_assign(p):
	''' assignation : IDENTIFIER EQU expression '''
	p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_error(p):
    print ("Syntax error in line %d" % p.lineno)
    yacc.errok()


yacc.yacc(outputdir='generated')

if __name__ == "__main__":
	import sys 
	
	prog = open(sys.argv[1]).read()
	ast = yacc.parse(prog)
	print (ast)
	
	import os
	os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
	graph = ast.makegraphicaltree()
	name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
	graph.write_pdf(name) 
	print ("wrote ast to", name)
	