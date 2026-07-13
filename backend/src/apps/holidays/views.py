from datetime import date

from requests.exceptions import RequestException
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import services
from .serializers import HolidaySerializer


class HolidaysView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        year = request.query_params.get("year", date.today().year)
        try:
            year = int(year)
        except ValueError:
            return Response({"year": "Ano inválido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            holidays = services.get_national_holidays(year)
        except RequestException:
            return Response(
                {"detail": "Não foi possível consultar a API de feriados no momento."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        serializer = HolidaySerializer(holidays, many=True)
        return Response(serializer.data)
