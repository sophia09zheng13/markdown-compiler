"""
Line-by-line markdown transformations.
"""


def compile_headers(line):
    """
    Convert markdown headers into <h1>, <h2>, etc tags.
    """
    result = ""
    for i in range(6, 0, -1):
        prefix = "#" * i + " "
        if line[:i + 1] == prefix:
            result = f"<h{i}> {line[i + 1:]}</h{i}>"
    if result == "":
        return line
    return result


def compile_italic_star(line):
    """
    Convert "*italic*" into "<i>italic</i>".
    """
    result = ""

    start = line.find("*")
    if start != -1 and start + 1 < len(line) and line[start + 1] == "*":
        start = -1

    if start != -1:
        end = line.find("*", start + 1)
        if end != -1:
            result = f"{line[:start]}<i>{line[start + 1:end]}</i>{line[end + 1:]}"

    if result == "":
        return line
    return result


def compile_italic_underscore(line):
    """
    Convert "_italic_" into "<i>italic</i>".
    """
    result = ""

    start = line.find("_")
    if start != -1 and start + 1 < len(line) and line[start + 1] == "_":
        start = -1

    if start != -1:
        end = line.find("_", start + 1)
        if end != -1:
            result = f"{line[:start]}<i>{line[start + 1:end]}</i>{line[end + 1:]}"

    if result == "":
        return line
    return result


def compile_strikethrough(line):
    """
    Convert "~~strikethrough~~" to "<ins>strikethrough</ins>".
    """
    result = ""

    start = line.find("~~")
    if start != -1:
        end = line.find("~~", start + 2)
        if end != -1:
            result = (
                f"{line[:start]}<ins>{line[start + 2:end]}</ins>{line[end + 2:]}"
            )

    if result == "":
        return line
    return result


def compile_bold_stars(line):
    """
    Convert "**bold**" to "<b>bold</b>".
    """
    result = ""

    start = line.find("**")
    if start != -1:
        end = line.find("**", start + 2)
        if end != -1:
            result = f"{line[:start]}<b>{line[start + 2:end]}</b>{line[end + 2:]}"

    if result == "":
        return line
    return result


def compile_bold_underscore(line):
    """
    Convert "__bold__" to "<b>bold</b>".
    """
    result = ""

    start = line.find("__")
    if start != -1:
        end = line.find("__", start + 2)
        if end != -1:
            result = f"{line[:start]}<b>{line[start + 2:end]}</b>{line[end + 2:]}"

    if result == "":
        return line
    return result


def compile_code_inline(line):
    """
    Add <code> tags for backticks, escaping < and > (and & for safety).
    """
    result = ""

    if line[:3] == "```":
        return line

    start = line.find("`")
    if start != -1:
        end = line.find("`", start + 1)
        if end != -1:
            code_text = line[start + 1:end]
            code_text = code_text.replace("&", "&amp;")
            code_text = code_text.replace("<", "&lt;")
            code_text = code_text.replace(">", "&gt;")
            result = f"{line[:start]}<code>{code_text}</code>{line[end + 1:]}"

    if result == "":
        return line
    return result


def compile_links(line):
    """
    Add <a> tags for [text](url).
    """
    result = ""

    start = line.find("[")
    if start != -1:
        mid = line.find("](", start)
        if mid != -1:
            end = line.find(")", mid + 2)
            if end != -1:
                text = line[start + 1:mid]
                url = line[mid + 2:end]
                result = f'{line[:start]}<a href="{url}">{text}</a>{line[end + 1:]}'

    if result == "":
        return line
    return result


def compile_images(line):
    """
    Add <img> tags for ![alt](url).
    """
    result = ""

    start = line.find("![")
    if start != -1:
        mid = line.find("](", start + 2)
        if mid != -1:
            end = line.find(")", mid + 2)
            if end != -1:
                alt = line[start + 2:mid]
                src = line[mid + 2:end]
                img_tag = f'<img src="{src}" alt="{alt}" />'
                result = f"{line[:start]}{img_tag}{line[end + 1:]}"

    if result == "":
        return line
    return result
