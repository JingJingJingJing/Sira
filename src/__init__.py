MAJOR = 0
MINOR = 0
MICRO = 1
RELEASE = False

__version__ = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

if not RELEASE and '.dev0' not in __version__:
    __version__ += '.dev0'

__all__ = (
    
)