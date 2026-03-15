import gc
collected = gc.collect()
print(f"Garbage collector: collected {collected} objects")

import re
re.purge()
print("Regex cache purged")