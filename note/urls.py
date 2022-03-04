from . import views
from django.urls import path

urlpatterns=[
    path('add',views.add_note),
    path('list_note',views.list_note),
    path('page_note/<int:note_id>',views.page_note)
]