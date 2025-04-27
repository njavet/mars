import tomli


with open('pyproject.toml', 'rb') as f:
    data = tomli.load(f)


version = data.get('project')['version']

with open('frontend/src/js/version.js', 'w') as f:
    f.write(f'export const VERSION = "{version}";\n')

