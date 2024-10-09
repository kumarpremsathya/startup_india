
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_502_BAD_GATEWAY,
    HTTP_401_UNAUTHORIZED
    
)

from sui_api.models import *
from datetime import datetime

import re
from django.http import Http404





class Custom404View(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"result": "Resource not found"}, status=HTTP_404_NOT_FOUND)

def validate(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except:
        return False

class GetOrderdateView(APIView):

    
    def get(self, request):
        try:
            limit = int(request.GET.get('limit', 10))
            offset = int(request.GET.get('offset', 0))
        except ValueError:
            return Response({"result": "Invalid limit or offset value, must be an integer"}, status=HTTP_422_UNPROCESSABLE_ENTITY)

        date = str(request.GET.get('date', None))
        

        if date:

            if not validate(date):
                return Response({"result": "Please enter date or Incorrect date format, should be YYYY-MM-DD"}, status=HTTP_422_UNPROCESSABLE_ENTITY)
            valid_parameters = {'limit', 'offset', 'date'}
            provided_parameters = set(request.GET.keys())

            if not valid_parameters.issuperset(provided_parameters):
                return Response({"result": "Invalid query parameters, check spelling for given parameters"}, status=HTTP_400_BAD_REQUEST)

            try:
                
                order_details = sui_api.objects.filter(dateofScrapping__startswith=date).values('sr_no', 'DPIIT', 'companyName', 'stage', 'focusIndustry', 'focusSector', 'serviceArea', 'location', 'noOfYear', 'companyURL', 'aboutDetails', 'joinedDate', 'DPIITRecognised', 'activeSince','pageurl','Updated_date','dipp_number','legalName','cin','pan', 'company_availability_status','dateofScrapping')[offset:limit]
                total_count = sui_api.objects.filter(dateofScrapping__startswith=date).count()
                for entry in order_details:
                    for key, value in entry.items():
                        if value == "":
                            entry[key] = "Null"
                if len(order_details) > 0:
                    return Response({"result": order_details,'total_count': total_count},  status=HTTP_200_OK)
                else:
                    return Response({"result": "No Data Provided in your specific date!!!."}, status=HTTP_401_UNAUTHORIZED)
            except TimeoutError:
                return Response({"result": "timeout error"}, status=HTTP_502_BAD_GATEWAY)
            except Exception as err:
                return Response({"result": f"An internal server error occurred: {err}"}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            raise Http404("Page not found")