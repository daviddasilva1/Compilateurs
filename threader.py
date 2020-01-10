import AST
from AST import addToClass
import sys

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