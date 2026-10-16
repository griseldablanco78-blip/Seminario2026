# Revisi車n del repositorio de un compa?ero

**Repositorio revisado:** https://github.com/AraceliAmherdt/Proyecto_seminario
**Autora:** Araceli Amherdt
**Revisado por:** Griselda Blanco

Clon谷 el repositorio con `git clone` y lo revis谷 en modo solo lectura: no hice `push` ni modifiqu谷 nada.

```bash
git clone https://github.com/AraceliAmherdt/Proyecto_seminario.git
cd Proyecto_seminario
git log --oneline
```

## R迆brica

| Criterio | Resultado | Observaciones |
|---|---|---|
| README general | ? Cumple | Tiene t赤tulo, nombre de la alumna, descripci車n, tabla con una fila por clase (con links a cada README) y una secci車n "C車mo usar este repositorio". |
| Una carpeta por clase | ? Cumple | Existen `Clase_02`, `Clase_03`, `Clase_04`, `Clase_05` y `TP_Integrador`, con nombres consistentes y sin espacios. |
| README por clase | ? Cumple (seg迆n el README general) | El README general indica que cada carpeta tiene su propio `README.md` con instalaci車n y ejecuci車n. ?? Confirmar abriendo cada uno. |
| `.gitignore` | ? Cumple | Existe en la ra赤z. ?? Verificar que excluya el entorno virtual. |
| Alcanza para reproducir cada clase | ?? Completar | Cada clase tiene su propio `requirements.txt` seg迆n el README. ?? Indicar si est芍n todos y si las versiones est芍n fijadas. |
| Pude correr algo | ?? Completar | ?? Indicar qu谷 clase corr赤 (por ejemplo Clase_04 con Gradio), con qu谷 comandos y si funcion車. |
| Historial de commits | ? Cumple en cantidad | Tiene 10 commits en la rama `main`. ?? Revisar con `git log` si los mensajes son descriptivos y muestran el avance por clase. |

## C車mo intent谷 correrlo


```bash
cd Clase_04
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Resultado: ?? (se abri車 en http://127.0.0.1:7860 / dio un error).

## Problema concreto encontrado

```
- **Posible causa:** (por ejemplo, falta una librer赤a en `requirements.txt`, versi車n incompatible o ruta incorrecta).
- **Sugerencia para mejorarlo:** (por ejemplo, agregar la librer赤a faltante o indicar la versi車n de Python).

## Conclusi車n

El repositorio est芍 bien organizado: un README general claro, una carpeta por clase y un historial con varios commits. ?? Agregar una o dos l赤neas sobre qu谷 mejorar赤as o qu谷 te result車 迆til de su forma de organizarlo.