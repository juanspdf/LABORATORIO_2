# Sistema Distribuido de Gestión de Calificaciones Estudiantiles

## Descripción del Proyecto

Este proyecto implementa un sistema distribuido cliente-servidor para la gestión de calificaciones estudiantiles mediante arquitectura de red TCP/IP. El sistema permite operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre registros de calificaciones almacenados en formato CSV.

### Características Principales

- ✅ Arquitectura cliente-servidor con comunicación por sockets TCP
- ✅ Dos implementaciones de servidor: secuencial y concurrente
- ✅ Validación de materias mediante servidor auxiliar de NRCs
- ✅ Almacenamiento persistente en archivos CSV
- ✅ Protocolo de comunicación basado en comandos de texto
- ✅ Respuestas en formato JSON
- ✅ Interfaz de cliente interactiva mediante menú

---

## Componentes del Sistema

### 1. Servidor de Calificaciones (Sin Hilos)
**Archivo:** `sin_hilos/server.py`

Implementación secuencial que atiende un cliente a la vez:
- **Puerto:** 12345
- **Modelo:** Bloqueante - procesa una petición antes de aceptar la siguiente
- **Almacenamiento:** `sin_hilos/calificaciones.csv`
- **Validación de materias:** ❌ No implementada

### 2. Servidor de Calificaciones (Con Hilos)
**Archivo:** `con_hilos/server.py`

Implementación concurrente usando `threading`:
- **Puerto:** 12345
- **Modelo:** No bloqueante - múltiples clientes simultáneos
- **Almacenamiento:** `con_hilos/calificaciones.csv`
- **Validación de materias:** ✅ Consulta al servidor NRC antes de agregar/actualizar

### 3. Servidor NRC (Validación de Materias)
**Archivo:** `nrcs_server.py`

Servidor auxiliar para gestión de códigos NRC:
- **Puerto:** 12346
- **Función:** Valida que las materias existan antes de registrar calificaciones
- **Base de datos:** `nrcs.csv`
- **Concurrencia:** Soporta múltiples conexiones simultáneas

### 4. Cliente
**Archivos:** `sin_hilos/client.py` y `con_hilos/client.py`

Interfaz de usuario con menú interactivo que permite:
- Agregar nuevas calificaciones
- Buscar calificaciones por ID de estudiante
- Actualizar calificaciones existentes
- Listar todas las calificaciones
- Eliminar registros

---

## Arquitectura del Sistema

```
┌─────────┐                    ┌─────────────────────┐                    ┌──────────────┐
│ Cliente │ ───── TCP ────────>│ Servidor            │ ───── TCP ────────>│ Servidor NRC │
│         │    (puerto 12345)  │ Calificaciones      │  (puerto 12346)    │              │
└─────────┘                    │ (con hilos)         │                    └──────────────┘
                               └─────────────────────┘
                                         │
                                         ▼
                               ┌─────────────────────┐
                               │ calificaciones.csv  │
                               └─────────────────────┘
```

**Flujo de operaciones:**
1. Cliente envía comando al Servidor de Calificaciones
2. Servidor valida la materia consultando al Servidor NRC (solo versión con hilos)
3. Servidor ejecuta operación en `calificaciones.csv`
4. Servidor responde al cliente en formato JSON

---

## Integrantes del Grupo

- **Juan David Pasquel Ruiz**

---

## Estructura de Directorios

```
laboratorio2/
│
├── con_hilos/
│   ├── calificaciones.csv      # Almacén de calificaciones (servidor concurrente)
│   ├── client.py               # Cliente para servidor concurrente
│   └── server.py               # Servidor concurrente con threading
│
├── sin_hilos/
│   ├── calificaciones.csv      # Almacén de calificaciones (servidor secuencial)
│   ├── client.py               # Cliente para servidor secuencial
│   └── server.py               # Servidor secuencial sin threading
│
├── nrcs_server.py              # Servidor de validación de NRCs
├── nrcs.csv                    # Base de datos de materias y NRCs
└── README.md                   # Este archivo
```

---

## Requisitos del Sistema

### Dependencias

El proyecto utiliza **únicamente bibliotecas estándar de Python**:

| Módulo | Propósito |
|--------|-----------|
| `socket` | Comunicación por red TCP/IP |
| `csv` | Lectura y escritura de archivos CSV |
| `json` | Serialización de datos para respuestas |
| `os` | Operaciones del sistema de archivos |
| `threading` | Concurrencia (solo servidor con hilos) |

### Versión de Python

- **Python 3.6 o superior**

**No se requiere instalación de paquetes externos mediante `pip`.**

---

## Instrucciones de Ejecución

### Preparación Inicial

#### 1. Preparar el archivo de NRCs (opcional)

Cree o edite el archivo `nrcs.csv` en el directorio raíz con el siguiente formato:

```csv
NRC,Materia
12345,mate
67890,estadistica
54321,recreo
11111,fisica
22222,quimica
```

**Notas importantes:**
- La primera línea debe ser el encabezado: `NRC,Materia`
- Cada materia debe tener un NRC único
- Los nombres de materias deben estar en minúsculas
- No incluir espacios adicionales

#### 2. Verificar archivos CSV de calificaciones

Los archivos `calificaciones.csv` se crean automáticamente si no existen. Formato esperado:

```csv
ID_Estudiante,Nombre,Materia,Calificacion
101,Juan Perez,mate,4.5
102,Maria Lopez,estadistica,3.9
```

---

### Opción 1: Servidor Sin Hilos (Secuencial)

Esta opción es más simple pero **solo atiende un cliente a la vez**.

#### Terminal 1 - Iniciar Servidor

```bash
cd sin_hilos
python server.py
```

**Salida esperada:**
```
Servidor secuencial escuchando en puerto 12345...
```

#### Terminal 2 - Iniciar Cliente

```bash
cd sin_hilos
python client.py
```

**Menú del cliente:**
```
1. Agregar calificación
2. Buscar por ID
3. Actualizar calificación
4. Listar todas
5. Eliminar por ID
6. Salir
Elija opcion: 
```

---

### Opción 2: Servidor Con Hilos (Concurrente) - **RECOMENDADO**

Esta opción permite **múltiples clientes simultáneos** y valida materias.

#### Terminal 1 - Iniciar Servidor NRC

```bash
python nrcs_server.py
```

**Salida esperada:**
```
Servidor NRC escuchando en puerto 12346...
```

#### Terminal 2 - Iniciar Servidor de Calificaciones

```bash
cd con_hilos
python server.py
```

**Salida esperada:**
```
Servidor de calificaciones escuchando en puerto 12345...
Conectado al servidor NRC en puerto 12346
```

#### Terminal 3+ - Iniciar Clientes (múltiples permitidos)

```bash
cd con_hilos
python client.py
```

Puede abrir múltiples terminales con clientes y todos funcionarán simultáneamente.

---

## Ejemplos de Uso

### Ejemplo 1: Agregar Calificación con NRC Válido

**Requisito previo:** La materia debe existir en `nrcs.csv`

```
Elija opcion: 1
ID: 101
Nombre: Juan Perez
Materia: mate
Calificacion: 4.5
```

**Respuesta del servidor:**
```
Calificación agregada para Juan Perez
```

**Verificación:** Revise `calificaciones.csv` y verá el nuevo registro.

---

### Ejemplo 2: Buscar Calificación por ID

```
Elija opcion: 2
ID: 101
```

**Respuesta:**
```
Nombre: Juan Perez, Materia: mate, Calificacion: 4.5
```

---

### Ejemplo 3: Actualizar Calificación

```
Elija opcion: 3
ID: 101
Nueva calificacion: 4.8
```

**Respuesta:**
```
Calificación actualizada a 4.8
```

---

### Ejemplo 4: Listar Todas las Calificaciones

```
Elija opcion: 4
```

**Respuesta:**
```
{'ID_Estudiante': '101', 'Nombre': 'Juan Perez', 'Materia': 'mate', 'Calificacion': '4.8'}
{'ID_Estudiante': '102', 'Nombre': 'Maria Lopez', 'Materia': 'estadistica', 'Calificacion': '3.9'}
{'ID_Estudiante': '103', 'Nombre': 'Carlos Ruiz', 'Materia': 'fisica', 'Calificacion': '4.2'}
```

---

### Ejemplo 5: Eliminar Registro por ID

```
Elija opcion: 5
ID: 101
```

**Respuesta:**
```
Registro eliminado para ID 101
```

---

### Ejemplo 6: Validación de Materia Inválida (servidor con hilos)

Intente agregar una calificación con una materia que no existe en `nrcs.csv`:

```
Elija opcion: 1
ID: 103
Nombre: Carlos Ruiz
Materia: biologia
Calificacion: 4.0
```

**Respuesta del servidor:**
```
Error: Materia/NRC no valida
```

**Explicación:** El servidor con hilos consulta al servidor NRC antes de agregar. Si la materia no existe, rechaza la operación.

