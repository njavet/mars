import json
import tomli


def update_package_json_version():
    new_version = get_poetry_version()
    with open('frontend/package.json') as f:
        package = json.load(f)
    package['version'] = new_version
    with open('frontend/package.json', 'w') as f:
        json.dump(package, f, indent=2)
        f.write('\n')


def get_poetry_version():
    with open('pyproject.toml', 'rb') as f:
        data = tomli.load(f)
    version = data.get('project')['version']
    return version


if __name__ == '__main__':
    update_package_json_version()
