---
name: roadmap-omnios-illumos
description: >
  Roadmap completo y sin humos para instalar OmniOS (distribución
  illumos) en una máquina física o VM, llegar a un sistema usable con
  ZFS root, red, SMF, IPS y opcional zonas/bhyve. Citar cuando se vaya
  a desplegar OmniOS desde cero o se quiera comparar el ciclo de
  instalación con un Linux.
domain: sistemas-operativos-illumos
references:
  - "Conocimiento general del ciclo de instalación OmniOS r151xx LTS / stable"
  - "Comandos comprobados de la familia illumos: beadm, pkg, dladm, ipadm, zfs, zpool, svcs, svcadm, zonecfg, zoneadm"
related_skills:
  - verify
status: draft
last_updated: 2026-05-25
authority: inferred
---

## Resumen

> OmniOS es la distribución illumos comunitaria con soporte LTS de
> OmniOSce. Este roadmap cubre desde "qué descargar" hasta "primera
> zona corriendo", sin pasar por humos: ZFS root + boot environments
> con `beadm`, red con `dladm`/`ipadm`, paquetes con `pkg` (IPS),
> servicios con SMF (`svcs`/`svcadm`), y opcionalmente zonas o bhyve.
> Usar como guía operativa de instalación, no como manual exhaustivo.

## Contenido

### Fase 0 — Decisión y descarga

1. Elegir release: **LTS** (estable largo plazo) o **stable**
   (semestral). Para producción casi siempre LTS.
2. Descargar la ISO o USB image desde `omnios.org/download` (mirror
   oficial). Verificar SHA256 contra el fichero publicado.
3. Hardware mínimo realista: 2 GB RAM (4 GB cómodo), 20 GB disco,
   CPU x86_64 con virtualización si se piensa usar bhyve. ZFS quiere
   ECC en producción, pero no es bloqueante para laboratorio.

### Fase 1 — Boot e instalador

1. Arrancar desde la ISO/USB. El instalador es **modo texto**,
   curses-style.
2. Selección de disco → ZFS root pool (`rpool`) por defecto. Si hay
   varios discos, considerar `mirror` desde el instalador.
3. Configurar:
   - hostname
   - timezone
   - root password
   - usuario admin inicial (recomendado: añadir a perfiles RBAC en
     vez de dar sudo total)
4. Red: el instalador deja a menudo configuración mínima; se ajusta
   tras el reboot con `dladm`/`ipadm`.
5. Reboot desde disco.

### Fase 2 — Primer login y verificación

```bash
uname -a            # SunOS <host> 5.11 omnios-r151xxx
zpool status        # rpool ONLINE
zfs list            # datasets root, var, home...
beadm list          # boot environments; debe existir 'omnios' activo
svcs -x             # servicios en estado degradado/maintenance
```

Si `svcs -x` da algo, resolverlo antes de seguir (`svcs -l <fmri>`,
`svcadm clear <fmri>`).

### Fase 3 — Red

illumos separa **capa de enlace** (`dladm`) y **capa IP** (`ipadm`).

```bash
dladm show-phys                       # NICs físicos
dladm show-link                       # links lógicos
ipadm create-if e1000g0               # crear interfaz IP
ipadm create-addr -T static \
  -a 192.0.2.10/24 e1000g0/v4
route -p add default 192.0.2.1        # gateway persistente
echo 'nameserver 1.1.1.1' > /etc/resolv.conf
cp /etc/nsswitch.dns /etc/nsswitch.conf
svcadm restart network/physical
```

Para DHCP: `ipadm create-addr -T dhcp e1000g0/dhcp`.

### Fase 4 — Paquetes (IPS) y publishers

```bash
pkg publisher                          # publishers configurados
pkg update                             # aplica actualizaciones
beadm list                             # nuevo BE creado automáticamente
pkg install developer/gcc14 \
            text/gnu-coreutils \
            editor/vim
```

Notas:
- Un `pkg update` que cambie el kernel crea un **boot environment**
  nuevo. Reboot → arranca el BE nuevo. Si algo va mal:
  `beadm activate <be-anterior>` y reboot.
- `pkg search`, `pkg info`, `pkg contents` son los equivalentes a
  `apt search/show/-L`.
- El repo `extra.omnios` añade paquetes fuera del core.

### Fase 5 — Usuarios y RBAC (no abusar de root)

```bash
useradd -m -s /bin/bash -G staff alex
passwd alex

# Asignar perfiles en vez de sudo total:
usermod -P 'Primary Administrator' alex

# Inspección
profiles alex
roles alex
ppriv -v $$
```

Para `sudo` clásico hay paquete (`pkg install ooce/security/sudo`),
pero idiomáticamente illumos prefiere `pfexec` + perfiles RBAC.

### Fase 6 — SMF (servicios)

