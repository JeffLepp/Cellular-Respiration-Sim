import logging
import subprocess
import sys

# Regular logger
log_filename = "simulation.log"
logger = logging.getLogger("ETC")

if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_filename)
    logger.addHandler(file_handler)

# NEW: Molecule logger
molecule_log_filename = "molecules.log"
molecule_logger = logging.getLogger("MoleculeLogger")

if not molecule_logger.handlers:
    molecule_logger.setLevel(logging.DEBUG)
    molecule_file_handler = logging.FileHandler(molecule_log_filename)
    molecule_logger.addHandler(molecule_file_handler)

# NEW: CAC (Citric Acid Cycle) logger
cac_log_filename = "cac.log"
CAC_logger = logging.getLogger("CACLogger")

if not CAC_logger.handlers:
    CAC_logger.setLevel(logging.DEBUG)
    cac_file_handler = logging.FileHandler(cac_log_filename)
    CAC_logger.addHandler(cac_file_handler)

# Launch terminals
if sys.platform.startswith('linux'):
    subprocess.Popen(["x-terminal-emulator", "-e", f"tail -f {log_filename}"])
    subprocess.Popen(["x-terminal-emulator", "-e", f"tail -f {molecule_log_filename}"])
    subprocess.Popen(["x-terminal-emulator", "-e", f"tail -f {cac_log_filename}"])


open(molecule_log_filename, 'w').close()  # Clears old content
open(log_filename, 'w').close()  # Clears old content
