from gheat import pil_ as backend
import logging
import os
import stat

# Logging config
# ==============

level = logging.INFO
logging.basicConfig(level=level) # Ack! This should be in Aspen. :^(
log = logging.getLogger('gheat')

# Configuration
# =============
# Set some things that backends will need.

conf = { 
        '_always_build' : 'no',
        '_build_empties' : 'no',
        }

ALWAYS_BUILD = ('true', 'yes', '1')
ALWAYS_BUILD = conf.get('_always_build', '').lower() in ALWAYS_BUILD

BUILD_EMPTIES = ('true', 'yes', '1')
BUILD_EMPTIES = conf.get('_build_empties', 'true').lower() in BUILD_EMPTIES

#DIRMODE = conf.get('dirmode', '0755')
#DIRMODE = int(eval(DIRMODE))

SIZE = 256 # size of (square) tile; NB: changing this will break gmerc calls!
MAX_ZOOM = 31 # this depends on Google API; 0 is furthest out as of recent ver.


color_schemes = dict()          # this is used below
#_color_schemes_dir = os.path.join(aspen.paths.__, 'etc', 'color-schemes')
_color_schemes_dir = os.path.join('etc', 'color-schemes')

for fname in os.listdir(_color_schemes_dir):
  if not fname.endswith('.png'):
    continue
  name = os.path.splitext(fname)[0]
  fspath = os.path.join(_color_schemes_dir, fname)
  color_schemes[name] = backend.ColorScheme(name, fspath)

def load_dots(backend):
  """Given a backend module, return a mapping of zoom level to Dot object.
  """
  return dict([(zoom, backend.Dot(zoom)) for zoom in range(MAX_ZOOM)])
dots = load_dots(backend) # factored for easier use from scripts



