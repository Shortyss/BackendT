from rest_framework import serializers

from viewer.models import Movie, Person


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        # fields = '__all__'
        fields = ['title_orig', 'year', 'description']


class MovieDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'
