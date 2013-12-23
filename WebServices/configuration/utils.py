import urllib2
import logging
logger = logging.getLogger(__name__)

from django.utils import simplejson

__SLO_LAT__ = 35.347099
__SLO_LON__ = -120.455299

def get_remote_user_location(ip=None, \
        geoplugin_ip='http://www.geoplugin.net/json.gp?ip='):
    """
    This method returns the current geolocation of a given IP address by using
    the WebService provided by GeoPlugin. In case no ip address is given, it
    returns None.
    """

    if not ip:
        return None
    
    
    if ip == "127.0.0.1":
        return __SLO_LAT__, __SLO_LON__
    
    try:
    
        json_r = urllib2.urlopen(geoplugin_ip + ip).read()
        r = simplejson.loads(json_r)
        latitude = r['geoplugin_latitude']
        longitude = r['geoplugin_longitude']
        
    except ex:
    
        logging.exception(ex)

    return latitude, longitude

