from contextlib import contextmanager
import time

debug = True
glogger = None


@contextmanager
def monitor(name, level=0, debug_single=None, numofbar=80, logger=None):
    if logger is None:
        logger = glogger
    if debug_single or (debug_single is None and debug):
        if level == 0:
            if logger:
                logger.info('-' * numofbar)
            else:
                print('-' * numofbar)
        name = '[' + '-' * level + name + ']'
        if logger:
            logger.info(name)
        else:
            print(name)
        start = time.time()
        yield
        if logger:
            logger.info('{0} finished in {1:.6f} seconds'.format(name, time.time() - start))
        else:
            print('{0} finished in {1:.6f} seconds'.format(name, time.time() - start))
        if level == 0:
            if logger:
                logger.info('-' * numofbar)
            else:
                print('-' * numofbar)
    else:
        yield
