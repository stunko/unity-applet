#!/usr/bin/python
import os
import sys
from gi.repository import Gtk, GObject
from gi.repository import AppIndicator3 as appindicator
import requests
from collections import namedtuple

# Set constants
Resources = namedtuple('Resources', ("icon", "url", "period"))

resources = Resources(
    os.path.join(os.path.dirname(__file__), "images/flags"),
    'http://www.telize.com/geoip',
    10000)


class IPIndicator:
    def __init__(self):

        self.ind = appindicator.Indicator.new("ip-indicator", "", appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.ind.set_menu(self._setup_menu())
        self.ind.set_icon_theme_path(resources.icon)
    
    def _setup_menu(self):
        menu = Gtk.Menu()

        quit = Gtk.MenuItem('Quit')
        quit.connect("activate", self._quit)
        quit.show()
        menu.append(quit)

        return menu

    @property
    def ip_geo_info(self):
        try:
            req = requests.get(resources.url, timeout=10)
            req.raise_for_status()
            req = req.json()
            res = '{city}:{sep}{ip}'.format(sep=' '*5, **req),  req['country_code'].lower()
        except:
            res = 'No connection with geoip service.', 'index'
        return res

    def _refresh(self):
        ip, flag = self.ip_geo_info
        self.ind.set_icon(flag)
        self.ind.set_label(ip, '')
        GObject.timeout_add(resources.period, self._refresh)

    def main(self):
        self._refresh()
        Gtk.main()

    def _quit(self, widget):
        sys.exit(0)


if __name__ == "__main__":
    indicator = IPIndicator()
    indicator.main()



