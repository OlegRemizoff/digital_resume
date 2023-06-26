from transliterate import translit

import re


def slugify(s):
    s = translit(s, 'ru', reversed=True)
    pattern = r'[^\w+]'
    format_str =  re.sub(pattern, '_', s.lower())
    while '__'  and ' ' in format_str:
        format_str.replace('__', '_')
        format_str.replace(' ', '_')
    return format_str




