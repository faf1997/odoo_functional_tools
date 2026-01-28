# Secret Management - Odoo 17

## Descripción

Módulo para gestionar credenciales del cliente en Odoo 17. Permite almacenar información sensible de tipo clave-valor asociada a partners específicos.

## Características

- **Almacenamiento seguro**: Credenciales tipo clave-valor con campo de valor protegido
- **Asociación a partners**: Cada credencial está vinculada a un partner específico
- **Control de acceso**: Dos grupos de permisos (lectura y acceso total)
- **Validación única**: La misma clave no puede repetirse para un mismo partner
- **Archivado**: Posibilidad de archivar credenciales sin eliminarlas
- **Integración**: Menú integrado en el módulo de Proyectos

## Instalación

1. Copiar el módulo `secret_management` en el directorio de addons de Odoo
2. Actualizar la lista de aplicaciones en Odoo
3. Buscar "Secret Management" e instalar el módulo

## Configuración

### Grupos de Seguridad

El módulo crea dos grupos de permisos:

1. **Secret User (Read Only)**: Acceso de solo lectura a las credenciales
2. **Secret Manager (Full Access)**: Acceso completo (crear, leer, actualizar, eliminar)

Para asignar permisos a los usuarios:
1. Ir a Configuración > Usuarios y Compañías > Usuarios
2. Seleccionar el usuario
3. En la pestaña "Derechos de Acceso", asignar el grupo correspondiente en la categoría "Secret Management"

## Uso

### Acceder al módulo

El menú "Client Credentials" está disponible dentro del módulo de Proyectos, visible solo para usuarios con los permisos adecuados.

### Crear una credencial

1. Ir a Proyectos > Client Credentials
2. Hacer clic en "Crear"
3. Completar los campos:
   - **Partner**: Seleccionar el partner (obligatorio)
   - **Key**: Ingresar la clave
   - **Value**: Ingresar el valor (se mostrará como contraseña)
4. Guardar

### Buscar y filtrar

La vista de búsqueda permite:
- Buscar por partner, clave o valor
- Filtrar credenciales archivadas
- Agrupar por partner, clave o valor

### Archivar credenciales

Para archivar una credencial:
1. Abrir la credencial en vista formulario
2. Hacer clic en el botón "Archivar" en la parte superior derecha

## Validaciones

- El partner es obligatorio en todas las credenciales
- No se pueden crear dos credenciales activas con la misma clave para un mismo partner
- Las credenciales archivadas no participan en la validación de unicidad

## Información Técnica

- **Versión**: 17.0.0.0.1
- **Autor**: Francisco Fiorentino
- **Dependencias**: base, project
- **Modelo principal**: secret.secret
- **Licencia**: LGPL-3

## Estructura del Módulo

```
secret_management/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── secret_secret.py
├── security/
│   ├── secret_security.xml
│   └── ir.model.access.csv
└── views/
    ├── secret_secret_views.xml
    └── menu_items.xml
```

## Soporte

Para reportar problemas o sugerencias, contactar al autor del módulo.
