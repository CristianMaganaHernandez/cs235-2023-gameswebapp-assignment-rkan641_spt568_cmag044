# Helper function to find out whether the name string includes the substring.
# Case insensitive search.
def search_string(name: str, substring: str):
    return substring.strip().lower() in name.lower()

# Used for sorting by title alphabetically with extra logics
def title_for_sorting(title: str)->str:
    # Only extracts alphabets for sorting (no digits and special characters)
    alphabet_list = [char.lower() for char in title if char.isalpha()]
    alphabets = ''.join(alphabet_list)

    # If there are alphabets in title, return it for sorting
    # The title should start with alphabets to be prioritized for sorting.
    if alphabets and title[0].isalpha():
        return alphabets

    # If there are no alphabets in the title, put 'z' in front so that those titles are placed at the end
    # in the sorting process (otherwise the titles with special characters will come first in sorting due to ASCII order)
    return f'z{title}'

# Sort list of entities by title alphabetically,
# such as list of games that have title attributes
def sort_entities_by_title(items: list) -> list:
    items.sort(key=lambda entity: title_for_sorting(entity.title))
    return items
