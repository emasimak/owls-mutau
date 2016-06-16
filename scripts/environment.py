# owls-cache imports
from owls_cache.persistent import \
        set_cache_debug as set_persistent_cache_debug
from owls_cache.persistent.caches.redis import RedisPersistentCache

# owls-parallel imports
from owls_parallel.backends.multiprocessing import \
    MultiprocessingParallelizationBackend


# Make it clear that we're in this environment
print('Using mu+tau T&P environment...')

# Enable cache debugging
#set_persistent_cache_debug(True)

# Set the persistent cache
persistent_cache = RedisPersistentCache() 

# Disable the persistent cache
#persistent_cache = None

# Create parallelization backend
#parallelization_backend = MultiprocessingParallelizationBackend(24)
parallelization_backend = MultiprocessingParallelizationBackend(16)
#parallelization_backend = MultiprocessingParallelizationBackend(1)

# Disable parallelization
#parallelization_backend = None
