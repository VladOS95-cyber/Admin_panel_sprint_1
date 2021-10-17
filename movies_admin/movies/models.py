from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(TimeStampedMixin, models.Model):
    name = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        db_table = "content\".\"genre"


class FilmworkGenre(models.Model):
    filmwork = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('TV Show')


class Filmwork(TimeStampedMixin, models.Model):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'), blank=True)
    certificate = models.TextField(_('certificate'), blank=True)
    file_path = models.FileField(_('file'), upload_to='film_works/', blank=True)
    rating = models.FloatField(_('rating'), validators=[MinValueValidator(0)], blank=True)
    type = models.CharField(_('type'), max_length=20, choices=FilmworkType.choices)
    genres = models.ManyToManyField(Genre, through='FilmworkGenre')

    class Meta:
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')
        db_table = "content\".\"film_work"


class Person(TimeStampedMixin, models.Model):
    full_name = models.CharField(_('full_name'), max_length=255)
    birth_date = models.DateField(_('birth_date'), blank=True)

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        db_table = "content\".\"person"


class PersonRole(models.TextChoices):
    DIRECTOR = 'director', _('director')
    WRITER = 'writer', _('writer')
    ACTOR = 'actor', _('actor')


class PersonFilmWork(models.Model):
    filmwork = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(_('role'), max_length=20, choices=PersonRole.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
