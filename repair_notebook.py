import json
import re

nb_path = "/Users/rexoghenerobo/Downloads/My Repo's/DataAnalytics/Project 1.ipynb"
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

changed = False
for cell in nb.get('cells', []):
    if cell.get('cell_type') != 'code':
        continue
    source = cell.get('source', [])
    joined = ''.join(source)
    # toggle DEBUG flag if present in setup cell
    if 'DEBUG = False' in joined:
        print('Setting DEBUG=True in setup cell')
        new_source = []
        for line in source:
            if 'DEBUG = False' in line:
                new_source.append(line.replace('DEBUG = False', 'DEBUG = True'))
            else:
                new_source.append(line)
        cell['source'] = new_source
        changed = True
    if '# Read keywords' in joined and 'keywords = [k.strip() for k in content.split' in joined:
        print('Modifying cell with keyword parsing...')
        # build new source lines
        new_lines = []
        in_block = False
        for line in source:
            if '# Read keywords' in line:
                new_lines.append(line)
                in_block = True
                # insert new robust code here
                new_lines.extend([
                    "            with open(tags_path, 'r', encoding='utf-8', errors='ignore') as f:\n",
                    "                content = f.read().strip()\n",
                    "                parts = content.split(None, 1)\n",
                    "                if len(parts) > 1 and ',' in parts[1]:\n",
                    "                    keywords = [k.strip() for k in parts[1].split(',') if k.strip()]\n",
                    "                else:\n",
                    "                    if ',' in content:\n",
                    "                        keywords = [k.strip() for k in content.split(',') if k.strip()]\n",
                    "                    else:\n",
                    "                        keywords = [k.strip() for k in content.splitlines() if k.strip()]\n",
                    "                if keywords and keywords[0].startswith('http'):\n",
                    "                    keywords = keywords[1:]\n",
                    "                if DEBUG:\n",
                    "                    print(f\"[{ds_name}] {folder_name} keywords ({len(keywords)}): {keywords[:5]}\")\n",
                ])
                # skip old lines until after keywords block
                continue
            if in_block:
                # skip until we leave the old block
                if line.strip().startswith('# Parse HTML'):
                    in_block = False
                    new_lines.append(line)
                # else skip
            else:
                new_lines.append(line)
        cell['source'] = new_lines
        changed = True

if changed:
    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
    print('Notebook updated.')
else:
    print('No matching cell found; nothing changed.')
