#!/usr/bin/env python3
"""
run_sql.py (Root entrypoint)
Calls python/run_sql.py
"""
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(base_dir, 'python', 'run_sql.py')
with open(script_path, 'r', encoding='utf-8') as f:
    code = f.read()
exec(compile(code, script_path, 'exec'), {'__file__': script_path, '__name__': '__main__'})
