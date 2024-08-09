from flask import Flask, request, send_file, render_template
import os
import yaml
import openpyxl
from pathlib import Path

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/swagger_to_excel', methods=['POST'])
def swagger_to_excel():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = 'swagger_file.yaml'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        with open(file_path, 'r') as f:
            swagger = yaml.safe_load(f)
        
        endpoints = []
        for path, methods in swagger.get('paths', {}).items():
            for method, details in methods.items():
                endpoints.append({
                    'Path': path,
                    'Method': method.upper(),
                    'Summary': details.get('summary', ''),
                    'OperationId': details.get('operationId', '')
                })
        
        output_excel_path = os.path.join(app.config['UPLOAD_FOLDER'], 'swagger_endpoints.xlsx')
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "API Endpoints"
        ws.append(['Path', 'Method', 'Summary', 'OperationId'])
        for endpoint in endpoints:
            ws.append([endpoint['Path'], endpoint['Method'], endpoint['Summary'], endpoint['OperationId']])
        wb.save(output_excel_path)
        
        return send_file(output_excel_path, as_attachment=True)

@app.route('/swagger_vx_to_v3', methods=['POST'])
def swagger_vx_to_v3():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Call swagger_to_v3.py script (assuming it's in the scripts folder)
        output_file = os.path.join(app.config['UPLOAD_FOLDER'], 'openapi_v3.yaml')
        os.system(f"python3 scripts/swagger_to_v3.py {file_path} {output_file}")
        
        return send_file(output_file, as_attachment=True)

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)
    except Exception as e:
        return f"Error sending file: {str(e)}", 500

if __name__ == "__main__":
    Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
    app.run(debug=True)
