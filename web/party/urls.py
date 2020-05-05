from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from party.account.views import qr_code_scan, user_detail, event_users_list, UserView, PartyMembers, PositionList
from party.core.utils import STAGING_ENV
from party.core.views import AgreementView, IndexView
from party.event.views import EventViewSet, EventDiscussionsViewSet
from party.locations.views import CityList, DistrictList, RegionList
from party.post.views import PostViewSet, PostImagesViewsSet, PostCommentViewSet, post_favorite
from party.vote.views import QuestionViewSet, vote, QuestionDiscussionsViewSet, UserQuestionDiscussionsList
from rest_framework_swagger.views import get_swagger_view
from django.conf import settings
from django.urls import include, path  # For django versions from 2.0 and up

schema_view = get_swagger_view(title='KG7 API')

router = DefaultRouter()
router.register('post', PostViewSet)
router.register('post_comments', PostCommentViewSet)
router.register('post_images', PostImagesViewsSet)
router.register('users', UserView)
router.register('event', EventViewSet)
router.register('event_discussions', EventDiscussionsViewSet)
router.register('question', QuestionViewSet)
router.register('question_discussions', QuestionDiscussionsViewSet)

urlpatterns = [
    path('qr_code/<int:pk>/', qr_code_scan, name='qr_code'),
    path('event/<int:pk>/users/list/', event_users_list, name='event_visits_list'),
    path('user/detail/<int:pk>/', user_detail, name='user_detail'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('party.api_auth.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/vote/', vote),
    path('api/v1/post_favorite/', post_favorite),
    path('api/v1/party_members/', PartyMembers.as_view()),
    path('api/v1/positions', PositionList.as_view()),
    path('api/v1/citys', CityList.as_view()),
    path('api/v1/districts', DistrictList.as_view()),
    path('api/v1/regions', RegionList.as_view()),
    path('api/v1/user_question_discussions', UserQuestionDiscussionsList.as_view()),
    path('agreement/', AgreementView.as_view()),
    path('', IndexView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# docs will be available only in staging and locally
if settings.ENV == STAGING_ENV or settings.DEBUG:
    urlpatterns.append(
        path('api/v1/docs/', schema_view),
    )

    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns