# chimera - observatory automation system
# Copyright (C) 2006-2007  P. Henrique Silva <henrique@astro.ufsc.br>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

from chimera.core.chimeraobject import ChimeraObject
from chimera.interfaces.weatherstation import WeatherStation

import astropy.units as units


class WeatherBase(ChimeraObject, WeatherStation):

    def __init__(self):
        ChimeraObject.__init__(self)

        self._supports = {}

    def _convert_units(self, value, unit_in, unit_out, equivalencies=None):
        if unit_in == unit_out:
            return value

        return (value * unit_in).to(unit_out, equivalencies).value

    def supports(self, feature=None):
        if feature in self._supports:
            return self._supports[feature]
        else:
            self.log.info("Invalid feature: %s" % str(feature))
            return False

    def humidity(self, unit_out=units.pct):
        raise NotImplementedError()

    def temperature(self, unit_out=units.Celsius):
        raise NotImplementedError()

    def wind_speed(self, unit_out=units.meter/units.second):
        raise NotImplementedError()

    def wind_direction(self, unit_out=units.degree):
        raise NotImplementedError()

    def dew_point(self, unit_out=units.Celsius):
        raise NotImplementedError()

    def pressure(self, unit_out=units.cds.mmHg):
        raise NotImplementedError()

    def rain(self, unit_out=units.liter / units.hour):
        raise NotImplementedError()

    def getMetadata(self, request):
        #TODO: Check if metadata parameter is implemented or not.
        return [('METMODEL', str(self['model']), 'Weather station Model'),
                ('METRH', str(self.humidity().value), '[%] Weather station relative humidity'),
                ('METTEMP', str(self.temperature().value), '[degC] Weather station temperature'),
                ('METWINDS', str(self.wind_speed().value), '[m/s] Weather station wind speed'),
                ('WINDDIR',  str(self.wind_direction().value), '[deg] Weather station wind direction'),
                ('METDEW',  str(self.dew_point().value), '[degC] Weather station dew point'),
                ('METPRES', str(self.pressure().value), '[hPa] Weather station air pressure'),
                ('METRAIN', str(self.rain().value), 'Weather station rain indicator'),
                ]