# sudoku/urls.py
from django.urls import path
from .views import SudokuView,upload_image

urlpatterns = [
    path('api/sudoku/', SudokuView.as_view(), name='sudoku'),
    path('api/upload/', upload_image, name='upload_image')
]
