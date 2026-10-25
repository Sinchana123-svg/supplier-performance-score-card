#!/usr/bin/env python3
"""
create_db.py (Root entrypoint)
Calls python/create_db.py
"""
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(base_dir, 'python', 'create_db.py')
with open(script_path, 'r', encoding='utf-8') as f:
    code = f.read()
exec(compile(code, script_path, 'exec'), {'__file__': script_path, '__name__': '__main__'})
