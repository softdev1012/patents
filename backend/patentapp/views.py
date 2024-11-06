from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import check_patents


class CheckPatentView(APIView):
    def get(self, request):
        patent_id = request.query_params.get('patentId')
        company_name = request.query_params.get('companyName')

        if not patent_id:
            return Response({"message": "patentId is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not company_name:
            return Response({"message": "companyName is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            result = check_patents(patent_id, company_name)
            if result:
                return Response(result)
            else:
                return Response({"message": "Patent not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)