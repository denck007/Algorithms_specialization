'''
Algorithms Divide and Conquer
Week 1
Programming assignment 1

Implement Karatsuba's algotithm to multiply 2 64 digit numbers
Use recursion
Build test cases

My method to solve:
* Number is input as a string
* Convert string to list of strings where each list entry is a single digit
* Get both inputs to be the same length
* Recursivly call the karatsuba method 

Note that this is not the full karatsuba method, but is really close to it
* In this implementation we do recursion on all 4 n/2 multiplication combinations
'''
import math
import copy

def left_pad(input,n):
    '''
    Add n zeros to the left side of input
    returns a modified copy of the input
    '''
    output = copy.copy(input)
    while len(output) < n:
        output.insert(0,'0')
    return output

def multiply_by_10(input,n):
    '''
    Multiply the input by 10^n, which is reall a right padding of n zeros
    returns a modified copy of the input
    '''
    output = copy.copy(input)
    output.extend(['0']*int(n))
    return output

def test_left_pad():
    output = left_pad(['1'],1)
    expected = ['1']
    assert  expected == output, "Failed on {}".format(expected)
    output = left_pad(['1'],2)
    expected = ['0','1']
    assert  expected == output, "Failed on {}".format(expected)
    output = left_pad(['1'],4)
    expected = ['0','0','0','1']
    assert  expected == output, "Failed on {}".format(expected)
    print("left_pad() passed!")

def test_multiply_by_10():
    output = multiply_by_10(['1'],0)
    expected = ['1']
    assert  expected == output, "Failed on {}".format(expected)
    output = multiply_by_10(['1'],1)
    expected = ['1','0']
    assert  expected == output, "Failed on {}".format(expected)
    output = multiply_by_10(['1'],5)
    expected = ['1','0','0','0','0','0']
    assert  expected == output, "Failed on {}".format(expected)
    print("multiply_by_10() passed!")

def single_digit_multiply(x,y):
    '''
    calculate the product of 2 single integers
    x and y are each a list of strings, both lists are of len == 1
    '''
    prod = int(x[0])*int(y[0])
    prod = [i for i in "{:02d}".format(prod)]
    return prod

def add(x_in,y_in):
    '''
    given 2 lists of single digit strings, add the values together and return list of strings
    '''
    n = max(len(x_in),len(y_in))
    x = left_pad(x_in,n+1)
    y = left_pad(y_in,n+1)

    output = ['0']*(n+1)
    carry = 0

    for ii in range(n,-1,-1):
        a = int(x[ii])
        b = int(y[ii])
        
        s = a + b + carry
        sum_string = "{:02d}".format(s)
        carry = int(sum_string[0])
        output[ii] = sum_string[1]

    return output

def test_add():
    x = ['1']
    y = ['1']
    output = add(x,y)
    expected = ['0','2']
    assert output == expected,"Failed on {} + {} = {}, yielded {}".format(x,y,expected,output)

    x = ['9']
    y = ['9']
    output = add(x,y)
    expected = ['1','8']
    assert output == expected,"Failed on {} + {} = {}, yielded {}".format(x,y,expected,output)

    x = ['9','9']
    y = ['9']
    output = add(x,y)
    expected = ['1','0','8']
    assert output == expected,"Failed on {} + {} = {}, yielded {}".format(x,y,expected,output)
    print("add() passed!")

def clean_inputs(x,y):
    '''
    Convert the input from a string to a list of strings
    pad the inpust so they are the same length
    '''
    if type(x) is int:
        x = str(x)
    if type(y) is int:
        y = str(y)

    n = max(len(x),len(y))
    power = math.ceil(math.log2(n))
    n = 2**power
    x = [i for i in x]
    y = [i for i in y]
    x = left_pad(x,n)
    y = left_pad(y,n)

    return x,y

test_left_pad()
test_multiply_by_10()
test_add()


def karatsuba(x,y):
    '''
    Recursive function to calculate karatsuba multiplication
    '''
    n = len(x)
    assert len(y) == n, 'Length of inputs are not same! x: {} y: {}'.format(x,y)

    # zero pad
    if n == 1:
        x = ['0',x[0]]
        y = ['0',y[0]]
        n = 2
    a = x[:n//2]
    b = x[n//2:]
    c = y[:n//2]
    d = y[n//2:]
    if n == 2:
        ac = single_digit_multiply(a,c)
        bd = single_digit_multiply(b,d)
        ad = single_digit_multiply(a,d)
        bc = single_digit_multiply(b,c)
    else:
        ac = karatsuba(a,c)
        bd = karatsuba(b,d)
        ad = karatsuba(a,d)
        bc = karatsuba(b,c)

    # 10^n*ac
    part1 = multiply_by_10(ac,n)
    # (ad+bc)
    part2 = add(ad,bc)
    # 10^(n/2)*(ad+bc)
    part3 = multiply_by_10(part2,n/2)
    # 10^(n/2)*(ad+bc) + bd
    part4 = add(part3,bd)
    output = add(part1,part4)

    while (output[0] == '0') and (len(output) > 1):
        output.pop(0)

    return output

def test_karatsuba():
    x = 1
    y = 1
    out_string = "{} * {} = ".format(x,y)
    expected = [i for i in "{:d}".format(x*y)]
    x,y = clean_inputs(x,y)
    output = karatsuba(x,y)
    assert expected== output,'Failed on x= {} y={}, got {}, expected: {}'.format(x,y,output,expected)
    output = str(output).replace("['","").replace("', '","").replace("']","")
    print("{} {}".format(out_string,output))

    x = 99
    y = 23
    out_string = "{} * {} = ".format(x,y)
    expected = [i for i in "{:d}".format(x*y)]
    x,y = clean_inputs(x,y)
    output = karatsuba(x,y)
    assert expected== output,'Failed on x= {} y={}, got {}, expected: {}'.format(x,y,output,expected)
    output = str(output).replace("['","").replace("', '","").replace("']","")
    print("{} {}".format(out_string,output))

    x = 1234
    y = 5678
    out_string = "{} * {} = ".format(x,y)
    expected = [i for i in "{:d}".format(x*y)]
    x,y = clean_inputs(x,y)
    output = karatsuba(x,y)
    assert expected== output,'Failed on x= {} y={}, got {}, expected: {}'.format(x,y,output,expected)
    output = str(output).replace("['","").replace("', '","").replace("']","")
    print("{} {}".format(out_string,output))

    x = 1234586
    y = 56785614
    out_string = "{} * {} = ".format(x,y)
    expected = [i for i in "{:d}".format(x*y)]
    x,y = clean_inputs(x,y)
    output = karatsuba(x,y)
    assert expected== output,'Failed on x= {} y={}, got {}, expected: {}'.format(x,y,output,expected)
    output = str(output).replace("['","").replace("', '","").replace("']","")
    print("{} {}".format(out_string,output))

    print("karatsuba passed!")

test_karatsuba()

print("Running final calculation...")
x = "3141592653589793238462643383279502884197169399375105820974944592"
y = "2718281828459045235360287471352662497757247093699959574966967627"
x,y = clean_inputs(x,y)
output = karatsuba(x,y)
output = str(output).replace("['","").replace("', '","").replace("']","")

print("Result is:")
print(output)






    



