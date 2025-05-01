import logging
import subprocess
import sys

# NEW: Regular logger ------------------------------------------------------------
log_filename = "simulation.log"
logger = logging.getLogger("ETC")

if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_filename)
    logger.addHandler(file_handler)

# NEW: Molecule logger ------------------------------------------------------------
molecule_log_filename = "molecules.log"
molecule_logger = logging.getLogger("MoleculeLogger")

if not molecule_logger.handlers:
    molecule_logger.setLevel(logging.DEBUG)
    molecule_file_handler = logging.FileHandler(molecule_log_filename)
    molecule_logger.addHandler(molecule_file_handler)

# NEW: CAC (Citric Acid Cycle) logger --------------------------------------------
cac_log_filename = "cac.log"
CAC_logger = logging.getLogger("CACLogger")

if not CAC_logger.handlers:
    CAC_logger.setLevel(logging.DEBUG)
    cac_file_handler = logging.FileHandler(cac_log_filename)
    CAC_logger.addHandler(cac_file_handler)

# NEW: Glycolysis logger --------------------------------------------
gly_log_filename = "gly.log"
GLY_logger = logging.getLogger("GLYLogger")

if not GLY_logger.handlers:
    GLY_logger.setLevel(logging.DEBUG)
    gly_file_handler = logging.FileHandler(gly_log_filename)
    GLY_logger.addHandler(gly_file_handler)

# Launch terminals
if sys.platform.startswith('linux'):
    subprocess.Popen(["gnome-terminal", "--title=ETC Monitoring Viewer", "--", "tail", "-f", log_filename])
    subprocess.Popen(["gnome-terminal", "--title=Matrix Molecule Stock Viewer", "--", "tail", "-f", molecule_log_filename])
    subprocess.Popen(["gnome-terminal", "--title=TCA Molecule Stock Viewer", "--", "tail", "-f", cac_log_filename])
    subprocess.Popen(["gnome-terminal", "--title=Glycolysis Molecule Stock Viewer", "--", "tail", "-f", gly_log_filename])


open(molecule_log_filename, 'w').close()  # Clears old content
open(cac_log_filename, 'w').close()  # Clears old content
open(log_filename, 'w').close()  # Clears old content
open(gly_log_filename, 'w').close()  # Clears old content

