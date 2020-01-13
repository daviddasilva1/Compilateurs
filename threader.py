import AST
from AST import addToClass
import sys


'''
Ce fichier sert à faire l'analyse sémantique, qui donnera une coutûre comme résultat.
Le but est de savoir si le code est analysé dans le bon ordre, et aussi de faire
une gestion des erreurs si ce n'est pas le cas. Utilisation d'un décorateur dans AST.py.

David da Silva
Robin Alfred
'''
dict_variables = {} #contiendra toutes les variables et leur types

@addToClass(AST.Node)
def thread(self, lastNode):
    for c in self.children: #tant qu'on a d'enfant on continue
        lastNode = c.thread(lastNode)
    lastNode.addNext(self)
    return self

'''
Vérifie la couture pour une boucle while
'''
@addToClass(AST.WhileNode)
def thread(self, lastNode):
    beforeCond = lastNode
    exitCond = self.children[0].thread(lastNode)
    exitCond.addNext(self)
    exitBody = self.children[1].thread(self)
    exitBody.addNext(beforeCond.next[-1])

    if self.children[0].children: #si on a des enfants d'enfants
        if self.children[0].children[0].tok not in dict_variables: # et que celui ci n'est pas encore dans le dictionnaire
            print("error : "+self.children[0].children[0].tok+ " is not defined")
            sys.exit() # message d'erreur donc on arrête le programme
    else:
         if self.children[0].tok not in dict_variables: #si celui-ci n'est pas dans le dictionnaire
            print("error : "+self.children[0].tok+ " is not defined")
            sys.exit() #message d'erreur et on arrête le programme

    return self


'''
Vérifier couture du bloc if
'''
@addToClass(AST.IfNode)
def thread(self,lastNode):
    beforeCond = lastNode
    exitCond = self.children[0].thread(lastNode)
    exitCond.addNext(self)
    exitBody = self.children[1].thread(self)
    exitBody.addNext(beforeCond.next[-1])
    if self.children[0].children: #si l'enfant a des enfants
        if self.children[0].children[0].tok not in dict_variables: #si le token n'est pas dans le dictionnaire
            print("error : "+self.children[0].children[0].tok+ " is not defined")
            sys.exit() #message d'erreur et on arrête le programme
    else:
         if self.children[0].tok not in dict_variables: #s'il n'est pas dans le dictionnaire
            print("error : "+self.children[0].tok+ " is not defined")
            sys.exit() #message d'erreur et on arrête le programme

    return self  

'''
Vérifie la couture pour une assignation
'''
@addToClass(AST.AssignNode)
def thread(self,lastNode):
    '''
    utilisation mot clé global car le dictionnaire devra être utilisée dans plusieurs functions.
    sans le mot clé, après la sortie de ce bloc, le dictionnaire n'aura pas le même contenu dans d'autres functions.
    '''
    global dict_variables
    
    if self.children[0].tok in dict_variables: #si la variable est déjà dans le dictionnaire
        if self.children[1].children: #si l'enfant a des enfats (exemple : 3+5)
            if isinstance(self.children[1].children[0].tok,float) or isinstance(self.children[1].children[1].tok,float): #si les deux enfants sont des gloat
                if dict_variables.get(self.children[0].tok)=='float': #si cette variable est de type float
                    pass # on fait rien car le type n'a pas changé
                else:
                    print("error : confliting declaration int "+self.children[0].tok)
                    sys.exit() #message d'erreur et on arrête le programme
            else:
                if dict_variables.get(self.children[0].tok)=='int':
                    pass
                else:
                    print("error : confliting declaration int "+self.children[0].tok)
                    sys.exit()

        else:
            if isinstance(self.children[1].tok,float):
                if dict_variables.get(self.children[0].tok)=='float':
                    pass #on a le meme type, donc on fait rien
                else:
                    print("error : confliting declaration int "+self.children[0].tok)
                    sys.exit() #message d'erreur et on arrête le programme
            else:
                if dict_variables.get(self.children[0].tok)=='int':
                    pass #on a le meme type donc on fait rien
                else:
                    print("error : confliting declaration float "+self.children[0].tok)
                    sys.exit() #message d'erreur et on arrête le programme

    if self.children[1].children:
        if isinstance(self.children[1].children[0].tok,float) or isinstance(self.children[1].children[1].tok,float): #si une des enfants est un float
            dict_variables[self.children[0].tok]= 'float' #la variable est forcément de type float
        else:
            dict_variables[self.children[0].tok]= 'int' # variable de type int   
    else:
        if isinstance(self.children[1].tok,float):
            dict_variables[self.children[0].tok] = 'float'
        else:
            dict_variables[self.children[0].tok] = 'int'

    for c in self.children:
        lastNode = c.thread(lastNode)
    lastNode.addNext(self)

    return self
    

'''
Vérifie la couture pour les opérateurs
'''
@addToClass(AST.OpNode)
def thread(self, lastNode):

    if self.op=='/' and int(self.children[1].tok)==0: #si '/ est suivi d'un 0
        print("ZeroDivisionError: integer division or modulo by zero ")
        sys.exit()
    else:
        for c in self.children:
            lastNode = c.thread(lastNode)
        lastNode.addNext(self)

        return self

'''
Vérifie la couture pour un print
'''
@addToClass(AST.PrintNode)
def thread(self,lastNode):
    if self.children[0].children:
        if self.children[0].children[0].tok not in dict_variables: #si la variable n'est pas encore dans le dictionnaire
            print("error : "+self.children[0].children[0].tok+ " is not defined")
            sys.exit()
    else:
        if self.children[0].tok not in dict_variables:
            if not isinstance(self.children[0].tok,float): #si c'est pas un float
                try:
                    isinstance(int(self.children[0].tok),int) #tentative de convertir en int, obligation d'utiliser try, if ne suffit pas
                except:
                    print("error : "+self.children[0].tok+ " is not defined")
                    sys.exit() #ca veut dire que c'est un string, donc comme pas présent dans le dictionnaire, message d'erreur et arrêt du programme

    for c in self.children:
        lastNode = c.thread(lastNode)
    lastNode.addNext(self)
    
    return self


def thread(tree):
    entry = AST.EntryNode()
    tree.thread(entry)
    return entry

if __name__ == "__main__":
    from pythonParser import parse
    import sys, os
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    entry = thread(ast)

    graph = ast.makegraphicaltree()
    entry.threadTree(graph)
    
    name = os.path.splitext(sys.argv[1])[0]+'-ast-threaded.pdf'
    graph.write_pdf(name) 
    print ("wrote threaded ast to", name)    