from gheat import pil_ as backend, color_schemes, MAX_ZOOM, dots, fspath, \
  ALWAYS_BUILD
from google.appengine.ext import webapp
from os import environ
import logging

log = logging.getLogger('heat_tile')

class MainPage(webapp.RequestHandler):

  def get(self):
    path = environ['PATH_INFO']

    log.debug("Path:" + path)
    if path.endswith('.png') and 'empties' not in path: 
        # let people hit empties directly if they want; why not?

        # Parse and validate input.
        # =========================
        # URL paths are of the form:
        #
        #   /<color_scheme>/<zoom>/<x>,<y>.png
        #
        # E.g.:
        #
        #   /classic/3/0,1.png

        raw = path[:-4] # strip extension
        try:
            assert raw.count('/') == 3, "%d /'s" % raw.count('/')
            foo, color_scheme, zoom, xy = raw.split('/')
            assert color_scheme in color_schemes, ("bad color_scheme: "
                                                  + color_scheme
                                                   )
            assert xy.count(',') == 1, "%d /'s" % xy.count(',')
            x, y = xy.split(',')
            assert zoom.isdigit() and x.isdigit() and y.isdigit(), "not digits"
            zoom = int(zoom)
            x = int(x)
            y = int(y)
            assert 0 <= zoom <= (MAX_ZOOM - 1), "bad zoom: %d" % zoom
        except AssertionError, err:
            log.warn(err.args[0])
            self.response.headers["Content-Type"] = 'text/plain'
            self.response.set_status(400, "Bad Request  (%s)" % err)
            return

        # Build and save the file.
        # ========================
        # The tile that is built here will be served by the static handler.

        color_scheme = color_schemes[color_scheme]
        tile = backend.Tile(color_scheme, dots, zoom, x, y, fspath)
        if tile.is_empty():
            log.info('serving empty tile %s' % path)
            fspath = color_scheme.get_empty_fspath(zoom)
        elif tile.is_stale() or ALWAYS_BUILD:
            log.info('rebuilding %s' % path)
            tile.rebuild()
            tile.save()
        else:
            log.info('serving cached tile %s' % path)


    #environ['PATH_TRANSLATED'] = fspath
    #return static_handler(environ, start_response)


def main():
    application = webapp.WSGIApplication(
        [('/(.*)/(.*)/(.*).png', MainPage)],
        debug=True)


if __name__ == "__main__":
  main()

