# HikariList, página de gestión de series anime

![miku](imagenes/47tj.gif)

## ¿Qué es HikariList?
- HikariList es una aplicación de gestíon de series y peliculas animes dónde los usuarios pueden gestionar todas las series que quieran ver o hayan visto y tener su propia biblioteca digital, además de puntuar las obras que haya visto. La aplicación dispone de un ranking con las obras mejores votadas.

## ¿En qué destaca HikariList?
- HikariList destaca en su diseño simple y limpio, destinada a todos esos usuarios que no tienen experiencia en navegar por páginas webs complejas y quieren algo que no requiera mucha dificultad de uso, todos esos amantes de los animes que simplemente quieran disfrutar del anime y controlar todo lo que ven, ¡es su sitio!

## ¿Qué tecnologias se han utilizado para desarrollar HikariList?
- Esta página web tiene su base en el lenguaje de programación python, en el framework de Django.
- En la parte de diseño se utiliza HTML, CSS y Javascript, además de boostrap
- En la parte de despligue he desplegado mi proyecto utilizando Docker en una instancia AWS asociada a una IP elástica, con un dominio de tech.domains.
- Para la base de datos he utilizado PostgresSQL

## Creador de la aplicación web:
- Sergio Dorantes Godino

## ¿Cómo funciona la aplicación?
- Esta aplicación está desplegada con docker en una instancia en AWS y accesible desde la URL hikarilist.yelardo.tech, sin embargo, también podréis acceder a la app instalandola de manera local, voy a proceder a explicar como podéis ejecutar la aplicación web en local:

 1.- Descargue el código en un .zip y descomprimalo
 
 2.- Una vez descomprimido, o bien en un IDE o en una consola de comandos, ejecute lo siguiente:
 ```python

docker compose build

````
3.- Con ese comando habremos construido nuestra imagen docker, ahora vamos a levantarlo: 
```python

docker compose up -d

````
4.- Luego debemos aplicar las migraciones 
```python

docker compose exec web python manage.py migrate

````
5.-Con todo listo podemos acceder al proyecto añadiendo la siguiente ruta dentro del navegador
```python

http://localhost:8000/

````
6.- Si simplemente deseas visitar la web, te dejo aquí la url de al app
```python

http://hikarilist.yelardo.tech

````
## Antes de empezar a hablar del despliegue, el diseño y el backend, voy a hacer un pequeño tutorial muy sencillo de cómo funciona mi web: 

### Inicio:
- Una vez despleguemos la web, ya sea en local o desde la url, nos aparecerá lo siguiente:

![inicio1](imagenes/inicio.PNG)


- Una vez iniciemos sesión, o nos registremos por primera vez, le deberemos de dar al botón de comenzar:
![inicio2](imagenes/Captura.PNG)


### Página principal:
 - Esta es la página principal, donde tendremos siempre a nuestra disposición la barra de navegación, para movernos por la app, además de unas noticias destacadas de la semana y los animes mas destacados de ella.
![principal](imagenes/principal.PNG)


 - También tendremos la barra de busqueda que nos permitirá buscar el anime que queramos 
![busqueda](imagenes/buscador.PNG)

- Si seguimos bajando tendremos los animes más destacados de esta temporada primavera-verano
![busqueda](imagenes/emision.PNG)

- Por último tendríamos los animes mejores valorados por los usuarios de la web
![busqueda](imagenes/mejoresvalorados.PNG)

### Detalles de los animes:

- Si pulsamos en cualquier anime, nos aparecerá la información sobre dicho anime, una breve sinopsis y además podremos añadirlo a nuestra lista dependiendo de la categoría en la que lo queramos meter, y podremos añadirle una nota.
 ![detallesanime](imagenes/detallesanime.PNG)

### Perfil:

- Si pulsamos en el botón de perfil, nos llevara a nuestro perfil, donde se nos asignará un avatar por defecto pero podremos cambiarlo, nos pondrá desde cuando somos miembros de la página y tendremos acceso a nuestra biblioteca entera, y podrémos ir viendo todos los animes que hemos añadido y en que estado los tenemos, además de el numero total de animes de cada sección.
![perfil](imagenes/perfil.PNG)

### Directorio anime:

- Si pulsamos en directorio anime, nos llevará a una página con todo el catalogo anime que existe en la web.
 ![all](imagenes/2.PNG)

# Diseño de la web

# Backend, apis y panel de administrador de la web 
- Esta web ha sido desarrollada en Django, usando un modelo de MVC, mi web está siendo controlada todo desde una misma app, dónde controlo todo lo que ocurre en ella y desde el panel de administración.
  ### Modelos:
  - Aquí estan recogidos todos los modelos de mi aplicación, desde la gestión de todos los animes y la creación de ellos mismos hasta los usuarios y las notas medias.
 ```python

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Avg

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Anime(models.Model):
    FORMAT_CHOICES = [
        ('TV', 'TV'),
        ('Movie', 'Movie'),
        ('OVA', 'OVA'),
        ('ONA', 'ONA'),
        ('Special', 'Special'),
    ]
    STATUS_CHOICES = [
        ('airing', 'En emisión'),
        ('finished', 'Finalizado'),
        ('upcoming', 'Proximamente'),
    ]

    title       = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    slug        = models.SlugField(unique=True, blank=True)
    genres      = models.ManyToManyField(Genre, blank=True)
    image       = models.URLField(blank=True, default="https://via.placeholder.com/150")
    format      = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES)
    episodes    = models.PositiveIntegerField()
    year        = models.DateField()
    is_trending = models.BooleanField(default=False)
    is_seasonal = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def aggregate_avg_score(self):
        agg = self.user_animes.exclude(score__isnull=True).aggregate(avg=Avg('score'))['avg']
        return round(agg or 0, 2)

    def __str__(self):
        return self.title

