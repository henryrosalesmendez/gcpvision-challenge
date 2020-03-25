

 # Detección de objetos en imágenes


En este repositorio se da solución al primer problema de la prueba de selección de Falabella **Gerencia IA Falabella retail**. El problema es el siguiente:
> Utilizando Google cloud platform y la Api de Computer vision se requiere crear un servicio REST que reciba como entrada una imagen y entregue como respuesta un analisis con informacion de la misma.

Para dar solución a este problema este proyecto se centra en detectar los objetos que aparecen en a imagen. Para el despliegue del proyecto se usó el *free tier* de Google Cloud Platform, donde se habilitaron dos **buckets** públicos: [gs://image-pool-falabella-test/](gs://image-pool-falabella-test/) y  [gs://image-pool-falabella-test-out/](gs://image-pool-falabella-test-out/) para almacenar las imágenes de entrada y salida respectivamente. 


## Diseño
La aplicación se creó usando buenas prácticas de diseño/programación/seguridad. El desarrollo se separó en dos partes: un fichero `routes.py`  que tiene el código Flask y provee el servicio web, y un fichero `objectdetection.py` con una clase Python que permite hacer las peticiones a la API de Cloud Vision, procesar las respuesta y mover los ficheros entre el entorno local y Storage.

El código se encapsuló en un docker, se almacenó en Container Registry de GCP, y se creó un clúster de 2 nodos manejado por Kubernetes usando un balanceador de carga. Esta opción es escalable, ya que Kubernetes aumentará los nodos en dependencia al volumen de peticiones que recibe la aplicación y la carga es repartida entre ellos. Por otro lado, esta aplicación es segura. Una primera capa de seguridad la brinda la infraestructura de GCP que es rebusta ante ataques de cargas, por otro lado, se creo una *service account* (en vez de usar la *service account* por defecto) siguiendo as recomendaciones de Google, que es la usada para hacer las peticiones a la API de Cloud Vision. 

## API
Como se solicitó, se usó la API de Cloud Visión que provee GCP, la cuál se corresponden a modelos de redes neuronales pre-entrenados. Se usó Python + Flask para crear un back-end que responde a peticiones RESTfull API. A continuación se muestra un llamado a la API donde indica como entrada una imagen de una bicicleta que puede encontrar [aquí](https://storage.cloud.google.com/image-pool-falabella-test/bicileta.jpg).

```bash
curl -H "Content-Type: application/json" -X POST -d '{"inputImage":"gs://image-pool-falabella-test/bicileta.jpg", "outputImage":"gs://image-pool-falabella-test-out/bicileta.jpg"}' http://35.225.113.7/falabella/api/v1.0/detectobjects
```

Como se muestra a continuación, el modelo de visión identifica correctamente que en la foto hay una bicicleta, una rueda de bicicleta y una llanta-neumático de bicicleta. También devuelve en una imagen con estos objetos identificados ([link](https://storage.cloud.google.com/image-pool-falabella-test-out/bicileta.jpg)).
```json
{
  "bucket_output:":"https://storage.cloud.google.com/image-pool-falabella-test-out/bicileta.jpg",
  "msg":"Objetos detectados en la imagen: Bicycle wheel, Bicycle, Tire"
}
```
<img src="https://users.dcc.uchile.cl/~hrosales/img/bicileta.jpg"  
alt="Markdown Monster icon"  
style="float: left; margin-right: 10px;" />

La API no necesita token, a continuación se detalla su uso:
> URL: http://35.225.113.7/falabella/api/v1.0/detectobjects
>
> Método: POST
>
> Body: debe indicar la dirección en el storage donde se imagen de entrada y donde poner la de salida
```json
{
    "inputImage": "DIRECCION EN CLOUD STORAGE DE UNA IMAGEN",
    "outputImage": "DIRECCION EN CLOUD STORAGE DE LA IMAGEN RESULTANTE"
}
```
>
>
>
> Resultado: un bucket con la dirección en el storage de la imagen resultante accesible desde un navegador web y un mensaje relacionado a los objetos que se encuentran en la imagen.
```
{
   "bucket_output": "DIRECCION PUBLICA DONDE SE ENCUENTRA LA IMAGEN RESULTANTE",
   "msg": "LISTADO DE OBJECTOS DESCUBIERTOS EN LA IMAGEN"
}
```
>
> En caso de que no se detecte ningún objeto o no se encuentre la imagen en el storage especificado, entonces la API devolverá el mensaje:
> "No se pudo obtener información de esta imagen"



## Front-end
Adicional a la API, se creó una interfaz visual usando Boostrap v4 que permite subir la una imagen y automáticamente muestra el nombre de los objetos detectados, el bucket de salida de la imagen y la imagen con los objetos resaltados. Para acceder a la imagen puede hacerlo por el siguiente enlace [http://35.225.113.7](http://35.225.113.7). 

A continuación una imagen visual de cómo se ve la interfaz. Para usar la aplicación primero se debe dar click en **Choose file**, seleccionar la imagen desde el ordenador local, y luego dar click en el boton **Submit**.

<img src="https://users.dcc.uchile.cl/~hrosales/img/main_view.png"  
alt="Markdown Monster icon"  
style="float: left; margin-right: 10px;" />
