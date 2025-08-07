# Política de Liberación de Software - Zapatería Hortencia

## Versión
Usamos control de versiones semánticas: `MAJOR.MINOR.PATCH` (ej: v1.0.0)

## Criterios para liberar
- ✅ Todas las pruebas deben pasar (`pytest` o `unittest`)
- ✅ Al menos 2 revisores deben aprobar el código en pull request
- ✅ El líder técnico debe validar con firma digital o comentario aprobado
- ✅ README.md debe estar actualizado
- ✅ CHANGELOG.md debe registrar los cambios
- ✅ El archivo VERSION.txt debe reflejar la versión liberada
- ✅ Firma del área QA (comentario en PR o firma en documento)

## Flujo
1. Crear nueva rama `release/vX.Y.Z`
2. Subir cambios, pruebas y documentación
3. Crear Pull Request a `main`
4. Validar pipeline en CI/CD (GitHub Actions)
5. Una vez aprobado, se genera el tag y se despliega