STATUS_CHOICES = [
    ('pending',   'Planeado para ver'),
    ('watching',  'Viéndolo'),
    ('paused',    'En pausa'),
    ('dropped',   'Dropeado'),
    ('completed', 'Finalizado'),
]

class Profile(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class UserAnime(models.Model):
    """
    Relaciona usuarios y animes, con estado y puntuación.
    """
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    anime     = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='user_animes')
    status    = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    score     = models.PositiveSmallIntegerField(null=True, blank=True)
    added_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'anime')

    def __str__(self):
        return f"{self.user.username} – {self.anime.title} ({self.get_status_display()})"



````
### Views:
- Aquí esta la mayor parte de la lógica de la web, cómo funciona el sistema de biblioteca digital, el inicio de sesión, el buscado y la api para las notas medias de los animes.
```python

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Avg
from rest_framework import viewsets, permissions
from .models import Anime, STATUS_CHOICES, UserAnime, Profile, Genre
from .forms import UserRegisterForm
from .serializers import AnimeSerializer, UserAnimeSerializer


def home(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('anime:home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('anime:home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('anime:home')


@login_required(login_url='anime:login')
def anime_index(request):
    trending = Anime.objects.filter(is_trending=True)
    seasonal = Anime.objects.filter(is_seasonal=True)
    top_rated = Anime.objects.annotate(avg=Avg('user_animes__score')) \
                     .filter(avg__isnull=False) \
                     .order_by('-avg')[:12]
    return render(request, 'pag_main/index.html', {
        'trending': trending,
        'seasonal': seasonal,
        'top_rated': top_rated,
    })


@login_required(login_url='anime:login')
def anime_detail(request, slug):
    anime = get_object_or_404(Anime, slug=slug)
    user_anime = None

    if request.user.is_authenticated:
        user_anime, _ = UserAnime.objects.get_or_create(user=request.user, anime=anime)
        if request.method == 'POST':
            status = request.POST.get('status')
            if status in dict(STATUS_CHOICES):
                user_anime.status = status
            score = request.POST.get('score')
            if score and score.isdigit() and 1 <= int(score) <= 10:
                user_anime.score = int(score)
            user_anime.save()
            return redirect('anime:detail', slug=slug)

    avg_score = UserAnime.objects.filter(anime=anime, score__isnull=False) \
                .aggregate(avg=Avg('score'))['avg']

    return render(request, 'pag_main/anime_details.html', {
        'anime': anime,
        'user_anime': user_anime,
        'status_choices': STATUS_CHOICES,
        'avg_score': round(avg_score, 2) if avg_score else None,
        'score_range': range(1, 11),  # Para el selector de puntuación
    })


@login_required(login_url='anime:login')
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    user_list = UserAnime.objects.filter(user=request.user).select_related('anime')
    grouped = [
        (code, label, user_list.filter(status=code))
        for code, label in STATUS_CHOICES
    ]
    return render(request, 'user_profile/profile.html', {
        'profile': profile,
        'grouped_animes': grouped,
        'status_choices': STATUS_CHOICES,
    })


def anime_search(request):
    q = request.GET.get('q', '').strip()
    results = []
    if q:
        qs = Anime.objects.filter(Q(title__icontains=q))[:10]
        for anime in qs:
            results.append({'slug': anime.slug, 'title': anime.title, 'image': anime.image})
    return JsonResponse({'results': results})


#api
class AnimeViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.query_params.get('ordering') == 'top':
            qs = qs.annotate(avg=Avg('user_animes__score')) \
                   .filter(avg__isnull=False) \
                   .order_by('-avg')
        return qs


class UserAnimeViewSet(viewsets.ModelViewSet):

    queryset = UserAnime.objects.all()
    serializer_class = UserAnimeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


@login_required(login_url='anime:login')
def all_anime_view(request):
    all_animes = Anime.objects.all().order_by('title')
    return render(request, 'pag_main/all_anime.html', {'all_animes': all_animes})


````

### URLS:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('anime/', include(('pagina_main.urls', 'anime'), namespace='anime')),  # Namespace correcto
    path('', include('pagina_main.urls')),  # Esto SIEMPRE debe ir al final
]

````

### URLS APP:
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import AnimeViewSet, UserAnimeViewSet  # <-- IMPORTANTE

app_name = 'anime'

router = DefaultRouter()
router.register(r'animes', AnimeViewSet, basename='anime')
router.register(r'ratings', UserAnimeViewSet, basename='rating')

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('list/', views.anime_index, name='index'),
    path('profile/', views.profile_view, name='profile'),
    path('search/', views.anime_search, name='anime_search'),
    path('allanime/', views.all_anime_view, name='allanime'),

    path('<slug:slug>/', views.anime_detail, name='detail'),

    path('api/', include(router.urls)),  # <-- Necesario para acceder a /api/animes y /api/ratings


]

````
### FORMS:
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Ingresa un correo válido.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

````
### SIGNALS:
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


````
### ADMIN:
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from .models import (
    Anime,Genre,UserAnime,Profile
)

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'format', 'status', 'year', 'is_trending', 'is_seasonal')
    list_filter = ('format', 'status', 'year', 'is_trending', 'is_seasonal')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_trending', 'is_seasonal')

@admin.register(UserAnime)
class UserAnimeAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime', 'status', 'score', 'added_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'anime__title')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')

admin.site.register(Genre)


````
### API(SERIALIZERS):

```python
from rest_framework import serializers
from django.db.models import Avg
from .models import Anime, UserAnime

