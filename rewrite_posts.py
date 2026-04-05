import re, os

def rewrite(text):
    # lowercase, remove trailing dots, remove apostrophes in contractions
    text = text.lower()
    # remove apostrophes in contractions (don't -> dont, it's -> its, etc.)
    text = re.sub(r"(?<=[a-z])'(?=[a-z])", '', text)
    # remove trailing period at end of sentence (before newline or end)
    text = re.sub(r'\.\s*$', '', text, flags=re.MULTILINE)
    return text

def process_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    in_code = False
    in_frontmatter = False
    fm_count = 0
    result = []

    for line in lines:
        stripped = line.rstrip('\n')

        # track frontmatter
        if stripped == '---':
            fm_count += 1
            in_frontmatter = fm_count < 2
            result.append(line)
            continue

        if in_frontmatter:
            result.append(line)
            continue

        # track code blocks
        if stripped.startswith('```'):
            in_code = not in_code
            result.append(line)
            continue

        if in_code:
            result.append(line)
            continue

        # skip lines that are CTF descriptions, flags, solves, headings, links, images, html
        if (stripped.startswith('Description:') or
            stripped.startswith('Flag:') or
            stripped.startswith('Solves:') or
            stripped.startswith('#') or
            stripped.startswith('!') or
            stripped.startswith('<') or
            stripped.startswith('[^') or
            stripped.startswith('> ') or
            stripped.startswith('####') or
            stripped == ''):
            result.append(line)
            continue

        result.append(rewrite(stripped) + '\n')

    with open(path, 'w') as f:
        f.writelines(result)

posts_dir = '/home/koala/Downloads/0xkoala/_posts'
for fname in os.listdir(posts_dir):
    if fname.endswith('.md'):
        process_file(os.path.join(posts_dir, fname))
        print(f'done: {fname}')
