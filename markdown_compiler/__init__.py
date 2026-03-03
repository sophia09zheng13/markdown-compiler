"""
Markdown compiler package.
"""

from markdown_compiler.util.line_functions import (
    compile_bold_stars,
    compile_bold_underscore,
    compile_code_inline,
    compile_headers,
    compile_images,
    compile_italic_star,
    compile_italic_underscore,
    compile_links,
    compile_strikethrough,
)

__all__ = [
    "compile_lines",
    "markdown_to_html",
    "minify",
    "convert_file",
]


def compile_lines(text):
    """
    Apply markdown transformations to the input text, including paragraphs and
    fenced code blocks.
    """
    lines = text.split("\n")
    new_lines = []
    in_paragraph = False
    in_code_block = False

    for line in lines:
        raw_line = line
        stripped = line.strip()

        # Fenced code blocks: ``` or ```python
        if stripped.startswith("```"):
            if not in_code_block:
                in_code_block = True
                new_lines.append("<pre>")
            else:
                in_code_block = False
                new_lines.append("</pre>")
            continue

        # Inside code blocks: preserve indentation, no transforms
        if in_code_block:
            new_lines.append(raw_line)
            continue

        # Blank line closes paragraph
        if stripped == "":
            if in_paragraph:
                new_lines.append("</p>")
                in_paragraph = False
            else:
                new_lines.append("")
            continue

        # Headers should not be inside <p>
        if stripped.startswith("#") and in_paragraph:
            new_lines.append("</p>")
            in_paragraph = False

        # Start paragraph for non-header text
        if (not stripped.startswith("#")) and (not in_paragraph):
            new_lines.append("<p>")
            in_paragraph = True

        out = stripped
        out = compile_headers(out)

        # Inline code early so markdown inside code doesn't get parsed
        out = compile_code_inline(out)

        # Images before links
        out = compile_images(out)
        out = compile_links(out)

        out = compile_strikethrough(out)
        out = compile_bold_stars(out)
        out = compile_bold_underscore(out)
        out = compile_italic_star(out)
        out = compile_italic_underscore(out)

        new_lines.append(out)

    if in_paragraph:
        new_lines.append("</p>")

    return "\n".join(new_lines)


def markdown_to_html(markdown, add_css):
    """
    Convert markdown into full HTML, optionally adding CSS.
    """
    html = (
        "<html>\n"
        "<head>\n"
        "    <style>\n"
        "    ins { text-decoration: line-through; }\n"
        "    </style>\n"
    )

    if add_css:
        css_1 = (
            '<link rel="stylesheet" href="'
            "https://izbicki.me/css/code.css"
            '" />\n'
        )
        css_2 = (
            '<link rel="stylesheet" href="'
            "https://izbicki.me/css/default.css"
            '" />\n'
        )
        html += css_1 + css_2

    html += "</head>\n<body>\n"
    html += compile_lines(markdown)
    html += "\n</body>\n</html>\n"
    return html


def minify(html):
    """
    Remove redundant whitespace and convert all whitespace to single spaces.
    """
    return " ".join(html.split())


def convert_file(input_file, add_css):
    """
    Convert a markdown file to an HTML file with the same basename.
    """
    if input_file[-3:] != ".md":
        raise ValueError("input_file does not end in .md")

    with open(input_file, "r") as f:
        markdown = f.read()

    html = markdown_to_html(markdown, add_css)
    html = minify(html)

    output_file = input_file[:-2] + "html"
    with open(output_file, "w") as f:
        f.write(html)
