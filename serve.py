"""
Uvicorn entrypoint for the QuantumLogics UQEOS API.

The API package lives in ``vq-logics-api/`` — a hyphenated directory name,
which is NOT a valid Python module name, so ``uvicorn vq-logics-api.main:app``
can never import it. This shim loads ``vq-logics-api/main.py`` explicitly and
re-exports its ``app``.

Run locally (from repo root, with deps installed):
    uvicorn serve:app --host 0.0.0.0 --port 8000
"""

import importlib.util
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_API_DIR = os.path.join(_HERE, "vq-logics-api")

if _API_DIR not in sys.path:
    sys.path.insert(0, _API_DIR)

_spec = importlib.util.spec_from_file_location(
    "vq_logics_api_main", os.path.join(_API_DIR, "main.py")
)
_api_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_api_module)

app = _api_module.app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("serve:app", host="0.0.0.0", port=8000)
