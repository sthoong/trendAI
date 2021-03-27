from django.shortcuts import render

from .models import ClientAttributes, SimilarClientItem, RecommendedItem

# Create your views here.
def clientAttributeDetail(request, id):
    clientAttrib = ClientAttributes.objects.get(pk=id)
    return render(request, "client.html", {
        'clientAttrib': clientAttrib,
        'clientId': id
    })
