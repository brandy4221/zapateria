1. Número mínimo de revisores

Todo Pull Request debe ser revisado y aprobado por al menos 1 revisor antes de su integración.

Para cambios críticos (en seguridad, infraestructura, ramas main o release/*), se recomienda una revisión por al menos 2 personas.

El autor del PR no puede aprobar su propio PR.

2. Proceso de validación del Pull Request

Antes de aprobar un PR, se deben cumplir los siguientes requisitos:

a. Pruebas automatizadas (CI):

El PR debe activar el pipeline de pruebas automatizadas (unit tests, linters, builds, etc.).

Todas las pruebas deben completarse exitosamente antes de poder hacer merge.

b. Revisión de estilo de código:

El código debe seguir las convenciones y guías de estilo definidas para el proyecto.

Se deben evitar errores comunes como código duplicado, funciones demasiado largas o nombres poco descriptivos.

c. Documentación:

Si el cambio introduce nuevas funcionalidades o modifica el comportamiento existente, debe incluir:

Comentarios en el código (si aplica).

Actualización en la documentación técnica, manual de usuario o README.

Notas en el changelog (si el proyecto lo utiliza).

d. Claridad en el propósito del PR:

El título y la descripción del PR deben explicar claramente:

Qué problema resuelve.

Qué cambios se realizaron.

Cómo probar o validar los cambios (si aplica).

3. Tiempo máximo de respuesta a un Pull Request

Todo PR debe recibir una primera respuesta (comentario, revisión o solicitud de cambios) en un plazo máximo de 48 horas hábiles después de ser abierto.

En caso de urgencias o bloqueos, se debe comunicar al equipo para priorizar la revisión.

Si un PR no recibe respuesta en ese plazo, el autor puede notificar al Líder del Proyecto o mencionarlo directamente para asegurar su revisión.

Consideraciones finales

Se recomienda mantener los Pull Requests pequeños y enfocados (un solo propósito por PR).

Una vez aprobado, se debe utilizar squash merge para mantener un historial limpio.

Los PR deben ser cerrados si quedan obsoletos o sin actividad prolongada (más de 7 días sin actualizaciones).

