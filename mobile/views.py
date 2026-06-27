from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .builders.mobile_resource_builder import MobileResourceBuilder


class MobileResourceView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, assignment_id):

        builder = MobileResourceBuilder(
            request.user,
            assignment_id
        )

        return Response(builder.build())