# coding: latin-1
'''

Petit module utilitaire pour la construction, la manipulation et la 
représentation d'arbres syntaxiques abstraits.

Utilisation en parallèle de graphviz pour créer les arbres syntaxiques.
Contenu repris des TPs réalisés en cours. Les nouveautés faites par nous même.

David da Silva
Robin Alfred
'''

import pydot

class Node:
    count = 0
    type = 'Node (unspecified)'
    shape = 'ellipse'
    def __init__(self,children=None):
        self.ID = str(Node.count)
        Node.count+=1
        if not children: self.children = []
        elif hasattr(children,'__len__'):
            self.children = children
        else:
            self.children = [children]
        self.next= []

    def addNext(self,next):
        self.next.append(next)

    def asciitree(self, prefix=''):
        result = "%s%s\n" % (prefix, repr(self))
        prefix += '|  '
        for c in self.children:
            if not isinstance(c,Node):
                result += "%s*** Error: Child of type %r: %r\n" % (prefix,type(c),c)
                continue
            result += c.asciitree(prefix)
        return result
    
    def __str__(self):
        return self.asciitree()
    
    def __repr__(self):
        return self.type
    
    def makegraphicaltree(self, dot=None, edgeLabels=True):
            if not dot: dot = pydot.Dot()
            dot.add_node(pydot.Node(self.ID,label=repr(self), shape=self.shape))
            label = edgeLabels and len(self.children)-1
            for i, c in enumerate(self.children):
                c.makegraphicaltree(dot, edgeLabels)
                edge = pydot.Edge(self.ID,c.ID)
                if label:
                    edge.set_label(str(i))
                dot.add_edge(edge)
            return dot

    def threadTree(self, graph, seen = None, col=0):
            colors = ('red', 'green', 'blue', 'yellow', 'magenta', 'cyan')
            if not seen: seen = []
            if self in seen: return
            seen.append(self)
            new = not graph.get_node(self.ID)
            if new:
                graphnode = pydot.Node(self.ID,label=repr(self), shape=self.shape)
                graphnode.set_style('dotted')
                graph.add_node(graphnode)
            label = len(self.next)-1
            for i,c in enumerate(self.next):
                if not c: return
                col = (col + 1) % len(colors)
                color = colors[col]                
                c.threadTree(graph, seen, col)
                edge = pydot.Edge(self.ID,c.ID)
                edge.set_color(color)
                edge.set_arrowsize('.5')
                edge.set_constraint('false') 
                if label:
                    edge.set_taillabel(str(i))
                    edge.set_labelfontcolor(color)
                graph.add_edge(edge)
            return graph
        
class ProgramNode(Node):
    type = 'Program'

class EntryNode(Node):
    type = 'Entry'
    def __init__(self):
        Node.__init__(self,None)
        
class TokenNode(Node):
    type = 'token'
    def __init__(self, tok):
        Node.__init__(self)
        self.tok = tok
        
    def __repr__(self):
        return repr(self.tok)
    
class OpNode(Node):
    def __init__(self, op, children):
        Node.__init__(self,children)
        self.op = op #pour avoir l'operateur utilisé (+,-,/,*,<,>)
        try:
            self.nbargs = len(children)
        except AttributeError:
            self.nbargs = 1
        
        
    def __repr__(self):
        return "%s (%s)" % (self.op, self.nbargs)
    

'''
si la règle concerne les assignations, un '=' sera utilisé dans l'arbre syntaxique
'''
class AssignNode(Node):
    type = '='

'''
si la règle concerne les print, un 'print' sera utilisé dans l'arbre syntaxique
'''
class PrintNode(Node):
    type = 'print'

'''
si la règle concerne les bloc if, un 'if' sera utilisé dans l'arbre syntaxique
'''
class IfNode(Node):
    type= 'if'

'''
si la règle concerne les boucle while, un 'while' sera utilisé dans l'arbre syntaxique
'''
class WhileNode(Node):
    type= 'while'

'''
si la règle concerne les fonctions, un 'def' sera utilisé dans l'arbre syntaxique
'''
class FunctionNode(Node):
    type= 'def'



def addToClass(cls):
    ''' Décorateur permettant d'ajouter la fonction décorée en tant que méthode
    à une classe.
    
    Permet d'implémenter une forme élémentaire de programmation orientée
    aspects en regroupant les méthodes de différentes classes implémentant
    une même fonctionnalité en un seul endroit.

    Code repris des TPs réalisés en cours.
    '''
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator