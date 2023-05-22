from django.urls import path
from . import views
from .views import SalesCreateView, SalesUpdateView, SalesDeleteView, Sales, SalesRecordCreateView,\
SalesRecordUpdateView, SalesRecordDeleteView, TestimonialDeleteView, TestimonialUpdateView, TestimonialCreateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Sales, name='home'),
    #path('', views.Sales.as_view(), name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="logout.html"), name='logout'),
path('sales/new/', SalesCreateView.as_view(), name='create-sales'),
path('sales/<int:pk>/update/', SalesUpdateView.as_view(), name='update-sales'),
path('sales/<int:pk>/delete/', SalesDeleteView.as_view(), name='delete-sales'),
path('sales/<int:pk>/detail/', views.salesDetail, name='sales-detail'),
path('search/', views.search, name='search'),
path('sales/<str:pk>/detail-record/', views.salesRecordsDetail, name='salesRecord-detail'),
path('sales/new/record', SalesRecordCreateView.as_view(), name='create-salesRecord'),
path('sales/<int:pk>/update-record/', SalesRecordUpdateView.as_view(), name='update-salesRecord'),
path('sales/<int:pk>/delete-record/', SalesRecordDeleteView.as_view(), name='delete-salesRecord'),
path('testimony/<str:pk>/testimony-detail/', views.testimonialDetail, name='testimony-detail'),
path('testimony/new/', TestimonialCreateView.as_view(), name='create-testimony'),
path('testimony/<int:pk>/update-testimony/', TestimonialUpdateView.as_view(), name='update-testimony'),
path('testimony/<int:pk>/delete-testimony/', TestimonialDeleteView.as_view(), name='delete-testimony'),
path('like-sale/', views.like_sale, name='like-sale'),
path('sale-message/<str:pk>/', views.messageSale, name="sale"),
path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
path('update-message/<str:pk>/', views.updateMessage, name="update-message")
]