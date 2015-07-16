# owls-cache imports
from owls_cache.persistent import \
        set_cache_debug as set_persistent_cache_debug
from owls_cache.persistent.caches.redis import RedisPersistentCache

# owls-parallel imports
from owls_parallel.backends.multiprocessing import \
    MultiprocessingParallelizationBackend


# Make it clear that we're in this environment
print('Using Ohman\'s environment...')

# Enable cache debugging
#set_persistent_cache_debug(True)

# Set the persistent cache
persistent_cache = RedisPersistentCache(
    #unix_socket_path='/home/ohman/src/owls/cache.sock',
)

# Disable the persistent cache
#persistent_cache = None

# Create parallelization backend
parallelization_backend = MultiprocessingParallelizationBackend(24)

# Disable parallelization
#parallelization_backend = None
