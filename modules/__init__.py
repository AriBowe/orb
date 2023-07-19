import os, re
mods = [f[:-3] for f in os.listdir('modules') if re.match(r'.*[^__]\.py', f)]
__all__ = mods