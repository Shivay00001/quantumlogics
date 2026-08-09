import torch

class LWE_CryptoEngine:
    """
    Post-Quantum Cryptography using Learning With Errors (LWE).
    A trapdoor one-way tensor function resistant to Quantum attacks.
    """
    def __init__(self, n=256, q=3329, device='cpu'):
        self.n = n # dimension of secret
        self.q = q # modulo
        self.device = torch.device(device)

    def keygen(self):
        # Matrix A (Public parameter) (m x n)
        m = self.n * 2
        A = torch.randint(0, self.q, (m, self.n), device=self.device)
        
        # Secret vector S (n x 1)
        S = torch.randint(0, self.q, (self.n, 1), device=self.device)
        
        # Error vector E (small errors)
        E = torch.randint(-2, 3, (m, 1), device=self.device)
        
        # Public key B = (A * S + E) mod q
        B = (torch.matmul(A, S) + E) % self.q
        
        return {"public_key": (A, B), "secret_key": S}

    def encrypt(self, public_key, message_bit):
        A, B = public_key
        m = A.shape[0]
        
        # Random ephemeral vector
        r = torch.randint(0, 2, (m, 1), device=self.device)
        
        # u = A^T * r
        u = torch.matmul(A.T, r) % self.q
        
        # v = B^T * r + message_bit * (q/2)
        encoded_msg = int(message_bit * (self.q // 2))
        v = (torch.matmul(B.T, r) + encoded_msg) % self.q
        
        return (u, v)

def run_crypto_keygen():
    engine = LWE_CryptoEngine()
    keys = engine.keygen()
    return {
        "status": "success",
        "post_quantum_public_key_shape": list(keys['public_key'][0].shape),
        "post_quantum_secret_key_shape": list(keys['secret_key'].shape)
    }
