# TODO:
# 1. Make Logger Cross-Platform (eg. os.path.join())

import logging
import subprocess
import sys

# Regular logger ------------------------------------------------------------
etc_log_filename = "MET3.5/Logs/ETC.log"
logger = logging.getLogger("ETC")

if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(etc_log_filename)
    logger.addHandler(file_handler)

# Molecule logger ------------------------------------------------------------
molecule_log_filename = "MET3.5/Logs/matrix.log"
molecule_logger = logging.getLogger("MoleculeLogger")

if not molecule_logger.handlers:
    molecule_logger.setLevel(logging.DEBUG)
    molecule_file_handler = logging.FileHandler(molecule_log_filename)
    molecule_logger.addHandler(molecule_file_handler)

# CAC (Citric Acid Cycle) logger --------------------------------------------
cac_log_filename = "MET3.5/Logs/TCA.log"
CAC_logger = logging.getLogger("CACLogger")

if not CAC_logger.handlers:
    CAC_logger.setLevel(logging.DEBUG)
    cac_file_handler = logging.FileHandler(cac_log_filename)
    CAC_logger.addHandler(cac_file_handler)

# Glycolysis logger --------------------------------------------
gly_log_filename = "MET3.5/Logs/glycolysis.log"
GLY_logger = logging.getLogger("GLYLogger")

if not GLY_logger.handlers:
    GLY_logger.setLevel(logging.DEBUG)
    gly_file_handler = logging.FileHandler(gly_log_filename)
    GLY_logger.addHandler(gly_file_handler)

# Cytoplasm logger --------------------------------------------
cyt_log_filename = "MET3.5/Logs/cytoplasm.log"
CYT_logger = logging.getLogger("CYTLogger")

if not CYT_logger.handlers:
    CYT_logger.setLevel(logging.DEBUG)
    cyt_file_handler = logging.FileHandler(cyt_log_filename)
    CYT_logger.addHandler(cyt_file_handler)

# Check if user wants terminals

# Launch terminals
if sys.platform.startswith('linux'):
    subprocess.Popen(["gnome-terminal", "--title=ETC Event Log", "--", "tail", "-f", etc_log_filename])
    subprocess.Popen(["gnome-terminal", "--title=Molecules in the matrix of cell", "--", "tail", "-f", molecule_log_filename])
    subprocess.Popen(["gnome-terminal", "--title=TCA-Related molecules", "--", "tail", "-f", cac_log_filename])
    subprocess.Popen(["gnome-terminal", "--title=Glycolysis-Related molecules", "--", "tail", "-f", gly_log_filename])
    subprocess.Popen(["gnome-terminal", "--title=Molecules in the cytosol of cell", "--", "tail", "-f", cyt_log_filename])


open(molecule_log_filename, 'w').close()  # Clears old content
open(cac_log_filename, 'w').close()  # Clears old content
open(etc_log_filename, 'w').close()  # Clears old content
open(gly_log_filename, 'w').close()  # Clears old content
open(cyt_log_filename, 'w').close()  # Clears old content


