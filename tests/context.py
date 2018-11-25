import sys
import os
full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print("FULL PATH", full_path)
sys.path.insert(0, full_path)

import libtvdb
