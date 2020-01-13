import ply.lex as lex

'''
Ce fichier sert à faire l'analyse lexicale de notre programme.
Une partie a été reprise du travail fait pendant les TPS et adapté
selon nos besoin. Tous les tokens qui doivent être analysés sont ici décrits.

David da Silva
Robin Alfred

'''



'''
Liste des mots reservés, concerne les structures dans le programme
que ce soit bloc ou boucle
'''
reserved_words = (
	'if',
	'print',
	'while',
	'def'
)

'''
Liste des tokens présents dans notre programme, qui seront analysés par la suite
dans l'analyse syntaxique
'''
tokens = (
	'COMPARATOR',
	'IDENTIFIER',
	'FLOAT',
	'INT',
	'EQU',
	'ENTER',
	'POINTS',
	'TAB',
	'ADD_OP',
	'MUL_OP'
) + tuple(map(lambda s:s.upper(),reserved_words))



literals = '.#():\s"'

def t_ENTER(t):
	r'\n'
	t.lexer.lineno += len(t.value)
	return t

def t_ADD_OP(t):
	r'[+-]'
	return t

def t_POINTS(t):
	r':'
	return t

def t_EQU(t):
	r'\='
	return t	
	
def t_MUL_OP(t):
	r'[*/]'
	return t

def t_COMPARATOR(t):
	r'[<>]'
	return t


def t_INT(t):
	r'\b(?<!\.)\d+(?!\.)\b'
	try:
		t.value = t.value   
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (t.lineno,t.value))
		t.value = 0
	return t

def t_ILLEGAL(t):
	r'\d+[a-zA-z]+'
	try:
		t.value = t.value   
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (t.lineno,t.value))
		t.value = 0
	return t

def t_FLOAT(t):
	r'\d+\.{1}\d+'
	try:
		t.value = float(t.value)   
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (t.lineno,t.value))
		t.value = 0.0
	return t

def t_IDENTIFIER(t):
	r'[A-Za-z_]\w*'
	if t.value in reserved_words:
		t.type = t.value.upper()
	return t

def t_TAB(t):
	r'[ \t]{4}'
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)


def t_IGNORE(t):
	r'[ /s]{1}'

def t_error(t):
	print ("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)


lex.lex()

if __name__ == "__main__":
	import sys
	prog = open(sys.argv[1]).read()

	lex.input(prog)

	while 1:
		tok = lex.token()
		if not tok: break
		print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))