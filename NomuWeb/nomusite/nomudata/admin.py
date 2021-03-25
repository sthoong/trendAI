from django.contrib import admin
from .models import NomuData, RecommendedItem, SimilarClientItem, ClientAttributes


# Register your models here.
admin.site.register(NomuData)
admin.site.register(RecommendedItem)
admin.site.register(SimilarClientItem)
admin.site.register(ClientAttributes)