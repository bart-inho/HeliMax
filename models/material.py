class Material:
    # This class is used to store the material information.

    def __init__(self, eps_r, sigma, mu_r, vel, name):
        self.eps_r = eps_r
        self.sigma = sigma
        self.mu_r = mu_r
        self.vel = vel
        self.name = name

    def __str__(self):
        # Returns the string representation of the Material instance.
        return f"{self.eps_r} {self.sigma} {self.mu_r} {self.vel} {self.name}"