# Firebase: propuesta de despliegue, todavía no activada

Firebase Authentication puede gestionar correo y contraseña sin conectar una bandeja Gmail ni usar una contraseña SMTP. Es un cambio del proveedor de identidad; el usuario de texto actual no se convierte automáticamente en un correo de Firebase. La propuesta utiliza Authentication para las credenciales, no documentos de Firestore con contraseñas legibles.

La ruta local `Seminario2026` no identifica un proyecto de Firebase. Para activar esta propuesta hace falta el ID que aparece en Configuración del proyecto de Firebase Console. Los archivos de cuentas de servicio y las claves privadas no forman parte del portfolio.

## Arquitectura propuesta

Navegador o Android -> Firebase Authentication -> token ID -> FastAPI -> permisos del hogar y datos.

Firebase Hosting sirve HTML, CSS y JavaScript con HTTPS. FastAPI necesita un entorno Python, como Cloud Run, con una reescritura `/api/**` desde Hosting. El servidor debe verificar el token con Firebase Admin y mapear su UID a los permisos; ocultar botones o confiar en un rol enviado por el navegador no es autorización.

## Estado y aspectos pendientes

El proyecto de Firebase aún no quedó identificado mediante un ID de consola. La integración depende de un proveedor de autenticación configurado, SDK de Web y Android y validación de tokens en FastAPI. La cuenta local no se migró automáticamente.

La persistencia actual utiliza JSON, SQLite y fotos locales. Un despliegue distribuido requiere almacenamiento durable, transacciones y copias de seguridad; el RLock del proceso no coordina varias instancias.

También permanecen pendientes los orígenes autorizados, CSP, secretos de servidor, reescritura de API, pruebas de revocación y mediciones de recursos. No se habilitaron servicios de pago ni se publicaron datos del hogar. Las contraseñas y claves privadas no forman parte del contenido del portfolio.

Documentación oficial consultada el 25/10/2026:

- https://firebase.google.com/docs/auth/web/password-auth
- https://firebase.google.com/docs/hosting
- https://firebase.google.com/docs/hosting/cloud-run
- https://firebase.google.com/docs/auth/admin/verify-id-tokens

Estado: diseño documentado. La integración con Firebase y el despliegue público no están implementados ni activos.
