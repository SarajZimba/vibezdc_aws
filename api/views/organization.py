from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from api.serializers.organization import BranchSerializer, OrganizationSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from datetime import datetime
from organization.models import Branch, Organization


class OrganizationApi(ReadOnlyModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.active()

    def list(self, request, *args, **kwargs):
        instance = Organization.objects.last()
        serializer_data = self.get_serializer(instance).data
        serializer_data['server_date'] = datetime.now().date()
        return Response(serializer_data)


class BranchApi(ReadOnlyModelViewSet):
    serializer_class = BranchSerializer
    queryset = Branch.objects.active().filter(is_central_billing=True)

    authentication_classes = [SessionAuthentication, BasicAuthentication]  # If you want to keep these authentication classes
    permission_classes = [AllowAny]  # Excludes authentication for this view