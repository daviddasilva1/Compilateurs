import AST
from AST import addToClass
import sys
from lex4 import reserved_words
import numbers

dict_variables = {}
used_variables = []

@addToClass(AST.Node)
def thread(self, lastNode):
    for c in self.children:
        lastNode = c.thread(lastNode)
    lastNode.addNext(self)
    return self

@addToClass(AST.WhileNode)
def thread(self, lastNode):
    beforeCond = lastNode
    exitCond = self.children[0].thread(lastNode)
    exitCond.addNext(self)
    exitBody = self.children[1].thread(self)
    exitBody.addNext(beforeCond.next[-1])
    if self.children[0].children:
        if self.children[0].children[0].tok not in dict_variables:
            print("error : "+self.children[0].children[0].tok+ " is not defined")
            sys.exit()
    else:
         if self.children[0].tok not in dict_variables:
            print("error : "+self.children[0].tok+ " is not defined")
            sys.exit()

    return self


@addToClass(AST.IfNode)
def thread(self,lastNode):
    beforeCond = lastNode
    exitCond = self.children[0].thread(lastNode)
    exitCond.addNext(self)
    exitBody = self.children[1].thread(self)
    exitBody.addNext(beforeCond.next[-1])
    if self.children[0].children:
        if self.children[0].children[0].tok not in dict_variables:
            print("error : "+self.children[0].children[0].tok+ " is not defined")
            sys.exit()
    else:
         if self.children[0].tok not in dict_variables:
            print("error : "+self.children[0].tok+ " is not defined")
            sys.exit()

    return self  

@addToClass(AST.AssignNode)
def thread(self,lastNode):
        global dict_variables
        
        if self.children[0].tok in dict_variables:
            if self.children[1].children:
                if isinstance(self.children[1].children[0].tok,float) or isinstance(self.children[1].children[1].tok,float):
                    if dict_variables.get(self.children[0].tok)=='float':
                        pass
                    else:
                        print("error : confliting declaration int "+self.children[0].tok)
                        sys.exit()
                else:
                    if dict_variables.get(self.children[0].tok)=='int':
                        pass
                    else:
                        print("error : confliting declaration int "+self.children[0].tok)
                        sys.exit()

            else:
                if isinstance(self.children[1].tok,float):
                    if dict_variables.get(self.children[0].tok)=='float':
                        pass
                    else:
                        print("error : confliting declaration int "+self.children[0].tok)
                        sys.exit()
                else:
                    if dict_variables.get(self.children[0].tok)=='int':
                        pass
                    else:
                        print("error : confliting declaration float "+self.children[0].tok)
                        sys.exit()

        if self.children[1].children:
            print(self.children[1].children[1].tok)
            if isinstance(self.children[1].children[0].tok,float) or isinstance(self.children[1].children[1].tok,float):
                dict_variables[self.children[0].tok]= 'float'
            else:
                dict_variables[self.children[0].tok]= 'int'

             
        else:
         
            if isinstance(self.children[1].tok,float):
                dict_variables[self.children[0].tok] = 'float'
            else:
                dict_variables[self.children[0].tok] = 'int'

        
        
        for c in self.children:
            lastNode = c.thread(lastNode)
        lastNode.addNext(self)

        return self
        


@addToClass(AST.OpNode)
def thread(self, lastNode):
    if self.op=='/' and int(self.children[1].tok)==0:
        print("ZeroDivisionError: integer division or modulo by zero ")
        sys.exit()
    else:
        for c in self.children:
            lastNode = c.thread(lastNode)
        lastNode.addNext(self)

        return self

@addToClass(AST.PrintNode)
def thread(self,lastNode):
    print(dict_variables)
    if self.children[0].children:
        if self.children[0].children[0].tok not in dict_variables:
            print("error : "+self.children[0].children[0].tok+ " is not defined")
            sys.exit()
    else:
        print("---------------")
        print(self)
        print("---------------")
        if self.children[0].tok not in dict_variables:
            if not isinstance(self.children[0].tok,float):
                try:
                    isinstance(int(self.children[0].tok),int)
                except:
                    print("error : "+self.children[0].tok+ " is not defined")
                    sys.exit()
            

            
    for c in self.children:
        lastNode = c.thread(lastNode)
    lastNode.addNext(self)
    
    return self


def thread(tree):
    entry = AST.EntryNode()
    tree.thread(entry)
    return entry

if __name__ == "__main__":
    from parser4 import parse
    import sys, os
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    entry = thread(ast)

    graph = ast.makegraphicaltree()
    entry.threadTree(graph)
    
    name = os.path.splitext(sys.argv[1])[0]+'-ast-threaded.pdf'
    graph.write_pdf(name) 
    print ("wrote threaded ast to", name)    