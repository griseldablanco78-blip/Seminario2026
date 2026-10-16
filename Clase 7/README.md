# Expensa House

MVP Android en Kotlin + Jetpack Compose para administrar los gastos y el inventario del hogar.

## Incluye

- Presupuesto mensual con progreso de gastos.
- Inventario de mercaderia nueva y en uso.
- Alerta visual cuando queda la ultima unidad.
- Lista de compras con pendientes marcables.
- Sugerencia de compra con IA simulada para el MVP.
- Ofertas de supermercados ubicadas en Balvanera, CABA.
- Alta rapida de productos desde Inventario.

## Abrir

Abrir la carpeta en Android Studio y ejecutar la configuracion `app` en un emulador o dispositivo con Android 8.0 o superior. Android Studio descargara las dependencias de Gradle durante la sincronizacion.

## Proximo corte tecnico

1. Persistencia local con Room y movimientos de stock.
2. Notificaciones con WorkManager para reposicion.
3. API de ofertas por supermercado y geolocalizacion.
4. Servicio de IA para leer consumo historico y optimizar el presupuesto.
5. Cuenta familiar y sincronizacion segura.

## Plan web y EDA

La base Room actual es local al telefono y no puede ser leida directamente por una pagina web. La integracion propuesta es Android -> API Python -> dashboard Streamlit. El plan completo de sincronizacion, dataset historico, modelos, voz, imagenes y avatar esta en [PLAN_PROYECTO.md](PLAN_PROYECTO.md).

Para el trabajo practico se recomienda comenzar exportando los datos de Room y registrando movimientos de stock. El inventario actual sirve como estado inicial, pero no alcanza por si solo para entrenar un modelo predictivo: hace falta conservar fechas, cantidades y tipos de movimiento.

## Probar la sincronizacion local Android-Web

La API FastAPI es el puente entre Room y la pagina web. En el primer inicio, si Room esta vacia, Android descarga el estado inicial del servidor. Luego, cada cambio guardado en Android se envia a la API; el boton de sincronizacion de la app tambien permite reenviar el estado manualmente. La pagina web muestra los cambios al recargar o al pulsar su boton 🔄; no usa actualizacion push en tiempo real.

1. En Windows, iniciar la API desde la carpeta del proyecto:

   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn web.api:app --host 0.0.0.0 --port 8000
   ```

2. Abrir `http://127.0.0.1:8000` en la PC para usar la web.
3. Para probar con un telefono fisico en la misma red Wi-Fi, agregar a `local.properties` la URL de la PC (usar su direccion IPv4 local y conservar la barra final):

   ```properties
   expensa.apiBaseUrl=http://DIRECCION_IPV4_DE_LA_PC:8000/
   ```

   El valor predeterminado `http://10.0.2.2:8000/` es para el emulador de Android Studio. Volver a sincronizar Gradle y ejecutar la variante `debug` despues de cambiar la URL.

La variante `debug` permite HTTP para esta prueba local. No publicar la API de esta forma en Internet: antes de desplegarla hacen falta HTTPS, autenticacion y almacenamiento adecuado.
