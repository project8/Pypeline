try:
    from check_pulse import check_pulse  # fix this to work on python3
except ImportError:
    from check_pulse import check_pulse
from dpph_lockin import dpph_lockin
from run_mantis import run_mantis