class UserAnimeSerializer(serializers.ModelSerializer):
    anime = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Anime.objects.all()
    )

    class Meta:
        model = UserAnime
        fields = ['id', 'anime', 'status', 'score']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        instance, created = UserAnime.objects.update_or_create(
            user=validated_data['user'],
            anime=validated_data['anime'],
            defaults={
                'status': validated_data.get('status', 'plan_to_watch'),
                'score': validated_data.get('score', None),
            }
        )
        return instance

    def update(self, instance, validated_data):
        validated_data.pop('user', None)  # No permitir cambiar el usuario
        return super().update(instance, validated_data)


class AnimeSerializer(serializers.ModelSerializer):
    avg_score = serializers.SerializerMethodField()

    class Meta:
        model = Anime
        fields = ['id', 'title', 'slug', 'image', 'format', 'status', 'avg_score']

    def get_avg_score(self, obj):
        avg = obj.user_animes.filter(score__isnull=False).aggregate(average=Avg('score'))['average']
        return round(avg, 2) if avg is not None else None


````
### PANEL DE ADMINISTRADOR:
- Dede el panel de administrador puedo tener control total de todo lo que hacen los usuarios en mi web, además de crear nuevos registros y perfiles, la url para acceder al panel de administración es:
```python
hikarilist.yelardo.tech/admin
````
- Una vez estamos dentro del panel de administración debemos iniciar sesión con un usuario con permisos de staff y veremos lo siguiente:

 ![admin](imagenes/adming.PNG)

 - Pulsando en anime veremos todos los animes que han sido creados con sus características propias.

 ![adming](imagenes/animesadmin.PNG)

 - Si pulsamos en añadir anime tendremos la siguiente plantilla para añadir nuevos animes a la web, además de poder ponerlo en diferentes categorías de la aplicación, ya sea en tendencia o en seasonal(o las 2):

 ![addanime](imagenes/addanime.PNG)

- En el apartado de géneros nos salen todos los generos creados para la web y asignarlo a un anime

   ![generos](imagenes/generos.PNG)

- Si nos vamos al apartado de perfiles, nos apareceran todos los usuarios que tienen un perfil en la web:
   ![usuarios](imagenes/usuarios.PNG)
  
- Desde la parte de User Anime, podremos ver toda la actividad de la página, qué animes eligen los usuarios y las notas que les ponen a los mismos, además del estado y en la fecha que hizo esos movimientos

   ![useranime](imagenes/useranime.PNG)

- Como se puede apreciar, desde el panel de administrador se puede controlar, practicamente casi todo lo que sucede en la aplicación, sin necesidad de acceder a la base de datos para comprobarlo.

### API:
- La api que he diseñado para la web está hecha por mi utilizando Django Rest framework y consiste en que todos los usuarios pueden puntuar cualquier anime, y de esas puntuaciones se hace una media de las notas y las mejores notas se muestran en la página principal. Para acceder a los datos de la api tenemos que escribir en el navegador la siguiente url:
  ```python
  hikarilist.yelardo.tech/api/animes
  ````
- Además podemos ver también el movimiento de los usuarios desde la api y las notas que les ponen:
    ```python
  hikarilist.yelardo.tech/api/ratings
  ````

  

# Despligue del proyecto 


  




  





 

 
  




