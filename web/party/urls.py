from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from party.account.views import qr_code_scan, user_detail, event_users_list, UserView, PartyMembers, PositionList
from party.event.views import EventViewSet, EventDiscussionsViewSet
from party.locations.views import CityList
from party.post.views import PostViewSet, PostImagesViewsSet, PostCommentViewSet, post_favorite
from party.vote.views import QuestionViewSet, vote, QuestionDiscussionsViewSet

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
    path('api/v1/citys', CityList.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