---

## Pruebas de Concurrencia

### Prueba 1: Limitación del Servidor Sin Hilos

**Objetivo:** Demostrar que el servidor secuencial solo atiende un cliente a la vez.

**Pasos:**
1. Inicie el servidor sin hilos
2. Abra dos terminales con clientes
3. En el **Cliente 1**, seleccione opción 4 (Listar) - notará que tarda unos segundos
4. Mientras el Cliente 1 está procesando, intente usar el **Cliente 2**
5. **Observación:** El Cliente 2 debe esperar a que el Cliente 1 termine completamente

**Conclusión:** El servidor secuencial **bloquea** nuevas conexiones mientras atiende una solicitud.

---

### Prueba 2: Concurrencia Real con Servidor Con Hilos

**Objetivo:** Demostrar que múltiples clientes pueden operar simultáneamente.

**Pasos:**
1. Levante `nrcs_server.py` y el servidor con hilos
2. Abra **3 o más terminales** con clientes
3. Ejecute operaciones simultáneamente desde diferentes clientes:
   - **Cliente 1:** Listar todas las calificaciones (opción 4)
   - **Cliente 2:** Agregar nueva calificación (opción 1)
   - **Cliente 3:** Buscar por ID (opción 2)
   - **Cliente 4:** Actualizar calificación (opción 3)

**Observación en el servidor:**
```
Cliente conectado desde ('127.0.0.1', 54321) en hilo Thread-1
Cliente conectado desde ('127.0.0.1', 54322) en hilo Thread-2
Cliente conectado desde ('127.0.0.1', 54323) en hilo Thread-3
```

**Conclusión:** Cada cliente tiene su propio hilo (`Thread-X`) y todos son atendidos **simultáneamente**.

---

### Prueba 3: Verificar Logs de Hilos

El servidor con hilos imprime información detallada:

```
Cliente conectado desde ('127.0.0.1', 52134) en hilo Thread-3
Comando recibido: AGREGAR|104|Ana Torres|estadistica|4.9
Validando materia 'estadistica' con servidor NRC...
Materia validada correctamente
Cliente ('127.0.0.1', 52134) desconectado
```

**Identificadores únicos:** Cada conexión muestra un `Thread-X` diferente, confirmando la concurrencia.

---

## Protocolo de Comunicación

### Comandos del Servidor de Calificaciones

| Operación | Formato | Ejemplo |
|-----------|---------|---------|
| **Agregar** | `AGREGAR\|ID\|Nombre\|Materia\|Calificacion` | `AGREGAR\|1\|Juan\|mate\|4.5` |
| **Buscar** | `BUSCAR\|ID` | `BUSCAR\|1` |
| **Actualizar** | `ACTUALIZAR\|ID\|NuevaCalificacion` | `ACTUALIZAR\|1\|4.8` |
| **Listar** | `LISTAR` | `LISTAR` |
| **Eliminar** | `ELIMINAR\|ID` | `ELIMINAR\|1` |

**Notas sobre el protocolo:**
- Los campos se separan con el carácter pipe (`|`)
- Todos los comandos deben terminar sin espacios adicionales
- Los IDs son cadenas de texto, no necesariamente numéricos

---

### Comandos del Servidor NRC

| Operación | Formato | Ejemplo |
|-----------|---------|---------|
| **Buscar NRC** | `BUSCAR_NRC\|Materia` | `BUSCAR_NRC\|mate` |
| **Listar** | `LISTAR` | `LISTAR` |

---

### Formato de Respuestas

Todas las respuestas del servidor están en formato **JSON**:

#### Respuesta Exitosa
```json
{
  "status": "ok",
  "mensaje": "Operación exitosa",
  "data": {
    "ID_Estudiante": "101",
    "Nombre": "Juan Perez",
    "Materia": "mate",
    "Calificacion": "4.5"
  }
}
```

#### Respuesta de Error
```json
{
  "status": "error",
  "mensaje": "Descripción del error específico"
}
```

**Ejemplos de mensajes de error:**
- `"ID no encontrado"`
- `"Materia/NRC no valida"`
- `"Comando inválido"`
- `"Error al conectar con servidor NRC"`

---

## Limitaciones y Consideraciones

### Limitaciones Conocidas

#### 1. **Archivo CSV No Bloqueado** ⚠️
**Problema:** Los servidores no implementan mecanismos de bloqueo de archivos (`flock` o semáforos).

