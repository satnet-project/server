from django.core.validators import RegexValidator
from django.db import models

from accounts.models import UserProfile

"""
This module contains all the database models for the configuration of the
spacecraft, ground stations and channels.

There is a set of 'base' models that are designed for containing the different
options for the configuration requirements of communications channels. Their
name is ended with 'Options'. This way, users may add new options for
modulations, bitrates and bandwidth as soon as they are needed. Polarization 
options may remain fixed to 'Any', 'LHCP' or 'RHCP' at least for the first
releases.

TODO :: incompatibilities in between modulation fields.    

:Author:
    Ricardo Tubio-Pardavila (rtubiopa@calpoly.edu)
"""

class GroundStationConfigurationManager(models.Manager):
    """
    Manager for the Ground Station Configuration objects.
    """
    
    def get_groundstation_channels(self, groundstation_pk):
        
        gs_ch = GroundStationChannels\
                    .objects.get(groundstation=groundstation_pk)
        ch_list = []
        
        for gs_ch_i in gs_ch:
            
            gs_i = gs_ch_i.groundstation
            ch_i = gs_ch_i.channel
            ch_list.append(GroundStationChannel.objects.get(pk=ch_i))
        
        return ch_list

class AvailableModulations(models.Model):
    """
    This class permits the storage in the database of the modulation options 
    for creating communication channels. This way, the modulation field of a 
    Channel object must be filled only with data from this model.
    
    MODULATION_CHOICES = (
        ('AFSK', 'Audio Frequency-Shift Keying (AFSK)'),
        ('FSK', 'Frequency-Shift Keying (FSK)'),
        ('GMSK', 'Gaussian Minimum Shift Keying (GMSK)'),
    )
    """

    modulation = models.CharField('Modulation', max_length=4)

class AvailableBitrates(models.Model):
    """
    This class permits the storage in the database of the bitrate options
    for creating communication channels. This way, the bitrate field of a 
    Channel object must be filled only with data from this model.
    
    BITRATE_CHOICES = (
        (300, '300 bps'),
        (600, '600 bps'),
        (900, '900 bps'),        
    )
    
    """

    bitrate = models.IntegerField('Bitrate (bps)')
    
class AvailableBandwidths(models.Model):
    """
    This class permits the storage in the database of the bandwidth options
    for creating communication channels. This way, the bandwidth field of a 
    Channel object must be filled only with data from this model.
    
    BANDWIDTH_CHOICES = (
        (12500.000, '12500 Hz'),
        (25000.000, '25000 Hz'),        
    )
    
    """

    bandwidth = models.DecimalField('Bandwidth (Hz)', max_digits=9, \
                                        decimal_places=3)

class AvailablePolarizations(models.Model):
    """
    This class permits the storage in the database of the bandwidth options
    for creating communication channels. This way, the bandwidth field of a 
    Channel object must be filled only with data from this model.
    """
    
    POLARIZATION_CHOICES = (
        ('Any', 'Any polarization type'),
        ('RHCP', 'RHCP polarization'),
        ('LHCP', 'LHCP polarization'),
    )

    polarization = models.CharField('Polarization modes', \
                                        max_length=4, \
                                        choices=POLARIZATION_CHOICES)

class SpacecraftChannel(models.Model):
    """
    This class models the database model for a spacecraft communications 
    channel.
    """
    
    identifier = models.CharField('Unique identifier', \
                                    max_length=30, \
                                    unique=True, \
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9.-_]*$',
                message="Channel identifier must be Alphanumeric, with '.-_'",
                code='invalid_channel_identifier'
            ),
        ]
    )
    
    modulation = models.ForeignKey(AvailableModulations)
    bitrate = models.ForeignKey(AvailableBitrates)
    bandwidth = models.ForeignKey(AvailableBandwidths)
    polarization = models.ForeignKey(AvailablePolarizations)
    
    # In Hz, mili-Hz resolution, up to 1 EHz, central frequency
    frequency = models.DecimalField('Central frequency (Hz)', \
                                        max_digits=15, decimal_places=3)


class GroundStationChannel(models.Model):
    """
    This class models the database model for a ground station communications 
    channel.
    """
    
    
    identifier = models.CharField('Unique identifier', \
                                    max_length=30, \
                                    unique=True, \
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9.-_]*$',
                message="Channel identifier must be Alphanumeric, with '.-_'",
                code='invalid_channel_identifier'
            ),
        ]
    )
    
    modulation = models.ForeignKey(AvailableModulations)
    bitrate = models.ForeignKey(AvailableBitrates)
    bandwidth = models.ForeignKey(AvailableBandwidths)
    polarization = models.ForeignKey(AvailablePolarizations)
    
    min_frequency_range = models.DecimalField('Minimum frequency (Hz)', \
                                                max_digits=15, \
                                                decimal_places=3)
    max_frequency_range = models.DecimalField('Maximum frequency (Hz)', \
                                                max_digits=15, \
                                                decimal_places=3)
    
    enabled = models.BooleanField('Enabled')

class SpacecraftConfiguration(models.Model):
    """
    This class models the configuration required for managing any type of
    spacecraft in terms of communications and pass simulations.
    """
    
    user = models.ForeignKey(UserProfile)
    
    identifier = models.CharField('Identifier', \
                                    max_length=30, \
                                    unique=True, \
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9.\-_]*$',
                message="Segment identifier must be Alphanumeric, with '.-_'",
                code='invalid_segment_identifier'
            ),
        ]
    )
    
    callsign = models.CharField('Callsign', max_length=10, \
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9]*$',
                message='Callsign must be Alphanumeric',
                code='invalid_callsign'
            ),
        ]
    )
    
    celestrak_id = models.CharField('Celestrak identifier', max_length=100)

class GroundStationConfiguration(models.Model):
    """
    This class models the configuration required for managing a generic ground
    station, in terms of communication channels and pass simulations.
    """

    user = models.ForeignKey(UserProfile)
    
    identifier = models.CharField('Identifier', \
                                    max_length=30, \
                                    unique=True, \
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9.\-_]*$',
                message="Segment identifier must be Alphanumeric, with '.-_'",
                code='invalid_segment_identifier'
            ),
        ]
    )
    
    callsign = models.CharField('Callsign', max_length=10, \
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9]*$',
                message='Callsign must be Alphanumeric',
                code='invalid_callsign'
            ),
        ]
    )
    
    contact_elevation \
        = models.DecimalField('Contact elevation (degrees)', \
                                    max_digits=4, decimal_places=2)

    longitude = models.FloatField()
    latitude = models.FloatField()

class SpacecraftChannels(models.Model):
    """
    This model contains the relationship in between Spacecraft and the Channels
    that they implement.
    """

    spacecraft = models.ForeignKey(SpacecraftConfiguration)
    channel = models.ForeignKey(SpacecraftChannel)

class GroundStationChannels(models.Model):
    """
    This model contains the relationship in between Ground Stations and the 
    Channels that they implement.
    """

    ground_station = models.ForeignKey(GroundStationConfiguration)
    channel = models.ForeignKey(GroundStationChannel)

class SlotsAvailable(models.Model):
    """
    This model describes the start and ending for a given slot.
    """

    initial_date = models.DateField('Initial date for the available slot')
    final_date = models.DateField('Final date for the available slot')

