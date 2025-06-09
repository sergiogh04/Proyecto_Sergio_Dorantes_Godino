# HikariList, página de gestión de series anime

![miku](imagenes/47tj.gif)

## ¿Qué es HikariList?
- HikariList es una aplicación de gestíon de series y peliculas animes dónde los usuarios pueden gestionar todas las series que quieran ver o hayan visto y tener su propia biblioteca digital, además de puntuar las obras que haya visto. La aplicación dispone de un ranking con las obras mejores votadas.

## ¿En qué destaca HikariList?
- HikariList destaca en su diseño simple y limpio, destinada a todos esos usuarios que no tienen experiencia en navegar por páginas webs complejas y quieren algo que no requiera mucha dificultad de uso, todos esos amantes de los animes que simplemente quieran disfrutar del anime y controlar todo lo que ven, ¡es su sitio!

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


 

 
  




