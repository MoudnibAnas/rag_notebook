from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
import sys
from flask_cors import CORS
import json

app = Flask(__name__, static_folder='frontend/dist')
CORS(app)

# API Routes (must be defined before frontend routes)
@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Simple test endpoint"""
    return jsonify({
        'success': True,
        'message': 'Backend server is working'
    })

@app.route('/api/generate', methods=['POST'])
def generate_debate():
    """Generate debate via API - Full LLM version with Ollama"""
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        
        if not topic:
            return jsonify({
                'success': False,
                'error': 'No topic provided'
            })
        
        # Check if database exists
        if not os.path.exists('chroma_db'):
            return jsonify({
                'success': False,
                'error': 'Database not found. Please run "python create_database.py" first.'
            })
        
        # Run the debate generation script with proper timeout
        cmd = [sys.executable, 'query_debate.py', topic]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout for LLM startup and generation
            )
            
            if result.returncode == 0:
                # Extract just the debate part (skip the header info)
                output_lines = result.stdout.split('\n')
                debate_start = False
                debate_content = []
                
                for line in output_lines:
                    if line.strip() == "="*60 and not debate_start:
                        debate_start = True
                        continue
                    elif debate_start:
                        debate_content.append(line)
                
                debate_text = '\n'.join(debate_content).strip()
                
                return jsonify({
                    'success': True,
                    'result': debate_text
                })
            else:
                return jsonify({
                    'success': False,
                    'error': result.stderr or 'Failed to generate debate'
                })
                
        except subprocess.TimeoutExpired:
            return jsonify({
                'success': False,
                'error': 'Debate generation timed out. Try a simpler topic or check system resources.'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error running debate generator: {str(e)}'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

@app.route('/api/notebooks', methods=['GET'])
def get_notebooks():
    """Get list of notebooks"""
    try:
        # For now, return default notebooks - in a real implementation
        # this would come from a database
        notebooks = [
            {
                'id': 'main',
                'name': 'Main Debate Notebook',
                'description': 'Default notebook for debates',
                'createdAt': '2025-12-27T00:00:00Z',
                'updatedAt': '2025-12-27T00:00:00Z',
                'documentCount': 0,
                'color': '#1a73e8'
            },
            {
                'id': 'research',
                'name': 'Research Papers',
                'description': 'Academic papers and research',
                'createdAt': '2025-12-27T00:00:00Z',
                'updatedAt': '2025-12-27T00:00:00Z',
                'documentCount': 0,
                'color': '#34a853'
            }
        ]
        
        return jsonify({
            'success': True,
            'notebooks': notebooks
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error getting notebooks: {str(e)}'
        })

@app.route('/api/notebooks', methods=['POST'])
def create_notebook():
    """Create a new notebook"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        color = data.get('color', '#1a73e8')
        
        if not name:
            return jsonify({
                'success': False,
                'error': 'Notebook name is required'
            })
        
        # For now, just return the created notebook - in a real implementation
        # this would be saved to a database
        notebook = {
            'id': name.lower().replace(' ', '-'),
            'name': name,
            'description': description,
            'createdAt': '2025-12-27T00:00:00Z',
            'updatedAt': '2025-12-27T00:00:00Z',
            'documentCount': 0,
            'color': color
        }
        
        return jsonify({
            'success': True,
            'notebook': notebook
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error creating notebook: {str(e)}'
        })

@app.route('/api/notebooks/<notebook_id>/documents', methods=['GET'])
def get_notebook_documents(notebook_id):
    """Get documents for a specific notebook"""
    try:
        documents = []
        if os.path.exists('data'):
            for file in os.listdir('data'):
                if file.endswith('.pdf'):
                    file_path = os.path.join('data', file)
                    try:
                        # Try to get file size and basic info
                        size = os.path.getsize(file_path)
                        documents.append({
                            'id': file.replace('.pdf', ''),
                            'name': file,
                            'size': size,
                            'type': 'PDF',
                            'uploadedAt': '2025-12-27T00:00:00Z',
                            'pages': 10  # Mock page count
                        })
                    except:
                        documents.append({
                            'id': file.replace('.pdf', ''),
                            'name': file,
                            'size': 0,
                            'type': 'PDF',
                            'uploadedAt': '2025-12-27T00:00:00Z',
                            'pages': 0
                        })
        
        return jsonify({
            'success': True,
            'documents': documents
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error getting documents: {str(e)}'
        })

