# Bridge Geometry Comparison

**[Project website](https://gabrielcirker.github.io/bridge-research/)** · **[Report](paper/Mathematical%20Optimization%20of%20Lightweight%20Bridge%20Structures.pdf)** · **[Model](src/bridge_model.py)** · **[Research archive](https://gabrielcirker.github.io/bridge-research/archive/)**

This project compares three equal-mass beam sections using Euler–Bernoulli finite elements. A midpoint transverse load gives deflection, and a separate axial load case gives an ideal elastic buckling load. The hollow section uses a larger outer envelope than the baseline so that it has a real cavity at equal mass.

The 80-element results are 0.977, 0.281 and 0.688 mm maximum deflection for the solid, hollow and tapered sections, respectively. The corresponding axial buckling loads are 210.6, 730.5 and 276.7 kN. These are idealized comparisons, not a practical bridge design or a global optimization. See the paper for the model assumptions and numerical checks.

## Project files

- [src/](src/): numerical model and plot generation.
- [paper/](paper/): current report, LaTeX source, and original manuscript.
- [figures/](figures/) and [results/](results/): saved model outputs.
- [tests/](tests/): numerical checks, website links, and archive integrity checks.
- [MODEL_CHECKS.md](MODEL_CHECKS.md): model scope and verification notes.
- [archive/](archive/): historical versions, provenance, and a file manifest.

## Run and check the model

Run these commands from the repository folder with Python 3:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python src/bridge_model.py
python -m unittest discover -s tests -v
```

Running the model regenerates the figure and results summary. The tests compare the solid beam with a closed-form solution, check taper mesh convergence, and validate the website and archive files.

## Website and archive

This is the public presentation repository. The site is a static website served from the root of `main`, with no JavaScript build step. The report can be read inline, opened as a PDF, or read as [plain text](assets/report/report-text.txt).

Historical drafts are preserved in the [research archive](archive/README.md) and are distinct from the current report. Changes to the presentation should preserve the model's assumptions, scientific caveats, and archive provenance.
