# numexpr imports
import numexpr as ne

# owls-cache imports
from owls_cache.transient import set_cache_debug as set_transient_cache_debug
from owls_cache.persistent import set_cache_debug as set_persistent_cache_debug
from owls_cache.persistent.caches.redis import RedisPersistentCache

# owls-parallel imports
from owls_parallel.backends.multiprocessing import \
    MultiprocessingParallelizationBackend


# Make it clear that we're in this environment
print('Using Ohman\'s environment...')

# Set the maximum number of threads that a single evaulator process can use
# NOTE: This needs to be done before creating the parallelization backend so
# that the setting is fork()'d properly
ne.set_num_threads(1)

# Enable cache debugging
# set_transient_cache_debug(True)
# set_persistent_cache_debug(True)

# Set the persistent cache
persistent_cache = RedisPersistentCache(
    unix_socket_path='/home/howard/.cache.sock'
)

# Create parallelization backend
parallelization_backend = MultiprocessingParallelizationBackend(4)

# Disable parallelization
# parallelization_backend = None
