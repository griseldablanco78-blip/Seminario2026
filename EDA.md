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

## 8. Ejercicio 2: validación de subida sin ignorar una carpeta

Se realizó una prueba adicional para confirmar que una carpeta no ignorada se sube normalmente a GitHub.

### Paso realizado

1. Se creó la carpeta `datos_prueba/`
2. Se agregó un archivo dentro: `datos_prueba/archivo.txt`
3. Se ejecutó `git add .`
4. Se ejecutó `git commit -m "Agregar carpeta datos_prueba"`
5. Se ejecutó `git push origin main`

### Resultado verificado

La operación fue exitosa y Git mostró el siguiente resultado:

- commit creado: `Agregar carpeta datos_prueba`
- archivo agregado: `datos_prueba/archivo.txt`
- push realizado correctamente a GitHub

Esto confirma que, cuando una carpeta no está en `.gitignore`, Git la incorpora al repositorio y la sube correctamente.

---

## 9. Ejercicios prácticos de Git y GitHub

A continuación se detallan los tres ejercicios realizados y la explicación paso a paso de cada uno.

### Ejercicio 1: repositorio con README y conflicto de sincronización

Este ejercicio consistió en crear un repositorio en GitHub con README y luego tratar de conectarlo a un repositorio local distinto creado con `git init`.

#### Pasos ejecutados

1. Crear repo nuevo en GitHub con README.
2. Hacer `git init` en una carpeta local distinta.
3. Crear un archivo y hacer `git add` + `git commit`.
4. Conectar con `git remote add origin ...`.
5. Intentar `git push origin main`.
6. Si aparece el error de historial distinto, ejecutar:

```bash
git fetch origin
git pull --rebase origin main
```

7. Resolver conflictos si existen y continuar con:

```bash
git add .
git rebase --continue
git push origin main
```

#### Aprendizaje

El problema no estaba en la carpeta virtual, sino en que el repositorio remoto ya tenía un historial distinto del local. Git bloquea el push para evitar mezclar historiales incompatibles.

---

### Ejercicio 2: carpeta no ignorada se sube a GitHub

Este ejercicio buscó confirmar que una carpeta no ignorada sí se sube correctamente al repositorio.

#### Pasos ejecutados

```bash
mkdir datos_prueba
cd datos_prueba
"archivo de prueba" > archivo.txt
```

Luego, desde la raíz del proyecto:

```bash
git add .
git commit -m "Agregar carpeta datos_prueba"
git push origin main
```

#### Resultado verificado

La carpeta y el archivo fueron incluidos en el commit y subidos con éxito a GitHub.

Esto demostró que, si la carpeta no está en `.gitignore`, Git la envía normalmente.

Luego se ejecutó esta corrección para que no vuelva a ocurrir:

```bash
git rm -r --cached datos_prueba
git commit -m "dejar de trackear datos_prueba"
git push
```

Y finalmente se agregó al `.gitignore`:

```gitignore
datos_prueba/
~$*
```

---

### Ejercicio 3: conflicto entre master y main

Este ejercicio se centró en cuando el repositorio local se crea con la rama `master`, pero GitHub usa `main` por defecto.

#### Pasos para probarlo

```bash
git config --global init.defaultBranch master
mkdir prueba-rama
cd prueba-rama
git init
```

Crear archivo inicial:

```bash
echo "# prueba-rama" > README.md
git add README.md
git commit -m "commit inicial"
```

Crear repositorio vacío en GitHub y conectarlo:

```bash
git remote add origin https://github.com/TU_USUARIO/mi-repo.git
```

Intentar subir:

```bash
git push -u origin master
```

#### Solución correcta

```bash
git branch -m master main
git push -u origin main
git push origin --delete master
```

Y para evitar que vuelva a pasar en el futuro:

```bash
git config --global init.defaultBranch main
```

#### Aprendizaje

GitHub usa `main` por defecto en muchos casos, por lo que hay que alinear el nombre de la rama local con la remota para evitar errores de push.

---

## 10. Siguientes pasos sugeridos

A medida que avance el ejercicio, se puede continuar actualizando este documento con nuevos aspectos como:

- mejoras en la interfaz
- agregado de más funciones
- explicación de los componentes de Gradio
- captura de resultados y ejemplos
- documentación final para entrega del seminario

---

## 11. Conclusión

Este ejercicio sirvió para comprender la relación entre programación, control de versiones y publicación en GitHub.

No solo se desarrolló una aplicación funcional, sino que también se aprendió a:

- organizar un proyecto
- ignorar archivos innecesarios
- manejar errores reales de Git
- resolver conflictos
- dejar un repositorio ordenado y listo para entregar
- trabajar con ramas y sincronización remota

---

## 12. Registro de actualización

- Fecha de actualización: 2026-08-30
- Estado: en progreso / funcionando
- Último punto verificado: aplicación ejecutándose correctamente, repositorio sincronizado con GitHub, prueba de carpeta no ignorada exitosa, y explicación de los tres ejercicios actualizados en este documento

---

Este documento puede ir actualizándose a medida que se avance con el ejercicio y se agreguen nuevas funcionalidades o mejoras al proyecto.

Este ejercicio sirvió para comprender la relación entre programación, control de versiones y publicación en GitHub.

No solo se desarrolló una aplicación funcional, sino que también se aprendió a:

- organizar un proyecto
- ignorar archivos innecesarios
- manejar errores reales de Git
- resolver conflictos
- dejar un repositorio ordenado y listo para entregar

---

## 11. Registro de actualización

- Fecha de creación: 2026-08-30
- Estado: en progreso / funcionando
- Último punto verificado: aplicación ejecutándose correctamente, repositorio sincronizado con GitHub y prueba de carpeta no ignorada exitosa

---

Este documento puede ir actualizándose a medida que se avance con el ejercicio y se agreguen nuevas funcionalidades o mejoras al proyecto.
