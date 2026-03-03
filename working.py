def compile_italic_star(line):
    '''
    Convert "*italic*" into "<i>italic</i>".

    HINT:
    Italics require carefully tracking the beginning and ending positions of the text to be replaced.
    This is similar to the `delete_HTML` function that we implemented in class.
    It's a tiny bit more complicated since we are not just deleting substrings from the text,
    but also adding replacement substrings.

    >>> compile_italic_star('*This is italic!* This is not italic.')
    '<i>This is italic!</i> This is not italic.'
    >>> compile_italic_star('*This is italic!*')
    '<i>This is italic!</i>'
    >>> compile_italic_star('This is *italic*!')
    'This is <i>italic</i>!'
    >>> compile_italic_star('This is not *italic!')
    'This is not *italic!'
    >>> compile_italic_star('*')
    '*'
    '''
    #you can use the .find or hte .count to find and count functions 
    accumulator = ''
    has_opened = False #have we seen a * yet? 
    for char in line: 
        if char =='*':
            if not has_opened:
                accumulator +='<i>'
                has_opened = True 
            else: 
                accumulator += '</i>'
                has_opened = False 

    return accumulator
#the reason why this is harder than the previous function is that the markdown 
#code can appear anywhere in the string not just the beginning 
#also there are two pieces of indo we need to match 
#first * is the <i>
#second * is the </i>
#all functions are the easiest to implement with the accumulator pattern 