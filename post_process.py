import os
import re

def post_process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- Aggressively remove all leading whitespace from every line ---
    # This fixes all indentation issues at the risk of flattening nested lists.
    content = re.sub(r'^\s+', '', content, flags=re.MULTILINE)

    # --- Fix Callouts ---
    # This pattern should still work on un-indented content.
    callout_pattern = re.compile(
        r"!\[\]\(https://www\.notion\.so/icons/.*\.svg\)\s*(.*?)\s*<br/>",
        re.DOTALL
    )
    def replace_callout(match):
        callout_content = match.group(1).strip()
        indented_content = '\n'.join([f'> {line.strip()}' for line in callout_content.splitlines() if line.strip()])
        return f'> [!note]\n{indented_content}'
    content = callout_pattern.sub(replace_callout, content)

    # --- Convert Image Links to Obsidian Wikilinks ---
    # Now that content is un-indented, this can be a simpler pattern.
    # It still handles optional backticks.
    image_pattern = re.compile(
        r"(?:`{1,3})?!\\[.*?\\]\((.*?)\)(?:`{1,3})?"
    )
    def to_wikilink_callback(match):
        filename = match.group(1)
        if filename.startswith(('http://', 'https://')):
            return match.group(0)
        return f"\n![[{filename}]]"
    content = image_pattern.sub(to_wikilink_callback, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    # a file from the last backup
    file_to_process = "D:/notionsafe/notion2md-output/2025-11-05_23-15-43/Measurements.md"
    post_process_file(file_to_process)