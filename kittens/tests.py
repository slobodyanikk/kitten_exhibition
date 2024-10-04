import pytest
from django.contrib.auth.models import User
from .models import Kitten, Breed, Rating


@pytest.mark.django_db
def test_create_kitten():
    user = User.objects.create(username='testuser')
    breed = Breed.objects.create(name='Siamese')
    kitten = Kitten.objects.create(breed=breed, color='White', age=2, description='Fluffy kitten', owner=user)

    assert kitten.breed == breed
    assert kitten.color == 'White'
    assert kitten.age == 2
    assert kitten.description == 'Fluffy kitten'
    assert kitten.owner == user


@pytest.mark.django_db
def test_update_kitten():
    user = User.objects.create(username='testuser')
    breed = Breed.objects.create(name='Bengal')
    kitten = Kitten.objects.create(breed=breed, color='Brown', age=1, description='Cute kitten', owner=user)

    kitten.color = 'Dark Brown'
    kitten.save()

    assert kitten.color == 'Dark Brown'


@pytest.mark.django_db
def test_delete_kitten():
    user = User.objects.create(username='testuser')
    breed = Breed.objects.create(name='Persian')
    kitten = Kitten.objects.create(breed=breed, color='White', age=3, description='Fluffy Persian kitten', owner=user)

    kitten_id = kitten.id
    kitten.delete()

    assert Kitten.objects.filter(id=kitten_id).count() == 0


@pytest.mark.django_db
def test_filter_kittens_by_breed():
    user = User.objects.create(username='testuser')
    breed1 = Breed.objects.create(name='Siamese')
    breed2 = Breed.objects.create(name='Bengal')
    Kitten.objects.create(breed=breed1, color='Cream', age=2, description='Lovely kitten', owner=user)
    Kitten.objects.create(breed=breed2, color='Brown', age=1, description='Playful kitten', owner=user)

    kittens = Kitten.objects.filter(breed=breed1)
    assert kittens.count() == 1
    assert kittens.first().breed == breed1


@pytest.mark.django_db
def test_rate_kitten():
    user = User.objects.create(username='testuser')
    breed = Breed.objects.create(name='Bengal')
    kitten = Kitten.objects.create(breed=breed, color='Brown', age=1, description='Adorable kitten', owner=user)

    rating = Rating.objects.create(kitten=kitten, user=user, rating=5)

    assert rating.kitten == kitten
    assert rating.user == user
    assert rating.rating == 5
