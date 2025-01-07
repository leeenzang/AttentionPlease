from django.urls import path
from .views import FeedbackProcessingView

urlpatterns = [
    path('process/<int:upload_id>/', FeedbackProcessingView.as_view(), name='feedback-process'),
]