import torch

class BallisticSimulatedBifurcation:
    """
    State-of-the-art Ballistic Simulated Bifurcation (bSB) algorithm (Goto 2021).
    Outperforms standard greedy heuristics for Max-Cut and QUBO.
    """
    def __init__(self, steps=1000, dt=1.0, device='cpu'):
        self.steps = steps
        self.dt = dt
        self.device = torch.device(device)

    def solve(self, J, batch_size=16):
        N = J.shape[0]
        J_tensor = torch.tensor(J, dtype=torch.float32, device=self.device)
        
        # Auto-tuning constants
        # In bSB, we normalize J by its max eigenvalue or spectral radius
        # For speed, we estimate it with the maximum row sum
        row_sums = torch.sum(torch.abs(J_tensor), dim=1)
        J_norm = torch.max(row_sums)
        if J_norm > 0:
            J_tensor = J_tensor / J_norm
            
        a0 = 1.0
        c0 = 1.0
        
        x = (torch.rand((batch_size, N), device=self.device) * 0.2 - 0.1)
        y = (torch.rand((batch_size, N), device=self.device) * 0.2 - 0.1)
        
        a_t = torch.linspace(0, 1.0, self.steps, device=self.device)
        
        for i in range(self.steps):
            a = a_t[i]
            
            # Matrix mult for interactions
            interactions = torch.matmul(x, J_tensor)
            
            # bSB differential equations
            dy = -(a0 - a) * x + c0 * interactions
            y = y + dy * self.dt
            
            # The ballistic variant applies a hard wall limit instead of c*x^3
            dx = y
            x = x + dx * self.dt
            
            # Hard wall: limit x to [-1, 1], if it hits the wall, kill momentum
            mask_out_bounds = torch.abs(x) > 1.0
            x = torch.clamp(x, -1.0, 1.0)
            y[mask_out_bounds] = 0.0

        spins = torch.sign(x)
        energies = -0.5 * torch.sum(spins * torch.matmul(spins, J_tensor), dim=1)
        best_idx = torch.argmin(energies)
        
        return spins[best_idx].cpu().numpy(), energies[best_idx].item()
