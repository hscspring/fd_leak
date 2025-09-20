import builtins
import traceback

original_import = builtins.__import__

def traced_import(name, globals=None, locals=None, fromlist=(), level=0):
    stack = "".join(traceback.format_stack(limit=5))
    print(f"Importing {name}, called from:\n{stack}")
    return original_import(name, globals, locals, fromlist, level)

builtins.__import__ = traced_import

import sentry_sdk