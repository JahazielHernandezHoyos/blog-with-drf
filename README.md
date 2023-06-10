# BOILERPLATE

This boilerplate is a combination between two different APIs, which is good becase we have the best of both worlds, the
first one, uses elastic-search and is complete when talking about tools and setup, the other api is a bit more lite.

You will find in this repo a LOT  of example code, about how we do need to write our code. There are tests, managers,
decorators, and a lot of other tools, please clone this repo for creating new projects, get guide with the current code,
and clean the template for starting your new project based on this.

# CRS-API

Requerimientos

- Tener instalado Docker Y Docker compose
- Sistema operativo: Unix, Linux o Mac


El objetivo de esta prueba es crear un servicio que permita:
- Búsqueda de disponibilidad, mediante el cual se pueda consultar si hay habitaciones disponibles, es decir con cupo y precio, para un hotel y rango de fechas dado.
- Consultar y modificar la información básica necesaria para cargar la información de propiedades (hotel, habitaciones) e inventario (tarifas y precios).

Para levantar el proyecto se debe clonar de este repositorio y luego navegar hasta el en el terminal

<img width="804" alt="Captura de Pantalla 2022-11-30 a la(s) 11 23 26 p m" src="https://user-images.githubusercontent.com/8086136/204965409-b9aa6bb7-bbf9-4807-8843-7b606aa69945.png">

para correr el proyecto solo se debe hacer uso de los comandos escritos en el Makefile, tiene comandos tanto para desarrollo, tests, cobertura, creacion de usuarios administradores, reiniciar contenedores y mas

### Levantar el proyecto

para levantar el proyecto, solo se debe correr en la raiz del mismo el siguiente comando:

`make up`

este comando construirá la imagen de docker de este proyecto, ademas instalará de manera automatizada las dependencias, ejecutará las migraciones y cargará los archivos estáticos

<img width="812" alt="Captura de Pantalla 2022-11-30 a la(s) 11 33 02 p m" src="https://user-images.githubusercontent.com/8086136/204966400-ba12119d-42fd-4381-be6f-fcfbd9312ad8.png">

Los contenedores son:
- backend (contiene el api)
- elastic (contiene elastic search para hacer búsquedas sencillas y evitar golpear la base de datos)
- postgres-skeleton-db (contiene la base de datos en postgres)

nuestra imagen con los contenedores por dentro seria esta

