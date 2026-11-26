# Evaluation Fixture (Vault): Neural Networks — Existing Notes & Weak Areas

*Controlled evaluation vault fixture for Eval Case 38 (`revision-strategy` & `revision-pack` without fabricated quiz history).*

## Covered Vault Sections (`[[Neural Networks]]`)

- `[[Neural Networks#Forward Pass & Linear Layers]]`: Matrix multiplication $\mathbf{z}^{[l]} = W^{[l]}\mathbf{a}^{[l-1]} + \mathbf{b}^{[l]}$ and non-linear activation $\mathbf{a}^{[l]} = g(\mathbf{z}^{[l]})$.
- `[[Neural Networks#Backpropagation & Chain Rule]]`: Local Jacobian propagation $\delta^{[l]} = (W^{[l+1]\top}\delta^{[l+1]}) \odot g'(\mathbf{z}^{[l]})$.
- `[[Neural Networks#Vanishing Gradients]]`: Saturation of sigmoid/tanh derivatives when $|\mathbf{z}|$ grows large vs. ReLU constant slope on $z > 0$.

## Documented Weak Areas (User-Recorded Only — No Historical Quiz Scores Recorded)

- **Backpropagation shape tracking:** Confusion between multiplying by $W^{[l+1]}$ vs. $W^{[l+1]\top}$ across layer dimensions.
- **ReLU dead-neuron boundary:** Uncertainty about why learning rates that are too large can push pre-activations permanently negative.

*(There are no past quiz scores, mastery percentages, or timestamps recorded in this vault.)*
