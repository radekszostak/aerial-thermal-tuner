import imp
import subprocess
import os
import re
from tqdm import tqdm
def dms2dec(dms):
    d = float(dms[0])
    m = float(dms[1])
    s = float(dms[2])
    return (d+m/60+s/3600)*(-1 if dms[3] in ['W', 'S'] else 1)

