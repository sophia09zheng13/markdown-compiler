'''
Each of the functions in this file takes a single line of input and transforms the line in some way.
'''
#run doctest function to test the file: python3 -m doctest util/line_functions.py 


def compile_headers(line):
    result = ""
    for i in range(6,0,-1):
      prefix = '#' * i + " "
      if line[:i + 1] == prefix:
         result = "<h" + f"{i}" + "> " + line[i+1:] + "</h" + f"{i}" + ">"
    if result == "":
     return line
    return result 


def compile_italic_star(line):
    result = ""

    start = line.find('*')
    if start != -1:
        # avoid treating "**" as italics
        if start + 1 < len(line) and line[start + 1] == '*':
            start = -1

    if start != -1:
        end = line.find('*', start + 1)
        if end != -1:
            result = line[:start] + "<i>" + line[start + 1:end] + "</i>" + line[end + 1:]

    if result == "":
        return line
    return result

   


def compile_italic_underscore(line):
    result = ""

    start = line.find('_')
    if start != -1:
        # avoid treating "__" as italics
        if start + 1 < len(line) and line[start + 1] == '_':
            start = -1

    if start != -1:
        end = line.find('_', start + 1)
        if end != -1:
            result = line[:start] + "<i>" + line[start + 1:end] + "</i>" + line[end + 1:]

    if result == "":
        return line
    return result 



def compile_strikethrough(line):
    result = ""

    start = line.find("~~")
    if start != -1:
        end = line.find("~~", start + 2)
        if end != -1:
            result = line[:start] + "<ins>" + line[start + 2:end] + "</ins>" + line[end + 2:]

    if result == "":
        return line
    return result


def compile_bold_stars(line):
    result = ""

    start = line.find("**")
    if start != -1:
        end = line.find("**", start + 2)
        if end != -1:
            result = line[:start] + "<b>" + line[start + 2:end] + "</b>" + line[end + 2:]

    if result == "":
        return line
    return result



def compile_bold_underscore(line):
    result = ""

    start = line.find("__")
    if start != -1:
        end = line.find("__", start + 2)
        if end != -1:
            result = line[:start] + "<b>" + line[start + 2:end] + "</b>" + line[end + 2:]

    if result == "":
        return line
    return result



def compile_code_inline(line):
    result = ""

    # match doctests: don't treat fenced-code markers as inline code
    if line[:3] == "```":
        return line

    start = line.find("`")
    if start != -1:
        end = line.find("`", start + 1)
        if end != -1:
            code_text = line[start + 1:end]

            # escape HTML-ish characters inside inline code
            code_text = code_text.replace("&", "&amp;")
            code_text = code_text.replace("<", "&lt;")
            code_text = code_text.replace(">", "&gt;")

            result = line[:start] + "<code>" + code_text + "</code>" + line[end + 1:]

    if result == "":
        return line
    return result



def compile_links(line):
    result = ""

    start = line.find("[")
    if start != -1:
        mid = line.find("](", start)
        if mid != -1:
            end = line.find(")", mid + 2)
            if end != -1:
                text = line[start + 1:mid]
                url = line[mid + 2:end]
                result = line[:start] + '<a href="' + url + '">' + text + "</a>" + line[end + 1:]

    if result == "":
        return line
    return result
 
 


def compile_images(line):
    result = ""

    start = line.find("![")
    if start != -1:
        mid = line.find("](", start + 2)
        if mid != -1:
            end = line.find(")", mid + 2)
            if end != -1:
                alt = line[start + 2:mid]
                src = line[mid + 2:end]
                img_tag = '<img src="' + src + '" alt="' + alt + '" />'
                result = line[:start] + img_tag + line[end + 1:]

    if result == "":
        return line
    return result
  
