from search.serializers import SearchSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from search.api.position_stack import PositionStack as map_api
from search.api.google import GoogleMap as map_api
from xcacher.engine import Engine
from xcacher.errors import ItemNotFoundError

cache = Engine(persistence_path='cache')


def parse_error(errors):
    return_ = [errors[i][0] for i in errors]
    return ",".join(return_)


def respond(data, err, cached):
    response = {}
    if err:
        response['status'] = False
        response['error'] = data
    else:
        response['status'] = True
        response['results'] = data

    response['cached'] = True if cached else False
    return Response(response)


class SearchList(APIView):
    def get(self, request, format=None):
        serializer = SearchSerializer(data=request.GET)

        if not serializer.is_valid():
            return Response({'success': False,
                             'error': parse_error(serializer.errors)},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        cordinates = (serializer.validated_data['latitude'],
                      serializer.validated_data['longitude'])
        key = f'{cordinates[0]}_{cordinates[1]}'

        try:
            item = cache.get(key)
            return respond(item.data, False, True)

        except ItemNotFoundError:
            mapi = map_api(cordinates=cordinates)
            mapi.work()

            if not mapi.is_okay():
                respond(mapi.get_error(), True, False)
            else:
                cache.store(key, mapi.get_results())
                return respond(mapi.get_results(), False, False)
