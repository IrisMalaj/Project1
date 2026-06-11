from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # Home - Destination list
    path('', views.DestinationListView.as_view(), name='home'),

    # Destination CRUD
    path('destination/<int:pk>/', views.DestinationDetailView.as_view(), name='destination-detail'),
    path('destination/new/', views.DestinationCreateView.as_view(), name='destination-create'),
    path('destination/<int:pk>/update/', views.DestinationUpdateView.as_view(), name='destination-update'),
    path('destination/<int:pk>/delete/', views.DestinationDeleteView.as_view(), name='destination-delete'),

    # Destination comments
    path('destination/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment-delete'),

    # User auth
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),

    # Guides
    path('guides/', views.GuideListView.as_view(), name='guide-list'),
    path('guides/new/', views.GuideCreateView.as_view(), name='guide-create'),
    path('guides/<int:pk>/', views.GuideDetailView.as_view(), name='guide-detail'),
    path('guides/<int:pk>/edit/', views.GuideUpdateView.as_view(), name='guide-update'),
    path('guides/<int:pk>/delete/', views.GuideDeleteView.as_view(), name='guide-delete'),

    # Public Reviews
    path('reviews/', views.ReviewListView.as_view(), name='reviews'),
    path('leave-review/', views.leave_review, name='leave_review'),

    # Guide reviews
    path('guides/<int:pk>/review/', views.add_or_update_guide_review, name='guide-review'),
    path('reviews/<int:pk>/delete/', views.delete_guide_review, name='guide-review-delete'),

    # Guide comments
    path('guides/<int:pk>/comment/', views.add_guide_comment, name='guide-comment-add'),
    path('guide-comments/<int:pk>/edit/', views.edit_guide_comment, name='guide-comment-edit'),
    path('guide-comments/<int:pk>/delete/', views.delete_guide_comment, name='guide-comment-delete'),

    # Guide gallery
    path('guides/<int:pk>/gallery/add/', views.add_guide_image, name='guide-image-add'),
    path('guide-images/<int:pk>/delete/', views.delete_guide_image, name='guide-image-delete'),
]
