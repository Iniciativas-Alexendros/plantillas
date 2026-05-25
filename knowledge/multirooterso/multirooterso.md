---
name: multirooterso
description: >
  Investigación local sobre por qué el "root" (administrador) de un Unix
  cree ser único: UID 0 es local, los identificadores de máquina son
  débiles, y Linux/illumos descomponen el privilegio de forma distinta.
  Citar cuando se hable de identidad de superusuario, capabilities,
  privileges, namespaces, zonas o comparación Linux ↔ illumos/OmniOS.
domain: sistemas-operativos-unix
references:
  - "Evidencia local · /etc/passwd, /etc/machine-id, /proc/self/status, /proc/self/uid_map · contenedor Ubuntu 24.04"
related_skills:
  - verify
status: draft
last_updated: 2026-05-25
authority: inferred
---

## Resumen

> El UID 0 es un número local; ningún Unix lo ata a una identidad global.
> Cada root cree ser único dentro de su kernel, pero los identificadores
> de máquina (`hostid`, `machine-id`, `hostname`) son débiles o
> clonables, y mecanismos modernos (capabilities, namespaces en Linux;
> RBAC, privileges, zonas en illumos) permiten que coexistan varios
> "roots" incluso en la misma caja. Citar este artículo cuando se discuta
> identidad del superusuario, riesgo de colisión entre máquinas o el
> trasvase Linux → illumos/OmniOS.

## Contenido

### El UID 0 es local, no global

`getent passwd root` devuelve una entrada de `/etc/passwd`:

```
root:x:0:0:root:/root:/bin/bash
```

Nada en POSIX ni en el kernel de Linux liga ese 0 a una identidad inter-
máquina. La unicidad la imponen capas superiores (claves SSH de host,
principals Kerberos, certificados X.509, FreeIPA, AD), no el sistema.

### Identificadores de máquina, comparativa

| Identificador     | Tamaño   | Origen                                  | Fuerza            |
|-------------------|----------|-----------------------------------------|-------------------|
| `hostname`        | string   | `/etc/hostname`, mutable                | Cosmético         |
| `hostid` (Linux)  | 32 bits  | Derivado de IP en muchas distros        | Colisiona trivial |
| `hostid` (illumos)| 32 bits  | Histórico: serial/licencia              | Más estable       |
| `/etc/machine-id` | 128 bits | systemd/D-Bus, generado en instalación  | Fuerte pero clonable al copiar imagen |

Evidencia en este contenedor:

- `hostid` = `007f0100` → bytes `7f 01 00` = `127.0.1.x` (truco IP).
- `/etc/machine-id` = `0d0af05ee8fd4dc29275718f2ce4dff1`.
- `/etc/hostname` = `vm`.

### Linux descompone root con capabilities(7)

`/proc/self/status` en este proceso:

```
CapEff: 000001fffeffffff
```

`capsh --print` confirma que falta `cap_sys_resource`. Es decir: somos
UID 0 pero el kernel ya no nos da "todo". Hay 40+ capabilities y
cualquiera puede quitarse o concederse a binarios concretos
(`cap_net_bind_service` en un binario no setuid, por ejemplo).

### Linux permite múltiples roots con user namespaces

`/proc/self/ns/` contiene `user`, `pid`, `net`, `mnt`, `uts`, `ipc`,
`cgroup`, `time`. `cat /proc/self/uid_map`:

```
         0          0 4294967295
```

Aquí es identidad (estamos en docker pero sin user-ns hijo), pero el
mecanismo está disponible: el root de un contenedor puede mapearse al
UID 100000 del host. Resultado: varios UID 0 coexisten en la misma
máquina, cada uno "cree" ser el único dentro de su namespace.

### sudo / su / wheel: la respuesta histórica

En este sistema: sudo 1.9.15p5 con PAM, AppArmor, SELinux y audit.
`/etc/sudoers.d/` sólo trae `README`. La política estándar Ubuntu da
privilegios al grupo `sudo`. `sudo` resuelve la "unicidad" delegando,
registrando (`/var/log/auth.log`) y aplicando `use_pty`.

### illumos / OmniOS: el privilegio formalizado antes

- **RBAC** (`/etc/user_attr`, `/etc/security/prof_attr`,
  `/etc/security/exec_attr`): root puede ser un **rol**, no una cuenta
  de login. `roles=root` en cuentas normales obliga a `su` a un rol
  auditado.
- **Privileges** (`ppriv -l`): ~80 privilegios granulares
  (`file_dac_read`, `proc_exec`, ...). Análogo a capabilities pero
  anterior y más fino.
- **Zones**: equivalentes a contenedores, pero el `global zone` tiene
  un root explícitamente "más root" que el de las zonas no globales.
  La jerarquía es nombrada, no implícita como en Linux.
- **hostid** históricamente vinculado a licencia/serial: menos
  colisiones que el truco IP de Linux.

## Aplicación

- **Cuándo usar**: al diseñar políticas multi-máquina (gestión de
  flotas, IdM, autenticación SSH a escala), al explicar por qué un
  contenedor "root" no es root del host, al comparar Linux con illumos
  para decidir plataforma de hosting.
- **Cuándo NO usar**: para tareas operativas concretas que ya tienen
  su propio knowledge (p. ej. configuración de sudoers, ZFS).
- **Ejemplo mínimo** — comprobar la identidad real del root en cualquier
  Linux moderno:

```bash
id
getent passwd root
cat /etc/machine-id
hostid
cat /proc/self/status | grep -E '^Cap(Eff|Bnd)'
capsh --print 2>/dev/null | head
cat /proc/self/uid_map
ls /proc/self/ns/
systemd-detect-virt 2>/dev/null
```

En illumos/OmniOS el equivalente sería:

```bash
id
hostid
ppriv -v $$
roles
zonename
```

## Limitaciones

- Evidencia recogida en un contenedor Docker Ubuntu 24.04 minimizado;
  las manpages locales (`man capabilities`, `man machine-id`, etc.) no
  están instaladas. Los comandos `ppriv`, `roles`, `zonename` no se
  pudieron ejecutar localmente — la sección illumos se apoya en
  conocimiento general, sin docs locales que citar.
- `hostid` en Linux varía entre distros; el valor `007f0100` es típico
  de máquinas con resolución `127.0.1.1` y no debe tomarse como regla.
- Las capabilities y namespaces evolucionan rápido entre versiones de
  kernel; verificar siempre contra el kernel real de destino.

## Referencias

- Evidencia local: `/etc/os-release`, `/etc/passwd`, `/etc/hostname`,
  `/etc/machine-id`, `/etc/sudoers`, `/etc/sudoers.d/`,
  `/proc/self/status`, `/proc/self/uid_map`, `/proc/self/gid_map`,
  `/proc/self/ns/`, `/root/`.
- Kernel Linux 6.18.5, Ubuntu 24.04.4 LTS, sudo 1.9.15p5,
  `systemd-detect-virt` = `docker`.
