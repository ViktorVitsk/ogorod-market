#!/usr/bin/env python3
import json
import sys
import os
import subprocess
import time
import requests

def generate_openapi():
    print("🚀 Starting OpenAPI generation...")
    
    # Получаем абсолютный путь к проекту
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    api_path = os.path.join(project_root, 'apps', 'api')
    
    # Запускаем API в фоновом режиме
    print("Starting API server...")
    api_process = subprocess.Popen([
        sys.executable, '-m', 'uvicorn', 'app.main:app', 
        '--host', '0.0.0.0', '--port', '8000'
    ], cwd=api_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Ждем пока API запустится
    print("Waiting for API to start...")
    time.sleep(8)
    
    try:
        # Получаем OpenAPI схему через HTTP
        print("Fetching OpenAPI schema...")
        response = requests.get('http://localhost:8000/openapi.json', timeout=10)
        response.raise_for_status()
        
        openapi_schema = response.json()
        
        # Сохраняем в файл
        output_path = os.path.join(project_root, 'openapi.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
        
        print(f"✅ OpenAPI schema generated: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating OpenAPI: {e}")
        print("Make sure PostgreSQL is running: docker compose up -d postgres")
        return False
    finally:
        # Останавливаем API процесс
        print("Stopping API server...")
        api_process.terminate()
        api_process.wait()

if __name__ == "__main__":
    success = generate_openapi()
    sys.exit(0 if success else 1)