""" Written by Brian Hou for CSE571: Probabilistic Robotics (Winter 2019)
"""

import numpy as np

from utils import minimized_angle


class ExtendedKalmanFilter:
    def __init__(self, mean, cov, alphas, beta):
        self.alphas = alphas
        self.beta = beta

        self._init_mean = mean
        self._init_cov = cov
        self.reset()

    def reset(self):
        self.mu = self._init_mean
        self.sigma = self._init_cov

    def update(self, env, u, z, marker_id):
        """Update the state estimate after taking an action and receiving a landmark observation."""
        
        # Step 1: Predict the next mean state using the motion model
        mu_bar = env.forward(self.mu, u)  # predicted mean
        G = env.G(self.mu, u)             # Jacobian w.r.t. state
        V = env.V(self.mu, u)             # Jacobian w.r.t. control
        M = env.noise_from_motion(u, self.alphas)  # motion noise

        # Predict covariance
        sigma_bar = G @ self.sigma @ G.T + V @ M @ V.T

        # Step 2: Predict the observation based on predicted state
        z_hat = env.observe(mu_bar.ravel(), marker_id)

        # Step 3: Compute the Jacobian of the observation model
        H = env.H(mu_bar.ravel(), marker_id)

        # Step 4: Compute the innovation (observation residual)
        innovation = z - z_hat
        innovation[0] = minimized_angle(innovation[0])  # Normalize angle

        # Step 5: Compute the innovation covariance
        S = H @ sigma_bar @ H.T + self.beta

        # Step 6: Kalman gain
        K = sigma_bar @ H.T @ np.linalg.inv(S)

        # Step 7: Update mean and covariance
        mu_new = mu_bar + K @ innovation
        sigma_new = sigma_bar - K @ S @ K.T

        self.mu = mu_new
        self.sigma = sigma_new

        return self.mu, self.sigma



