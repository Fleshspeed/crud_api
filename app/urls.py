from .views import BookListView, BookDetailView,BookDeleteView,BookUpdateView
from django.urls import path, include
from .views import EmployeeViewSet
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
urlpatterns = [
    path('api/book/', BookListView.as_view(), name='book_list'),
    path('api/book/<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
    path('api/book/delete/<int:book_id>/', BookDeleteView.as_view(), name='book_delete'),
    path('api/book/update/<int:book_id>/', BookUpdateView.as_view(), name='book_update'),
    path('list/', views.list, name='list'),
    path('create/', views.create, name='create'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('api/', include(router.urls)),


    
]





