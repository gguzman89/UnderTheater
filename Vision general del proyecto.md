# Aplicación UnderTheater
## Motivación
El proyecto empezó porque el teatro under en la Argentina es mal difundido y para buscar una obra o clase de teatro todavia se sigue usando (en muchos casos) el boca a boca. Por este motivo es muy difícil como director de un teatro under difundir  tu arte. El mismo problema lo tiene el espectador para buscar una obra o una clase.

## Objetivo

**UnderTheater** tiene como objectivo principal la dfusión de clases, seminarios y obras de teatros 

## Circuito general
Un teatro con una obra a estrenar, se registrar en la aplicación y crea una publicación de la obra a estrenar.
La publicación la crea con el titulo de la obra, el precio, el teatro, la hora de función, la capacidad total del teatro, los actores, una foto y una sinopsis.
Un teatro con una nueva clase, se registrar en la aplicación, y crea una publicación de la nueva clase.
La publicación la crea con el titulo de la clase, el precio, el teatro, las horas que se dictan las clases, la cantidad de alumnos que entran en la clase, la cantidad de horas que dura la clase, una foto y una sinopsis.
Después que se crea la publicación se puede compartir en una red social(facebook o twitter) para generar mayor difusión de la clase. 
El mismo circuito para un seminario.
Un usuario cualquiera entra a la aplicación(ya sea porque la vio en una red social o porque el comentaron que esta pagina existía) en busca de una obra. Escribe el titulo de la obra en el buscador, la aplicación devuelve una serie de obras que son el resultado de su búsqueda, va a los detalles de la obra que buscaba y busca el contacto con el publicador(sea email, facebook o numero de teléfono). Una vez que tiene el contacto con el publicador se comunica para coordinar la entrega de la entrada.
El usuario después de ver la obra entra a la aplicación, busca la obra que ya vio y la califica dependiendo lo que le pareció la obra. Una vez que califico elige compartir en una red social su calificación para que los otro usuario puedan ver esa obra.
Un actor entra a la aplicación y busca una clase para tomar en el buscador. La aplicación devuelve una cantidad de resultados posibles. El actor entra a los detalles de la clase y busca el contacto con el publicador(sea email, facebook o numero de telefono). Una vez que tiene el contacto con el publicador se comunica para coordinar cuando empieza la clase.
El mismo circuito para buscar un seminario. 


## Casos de Uso principales  

##### Publicar una obra de teatro
1. El usuario director del teatro se loggea en la pagina 
2. Hace click en el boton "publicar una obra"
3. Llena el formulario con fotos de la obra, precio, nombre de la obra, syspnosis, cantidad de espacios disponibles, dia de la funcion, lugar donde se exibe
4.  Clickea en guardar
5.  Se redirige a los detalles de la obra
6.  Y se ven los datos de la obra con los datos de conctado del teatro. Los datos de contacto son email de teatro, numero de contacto, facebook o twitter

##### Buscar una obra
1. Un usuario espectador se loggea en la pagina
2. Ingrego en el buscador el nombre de una obra
3. Se redirige a una pagina con los resultados de la busqueda
4. Elijo una obra y entro a los detalles
5. Busco el numero de contacto o el email o el facebook y me comunico con el teatro para comprar la entrada. **Aclaracion:** Si no esta logeado podes ver los detalles de la obra pero **NO** podes ver el contacto del teatro

##### Registrarse en la  aplicacion
1. Un usuario entra a la aplicacion
2. Clickeo Login/registrarme
3. Lleno el formnulario de registro con: username(unico), email y password
4. Clickeo Registrarme
5. Y el usuario quedo registrado

##### Compartir una publicacion en una red social
1. Un usuario se loggea en la pagina 
2. Busca a una "publicacion"
3. Entra a los detalles de la publicacion
4. Clickea en el boton de la red social elegida
5. Se abre un dialogo para loggearse en al red elejida
6. Se comprueba los datos para publicar
7. Se clickea el boton publicar
8. Y la publicacion esta en tu perfil de esa red social
