from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import sys
import os
import uvicorn

# Ensure modules can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), '../vq-logics-opt'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../vq-logics-crypto'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../vq-logics-ai'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../vq-logics-chem'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../vq-logics-sim'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../vq-logics-fin'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../vq-logics-geo'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../vq-logics-sys'))

from bsb_solver import BallisticSimulatedBifurcation
from lwe_crypto import run_crypto_keygen
from tensor_nn import run_tensor_ai_inference
from tensor_vqe import run_molecule_simulation
from dmrg_sim import run_dmrg_simulation
from qae_finance import run_amplitude_estimation
from geo_router import run_geo_routing
from error_correction import run_surface_code_emulation

app = FastAPI(
    title="vq-logics: UQEOS 8-Pillar API",
    description="Unified Quantum-Emulation OS routing 32 Quantum Capabilities to Classical Emulation.",
    version="3.0.0"
)

# --- Core 4 Pillars ---

@app.post("/api/v1/opt/maxcut")
async def solve_maxcut(num_nodes: int, edges: list[list[float]]):
    """(1) Opt & Search: Logistics, Manufacturing, Grover-style Optimization"""
    import numpy as np
    J = np.zeros((num_nodes, num_nodes))
    for u, v, w in edges:
        J[int(u), int(v)] = -w
        J[int(v), int(u)] = -w
    solver = BallisticSimulatedBifurcation(dt=1.0, steps=1000, device='cpu')
    spins, energy = solver.solve(J, batch_size=16)
    return {"status": "success", "best_spins": spins.tolist(), "energy": energy}

@app.post("/api/v1/crypto/generate_keys")
async def generate_tensor_keys():
    """(2) Crypto: Post-Quantum Security & Cryptanalysis"""
    return run_crypto_keygen()

@app.post("/api/v1/ai/infer")
async def tensor_ai_infer(prompt_length: int = 256):
    """(3) AI: Tensor-Native LLMs & Discovery"""
    return run_tensor_ai_inference(prompt_length)

@app.post("/api/v1/chem/simulate")
async def simulate_molecule():
    """(4) Chem: Molecular VQE Simulation"""
    return run_molecule_simulation()


# --- New 4 Pillars (Expansion) ---

@app.post("/api/v1/sim/dmrg")
async def physics_simulation(num_sites: int = 10):
    """(5) Sim: Many-body physics and Materials via DMRG"""
    return run_dmrg_simulation(num_sites)

@app.post("/api/v1/fin/montecarlo")
async def finance_simulation():
    """(6) Fin: Quantum-Inspired Monte Carlo Amplitude Estimation"""
    return run_amplitude_estimation()

@app.post("/api/v1/geo/route")
async def geo_routing():
    """(7) Geo: Planetary, Space, and Climate Meta-Routing"""
    return run_geo_routing()

@app.post("/api/v1/sys/emulate_qec")
async def emulate_error_correction():
    """(8) Sys: Surface Code and Error Correction Emulation"""
    return run_surface_code_emulation()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
