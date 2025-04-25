from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    ProductWithReviewsSerializer,
    CategoryWithCountSerializer,
    CategoryValidateSerializer,
    ProductValidateSerializer,
    ReviewValidateSerializer
)
from django.db.models import Count
from django.shortcuts import get_object_or_404


class CategoryWithCountListCreateAPIView(APIView):
    def get(self, request):
        categories = Category.objects.annotate(products_count=Count('products'))
        data = CategoryWithCountSerializer(categories, many=True).data
        return Response(data=data)

    def post(self, request):
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = Category.objects.create(**serializer.validated_data)
        return Response(data=CategorySerializer(category).data, status=status.HTTP_201_CREATED)


class CategoryDetailAPIView(APIView):
    def get_object(self, id):
        return get_object_or_404(Category, id=id)

    def get(self, request, id):
        category = self.get_object(id)
        return Response(data=CategorySerializer(category).data)

    def put(self, request, id):
        category = self.get_object(id)
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(data=CategorySerializer(category).data)

    def delete(self, request, id):
        category = self.get_object(id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListCreateAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        data = ProductSerializer(products, many=True).data
        return Response(data=data)

    def post(self, request):
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.objects.create(**serializer.validated_data)
        return Response(data=ProductSerializer(product).data, status=status.HTTP_201_CREATED)


class ProductDetailAPIView(APIView):
    def get_object(self, id):
        return get_object_or_404(Product, id=id)

    def get(self, request, id):
        product = self.get_object(id)
        return Response(data=ProductSerializer(product).data)

    def put(self, request, id):
        product = self.get_object(id)
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category = serializer.validated_data.get('category')
        product.save()
        return Response(data=ProductSerializer(product).data)

    def delete(self, request, id):
        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductWithReviewsAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        data = ProductWithReviewsSerializer(products, many=True).data
        return Response(data=data)


class ReviewListCreateAPIView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data)

    def post(self, request):
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = Review.objects.create(**serializer.validated_data)
        return Response(data=ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


class ReviewDetailAPIView(APIView):
    def get_object(self, id):
        return get_object_or_404(Review, id=id)

    def get(self, request, id):
        review = self.get_object(id)
        return Response(data=ReviewSerializer(review).data)

    def put(self, request, id):
        review = self.get_object(id)
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.product = serializer.validated_data.get('product')
        review.save()
        return Response(data=ReviewSerializer(review).data)

    def delete(self, request, id):
        review = self.get_object(id)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
