from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    latitude = serializers.CharField(
        required=True,
        error_messages={'required': 'invalid latitude parameter',
                        'blank': 'invalid latitude parameter'})

    longitude = serializers.CharField(
        required=True,
        error_messages={'required': 'invalid longitude parameter',
                        'blank': 'invalid longitude parameter'})
