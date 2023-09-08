import sys
import os

# Get the absolute path of the parent directory (OptiLayer2)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# Add the parent directory to the Python path
sys.path.append(parent_dir)
# Add the OptiReOpt directory to the Python path
sys.path.append(parent_dir + "/OptiReOpt")
