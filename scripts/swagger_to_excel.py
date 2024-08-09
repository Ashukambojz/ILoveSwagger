import json
import yaml
import openpyxl
import sys

def extract_endpoints(swagger_dict):
    endpoints = []
    for path, methods in swagger_dict.get('paths', {}).items():
        for method, details in methods.items():
            endpoints.append({
                'Path': path,
                'Method': method.upper(),
                'Summary': details.get('summary', ''),
                'OperationId': details.get('operationId', '')
            })
    return endpoints

# Load JSON or YAML file
swagger_data = None
if len(sys.argv) > 1:
    json_file_path = sys.argv[1]
    output_excel_path = sys.argv[2]

    if json_file_path.endswith('.json'):
        with open(json_file_path, 'r') as f:
            swagger_data = json.load(f)
    elif json_file_path.endswith(('.yaml', '.yml')):
        with open(json_file_path, 'r') as f:
            swagger_data = yaml.safe_load(f)
    else:
        raise ValueError("Unsupported file format")

    # Extract endpoints
    endpoints = extract_endpoints(swagger_data)

    # Create an Excel workbook and add the extracted endpoints
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "API Endpoints"

    # Headers
    ws.append(['Path', 'Method', 'Summary', 'OperationId'])

    # Add data to Excel sheet
    for endpoint in endpoints:
        ws.append([endpoint['Path'], endpoint['Method'], endpoint['Summary'], endpoint['OperationId']])

    # Save the Excel file
    wb.save(output_excel_path)

    print(f"API endpoints have been extracted and saved to {output_excel_path}")
else:
    print("Please provide the file paths as arguments.")