**Impacto:** Con escrituras concurrentes en `server.py`, puede ocurrir:
- Corrupción de datos en el CSV
- Pérdida de registros
- Sobrescritura de datos

**Solución temporal:** Evite operaciones de escritura simultáneas en el mismo registro.

#### 2. **Sin Autenticación**
No hay validación de identidad de clientes. Cualquier conexión al puerto puede ejecutar operaciones.

#### 3. **Codificación Fija**
Solo soporta UTF-8. Caracteres especiales de otras codificaciones pueden causar errores.

#### 4. **Sin Reconexión Automática**
Si el servidor NRC (`nrcs_server.py`) está caído, el servidor con hilos falla al validar materias sin intentar reconectar.

**Mensaje de error:**
```
Error: No se pudo validar la materia. Servidor NRC no disponible.
```

#### 5. **Buffer Limitado**
Las respuestas están limitadas a **1024 bytes** por el tamaño del buffer en `client.py`:
```python
respuesta = cliente.recv(1024).decode()
```

Si la respuesta es mayor (por ejemplo, listar 100+ registros), se truncará.

#### 6. **Duplicados de ID**
No se valida la unicidad del `ID_Estudiante` al agregar calificaciones. Pueden existir múltiples registros con el mismo ID.

#### 7. **Bug en `buscar_por_id`** 🐛
**Descripción:** El `return` dentro del loop causa que solo se revise el primer registro del CSV.

**Código problemático:**
```python
def buscar_por_id(id_estudiante):
    with open('calificaciones.csv', 'r') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila['ID_Estudiante'] == id_estudiante:
                return fila
            return None  # ❌ BUG: Retorna después de la primera iteración
```

**Solución:**
```python
def buscar_por_id(id_estudiante):
    with open('calificaciones.csv', 'r') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila['ID_Estudiante'] == id_estudiante:
                return fila
        return None  # ✅ Retorna después de revisar todos los registros
```

---

### Diferencias Entre Versiones

| Característica | Sin Hilos | Con Hilos |
|----------------|-----------|-----------|
| **Concurrencia** | ❌ No (bloqueante) | ✅ Sí (múltiples hilos) |
| **Validación NRC** | ❌ No valida materias | ✅ Consulta servidor NRC |
| **Puerto servidor** | 12345 | 12345 |
| **Clientes simultáneos** | 1 | Ilimitados* |
| **Módulos adicionales** | Ninguno | `threading` |
| **Complejidad código** | Baja | Media |
| **Robustez** | Baja | Media-Alta |

\* *Limitado por recursos del sistema (memoria, CPU, file descriptors)*

---

## Recomendaciones de Prueba

### 1. Probar Límites de Concurrencia
Intente conectar **10+ clientes simultáneos** al servidor con hilos y ejecute operaciones de escritura concurrentes.

**Comando para automatizar (Linux/Mac):**
```bash
for i in {1..10}; do
  (cd con_hilos && python client.py) &
done
```

**Observación esperada:** Monitor de recursos del sistema mostrará múltiples hilos de Python activos.

---

### 2. Validar Integridad de Datos
Después de operaciones concurrentes, revise `calificaciones.csv`:

```bash
cat con_hilos/calificaciones.csv
```

**Verificar:**
- Que no haya líneas corruptas
- Que todos los registros tengan 4 campos
- Que no se hayan perdido datos

---

### 3. Simular Fallos del Servidor NRC
**Objetivo:** Probar manejo de errores en el servidor con hilos.

**Pasos:**
1. Inicie el servidor con hilos (`con_hilos/server.py`)
2. **No inicie** `nrcs_server.py`
3. Intente agregar una calificación desde un cliente

**Resultado esperado:**
```
Error: No se pudo conectar al servidor NRC
```

---

### 4. Medir Tiempos de Respuesta
Compare el rendimiento entre versiones:

**Con cronómetro manual:**
```bash
time python client.py  # Ejecutar opción 4 (Listar)
```

**Resultado esperado:**
- Servidor sin hilos: ~0.5-1s para 100 registros
- Servidor con hilos: ~0.3-0.5s para 100 registros (más eficiente con carga alta)

---

### 5. Prueba de Estrés con Múltiples Operaciones
**Script de prueba** (`test_stress.sh`):
```bash
#!/bin/bash
for i in {1..50}; do
  echo "AGREGAR|$i|Estudiante$i|mate|4.5" | nc localhost 12345 &
done
wait
echo "LISTAR" | nc localhost 12345
```

**Ejecutar:**
```bash
chmod +x test_stress.sh
./test_stress.sh
```

