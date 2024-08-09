import json
import yaml
import sys

def load_file(file_path):
    with open(file_path, 'r') as file:
        if file_path.endswith('.json'):
            return json.load(file)
        elif file_path.endswith(('.yaml', '.yml')):
            return yaml.safe_load(file)
        else:
            raise ValueError("Unsupported file format")

def save_file(data, file_path):
    with open(file_path, 'w') as file:
        if file_path.endswith('.json'):
            json.dump(data, file, indent=2)
        elif file_path.endswith(('.yaml', '.yml')):
            yaml.safe_dump(data, file, sort_keys=False)
        else:
            raise ValueError("Unsupported file format")

def convert_swagger_to_openapi(swagger):
    openapi = {
        'openapi': '3.0.0',
        'info': {
            'title': swagger['info']['title'],
            'version': swagger['info']['version']
        },
        'paths': swagger['paths'],
        'components': {
            'schemas': swagger.get('definitions', {})
        }
    }
    return openapi

def main(input_file, output_file):
    swagger = load_file(input_file)
    openapi = convert_swagger_to_openapi(swagger)
    save_file(openapi, output_file)
    print(f"Converted Swagger to OpenAPI 3.0 and saved to {output_file}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python swagger_to_v3.py <input_file> <output_file>")
    else:
        main(sys.argv[1], sys.argv[2])
