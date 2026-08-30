# EDA - Seminario de Actualización

## 1. Descripción general del proyecto

Este proyecto consiste en una aplicación sencilla desarrollada con Python y Gradio, cuya funcionalidad principal es recibir un nombre ingresado por el usuario y devolver un saludo personalizado.

La idea del ejercicio fue poner en práctica conceptos básicos de:

- creación de un proyecto en Python
- uso de entorno virtual
- instalación de dependencias
- trabajo con Git y GitHub
- control de versiones y sincronización remota
- publicación de un repositorio con archivos básicos y documentación

---

## 2. Objetivo del ejercicio

El objetivo principal fue aprender a:

- crear una aplicación pequeña pero funcional
- gestionar el proyecto desde Git
- manejar archivos ignorados como `.venv`
- resolver conflictos de sincronización con GitHub
- publicar el proyecto correctamente en un repositorio remoto

---

## 3. Desarrollo realizado

### 3.1. Creación del proyecto

Se creó una carpeta del proyecto con los archivos principales:

- `app.py`
- `requirements.txt`
- `README.md`
- `.gitignore`

La aplicación fue desarrollada con Gradio, lo que permite crear una interfaz simple sin necesidad de desarrollar un frontend complejo.

### 3.2. Archivo principal

El archivo principal de la aplicación es `app.py` y contiene la lógica para crear una interfaz con un campo de texto y un resultado de saludo.

La estructura inicial fue muy básica:

- entrada: texto con el nombre
- salida: saludo personalizado
- lanzamiento de la interfaz con Gradio

Posteriormente se ajustó para evitar que la app se ejecute al importar el módulo y solo se inicie cuando se ejecuta directamente.

### 3.3. Archivo de dependencias

El archivo `requirements.txt` se utilizó para definir la dependencia principal:

- `gradio`

Esto permite instalar exactamente lo que necesita la aplicación para funcionar correctamente.

### 3.4. Archivo README

Se creó y luego se fue mejorando el `README.md` para dejar una documentación clara acerca de:

- qué es el proyecto
- cómo instalarlo
- cómo ejecutarlo
- qué hace la aplicación
- cómo abrir la interfaz en el navegador

Esto fue importante para que el proyecto tenga un formato profesional y sea entendible por cualquier persona que lo reciba.

### 3.5. Archivo `.gitignore`

Se configuró un archivo `.gitignore` para excluir archivos que no deberían subirse a GitHub, como:

- `.venv/`
- `__pycache__/`
- archivos temporales de Python
- archivos pesados o innecesarios del proyecto

Esto evitó que la carpeta virtual se subiera al repositorio.

---

## 4. Problemas encontrados y cómo se resolvieron

### 4.1. Error al subir a GitHub

El problema real no era que la carpeta virtual no pudiera subirse, sino que el repositorio local y el remoto tenían historiales diferentes.

Esto apareció cuando se intentó hacer push a un repositorio que ya tenía cambios distintos en GitHub.

La solución fue:

1. revisar el estado del repo con `git status`
2. ver el origen remoto con `git remote -v`
3. detectar el conflicto de sincronización
4. resolver el conflicto en `README.md`
5. ejecutar rebase para integrar cambios remotos
6. finalmente hacer push exitoso

### 4.2. Conflicto en `README.md`

Al integrar cambios del repositorio remoto con la versión local, Git detectó un conflicto en `README.md` porque ambos lados modificaron ese mismo archivo.

Se resolvió combinando la información y dejando un texto final coherente.

### 4.3. Validación de la aplicación

Se ejecutó la aplicación con Python para verificar que la interfaz abrió correctamente en:

- http://127.0.0.1:7860

La verificación fue exitosa, lo que confirmó que el proyecto estaba funcionando correctamente.

---

## 5. Git y GitHub: práctica realizada

Se practicó el flujo de trabajo de Git para resolver problemas reales de colaboración y versionado.

### Comandos utilizados

- `git init`
- `git add .`
- `git commit -m "..."`
- `git remote add origin ...`
- `git pull --rebase origin main`
- `git push origin main`
- `git status`
- `git log`
- `git fetch origin`

### Aprendizaje principal

Cuando un repositorio remoto ya tiene archivos o un README inicial, y además se crea un repositorio local nuevo desde cero, Git bloqueará el push si los historiales no están sincronizados. En ese caso es necesario hacer fetch y rebase antes del push.

---

## 6. Repo de prueba para practicar Git

Además del repositorio principal del proyecto, se realizó una prueba separada para entender mejor el comportamiento de Git.

La secuencia práctica fue:

1. crear un repositorio en GitHub con README
2. clonarlo en la computadora
3. crear otro repo local con `git init`
4. hacer un commit local
5. conectarlo al mismo remoto
6. probar `git push`
7. observar el error por historial no sincronizado
8. resolverlo con `git pull --rebase`
9. continuar con el push

Esto permitió comprender la diferencia entre:

- repositorio local nuevo
- repositorio clonado
- historial local vs remoto

---

## 7. Estado actual del proyecto

El proyecto se encuentra en un estado funcional y publicado en GitHub.

El repositorio principal quedó sincronizado correctamente y la carpeta virtual quedó excluida mediante `.gitignore`.

El proyecto actual incluye:

- app funcional en Gradio
- README documentado
- configuración de dependencias
- control de versiones activo
- repositorio remoto conectado y actualizado

---

## 8. Siguientes pasos sugeridos

A medida que avance el ejercicio, se puede continuar actualizando este documento con nuevos aspectos como:

- mejoras en la interfaz
- agregado de más funciones
- explicación de los componentes de Gradio
- captura de resultados y ejemplos
- documentación final para entrega del seminario

---

## 9. Conclusión

Este ejercicio sirvió para comprender la relación entre programación, control de versiones y publicación en GitHub.

No solo se desarrolló una aplicación funcional, sino que también se aprendió a:

- organizar un proyecto
- ignorar archivos innecesarios
- manejar errores reales de Git
- resolver conflictos
- dejar un repositorio ordenado y listo para entregar

---

## 10. Registro de actualización

- Fecha de creación: 2026-08-30
- Estado: en progreso / funcionando
- Último punto verificado: aplicación ejecutándose correctamente y repositorio sincronizado con GitHub

---

Este documento puede ir actualizándose a medida que se avance con el ejercicio y se agreguen nuevas funcionalidades o mejoras al proyecto.
