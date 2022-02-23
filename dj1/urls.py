from django.urls import path, reverse_lazy
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'dj1'

urlpatterns = [

          path('signup/', views.signup, name = 'signup'),
          #path('profile_pic/', views.profile_pic, name='profile_pic'),
          
          path('profile/', views.profile, name='profile'),
          path('', views.PostListView.as_view(), name = 'home'),
          path('posts', views.PostListView.as_view(), name = 'all'),
          path('post/create', views.PostCreateView.as_view(success_url = reverse_lazy('dj1:all')), name = 'post_create'),
          path('post/<int:pk>', views.PostDetailView.as_view(), name = 'post_detail'),
          path('post/<int:pk>/update', views.PostUpdateView.as_view(success_url = reverse_lazy('dj1:all')), name = 'post_update'),
          path('post/<int:pk>/delete',views.PostDeleteView.as_view(success_url = reverse_lazy('dj1:all')), name = 'post_delete'),
          
          path('post/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='post_comment_create'),
          path('comment/<int:pk>/delete', views.CommentDeleteView.as_view(success_url = reverse_lazy('dj1')), name = 'post_comment_delete'),
    
    ]
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

