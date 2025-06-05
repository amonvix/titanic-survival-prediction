# prediction/views.py

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from scripts.predict_logic import predict_survival
from django.shortcuts import render

logger = logging.getLogger("prediction")


def form_view(request):
    return render(request, "predict_form.html")


class PredictView(APIView):
    def post(self, request):
        try:
            input_data = request.data
            logger.info(f"Received input: {input_data}")

            result = predict_survival(input_data)
            logger.info(f"Prediction result: {result}")

            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
