from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from .models import Product
from .serializers import ProductSerializer
from .pagination import StandartResultSetPagination

def index(request):
    return HttpResponse("Магазин")


class ProductList(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


    def list(self, request, shop_id, category_id):        
        queryset = self.queryset
        products = queryset.filter(shop=shop_id, category=category_id)
        page = self.paginate_queryset(products)
        serializer = ProductSerializer(page, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class UpdateProduct(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all() 

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


    def put(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.serializer_class(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Ok")
