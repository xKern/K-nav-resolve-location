from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    latitude = serializers.CharField()
    longitude = serializers.CharField()

    def __validate_cord_field(self, value, field):
        error_str = f"invalid {field} parameter"
        value = value.strip()
        if not len(value):
            raise serializers.ValidationError(error_str)

        try:
            float(value)
        except ValueError:
            raise serializers.ValidationError(error_str)

    def validate_latitude(self, value):
        self.__validate_cord_field(value, 'latitude')

    def validate_longitude(self, value):
        self.__validate_cord_field(value, 'longitude')
