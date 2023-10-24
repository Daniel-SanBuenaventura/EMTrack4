import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from external_receiver.core.serializers import MessageSerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

logger = logging.getLogger(__name__)


class MessageView(APIView):
    permission_classes = [TokenHasReadWriteScope]

    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = request.data
            logger.info(message)
            return Response(data=message, status=status.HTTP_200_OK)
        else:
            logger.info(serializer.errors)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenVerificationView(APIView):
    permission_classes = [TokenHasReadWriteScope]

    def get(self, request, *args, **kwargs):
        return Response(data="Token verified", status=status.HTTP_200_OK)
