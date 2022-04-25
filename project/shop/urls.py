from django.urls import path


from .views import index, ProductList, UpdateProduct


urlpatterns = [
        path('', index),
        path('shops/<int:shop_id>/categories/<int:category_id>/products/',
            ProductList.as_view()),
        path("products/<int:pk>/", UpdateProduct.as_view()),
]
