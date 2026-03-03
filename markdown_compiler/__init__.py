'''
This file contains functions that work on entire documents at a time
(and not line-by-line).
'''

from markdown_compiler.util.line_functions import (
    compile_headers,
    compile_italic_star,
    compile_italic_underscore,
    compile_strikethrough,
    compile_bold_stars,
    compile_bold_underscore,
    compile_code_inline,
    compile_links,
    compile_images,
)

def compile_lines(text):
    result = ""

    leading = ""
    i = 0
    while i < len(text) and text[i] == "\n":
        leading += "\n"
        i += 1
    text = text[i:]
    result += leading

    lines = text.splitlines(True)  

    in_paragraph = False

    for raw_line in lines:
        if raw_line.strip() == "":
            if in_paragraph:
                result += "</p>\n"
                in_paragraph = False
            continue

        if not in_paragraph:
            result += "<p>\n"
            in_paragraph = True

        content = raw_line.strip() + "\n"

        content = compile_headers(content)

        content = compile_code_inline(content)

        content = compile_images(content)
        content = compile_links(content)

  
        content = compile_bold_stars(content)
        content = compile_bold_underscore(content)
        content = compile_italic_star(content)
        content = compile_italic_underscore(content)
        content = compile_strikethrough(content)

        result += content

    if in_paragraph:
        result += "</p>"


    if result.endswith("</p>\n"):
        result = result[:-1]
    return result
    

    #NOTE:
    #This second set of test cases tests multiline code blocks.

    #HINT:
def compile_lines(text):
    lines = text.split('\n')
    new_lines = []
    in_paragraph = False
    in_code_block = False

    for line in lines:
        raw_line = line              # keep original indentation for code blocks
        stripped = line.strip()      # for detecting blank lines and fences

        # --- Handle fenced code blocks: ``` or ```python3 etc. ---
        if stripped.startswith('```'):
            if not in_code_block:
                in_code_block = True
                new_lines.append('<pre>')
            else:
                in_code_block = False
                new_lines.append('</pre>')
            continue

        # --- Inside a code block: keep line exactly, no markdown transforms ---
        if in_code_block:
            new_lines.append(raw_line)
            continue

        # --- Blank line: close paragraph if open, otherwise keep blank ---
        if stripped == '':
            if in_paragraph:
                new_lines.append('</p>')
                in_paragraph = False
            else:
                new_lines.append('')
            continue

        # If we see a header while in a paragraph, close paragraph first
        if stripped.startswith('#') and in_paragraph:
            new_lines.append('</p>')
            in_paragraph = False

        # Start a paragraph if needed (non-header content)
        if (not stripped.startswith('#')) and (not in_paragraph):
            new_lines.append('<p>')
            in_paragraph = True

        # Apply line-level transformations
        # (Order: headers first; inline code early; images before links; then rest)
        line_out = stripped
        line_out = compile_headers(line_out)

        line_out = compile_code_inline(line_out)

        line_out = compile_images(line_out)
        line_out = compile_links(line_out)

        line_out = compile_strikethrough(line_out)
        line_out = compile_bold_stars(line_out)
        line_out = compile_bold_underscore(line_out)
        line_out = compile_italic_star(line_out)
        line_out = compile_italic_underscore(line_out)

        new_lines.append(line_out)

    # Close paragraph if file ends while paragraph is still open
    if in_paragraph:
        new_lines.append('</p>')

    return '\n'.join(new_lines)




def compile_lines(text):

    lines = text.split('\n')
    new_lines = []
    in_paragraph = False
    in_code_block = False

    for line in lines:
        raw_line = line              # keep original (for code indentation)
        stripped = line.strip()      # used for detecting blank/fences/etc

    
        if stripped.startswith('```'):
            if not in_code_block:
                # opening fence
                in_code_block = True
                new_lines.append('<pre>')
            else:
                # closing fence
                in_code_block = False
                new_lines.append('</pre>')
            continue

        if in_code_block:
            # preserve indentation exactly like the doctest expects
            new_lines.append(raw_line)
            continue

        line = stripped

        # blank line closes paragraph (if open)
        if line == '':
            if in_paragraph:
                new_lines.append('</p>')
                in_paragraph = False
            else:
                # keep extra blank lines as blanks so doctests print <BLANKLINE>
                new_lines.append('')
            continue

        # If a header appears while a paragraph is open, close paragraph first
        if line.startswith('#') and in_paragraph:
            new_lines.append('</p>')
            in_paragraph = False

        # Start paragraph if not a header and not already in paragraph
        if (not line.startswith('#')) and (not in_paragraph):
            in_paragraph = True
            new_lines.append('<p>')

        # Apply transformations (order: headers first, then inline code, then rest)
        line = compile_headers(line)
        line = compile_code_inline(line)
        line = compile_images(line)
        line = compile_links(line)
        line = compile_strikethrough(line)
        line = compile_bold_stars(line)
        line = compile_bold_underscore(line)
        line = compile_italic_star(line)
        line = compile_italic_underscore(line)

        new_lines.append(line)

    # Close paragraph if file ends mid-paragraph
    if in_paragraph:
        new_lines.append('</p>')

    new_text = '\n'.join(new_lines)
    return new_text


def markdown_to_html(markdown, add_css):
    """
    Convert the input markdown into valid HTML,
    optionally adding CSS formatting.
    """
    html = '''
<html>
<head>
    <style>
    ins { text-decoration: line-through; }
    </style>
    '''
    if add_css:
        html += '''
<link rel="stylesheet" href="https://izbicki.me/css/code.css" />
<link rel="stylesheet" href="https://izbicki.me/css/default.css" />
        '''
    html += '''
</head>
<body>
    ''' + compile_lines(markdown) + '''
</body>
</html>
    '''
    return html

def minify(html):
    """
    Remove redundant whitespace (spaces and newlines) from the input HTML,
    and convert all whitespace characters into spaces.
    """
    # split() with no args splits on ANY whitespace and collapses runs
    # join puts single spaces back between tokens
    return ' '.join(html.split())


def convert_file(input_file, add_css):
    """
    Convert the input markdown file into an HTML file.
    If the input filename is `README.md`,
    then the output filename will be `README.html`.
    """
    # validate that the input file is a markdown file
    if input_file[-3:] != '.md':
        raise ValueError('input_file does not end in .md')

    # load the input file
    with open(input_file, 'r') as f:
        markdown = f.read()

    # generate the HTML from the Markdown
    html = markdown_to_html(markdown, add_css)
    html = minify(html)

    # write the output file
    with open(input_file[:-2] + 'html', 'w') as f:
        f.write(html)