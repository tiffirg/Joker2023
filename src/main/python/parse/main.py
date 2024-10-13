import random
import string
import html5lib

TAGS = ['section', 'article', 'div', 'span', 'a', 'b', 'i' 'p']
TEXT_TAGS = ['div', 'span', 'a', 'b', 'i' 'p']
SYMBOLS = ['<', '>', '&', '"', "'", "\n", "\t", '\x00', '\x01', '😃', '😄', '😁', '👿', '😈']
MAX_DEPTH = 5
MAX_VALUES = 5
k = 0.5


def create_random_sequence(size=8):
    char_set = string.ascii_letters + string.digits
    return ''.join(random.choice(char_set) for _ in range(size))


def generate_html_tree(depth=None):
    if depth is None:
        depth = 0
    if depth > MAX_DEPTH:
        return create_random_sequence()
    element = random.choice(TAGS)
    content = generate_html_tree(depth + 1)
    return f"<{element}>{content}</{element}>"


def create_html_with_random_attributes():
    html = ''
    for _ in range(random.randint(1, MAX_VALUES)):
        elem = random.choice(TAGS)
        if random.random() < k:
            attr = f"attr='{create_random_sequence()}'"
            html += f"<{elem} {attr}>{create_random_sequence()}</{elem}>"
        else:
            html += f"<{elem}>{create_random_sequence()}</{elem}>"
    return html


def create_partial_html():
    html = ''
    for _ in range(random.randint(1, MAX_VALUES)):
        elem = random.choice(TAGS)
        if random.random() < k:
            html += generate_html_tree()
        html += f"<{elem}>{create_random_sequence()}"
        if random.random() < k:
            continue
        html += f"</{elem}>"
    return html


def create_html_with_special_symbols():
    html = ''
    for _ in range(random.randint(1, MAX_VALUES)):
        elem = random.choice(TEXT_TAGS)
        content = ''.join(random.choice(
            string.ascii_letters + random.choice(SYMBOLS)) for _ in range(10))
        html += f"<{elem}>{content}</{elem}>"
    return html


def generate_random_html():
    generators = [
        generate_html_tree,
        create_html_with_random_attributes,
        create_partial_html,
        create_html_with_special_symbols
    ]

    generator = random.choice(generators)
    result_html = f'<!DOCTYPE html><html><body>{generator()}</body></html>'
    return result_html


def fuzz_test_parser(parser_func, iterations=100):
    errors_number = 0
    for _ in range(iterations):
        html_input = generate_random_html()
        try:
            parser_func(html_input)
        except Exception as err:
            errors_number += 1
            print(f"Error: '{err}' in '{html_input}'")

    print("Errors number:", errors_number)


if __name__ == "__main__":
    fuzz_test_parser(html5lib.parse)
