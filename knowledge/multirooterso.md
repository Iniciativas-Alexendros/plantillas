---
name: multirooterso
description: >
  Por qué tu sistema —sea un SO o un agente Claude— adopta como
  propios los ficheros/cambios que llegan de otra instancia con la
  misma etiqueta (UID 0, mismo usuario, mismo "yo de otro hilo"), y
  cómo defenderse con provenance explícito en vez de fusión silenciosa.
  Capa 1: SO Unix (USB, tar, NFS, ZFS send, contenedores). Capa 2:
  multi-sesión Claude Code (edits cruzados entre agentes en paralelo).
  Citar al importar datos externos o al diseñar flotas de agentes que
  comparten repo/filesystem.
domain: sistemas-operativos-unix
references:
  - "Evidencia local: /etc/passwd, /etc/machine-id, /proc/self/status, /proc/self/uid_map, /proc/self/ns/ — contenedor Ubuntu 24.04.4"
  - "Comportamiento de tar/rsync/zfs send/mount/git por contrato de la herramienta"
related_skills:
  - verify
status: draft
last_updated: 2026-05-25
authority: inferred
---

## Resumen

> Cuando llega un fichero o un cambio desde fuera —otra máquina, otro
> SO, otra sesión paralela de Claude— y trae la misma etiqueta que tú
> (UID 0, mismo usuario, misma rama git, mismo email de commit), tu
> sistema lo adopta como propio. No hay campo de origen, sólo
> coincidencia numérica. Es el reponedor de Mercadona que entra a
> Consum porque el uniforme se parece: nadie le para. La defensa real
> no es bloquear, es **avisar y exigir provenance** antes de fusionar.
> Aplica igual a un kernel Unix que a una flota de agentes que tocan
> el mismo repo.

## Contenido

### El razonamiento (la parte que importa)

Ponte en la situación. Estás trabajando. Llega un parche. Lo firma
"tu usuario", con tu email, sobre la rama en la que estás. Lo aplicas.
¿Es tuyo? Coincide la etiqueta, así que para tu git, tu kernel y tu
agente, sí. Pero igual viene de **otro tú** —otro hilo, otro Claude,
otra sesión que arrancó en paralelo— que no comparte tu estado mental
ni tus últimas decisiones. Si su edit no afecta a tu línea temporal,
da igual. Si la afecta, hay paradoja: estás operando sobre un futuro
que ya ha sido modificado por una versión de ti que no sabe lo que tú
sabes.

Esto no es metáfora barata. Es por lo que existen los conflictos de
merge, los locks, las firmas, los machine-id, los namespaces y, en
ficción, las películas de viajes en el tiempo: el sistema necesita
saber **de qué línea viene cada cambio**, no sólo qué etiqueta lleva.
Sin provenance, todo cambio del "yo de otro hilo" se aplica como si
fuera tuyo. Con provenance, al menos se puede decidir: lo integro, lo
rechazo, o aviso al operador.

### Capa 1 — SO: el malentendido numérico

UID/GID/etiquetas son **números locales** sin pasaporte. POSIX no
guarda "de qué máquina viene este inodo". Al montar USB, extraer un
tar, recibir un `zfs send`, montar NFS o levantar una imagen de VM,
el kernel:

1. Lee `i_uid` / `i_gid` (32 bits) del inodo.
2. Los cruza contra `/etc/passwd` y `/etc/group` **locales**.
3. Si el número existe, le pone cara local; si no, lo deja como
   número crudo.
4. Capabilities (`security.capability`) y xattrs viajan junto con el
   fichero y se honran sin pedir permiso.

Linux y illumos comparten el modelo; illumos añade idmapping NFSv4
por dominio (`NFSMAPID_DOMAIN`) y aislamiento real con zonas, pero el
problema base es el mismo.

### Capa 1 — Vectores y defensas concretas

| Vector              | Qué pasa por defecto                                               | Defensa                                                                                          |
|---------------------|--------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| USB / pendrive      | UID/GID del otro SO se mapean por número.                          | `mount -o nosuid,nodev,uid=$(id -u),gid=$(id -g)`                                                 |
| `tar -xpf` ajeno    | Restaura UID/GID, suid/sgid y xattrs como propios.                 | `tar --no-same-owner --no-same-permissions --no-xattrs --no-acls --numeric-owner`                 |
| `rsync -a` desde X  | UID 0 remoto = root local.                                         | `rsync --chown=user:group --no-owner --no-group --no-perms` o `--usermap`                         |
| NFSv3               | Mismo número = mismo dueño en el alambre.                          | `root_squash`, `all_squash`; migrar a NFSv4                                                       |
| NFSv4               | `user@dominio`; dominios iguales → mapeo silencioso.               | Dominio distinto por flota; `sec=krb5p`                                                            |
| `zfs send | recv`   | Stream binario preserva todo tal cual.                             | Recibir en dataset de cuarentena `readonly=on`, revisar y promover                                |
| Imagen de VM (loop) | UID 0 de la imagen = UID 0 del host.                               | `unshare --map-root-user`, montar en namespace                                                    |
| Contenedor OCI      | UID 0 del contenedor escribe como root en bind-mounts.             | `userns-remap` en Docker; rootless Podman; `subuid`/`subgid`                                      |

Receta corta para importar un tar ajeno sin contagiarse:

