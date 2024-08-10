def find_by_xpath(html_content, xpath_expression):
    from lxml import html  # type: ignore
    tree = html.fromstring(html_content)
    elements = tree.xpath(xpath_expression)
    return elements


def to_float(value):
    try:
        return float(value.replace(',', '.').replace('R$', '').strip())
    except ValueError:
        return 0.0
