# QuantumLogics

![Banner](https://via.placeholder.com/800x200.png?text=QuantumLogics)

A unified quantum-emulation framework routing quantum capabilities to classical hardware via tensor networks.

## About

QuantumLogics is a modular classical-emulation stack spanning AI, chemistry, cryptography, finance, geometry, optimization, simulation, and systems. It pairs Python modules (`vq-logics-*`) with a Rust core (`vq-logics-engine`) to execute quantum-inspired algorithms on standard hardware.

**Modules:**
- `vq-logics-ai` — Tensor neural networks (`tensor_nn.py`)
- `vq-logics-api` — Service layer (`main.py`)
- `vq-logics-chem` — Tensor VQE (`tensor_vqe.py`)
- `vq-logics-crypto` — LWE cryptography (`lwe_crypto.py`)
- `vq-logics-engine` — Rust core (`Cargo.toml`, `src/lib.rs`)
- `vq-logics-fin` — QAE finance (`qae_finance.py`)
- `vq-logics-geo` — Geo routing (`geo_router.py`)
- `vq-logics-opt` — Benchmark & solvers (`benchmark.py`, `bsb_solver.py`, `maxcut.py`, `sb_solver.py`)
- `vq-logics-sim` — DMRG simulation (`dmrg_sim.py`)
- `vq-logics-sys` — Error correction (`error_correction.py`)

## Installation

```bash
# Python dependencies
pip install -r requirements.txt

# Rust engine
cd vq-logics-engine && cargo build --release

# Docker (optional)
docker-compose up --build
```

## Usage

Run module-specific entry points directly or deploy the full stack via Docker Compose:

```bash
python vq-logics-ai/tensor_nn.py
python vq-logics-opt/maxcut.py
```

Run the UQEOS API server (all 8 pillars over HTTP):

```bash
pip install -r requirements.txt
uvicorn serve:app --host 0.0.0.0 --port 8000
# API docs: http://localhost:8000/docs
```

Note: `vq-logics-api/` is not a valid Python module name (hyphens), so
`serve.py` is the entrypoint shim that loads it for uvicorn.

See individual module directories for inputs, outputs, and benchmarks.

## Repository Structure

```
.
├── vq-logics-ai/        # Tensor NN
├── vq-logics-api/       # API service
├── vq-logics-chem/      # VQE chemistry
├── vq-logics-crypto/    # LWE crypto
├── vq-logics-engine/    # Rust core
├── vq-logics-fin/       # Finance QAE
├── vq-logics-geo/       # Geo router
├── vq-logics-opt/       # Optimization solvers
├── vq-logics-sim/       # DMRG simulation
├── vq-logics-sys/       # Error correction
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## License

See repository root for licensing details.
