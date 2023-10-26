'''
Name:           Evan Whitmer
Date:           October 25, 2023
Class:          CSC-310-A Programming Languages
Description:    To make a Python implementation of Sethi's Little Quilt Language. See the Power Point Presentation 
                Lecture 14 (9/29) for more details. A quilt atom will be a single letter either “a” or “b”. Quilt atoms
                represent squares which contain a pattern. They can be in one of 4 possible orientations. An oriented atom 
                is a tuple of the form (“q”,i) where “q” is a quilt atom and i is an integer in the range 0,1,2,3. (“q”, i) 
                represents “q” rotated clockwise through i clockwise 90 degree rotations. Note that (“a”,0) represents “a” 
                itself. A quilt is a list of rows, all of which need to have the same length. A row is a list of oriented atoms. 
                For example, [[(“a”,1), (”a”,0), (”b”,1)], [(“b”,2), (”a”,1), (”a”, 3)]] is a 2x3 quilt
                You should bind variable a to quilt [[“a”,0]] and b to [[“b”,0]] so that a and b can be regarded as the names 
                for building-block quilts.
                Atoms should print as nxn block of characters such as
                #@
                ##
                This will be represented as a Python string like "#@\n##". Such a block can be rotated
                For example
                #@ rotates to ##
                ##                  #@
'''

#2d array as in a list of a list of tuples
a = [[('a', 0)]]
b = [[('b', 0)]]

#base for quilt project turn atom
def turn_atom(c):
    '''keep 'a', increase 90 turn and if greater than 3, set to 0'''
    return (c[0], (c[1] + 1) % 4)               

#List of List section
def metamap(f, Lol):                            
    '''List of list function: apply function f to each member of each list'''
    return [list(map(f, row)) for row in Lol]

#
def rotate(quilty):
    tempQuilt = []                                                  # temp for new quilt
    quiltLength = len(quilty) - 1                                   # number of list in List of list - 1 for zero base appending
    
    for row in range(len(quilty[0])):                               # number of tuples in any of the lists
        changedRow = []                                             # row after change aka a new list of tuples
    
        for column in range(len(quilty)):                           # returns 0-base range
            changedRow.append(quilty[quiltLength - column][row])    # row x column quilt tuple becomes column x row quilt tuple
    
        tempQuilt.append(changedRow)                                # add the new row to the quilt
    
    return tempQuilt                                                #return new quilt
    
#given in HW 9
def turn(quilt):
    '''turn quilt 90 degrees clockwise'''
    return metamap(turn_atom,rotate(quilt))

def sew(quilt1, quilt2):
    '''Sew to quilts together'''
    if (len(quilt1) != len(quilt2)):                        # if quilts are not the same height raise an Exception
        raise Exception("Quilts are not the same height.")
    
    newQuilty = []                          # new sew Quilt
    
    for q1row,q2row in zip(quilt1, quilt2):     
        newQuilty.append(q1row + q2row)     # add the lists of each row together and append that to a new row in the sew quilt
    
    return newQuilty

def unturn(quilty):
    '''Rotate quilt 90 degrees counter-clockwise'''
    return turn(turn(turn(quilty)))

def pile(quilty1, quilty2):
    '''Piles the first quilt onto the second'''
    return unturn(sew(turn(quilty2),turn(quilty1))) # 

def pinwheel(quitly):
    '''his function creates a new quilt with twice the number of rows and twice the number of columns and can 
       be thought of as rotating about the lower right corner of the original quilt. It only makes sense for square quilts.'''
    return sew(pile(quitly, unturn(quitly)), pile(turn(quitly), turn(turn(quitly))))

def repeat_block(quilty, m, n):
    '''by sewing and piling, piece together a quilt with m times the rows and n times the columns of the original 
       quilt. This simply repeats the original pattern.'''
    newQuilty = quilty                          # copy quilty to new one
    
    for i in range(m - 1):                      # make it 0-base
        newQuilty = pile(newQuilty, quilty)     # pile the same row onto itself 
    quilty = newQuilty                          # avoid height error
    
    for j in range(n - 1):
        newQuilty = sew(newQuilty, quilty)
    
    return newQuilty

def quilt_to_string(quitly, string1, string2):
    '''returns a string representation of the quilt using the string representations of string1 for piece a and 
    string2 for piece b. The printed quilt should embedded “\\n” separating the lines so that it prints correctly.'''
    stringQuilty = ''
    for row in quitly:
        for atomly in row:                                  # if tuple is a
            if atomly[0] == 'a':                            # replace with first half of string 1 
                stringQuilty += (string1[atomly[1]])[:2]
            else:                                           # if tuple is b
                stringQuilty += (string2[atomly[1]])[:2]     # replace with first half of string 2
                
        stringQuilty += '\n'                                # separate the lines so prints the line 
        
        for atomly in row:                                  # if tuple is a
            if atomly[0] == 'a':                            # replace with second half of string 1
                stringQuilty += (string1[atomly[1]])[2:4]
            else:                                           # if tuple is b
                stringQuilty += (string2[atomly[1]])[2:4]    # replace with second half of string 2
        stringQuilty += '\n'
    return stringQuilty

#Testing grounds

print('Print a: ', a)

print('Turn a: ', turn(a))

print('Unturn a: ', unturn(a))

print('Sew a and b: ', sew(a,b))

print('Pile a on b:')
for row in pile(a,b):
    print(row)

print('Pinwheel of a')
for corner in pinwheel(a):
    print(corner)
    
print('Repeat block a: ')
for rows in repeat_block(a, 3, 3):
    print(rows)
    
#1 └
#2 ┓
#3 ┎
#4 ┙
stringer1 = ['└┓┎┙','┎└┙┓','┙┎┓└','┓┙└┎']
            #1234  #3142   #4321  #2413
            #12     31      43     24  
            #34     42      21     13
            
#1 ┣
#2 ┫
#3 ┳
#4 ┻
stringer2 = ['┣┫┳┻','┳┣┻┫','┻┳┫┣','┫┻┣┳']
            #1234  #3142   #4321  #2413
            #12     31      43     24  
            #34     42      21     13

print('Quilt experiment 1:')
THEQuilt = sew(sew(b,b), turn(pile(b,b)))
THEQuilt = sew(THEQuilt, sew(sew(a,a), turn(pile(a,a))))
print(quilt_to_string(THEQuilt, stringer1, stringer2))
THEQuilt = turn(turn(THEQuilt))
print(quilt_to_string(THEQuilt, stringer1, stringer2))

print('Quilt experiment 2:')
THEQuilt2 = sew(pile(b,b), turn(sew(b,b)))

for i in range(5):
    print(quilt_to_string(THEQuilt2, stringer1, stringer2), end='')
    THEQuilt2 = turn(THEQuilt2)


print('\nQuilt Experiment 3:')
THEQuilt3 = pinwheel(pinwheel(pinwheel(b)))
THEQuilt3 = sew(THEQuilt3, THEQuilt3)
THEQuilt3 = sew(THEQuilt3, THEQuilt3)
THEQuilt3 = sew(THEQuilt3, THEQuilt3)
print(quilt_to_string(THEQuilt3, stringer1, stringer2))