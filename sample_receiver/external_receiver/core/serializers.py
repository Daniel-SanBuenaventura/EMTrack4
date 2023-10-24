from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    customer = serializers.CharField(max_length=120, allow_null=True, allow_blank=True)
    created = serializers.DateTimeField(default_timezone=None, allow_null=True)
    license_plate = serializers.CharField(
        max_length=40, allow_null=True, allow_blank=True
    )
    fleet_id = serializers.CharField(max_length=64, allow_null=True, allow_blank=True)
    latitude = serializers.FloatField(allow_null=True)
    longitude = serializers.FloatField(allow_null=True)
    event_type = serializers.CharField(max_length=32, allow_null=True, allow_blank=True)
    iso_position = serializers.IntegerField(allow_null=True)
    pressure = serializers.IntegerField(
        help_text='Pressure in Pascals', allow_null=True
    )
    temperature = serializers.IntegerField(
        help_text='Temperature in degrees Celsius', allow_null=True
    )
    mileage = serializers.IntegerField(
        allow_null=True, help_text='Vehicle mileage in kilometers'
    )
    speed = serializers.IntegerField(
        allow_null=True, help_text='Speed in kilometers per hour'
    )
    heading = serializers.IntegerField(allow_null=True)
