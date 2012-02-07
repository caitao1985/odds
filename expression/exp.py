#!/usr/bin/python

def evaluateSimpleUnit(input):
    if len(input) < 3:
        raise Exception('invalid input ' + str(input))
    lhs, op, rhs = input[:3]
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

def evaluateSimpleUnitStr(input):
    #TODO make the parse more friendly.
    row = input.split(' ')
    if len(row) < 3:
        raise Exception('invalid input ' + input)
    row[0] = int(row[0])
    row[2] = int(row[2])
    return evaluateSimpleUnit(row)

def testEvaluateSimpleUnit():
    print evaluateSimpleUnitStr('1 + 2')
    print evaluateSimpleUnitStr('1 - 2')
    print evaluateSimpleUnitStr('3 * 2')
    print evaluateSimpleUnitStr('12 / 3')

def evaluateWithoutBracket(input):
    row = input.split(' ')
    for i in range(0, len(row),2):
        row[i] = int(row[i])
    i = 0
    #phase = 0, first calc * or /
    #phase = 1, calc + and -
    phase = 0
    while i < len(row) or phase < 1:
        if i >= len(row):
            phase = 1
            i = 0

        if row[i] != '*' and row[i] != '/' and phase == 0:
            i += 1
            continue

        if phase == 1 and row[i] != '+' and row[i] != '-':
            i += 1
            continue

        if i < 1 or i > len(row) - 2:
            raise Exception('invalid operator ' + row[i] + ' in ' + str(input))
        tmp = evaluateSimpleUnit(row[i-1:i+2])
        row = row[0:i-1] + [ tmp ] + row[i+2:]

    if len(row) != 1:
        raise Exception('invalid result ' + str(row) + ' expression ' + input)
    return row[0]

def testEvaluateWithoutBracket():
    print evaluateWithoutBracket('2 + 3 * 4 - 12 / 6')

def evaluate(input):
    left = input.find('(')
    if left == -1:
        return evaluateWithoutBracket(input)
    else:
        #find mathing right bracket.
        mark  = 1
        right = -1
        for i in range(left + 1, len(input)):
            if (input[i] == '('):
                mark += 1
            elif (input[i] == ')'):
                mark -= 1
            if mark == 0:
                right = i
                break
        if right == -1: raise Exception(" no right bracket match in " + input)
        tmp = evaluate(input[left + 1:right])
        return evaluate(input[0:left] + str(tmp) + input[right+1:])

def testEvaluate():
    print evaluate('2 * ((3 + 9 * 3) / 4)')

def main():
    testEvaluateSimpleUnit()
    testEvaluateWithoutBracket()
    testEvaluate()
    pass

if __name__ == "__main__":
    main()
