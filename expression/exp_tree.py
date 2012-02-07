#!/usr/bin/python
import re

class Node(object):
    def __init__(self, op = '', lhs = None, rhs = None):
        self.op  = op
        self.lhs = lhs
        self.rhs = rhs

SPS = re.compile('[ \t]+')
OPS = re.compile(r'[\+\-\*/\(\)]')  
def tokenizer(expr):
    expr = OPS.sub(' \g<0> ', expr)
    return SPS.split(expr.strip())

OPSET = set(['+', '-', '*', '/', '(', ')'])
NUMBERS = re.compile(r'\d+')
#TODO make sure that tokens r valid.
def filter(tokenList):
    for i in range(0, len(tokenList)):
        token = tokenList[i]
        if NUMBERS.match(token):
            tokenList[i] = int(token)
        #TODO floating point numbers.
        #operators check
        #other token check.
    return tokenList

def makeTokenList(expr):
    ret = tokenizer(expr)
    return filter(ret)
    
def buildSimpleUnit(input):
    if len(input) < 3:
        raise Exception('invalid input ' + str(input))
    lhs, op, rhs = input[:3]
    return Node(op, lhs, rhs)

def evaluateSimpleUnit(node):
    lhs, op, rhs = node.lhs, node.op, node.rhs
    if op == '+':
        return lhs + rhs
    elif op == '-':
        return lhs - rhs
    elif op == '*':
        return lhs * rhs
    elif op == '/':
        return lhs / rhs
    else:
        raise Exception('invalid operator ' + op + ' in input ' + input)

def evaluateTree(root):
    lhs = evaluateTree(root.lhs) if isinstance(root.lhs, Node) else root.lhs
    rhs = evaluateTree(root.rhs) if isinstance(root.rhs, Node) else root.rhs
    return evaluateSimpleUnit(Node(root.op, lhs, rhs))

def evaluateSimpleUnitStr(input):
    #TODO make the parse more friendly.
    row = input.split(' ')
    if len(row) < 3:
        raise Exception('invalid input ' + input)
    row[0] = int(row[0])
    row[2] = int(row[2])
    node = buildSimpleUnit(row)
    return evaluateSimpleUnit(node)

def buildExpressionWithNoBracket(tokenList):
    i = 0
    #phase = 0, first calc * or /
    #phase = 1, calc + and -
    phase = 0
    while i < len(tokenList) or phase < 1:
        if i >= len(tokenList):
            phase = 1
            i = 0

        if tokenList[i] != '*' and tokenList[i] != '/' and phase == 0:
            i += 1
            continue

        if phase == 1 and tokenList[i] != '+' and tokenList[i] != '-':
            i += 1
            continue

        if i < 1 or i > len(tokenList) - 2:
            raise Exception('invalid operator ' + tokenList[i] + ' in ' + str(tokenList))
        tmp = buildSimpleUnit(tokenList[i-1:i+2])
        tokenList = tokenList[0:i-1] + [ tmp ] + tokenList[i+2:]

    if len(tokenList) != 1:
        raise Exception('invalid result ' + str(tokenList) + ' expression ' + tokenList)
    return tokenList[0]


def buildExpressionTree(tokenList):
    while len(tokenList) > 0:
        try:
            left = tokenList.index('(')
        except ValueError:
            left = -1

        if left == -1:
            return buildExpressionWithNoBracket(tokenList)
        else:
            #finding mathing right bracket.
            mark  = 1
            right = -1
            for i in range(left + 1, len(tokenList)):
                if (tokenList[i] == '('):
                    mark += 1
                elif (tokenList[i] == ')'):
                    mark -= 1
                if mark == 0:
                    right = i
                    break
            if right == -1: raise Exception(" no right bracket match in " + str(tokenList))
            tmp = buildExpressionTree(tokenList[left + 1:right])
            tokenList = tokenList[0:left] + [tmp] + tokenList[right+1:]

def testEvaluate():
    tokenList = makeTokenList('2 * ((3 + 9 * 3) / 4)')
    tree      = buildExpressionTree(tokenList)
    print evaluateTree(tree)

def testEvaluateWithNoBracket():
    tokenList = makeTokenList('2 + 3 * 4 - 12 / 6')
    node = buildExpressionWithNoBracket(tokenList)
    print evaluateTree(node)

def testEvaluateSimpleUnit():
    print evaluateSimpleUnitStr('1 + 2')
    print evaluateSimpleUnitStr('1 - 2')
    print evaluateSimpleUnitStr('3 * 2')
    print evaluateSimpleUnitStr('12 / 3')

def main():
    testEvaluateSimpleUnit()
    testEvaluateWithNoBracket()
    testEvaluate()
    pass

if __name__ == "__main__":
    main()
