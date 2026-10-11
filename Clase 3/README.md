## Problemas encontrados y cómo los resolví

### 1. README duplicado

**Problema:** el repositorio tenía dos archivos README, lo que generaba confusión sobre cuál era el válido.

**Solución:** eliminé el archivo sobrante con Git, para que el borrado quedara registrado en el historial.

```bash
git rm archivo_a_eliminar.md
git commit -m "Elimino README duplicado"
git push
```

`git rm` borra el archivo y lo deja listo para el próximo commit.

---

### 2. Carpeta del entorno virtual sin ignorar

**Problema:** creé un `.gitignore` para excluir la carpeta del entorno virtual (`virtual`), pero Git seguía rastreándola porque ya la había subido antes. El `.gitignore` solo afecta a archivos que todavía no están versionados.

**Solución:** quité la carpeta del seguimiento de Git sin borrarla de mi computadora y luego subí el `.gitignore`.

```bash
git rm -r --cached virtual
git add .gitignore
git commit -m "Agrego .gitignore y dejo de versionar el entorno virtual"
git push
```

La opción `--cached` es la clave: elimina la carpeta del repositorio, pero la conserva en mi disco. Desde ese momento Git la ignora.

---

### 3. Rama principal: master vs. main

**Situación:** la rama principal de mi repositorio se llama `master`, y coincide con la rama por defecto del proyecto, por lo que no fue necesario hacer cambios.

**Si hiciera falta renombrarla a `main`:**

```bash
git branch -m master main
git push -u origin main
```

El primer comando renombra la rama local y el segundo la sube al remoto, dejándola configurada como rama de seguimiento (`-u`). Después habría que cambiar la rama por defecto en GitHub (*Settings → Branches*) y, opcionalmente, borrar la rama `master` del remoto.