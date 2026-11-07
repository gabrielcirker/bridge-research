# Bridge Geometry Comparison

This project compares three equal-mass beam sections using Euler–Bernoulli finite elements. A midpoint transverse load gives deflection, and a separate axial load case gives an ideal elastic buckling load. The hollow section uses a larger outer envelope than the baseline so that it has a real cavity at equal mass.

The 80-element results are 0.977, 0.281 and 0.688 mm maximum deflection for the solid, hollow and tapered sections, respectively. The corresponding axial buckling loads are 210.6, 730.5 and 276.7 kN. These are idealized comparisons, not a practical bridge design or a global optimization. See the paper for the model assumptions and numerical checks.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/bridge_model.py
```