---

## Solución de Problemas

### Error: "Address already in use"

**Causa:** El puerto 12345 o 12346 está siendo utilizado por otro proceso.

#### En Linux/Mac:
```bash
# Identificar proceso
lsof -i :12345

# Terminar proceso
kill -9 <PID>
```

#### En Windows:
```cmd
# Identificar proceso
netstat -ano | findstr :12345

# Terminar proceso
taskkill /PID <PID> /F
```

---

### Error: "Connection refused"

**Causas posibles:**
1. El servidor no está ejecutándose
2. El puerto configurado es incorrecto
3. Firewall/antivirus bloqueando la conexión

**Soluciones:**
```bash
# Verificar que el servidor está corriendo
ps aux | grep python  # Linux/Mac
tasklist | findstr python  # Windows

# Verificar puerto correcto en el código
grep "12345" server.py
grep "12346" nrcs_server.py

# Probar conexión manual
telnet localhost 12345
```

---

### El Cliente No Responde

**Causas posibles:**
1. Servidor NRC no está activo (para versión con hilos)
2. Servidor bloqueado procesando otra petición (sin hilos)
3. Error en el código del servidor

**Diagnóstico:**
```bash
# Verificar logs del servidor en la terminal
# Buscar mensajes de error o excepciones

# Verificar que nrcs_server.py está corriendo
ps aux | grep nrcs_server.py

# Reiniciar ambos servidores
pkill -f "python.*server.py"
python nrcs_server.py &
cd con_hilos && python server.py
```

---

### Archivo CSV Corrupto

**Síntomas:**
- Error: `csv.Error: line contains NULL byte`
- Registros incompletos
- Formato inconsistente

**Solución:**
```bash
# Hacer backup
cp calificaciones.csv calificaciones.csv.backup

# Recrear archivo limpio
echo "ID_Estudiante,Nombre,Materia,Calificacion" > calificaciones.csv
```

---

### Timeout al Listar Muchos Registros

**Causa:** Buffer de 1024 bytes insuficiente para respuestas grandes.

**Solución temporal:** Modificar `client.py`:
```python
# Cambiar
respuesta = cliente.recv(1024).decode()

# Por
respuesta = cliente.recv(4096).decode()  # 4KB buffer
```

---

## Mejoras Futuras Sugeridas

### Alta Prioridad
- [ ] Implementar bloqueo de archivos con `fcntl.flock()` o `threading.Lock()`
- [ ] Corregir bug en `buscar_por_id()`
- [ ] Validar unicidad de IDs antes de agregar
- [ ] Implementar reconexión automática al servidor NRC

### Media Prioridad
- [ ] Agregar logging con módulo `logging`
- [ ] Implementar manejo de señales (`SIGTERM`, `SIGINT`) para cierre limpio
- [ ] Agregar tests unitarios con `unittest` o `pytest`
- [ ] Implementar autenticación básica (usuario/contraseña)

### Baja Prioridad
- [ ] Migrar de CSV a base de datos SQLite
- [ ] Crear interfaz gráfica con `tkinter` o web con Flask
- [ ] Implementar cifrado TLS/SSL para comunicaciones
- [ ] Agregar compresión de datos para respuestas grandes

---

## Referencias Técnicas

### Documentación de Código
- [`sin_hilos/server.py`](sin_hilos/server.py) - Implementación secuencial básica
- [`con_hilos/server.py`](con_hilos/server.py) - Implementación concurrente con threading
- [`nrcs_server.py`](nrcs_server.py) - Servidor auxiliar de validación NRC
- [`con_hilos/client.py`](con_hilos/client.py) - Cliente de prueba con interfaz de menú

### Recursos Externos
- [Documentación oficial de `socket` en Python](https://docs.python.org/3/library/socket.html)
- [Guía de `threading` en Python](https://docs.python.org/3/library/threading.html)
- [Módulo `csv` de Python](https://docs.python.org/3/library/csv.html)
- [Protocolo TCP/IP](https://en.wikipedia.org/wiki/Transmission_Control_Protocol)

---

## Licencia

Este proyecto es un trabajo académico para fines educativos.

**Autor:** Juan David Pasquel Ruiz  
**Institución:** Universidad de las Fuerzas Armadas ESPE 
**NRC:** 27885 


---

## Contacto

Para preguntas o reportar problemas:
- **Email:** [jdpasquel1@espe.edu.ec]
- **GitHub:** [juanspdf/LABORATORIO_2]

---

**Última actualización:** Octubre 2025
