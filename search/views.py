from search.serializers import SearchSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from search.api.position_stack import PositionStack as map_api
# from search.api.google import GoogleMap as map_api


def parse_error(errors):
    return_ = [errors[i][0] for i in errors]
    return ",".join(return_)


class SearchList(APIView):
    def get(self, request, format=None):
        serializer = SearchSerializer(data=request.GET)

        if not serializer.is_valid():

            return Response({'success': False,
                             'error': parse_error(serializer.errors)},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        cordinates = (serializer.validated_data['latitude'],
                      serializer.validated_data['longitude'])

        mapi = map_api(cordinates=cordinates)
        mapi.work()

        if not mapi.is_okay():
            return Response({'success': False, 'error': mapi.get_error()},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response({'success': False, 'result': mapi.get_results()},
                            status=status.HTTP_200_OK)
