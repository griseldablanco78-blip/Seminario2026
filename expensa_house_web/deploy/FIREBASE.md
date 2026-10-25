# Firebase: propuesta de despliegue, todavía no activada

Firebase Authentication puede gestionar correo y contraseña sin conectar una bandeja Gmail ni usar una contraseña SMTP. Es un cambio del proveedor de identidad; el usuario de texto actual no se convierte automáticamente en un correo de Firebase. No almacenar contraseñas en documentos de Firestore.

La ruta local `Seminario2026` no identifica un proyecto de Firebase. Para activar esta propuesta hace falta el ID que aparece en Configuración del proyecto de Firebase Console. No publicar archivos de cuentas de servicio ni claves privadas en el portfolio.

## Arquitectura propuesta

Navegador o Android -> Firebase Authentication -> token ID -> FastAPI -> permisos del hogar y datos.

Firebase Hosting sirve HTML, CSS y JavaScript con HTTPS. FastAPI necesita un entorno Python, como Cloud Run, con una reescritura `/api/**` desde Hosting. El servidor debe verificar el token con Firebase Admin y mapear su UID a los permisos; ocultar botones o confiar en un rol enviado por el navegador no es autorización.

## Trabajo necesario antes del despliegue de producción

1. Identificar el proyecto y habilitar el proveedor de correo/contraseña si esa es la modalidad elegida. Conservar el login local hasta que se haya probado la migración de la administradora.
2. Integrar los SDK de Web y Android, y validación de tokens en FastAPI. No transferir hashes Argon2 como si fueran contraseñas Firebase; definir alta/migración con la propietaria.
3. Migrar JSON, SQLite y fotos a almacenamiento persistente con transacciones y copias de seguridad. El disco efímero de un contenedor no es persistencia durable; varias instancias no comparten el RLock local.
4. Configurar orígenes, CSP, dominios autorizados, secretos de servidor y reescritura de API; revisar el modelo CSRF al introducir cookies o tokens.
5. Probar los tres permisos y revocación con datos de prueba; verificar que nadie sin sesión acceda a stock, imágenes o tickets.
6. Medir recursos, revisar cuotas y facturación del proyecto antes de activar servicios. No se habilitaron servicios de pago ni se publicaron datos del hogar en esta revisión.

Documentación oficial consultada el 25/10/2026:

- https://firebase.google.com/docs/auth/web/password-auth
- https://firebase.google.com/docs/hosting
- https://firebase.google.com/docs/hosting/cloud-run
- https://firebase.google.com/docs/auth/admin/verify-id-tokens

Estado: diseño documentado. La integración con Firebase y el despliegue público no están implementados ni activos.
