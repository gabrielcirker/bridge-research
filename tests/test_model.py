import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import bridge_model as b

class BeamChecks(unittest.TestCase):
    def test_solid_closed_form(self):
        _, y, p = b.analyze('solid', 40)
        rigidity = b.E*b.section(0, 'solid')
        self.assertAlmostEqual(abs(y).max() / (b.LOAD*b.L**3/(48*rigidity)), 1, places=6)
        self.assertAlmostEqual(p / (np.pi**2*rigidity/b.L**2), 1, places=5)

    def test_taper_mesh_convergence(self):
        _, y40, p40 = b.analyze('tapered', 40)
        _, y80, p80 = b.analyze('tapered', 80)
        self.assertLess(abs(abs(y40).max()/abs(y80).max()-1), 1e-4)
        self.assertLess(abs(p40/p80-1), 1e-4)

if __name__ == '__main__': unittest.main()
