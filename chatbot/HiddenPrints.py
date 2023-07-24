import sys
import os
import warnings

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, "w")
        # Silence warnings
        warnings.filterwarnings("ignore")
        # Suppress all deprecation warnings
        warnings.filterwarnings("ignore", category=DeprecationWarning)

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._original_stdout
        # Restore warnings
        warnings.resetwarnings()