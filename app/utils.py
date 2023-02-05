from transliterate import translit
import re


def slugify(s):
    s = translit(s, 'ru', reversed=True)
    pattern = r'[^\w+]'
    format_str =  re.sub(pattern, '-', s.lower())
    while '--' in format_str:
        format_str.replace('--', '-')
    return format_str