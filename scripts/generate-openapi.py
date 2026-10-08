#!/usr/bin/env python3
"""Write openapi.json from the FastAPI application without starting a server."""

import json
import os
import sys


def main() -> None:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    api_path = os.path.join(project_root, 'apps', 'api')
    sys.path.insert(0, api_path)

    from app.main import app

    output_path = os.path.join(project_root, 'openapi.json')
    with open(output_path, 'w', encoding='utf-8') as output:
        json.dump(app.openapi(), output, indent=2, ensure_ascii=False)
        output.write('\n')
    print(f'OpenAPI schema written to {output_path}')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'Failed to generate OpenAPI schema: {exc}', file=sys.stderr)
        print('Set JWT_SECRET_KEY before generating the schema. See .env.example.')
        sys.exit(1)