![Captura de Pantalla 2022-11-30 a la(s) 11 27 58 p m](https://user-images.githubusercontent.com/8086136/204965868-97f8d7d4-4ee5-49b6-a285-54336854e979.png)

el backend está corriendo en el puerto 8500, en esta dirección -> http://0.0.0.0:8500/

una vez le des click al enlace vas a ver esta pantalla ->

![Captura de Pantalla 2022-11-30 a la(s) 11 35 03 p m](https://user-images.githubusercontent.com/8086136/204966631-45c8d41c-82b0-4268-a48b-232c1ec3c11c.png)

si haces un poco mas de scroll serás capaz de ver todos

![Captura de Pantalla 2022-11-30 a la(s) 11 35 57 p m](https://user-images.githubusercontent.com/8086136/204966703-4ca43a42-0bae-497b-bcfa-e1c8a85add94.png)

Un poco mas abajo se encuentran los modelos que contienen la definición de las estructuras de datos que vamos a manejar en el api

![Captura de Pantalla 2022-11-30 a la(s) 11 37 08 p m](https://user-images.githubusercontent.com/8086136/204966827-a36a11c1-c08f-4f0f-beb3-e99567afcfeb.png)

### Setup de datos

este proyecto tiene 2 maneras de crear data, por el api docs de swagger (que es bastante intuitiva) y por el admin de Django, la segunda me gusta más porque es bastante visual y mas directa a la hora de insertar los datos.

Para acceder al administrador solo basta con ir a este link http://0.0.0.0:8500/admin/

![Captura de Pantalla 2022-11-30 a la(s) 11 40 51 p m](https://user-images.githubusercontent.com/8086136/204967233-3825c906-db76-49d0-b50f-f5dc1f3f880d.png)

Para crear un usuario administrador debemos ir al terminar y escribir `make admin`, recuerda presionar enter cuando termines un paso, tambien recuerda que por seguridad no se muestra la longitud de la contraseña por lo que cuando termines de escribir cualquiera de los campos de password deberas presionar enter

<img width="677" alt="Captura de Pantalla 2022-11-30 a la(s) 11 45 04 p m" src="https://user-images.githubusercontent.com/8086136/204967756-a3b306dd-6b0b-458f-afb6-0886fe994536.png">

con nuestro usuario ya creado podremos volver al admin http://0.0.0.0:8500/admin/ e ingresar las credenciales que creamos para iniciar sesión

![Captura de Pantalla 2022-11-30 a la(s) 11 45 57 p m](https://user-images.githubusercontent.com/8086136/204967858-c7e10474-9e88-458d-9cfa-96426336422a.png)

![Captura de Pantalla 2022-11-30 a la(s) 11 46 12 p m](https://user-images.githubusercontent.com/8086136/204967881-216d6e62-e37c-4759-99de-e6e18db2b732.png)

una vez dentro nos dirigimos a Hotels y presionamos Add + para crear nuestro hotel y sus habitaciones

![Captura de Pantalla 2022-11-30 a la(s) 11 47 51 p m](https://user-images.githubusercontent.com/8086136/204968056-4e4b1fc9-d331-4445-9951-1a4a5297ebfa.png)

Hemos agregado un hotel con una habitación, podemos seguir agregando mas habitaciones en el futuro

![Captura de Pantalla 2022-11-30 a la(s) 11 56 52 p m](https://user-images.githubusercontent.com/8086136/204969012-5ebc1495-fb25-4d3d-a976-810ca2f47932.png)

El campo deleted hace referencia a un campo marcado que sirve para simbolizar un borrado logico, cuando se encuentra en true el registro no estará visible por fuera del admin, quiere decir que no será listado tampoco en ninguna de las apis

En caso de eliminación por error se podrán restablecer los objetos afectados sin problema, si se elimina un hotel, todos los registros asociados al hotel dejarán de mostrarse en la api

![Captura de Pantalla 2022-11-30 a la(s) 11 58 36 p m](https://user-images.githubusercontent.com/8086136/204969248-a6690ab6-01be-4426-8f38-9bda696f26ed.png)

Ahora vamos a crear un Rate, que pertenece solo a una habitación y tiene todos los precios y la ocupación para fechas especificas

![Captura de Pantalla 2022-12-01 a la(s) 12 02 16 a m](https://user-images.githubusercontent.com/8086136/204969726-46bc204f-f1a5-4375-97c5-6bef0bb56fa0.png)

podremos agregar tantos inventarios queramos, la única regla es que no se deben repetir fechas, cada fecha debe ser única en cada inventario asociado a un rate

con la data configurada podemos ver la información usando la ui de swagger http://0.0.0.0:8500/

![Captura de Pantalla 2022-12-01 a la(s) 12 08 08 a m](https://user-images.githubusercontent.com/8086136/204970442-4226a46a-172c-4ce0-9970-8ec810685118.png)

![Captura de Pantalla 2022-12-01 a la(s) 12 09 12 a m](https://user-images.githubusercontent.com/8086136/204970555-0b596a72-2d44-46d6-8487-c3655aefb015.png)

![Captura de Pantalla 2022-12-01 a la(s) 12 09 30 a m](https://user-images.githubusercontent.com/8086136/204970594-863502fd-aeb3-4c5f-8d13-6be11f3198be.png)

Con data ingresada ya estamos listos para probar el api que nos genera este esquema de datos

![Captura de Pantalla 2022-12-01 a la(s) 12 10 22 a m](https://user-images.githubusercontent.com/8086136/204970758-e68417d0-bb45-4e8a-a871-b7c056812f8c.png)

es esta

![Captura de Pantalla 2022-12-01 a la(s) 12 11 06 a m](https://user-images.githubusercontent.com/8086136/204970807-d0cad58e-bfc4-49b5-adbf-f50cf96484de.png)

![Captura de Pantalla 2022-12-01 a la(s) 12 11 59 a m](https://user-images.githubusercontent.com/8086136/204970964-0d54b360-040a-47ee-bcf4-09427495d0d4.png)

![Captura de Pantalla 2022-12-01 a la(s) 12 12 21 a m](https://user-images.githubusercontent.com/8086136/204971016-d5d12578-c9ee-4b09-85a9-f23048e01cb1.png)

### Anotaciones varias
- Todos los endpoints tienen las operaciones crud con posibilidad de reversión en el delete
- Toda la data de los endpoints get que listan objetos, contienen paginación
- Los filtros de los objetos eliminados se hacen a través del **BookingModelManager**
- Todos los endpoints devuelven la información con el esquema que promete excepto el de la disponibilidad porque los atributos no son claves fijas sino que son claves dinámicas armadas a partir de los valores que van arrojando las habitaciones, rates y más
- El unico endpoint que tiene tests es el de Availability y el de Hotels
- se hicieron tests de integración para probar los servicios
- en el servicio de availability solo se hacen 2 queries
- hay una clase de paginación propia que puede modificarse a conveniencia
- todas las apis a diferencia de la de disponibilidad contienen buscador y filtros que pueden agregarse a conveniencia

- la primera linea roja es un registro de una clase que permite crear nuevos validadores para los tipos de datos esperados en los parametros de las urls
![Captura de Pantalla 2022-12-01 a la(s) 12 23 06 a m](https://user-images.githubusercontent.com/8086136/204972364-6762de86-fe30-4f20-bc9f-6beaae65df2f.png)

se usó django-extensions para obtener los alias de las urls para evitar llamarlas explicitamente

<img width="998" alt="Captura de Pantalla 2022-11-30 a la(s) 5 25 31 p m" src="https://user-images.githubusercontent.com/8086136/204972813-aedf3247-c15b-4f3d-ae2a-41320aab6c08.png">


Estas son las tests que tiene el código actualmente

![Captura de Pantalla 2022-12-01 a la(s) 12 19 04 a m](https://user-images.githubusercontent.com/8086136/204971830-c7ba2a16-548a-439f-973a-53e46ef2d59c.png)

### cosas que hubiese querido hacer
- mejorar la estructura de los serializadores
- optimizar las queries
- testear todos los serializer
- testear todas las vistas
- testear todos los modelos
- testear todos los managers y querysets
- testear el decorador action_paginated para paginar actions en los viewsets como los rooms de los hotels


# Beer tap dispenser API

Anyone who goes to a festival at least one time knows how difficult is to grab some drinks from the bars. They are
crowded and sometimes queues are longer than the main artist we want to listen!

That's why some promoters are developing an MVP for new festivals. Bar counters where you can go and serve yourself
a beer. This will help make the waiting time much faster, making festival attendees happier and concerts even more
crowded, avoiding delays!

<p align="center">
    <img alt="Tap dispenser" width="300px" src="https://media.tenor.com/zYmG5cqTm-AAAAAC/beer-beer-tap.gif" />
</p>

## How it works?

The aim of this API is to allow organizers to set up these bar counters allowing the attendees self-serving.

So, once an attendee wants to drink a beer they just need to open the tap! The API will start counting how much flow
comes out and, depending on the price, calculate the total amount of money.

You could find the whole description of the API in the [OpenAPI description file](/api.spec.yaml) and send request to a
mock server with [this URL](https://rviewer.stoplight.io/docs/beer-tap-dispenser/juus8uwnzzal5-beer-tap-dispenser)

### Workflow

The workflow of this API is as follows:

1. Admins will **create the dispenser** by specifying a `flow_volume`. This config will help to know how many liters of
   beer come out per second and be able to calculate the total spend.
2. Every time an attendee **opens the tap** of a dispenser to puts some beer, the API will receive a change on the
   corresponding dispenser to update the status to `open`. With this change, the API will start counting how much time
   the tap is open and be able to calculate the total price later
3. Once the attendee **closes the tap** of a dispenser, as the glass is full of beer, the API receives a change on the
   corresponding dispenser to update the status to `close`. At this moment, the API will stop counting and mark it
   closed.

At the end of the event, the promoters will want to know how much money they make with this new approach. So, we have to
provide some information about how many times a dispenser was used, for how long, and how much money was made with each
service.

> ⚠️ The promoters could check how much money was spent on each dispenser while an attendee is taking beer!
> So you have to control that by calculating the time diff between the tap opening and the request time

---

## What are we looking for?

* **A well-designed solution and architecture.** Avoid duplication, extract re-usable code
  where makes sense. We want to see that you can create an easy-to-maintain codebase.
* **Test as much as you can.** One of the main pain points of maintaining other's code
  comes when it does not have tests. So try to create tests covering, at least, the main classes.
* **Document your decisions**. Try to explain your decisions, as well as any other technical requirement (how to run the
  API, external dependencies, etc ...)

This repository is a Python skeleton with Django & PostgreSQL designed for quickly getting started developing an API.
Check the [Getting Started](#getting-started) for full details.

## Technologies

* [Python 3.10](https://www.python.org/downloads/release/python-3100/)
* [Django](https://docs.djangoproject.com/en/4.1/releases/3.2/)
* [Django REST framework](https://www.django-rest-framework.org/)
* [Poetry](https://python-poetry.org/)
* [Coverage](https://coverage.readthedocs.io/en/6.3.1/)
* [Docker](https://www.docker.com/)
* [Make](https://www.gnu.org/software/make/manual/make.html)

## Getting Started

Within the [Makefile](Makefile) you can handle the entire flow to get everything up & running:

1. Install `make` on your computer, if you do not already have it.
2. Build the Docker image: `make build`
3. Migrate any DB pending task: `make migrate`
4. Start the application: `make up`

---

# Technical Decisions

### Packages installed

<img width="490" alt="Captura de Pantalla 2022-11-17 a la(s) 4 32 43 p m" src="https://user-images.githubusercontent.com/8086136/202675754-8687f579-c847-49fb-87ef-8ae6d57d948a.png">

- [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/) swagger implementation **easy to implement** on **Django** projects, api docs available on -> http://0.0.0.0:5050/, this library was used to generate api docs
<img width="1459" alt="Captura de Pantalla 2022-11-18 a la(s) 3 54 32 a m" src="https://user-images.githubusercontent.com/8086136/202680672-7f556eb5-ee05-4ece-8b4d-8469fc0624d3.png">

the api docs contains the schemes for all the projects

- [factory-boy](https://factoryboy.readthedocs.io/en/stable/) to create mocked data using django models through factories
- [django-extensions](https://github.com/django-extensions/django-extensions) for the aliases of the urls (to use **reverse('api:url')** instead of **/api/url'**), because is safer than use the link in the code, this package was used just on development (already removed)
<img width="886" alt="Captura de Pantalla 2022-11-18 a la(s) 11 06 00 a m" src="https://user-images.githubusercontent.com/8086136/202676296-112ed33e-8afa-436b-a9ce-a4e235132ebd.png">

### aliases of urls in the console
<img width="821" alt="Captura de Pantalla 2022-11-17 a la(s) 4 32 08 p m" src="https://user-images.githubusercontent.com/8086136/202675420-f27b9d2c-168f-48c6-a568-a8306af495d4.png">

### pyproject.toml after finish development
<img width="523" alt="Captura de Pantalla 2022-11-18 a la(s) 11 17 42 a m" src="https://user-images.githubusercontent.com/8086136/202678744-2909daa3-7228-477e-9986-33d26cb1ce71.png">


### Commands added

- static command was added to the make file and to the up command also because we need to run this commands to see the api docs that requires static files

<img width="602" alt="Captura de Pantalla 2022-11-18 a la(s) 3 54 16 a m" src="https://user-images.githubusercontent.com/8086136/202675520-0305af64-9a30-45d6-b3c6-f013672c66ac.png">

<img width="588" alt="Captura de Pantalla 2022-11-18 a la(s) 11 38 54 a m" src="https://user-images.githubusercontent.com/8086136/202684431-18658dd1-eacb-449e-8818-f23cc011f3e7.png">

- **django.contrib.staticfiles** added, because is required to use **drf-yasg**

<img width="698" alt="Captura de Pantalla 2022-11-18 a la(s) 11 31 24 a m" src="https://user-images.githubusercontent.com/8086136/202681806-007f7add-7777-4107-a538-8b8a076cb685.png">

<img width="1137" alt="Captura de Pantalla 2022-11-18 a la(s) 11 32 10 a m" src="https://user-images.githubusercontent.com/8086136/202682064-f069ee85-477c-439d-929f-b106643de520.png">

- **PRICE_BY_LITER** and **TIME_ZONE** added to the settings
<img width="1141" alt="Captura de Pantalla 2022-11-18 a la(s) 11 33 31 a m" src="https://user-images.githubusercontent.com/8086136/202682542-539bd7b8-cc4f-4cea-bc8e-f536cbf88933.png">

- **COERCE_DECIMAL_TO_STRING** added to **REST_FRAMEWORK** settings, to send decimals as number instead of string

<img width="1217" alt="Captura de Pantalla 2022-11-18 a la(s) 11 35 40 a m" src="https://user-images.githubusercontent.com/8086136/202683269-e8e00f08-ac71-4e56-9db8-2d80a13b1494.png">

<img width="545" alt="Captura de Pantalla 2022-11-18 a la(s) 11 35 57 a m" src="https://user-images.githubusercontent.com/8086136/202683401-609a81c5-270d-4ad0-98d3-413a80bd1bd5.png">

- ports added to **postgres-skeleton-db** container in order to connect outside the container

<img width="534" alt="Captura de Pantalla 2022-11-18 a la(s) 11 37 15 a m" src="https://user-images.githubusercontent.com/8086136/202683839-78b4a81b-9f3f-44e7-9905-4aade7190e0f.png">
<img width="1325" alt="Captura de Pantalla 2022-11-18 a la(s) 11 42 21 a m" src="https://user-images.githubusercontent.com/8086136/202685696-03433ea3-fed2-4d74-bc80-399a53d1d955.png">
<img width="691" alt="Captura de Pantalla 2022-11-18 a la(s) 11 42 38 a m" src="https://user-images.githubusercontent.com/8086136/202685765-728625ee-8019-4deb-8789-e5b08c62d89d.png">

- UUID as primary key

<img width="663" alt="Captura de Pantalla 2022-11-18 a la(s) 11 54 16 a m" src="https://user-images.githubusercontent.com/8086136/202689036-a5bee8b4-5b27-4abf-9b20-3df28f9f0e1e.png">

- TextChoices to status values
<img width="552" alt="Captura de Pantalla 2022-11-18 a la(s) 11 54 51 a m" src="https://user-images.githubusercontent.com/8086136/202689184-867020a1-bef3-46bf-80f6-52c1f2da23f3.png">

<img width="772" alt="Captura de Pantalla 2022-11-18 a la(s) 11 55 21 a m" src="https://user-images.githubusercontent.com/8086136/202689288-39ee33be-9014-47fd-9210-f0af64146861.png">

- migrations folder created

<img width="181" alt="Captura de Pantalla 2022-11-18 a la(s) 11 56 23 a m" src="https://user-images.githubusercontent.com/8086136/202689489-c2799996-e9df-461c-992d-a5322235e4df.png">

### testing

33 tests added successfully

<img width="956" alt="Captura de Pantalla 2022-11-18 a la(s) 11 51 59 a m" src="https://user-images.githubusercontent.com/8086136/202688607-35d96b7f-0c16-4635-bd06-1bc91b3a849c.png">

100% of coverage 🚀 🔥 😎

<img width="511" alt="Captura de Pantalla 2022-11-18 a la(s) 12 03 59 p m" src="https://user-images.githubusercontent.com/8086136/202691078-c4e3eaa9-a5d6-4791-9e92-eba6d5b654cb.png">

- I've added **# pragma: no cove**r to these methods because are not being used

<img width="737" alt="Captura de Pantalla 2022-11-18 a la(s) 12 05 08 p m" src="https://user-images.githubusercontent.com/8086136/202691191-1e0b08c5-f9cf-4f70-acf2-e297a5644800.png">
