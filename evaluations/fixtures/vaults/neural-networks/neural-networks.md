---
id: fixture-vault-neural-networks
aliases:
  - Neural Networks
topic: Neural Networks
tags:
  - domain/ml
  - subject/deep-learning
  - topic/neural-networks
nexttopics: []
---

# Neural Networks

## Forward Pass & Linear Layers
For layer $l$, pre-activations combine incoming activations linearly as $\mathbf{z}^{[l]} = W^{[l]}\mathbf{a}^{[l-1]} + \mathbf{b}^{[l]}$, followed by elementwise activation $\mathbf{a}^{[l]} = g(\mathbf{z}^{[l]})$. Notice shapes: if $\mathbf{a}^{[l-1]} \in \mathbb{R}^{d_{\text{in}}}$ and $\mathbf{z}^{[l]} \in \mathbb{R}^{d_{\text{out}}}$, then $W^{[l]} \in \mathbb{R}^{d_{\text{out}} \times d_{\text{in}}}$.

## Backpropagation & Chain Rule
To propagate error signals backward from layer $l+1$ to layer $l$, transpose $W^{[l+1]}$ so gradients map back into layer-$l$ dimension:
$$
\delta^{[l]} = \bigl(W^{[l+1]\top}\delta^{[l+1]}\bigr) \odot g'(\mathbf{z}^{[l]})
$$
Parameter gradients follow directly as $\frac{\partial J}{\partial W^{[l]}} = \delta^{[l]}\mathbf{a}^{[l-1]\top}$ and $\frac{\partial J}{\partial \mathbf{b}^{[l]}} = \delta^{[l]}$.

## Vanishing Gradients
Saturating activations ($\sigma(z)$, $\tanh(z)$) produce near-zero derivatives $g'(z) \approx 0$ when $|z|$ grows large, shrinking gradient norms across deep chains. By contrast, $\text{ReLU}(z) = \max(0, z)$ preserves derivative $1$ on $z > 0$; however, large learning rates or negative bias shifts can push pre-activations negative across current training examples, yielding zero activations and gradients on that observed batch (though a unit only remains inactive across the data distribution under those parameters—not irreversibly for every conceivable future input or upstream weight update).
