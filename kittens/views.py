from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Breed, Kitten, Rating
from django.db.models import Avg
from .serializers import BreedSerializer, KittenSerializer, RatingSerializer
from rest_framework.exceptions import PermissionDenied
from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>Welcome to the Kitten Exhibition!</h1>")


# Добавление нового котенка
class KittenCreateView(generics.CreateAPIView):
    serializer_class = KittenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Назначаем владельца котенку
        serializer.save(owner=self.request.user)


# Изменение информации о котенке
class KittenUpdateView(generics.UpdateAPIView):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        kitten = self.get_object()
        if kitten.owner != self.request.user:
            raise PermissionDenied("You do not own this kitten.")
        serializer.save()


# Удаление котенка
class KittenDeleteView(generics.DestroyAPIView):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not own this kitten.")
        instance.delete()


# Список всех пород
class BreedListView(generics.ListAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


# Список всех котят с фильтрацией по породе
class KittenListView(generics.ListAPIView):
    serializer_class = KittenSerializer

    def get_queryset(self):
        queryset = Kitten.objects.all()
        breed_id = self.request.query_params.get('breed')
        min_rating = self.request.query_params.get('min_rating')

        if breed_id:
            queryset = queryset.filter(breed_id=breed_id)

        if min_rating:
            queryset = queryset.annotate(avg_rating=Avg('ratings__rating')).filter(avg_rating__gte=min_rating)

        return queryset


# Детальная информация о котенке
class KittenDetailView(generics.RetrieveAPIView):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer


class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RatingListView(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
