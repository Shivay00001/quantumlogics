import torch
import numpy as np

class SimulatedBifurcationSolver:
    """
    Simulated Bifurcation (SB) solver for Ising models and QUBO problems.
    This provides quantum-inspired optimization capabilities on classical hardware.
    """
    def __init__(self, dt=0.1, steps=1000, device='cpu'):
        self.dt = dt
        self.steps = steps
        self.device = torch.device(device)

    def solve_ising(self, J, batch_size=1):
        """
        Solves the Ising model: min H = -0.5 * sum_{i,j} J_{i,j} s_i s_j
        
        Args:
            J: Adjacency matrix representing the Ising interactions (NxN).
               Should be symmetric with zeros on the diagonal.
            batch_size: Number of parallel trajectories to run.
            
        Returns:
            best_spins: The best found spin configuration (shape N).
            best_energy: The energy of the best configuration.
        """
        N = J.shape[0]
        J_tensor = torch.tensor(J, dtype=torch.float32, device=self.device)
        
        # SB Parameters (based on Goto et al.)
        a0 = 1.0
        c = 1.0
        
        # Scale J to ensure stable bifurcation
        # We need c0 * max_eigval(J) ~ 0.5 * a0 to 1.0 * a0
        # For simplicity, we approximate max eigenvalue using row sums
        row_sums = torch.sum(torch.abs(J_tensor), dim=1)
        max_strength = torch.max(row_sums)
        if max_strength == 0:
            c0 = 1.0
        else:
            c0 = 0.5 * a0 / max_strength
            
        J_scaled = c0 * J_tensor
        
        # Initialize position (x) and momentum (p) randomly
        # Shape: (batch_size, N)
        x = (torch.rand((batch_size, N), device=self.device) * 0.2 - 0.1)
        p = (torch.rand((batch_size, N), device=self.device) * 0.2 - 0.1)
        
        # Annealing schedule
        a_t = torch.linspace(0, 1.0, self.steps, device=self.device)
        
        # Symplectic Euler integration
        for i in range(self.steps):
            a = a_t[i]
            
            # dp/dt
            # Matrix-vector multiplication for interactions: J * x^T
            interactions = torch.matmul(x, J_scaled)
            dp = -(a0 - a) * x - c * x**3 + interactions
            
            # Update p
            p = p + dp * self.dt
            
            # Update x
            x = x + p * self.dt
            
            # Optional: Add boundary condition to keep x from exploding (bSB variant)
            # x = torch.clamp(x, -1.0, 1.0)
            
        # Extract spins
        spins = torch.sign(x)
        
        # Calculate energies
        # E = -0.5 * sum_batch (spins @ J @ spins.T)
        energies = -0.5 * torch.sum(spins * torch.matmul(spins, J_tensor), dim=1)
        
        # Find best solution in batch
        best_idx = torch.argmin(energies)
        return spins[best_idx].cpu().numpy(), energies[best_idx].item()