```bash
mkdir -p /var/quarantine/import-$(date +%s)
cd /var/quarantine/import-*
tar --no-same-owner --no-same-permissions --no-xattrs --no-acls \
    --numeric-owner -xpf /ruta/archivo.tar
find . -perm /6000 -printf 'SUID/SGID: %p (uid=%U gid=%G)\n'
find . -printf '%U %G\n' | sort -u
chown -R "$(id -un):$(id -gn)" .
```

Y para USB:

```bash
mount -o nosuid,nodev,noexec,uid=$(id -u),gid=$(id -g),fmask=0177,dmask=0077 \
      /dev/sdX1 /mnt/usb
```

### Capa 2 — Agentes Claude en paralelo: el mismo problema en otro tejido

Cuando varias sesiones de Claude Code corren a la vez sobre el mismo
repo (o sobre clones que se sincronizan vía PR/rebase), cada una es
"tu usuario" con "tu email" en "tu rama". El git de destino no
distingue qué Claude lo escribió; el filesystem tampoco. Vectores
equivalentes:

| Vector agente                                          | Qué pasa                                                          | Defensa                                                                                                     |
|--------------------------------------------------------|-------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| Dos sesiones editan el mismo fichero                   | Última en hacer push gana; la otra ve "limpio" pero con datos     | Una rama por sesión (`claude/<slug>` único); PR explícito; `git fetch --prune` antes de cualquier edit       |
| Auto-rebase silencioso de otro hilo sobre tu rama      | Pierdes contexto sin enterarte                                    | Hook `pre-commit`/`pre-push` que verifica fecha del `HEAD@{upstream}` y avisa si cambió                     |
| `webhook` o agente externo modifica artefactos         | Tu siguiente turno opera sobre un estado que no escribiste        | `git diff HEAD@{1}..HEAD` al arrancar turno; mensaje al operador si hay cambios "ajenos"                    |
| Mismo `machine-id` o mismo nombre de agente            | Logs y trazas se mezclan, indistinguibles                         | Identidad por sesión: `CLAUDE_SESSION_ID`, machine-id virtual, prefijo en commits/PR                         |
| Sub-agentes Claude que escriben en `/tmp` compartido   | Otro agente lee y asume autoría                                   | Dir por agente (`/tmp/claude-$SESSION`); evitar `/tmp` global; o usar isolation `worktree`                  |

Análogo directo a la capa 1: lo que en SO es `--no-same-owner` o
`root_squash`, aquí son hooks que **no permiten merges silenciosos sin
provenance**. El operador (el usuario real) es el equivalente a un
auditor: si llega un cambio y no se puede demostrar la línea temporal
de la que viene, se avisa antes de aceptarlo.

### El test mental ("¿este cambio es mío?")

1. **Etiqueta sin origen** — ¿coincide la etiqueta (UID, email,
   rama) pero no puedo demostrar de qué hilo/máquina viene?
2. **Afecta mi línea** — ¿modifica algo que yo estoy a punto de
   tocar o que ya he decidido? Si sí, no fusionar en silencio.
3. **Privilegios heredados** — ¿trae suid/sgid/xattrs/capabilities,
   o, en el caso de agentes, commits firmados con permisos de
   merge directos? Limpiarlos o exigir revisión.

Si las tres respuestas son "no preocupante", adopta. Si alguna es
"sí", avisa antes de seguir.

## Aplicación

- **Cuándo usar**: importar datos externos (USB, NFS, tar, rsync, ZFS
  send), levantar contenedores con volúmenes compartidos, restaurar
  backups, **o** coordinar varias sesiones de Claude Code sobre el
  mismo repo/filesystem.
- **Cuándo NO usar**: trabajo intra-host, intra-sesión, sin cruces
  externos — el problema no se materializa.
- **Regla operativa**: ante etiqueta sin provenance, **avisar** y
  pedir confirmación al humano. No fusionar en silencio.

## Limitaciones

- Defensas SO se evaden si quien las aplica es root distraído (el
  `--no-same-owner` no se asume por defecto cuando se extrae como
  root).
- Capa de agentes requiere disciplina en el `settings.json` y hooks
  reales; sin hooks instalados, sólo queda PRs y revisión humana.
- ZFS `recv` no tiene `--numeric-owner`; la defensa es el dataset de
  cuarentena.
- Contenedores OCI sin user-namespaces no protegen al host por más
  flags de mount que se pongan.
- La metáfora temporal es ilustrativa: en software no hay paradojas,
  hay `git reflog`. Pero el riesgo operativo —operar sobre estado que
  no escribiste— es real.

## Referencias

- Evidencia local: /etc/passwd, /etc/machine-id, /proc/self/status, /proc/self/uid_map, /proc/self/ns/ — contenedor Ubuntu 24.04.4.
- Comportamiento de tar/rsync/zfs send/mount/git por contrato de la herramienta.
- Linux: `user_namespaces(7)`, `capabilities(7)`, `mount(8)`,
  `xattr(7)`, `subuid(5)`, SELinux/AppArmor docs.
- illumos/OmniOS: `zones(5)`, `ppriv(1)`, `zfs(1M)`, `share_nfs(1M)`,
  `nfsmapid(1M)`.
- Claude Code: hooks `PreToolUse`/`PostToolUse` y `SessionStart`,
  variable `CLAUDE_SESSION_ID`, isolation `worktree` para sub-agentes.
- Evidencia local de este contenedor: `/etc/passwd`,
  `/etc/machine-id`, `/proc/self/uid_map`, `/proc/self/ns/`.
