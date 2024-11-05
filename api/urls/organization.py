from django.urls import path
from api.views.organization import OrganizationApi, BranchApi
from rest_framework import routers

router = routers.DefaultRouter()

router.register("organization", OrganizationApi)
router.register("branch", BranchApi, basename="branch")

urlpatterns = [] + router.urls
