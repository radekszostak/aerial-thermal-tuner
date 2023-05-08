# Mutliprocessing

import multiprocessing.pool as mpp
def istarmap(self, func, iterable, chunksize=1):
    """starmap-version of imap
    """
    self._check_running()
    if chunksize < 1:
        raise ValueError(
            "Chunksize must be 1+, not {0:n}".format(
                chunksize))

    task_batches = mpp.Pool._get_tasks(func, iterable, chunksize)
    result = mpp.IMapIterator(self)
    self._taskqueue.put(
        (
            self._guarded_task_generation(result._job,
                                          mpp.starmapstar,
                                          task_batches),
            result._set_length
        ))
    return (item for chunk in result for item in chunk)
mpp.Pool.istarmap = istarmap

from multiprocessing import Pool
import tqdm

def multiprocess(func, iterable, n_jobs=6):
    iterable = list(iterable)
    with Pool(n_jobs) as pool:
        for _ in tqdm.tqdm(pool.istarmap(func, iterable),
                        total=len(iterable)):
            pass

# Recreate directory
import os
import shutil
def recreate_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    return path

# Load config
import importlib
def load_config(path):
    spec = importlib.util.spec_from_file_location("CFG", path)
    CFG = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(CFG)
    return CFG