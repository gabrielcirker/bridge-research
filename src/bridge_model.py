"""Compare equal-mass beams using Euler–Bernoulli finite elements."""
from pathlib import Path
import numpy as np
from scipy.linalg import eigh, solve
import matplotlib.pyplot as plt

E, RHO, L, LOAD = 200e9, 7850.0, 1.0, 1000.0
B, H = 0.02, 0.04
AREA = B * H
MASS = RHO * AREA * L


def section(x, geometry):
    if geometry == 'solid':
        return B * H**3 / 12
    if geometry == 'hollow':
        # Larger envelope allows a genuine cavity at the baseline area.
        b, h = 0.04, 0.06
        t = ((b + h) - np.sqrt((b + h)**2 - 4 * AREA)) / 4
        return (b*h**3 - (b-2*t)*(h-2*t)**3) / 12
    if geometry == 'tapered':
        alpha = 0.5
        height = H / (1-alpha/3) * (1-alpha*(2*x/L-1)**2)
        return B * height**3 / 12
    raise ValueError(geometry)


def analyze(geometry, n=80):
    """Pinned ends, midpoint transverse load and separate axial buckling load."""
    if n < 2 or n % 2:
        raise ValueError('n must be an even integer of at least 2')
    dx = L/n
    stiffness = np.zeros((2*n+2, 2*n+2))
    geometric = np.zeros_like(stiffness)
    # Two-point Gauss quadrature integrates the element bending energy.
    for e in range(n):
        ke = np.zeros((4, 4))
        for xi in (0.5 - 1/(2*np.sqrt(3)), 0.5 + 1/(2*np.sqrt(3))):
            curvature = np.array([(-6+12*xi)/dx**2, (-4+6*xi)/dx,
                                  (6-12*xi)/dx**2, (-2+6*xi)/dx])
            ke += E * section((e+xi)*dx, geometry) * np.outer(curvature, curvature) * dx/2
        kg = np.array([[36, 3*dx, -36, 3*dx], [3*dx, 4*dx**2, -3*dx, -dx**2],
                       [-36, -3*dx, 36, -3*dx], [3*dx, -dx**2, -3*dx, 4*dx**2]])/(30*dx)
        ids = np.arange(2*e, 2*e+4)
        stiffness[np.ix_(ids, ids)] += ke
        geometric[np.ix_(ids, ids)] += kg
    free = np.setdiff1d(np.arange(2*n+2), [0, 2*n])
    force = np.zeros(2*n+2)
    force[n] = -LOAD
    displacement = np.zeros(2*n+2)
    displacement[free] = solve(stiffness[np.ix_(free, free)], force[free], assume_a='pos')
    critical = eigh(stiffness[np.ix_(free, free)], geometric[np.ix_(free, free)], subset_by_index=[0, 0], eigvals_only=True)[0]
    return np.linspace(0, L, n+1), displacement[::2], critical


def main():
    root = Path(__file__).resolve().parents[1]
    lines = ['Equal-mass beam comparison (80 elements)', f'Mass: {MASS:.3f} kg']
    for geometry in ('solid', 'hollow', 'tapered'):
        x, y, critical = analyze(geometry)
        lines.append(f'{geometry}: max deflection = {abs(y).max()*1000:.4f} mm; axial critical load = {critical/1000:.3f} kN; load/weight = {critical/(MASS*9.81):.1f}')
        plt.plot(x, y*1000, label=geometry.title())
    print('\n'.join(lines))
    (root/'results'/'results_summary.txt').write_text('\n'.join(lines)+'\n')
    plt.xlabel('Position (m)'); plt.ylabel('Deflection (mm)'); plt.grid(); plt.legend(); plt.tight_layout()
    plt.savefig(root/'figures'/'deflection_plot.png', dpi=150)

if __name__ == '__main__':
    main()