@app.route('/api/notebooks/<notebook_id>/documents', methods=['POST'])
def upload_notebook_documents(notebook_id):
    """Upload documents to a specific notebook"""
    try:
        if 'files' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No files provided'
            })
        
        files = request.files.getlist('files')
        uploaded_files = []
        
        # Ensure data directory exists
        if not os.path.exists('data'):
            os.makedirs('data')
        
        for file in files:
            if file.filename.endswith('.pdf'):
                # Save file to data directory
                file_path = os.path.join('data', file.filename)
                file.save(file_path)
                uploaded_files.append(file.filename)
        
        # Regenerate database after upload
        if uploaded_files:
            cmd = [sys.executable, 'create_database.py']
            subprocess.run(cmd, capture_output=True, text=True)
        
        return jsonify({
            'success': True,
            'message': f'Successfully uploaded {len(uploaded_files)} files',
            'files': uploaded_files
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error uploading files: {str(e)}'
        })

@app.route('/api/documents', methods=['GET'])
def get_documents():
    """Get list of documents in the data folder (legacy endpoint)"""
    try:
        documents = []
        if os.path.exists('data'):
            for file in os.listdir('data'):
                if file.endswith('.pdf'):
                    file_path = os.path.join('data', file)
                    try:
                        # Try to get file size and basic info
                        size = os.path.getsize(file_path)
                        documents.append({
                            'name': file,
                            'size': size,
                            'type': 'PDF'
                        })
                    except:
                        documents.append({
                            'name': file,
                            'size': 0,
                            'type': 'PDF'
                        })
        
        return jsonify({
            'success': True,
            'documents': documents
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error getting documents: {str(e)}'
        })

@app.route('/api/upload', methods=['POST'])
def upload_documents():
    """Upload PDF documents"""
    try:
        if 'files' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No files provided'
            })
        
        files = request.files.getlist('files')
        uploaded_files = []
        
        # Ensure data directory exists
        if not os.path.exists('data'):
            os.makedirs('data')
        
        for file in files:
            if file.filename.endswith('.pdf'):
                # Save file to data directory
                file_path = os.path.join('data', file.filename)
                file.save(file_path)
                uploaded_files.append(file.filename)
        
        # Regenerate database after upload
        if uploaded_files:
            cmd = [sys.executable, 'create_database.py']
            subprocess.run(cmd, capture_output=True, text=True)
        
        return jsonify({
            'success': True,
            'message': f'Successfully uploaded {len(uploaded_files)} files',
            'files': uploaded_files
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error uploading files: {str(e)}'
        })

@app.route('/api/create_database', methods=['POST'])
def create_database_endpoint():
    """Create database from uploaded documents"""
    try:
        cmd = [sys.executable, 'create_database.py']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Database created successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': result.stderr or 'Failed to create database'
            })
            
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Database creation timed out'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error creating database: {str(e)}'
        })

# Serve React frontend (must be last)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    print("="*60)
    print("NOTEBOOK LM STYLE RAG DEBATE GENERATOR")
    print("="*60)
    print("Starting backend server...")
    print("Frontend will be served at http://localhost:5000")
    print("API endpoints available at http://localhost:5000/api/")
    print("="*60)
    
    # Build frontend if it exists
    if os.path.exists('frontend'):
        print("Building frontend...")
        os.system('cd frontend && npm run build')
    
    app.run(debug=True, port=5000, host='127.0.0.1')