```bash
svcs                                   # listado
svcs -a | grep ssh
svcadm enable -s svc:/network/ssh:default
svcadm disable <fmri>
svcadm refresh <fmri>
svccfg -s <fmri> setprop config/<k>=<v>
svccfg -s <fmri> refresh
```

`svc.startd` es el equivalente conceptual a systemd, pero anterior.
Manifiestos XML en `/lib/svc/manifest/`, perfiles en
`/etc/svc/profile/`.

### Fase 7 — Zonas (opcional, pero el punto fuerte de illumos)

```bash
zfs create -o mountpoint=/zones rpool/zones

zonecfg -z web01 <<'EOF'
create
set zonepath=/zones/web01
set autoboot=true
set ip-type=exclusive
add net
  set physical=web01_0
end
EOF

dladm create-vnic -l e1000g0 web01_0

zoneadm -z web01 install
zoneadm -z web01 boot
zlogin -C web01                        # consola para sysconfig
```

Dentro de la zona se hace `sysconfig configure` la primera vez. Tras
eso, `zlogin web01` da shell.

### Fase 8 — bhyve (opcional, VMs)

```bash
pkg install system/bhyve
# bhyve necesita VT-x/AMD-V; comprobar con: pagesize, isainfo -x
# Lo idiomático en OmniOS es usar zonas tipo 'bhyve' brand:
pkg install brand/bhyve
zonecfg -z vm01 'create -t SYSbhyve; ...; commit'
```

### Fase 9 — Backups, snapshots y BE

```bash
zfs snapshot -r rpool/ROOT/omnios@pre-cambio
zfs send -R rpool/ROOT/omnios@pre-cambio | \
  ssh backup zfs recv tank/omnios-bk
beadm create pre-cambio
beadm activate pre-cambio              # reboot para volver atrás
```

Regla práctica: snapshot antes de cualquier `pkg update`, y
`beadm activate` de vuelta si la actualización rompe arranque.

### Fase 10 — Endurecimiento mínimo

- `passwd -N root` o `rolemod -K type=role root` → convertir root en
  **rol**.
- Auditar: `auditconfig`, `audit -s`.
- Quitar privilegios al usuario por defecto: `usermod -K
  defaultpriv=basic,!proc_info alex`.
- Firewall: `pkg install network/firewall` (ipf) o usar `pf` si la
  versión de OmniOS lo trae.

## Aplicación

- **Cuándo usar**: cuando se va a montar un OmniOS desde cero, o se
  necesita un checklist operativo para comparar con un Linux.
- **Cuándo NO usar**: para SmartOS (basado en illumos pero con
  modelo de despliegue distinto: hipervisor inmutable + zonas), o
  para FreeBSD (otra rama BSD, no illumos).
- **Atajo mental Linux → illumos**:

| Linux                       | illumos / OmniOS                |
|-----------------------------|---------------------------------|
| `apt install`               | `pkg install`                   |
| `systemctl status`          | `svcs -l <fmri>`                |
| `systemctl enable --now`    | `svcadm enable -s <fmri>`       |
| `ip addr add`               | `ipadm create-addr`             |
| `ip link`                   | `dladm show-link`               |
| `sudo`                      | `pfexec` + perfiles RBAC        |
| `setcap cap_xxx`            | `ppriv` + `defaultpriv`         |
| `lxc`/`docker`              | zonas (`zonecfg`, `zoneadm`)    |
| Snapshots LVM/btrfs         | `zfs snapshot`, `beadm`         |
| GRUB entries                | boot environments (BE)          |

## Limitaciones

- No se ha podido validar ningún comando contra una máquina OmniOS
  real desde este contenedor; las salidas son las esperadas según el
  contrato de cada herramienta, no capturas en vivo.
- Las versiones LTS de OmniOS cambian de número (`r151046`, `r151050`,
  ...) cada ~2 años; comandos exactos pueden variar (en especial
  `brand/bhyve`, perfiles RBAC por defecto y nombres de publishers).
- SmartOS, OpenIndiana y Tribblix comparten kernel illumos pero
  difieren en instalador y gestor de paquetes — este roadmap no aplica
  literalmente.
- Si el hardware no está en la HCL de illumos (sobre todo NICs
  modernos y NVMe específicos), parte del Fase 3 puede requerir
  drivers de comunidad (`pkg install driver/...`).

## Referencias

- Comandos del contrato illumos: `beadm(1M)`, `pkg(1)`, `dladm(1M)`,
  `ipadm(1M)`, `svcs(1)`, `svcadm(1M)`, `zonecfg(1M)`, `zoneadm(1M)`,
  `zfs(1M)`, `zpool(1M)`, `ppriv(1)`, `profiles(1)`, `pfexec(1)`.
- Distribución: OmniOS Community Edition (omnios.org).
