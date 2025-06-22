# Tienda Virtual - Kivy

## Descripción
Esta es una aplicación de escritorio para una tienda virtual desarrollada con **Python** y **Kivy**. Permite a los usuarios registrarse, iniciar sesión, gestionar categorías, marcas y productos, y asociar fotos a los productos. La aplicación utiliza **SQLite** como base de datos y almacena las rutas de las imágenes en una carpeta local. Kivy es ideal para aplicaciones multiplataforma, incluyendo móviles.

### Funcionalidades
- Registro e inicio de sesión con autenticación segura (contraseñas hasheadas con `bcrypt`).
- Gestión de categorías: crear y listar.
- Gestión de marcas: crear y listar.
- Gestión de productos: crear, asociar categorías y marcas, y subir fotos.
- Visualización de imágenes de productos en la interfaz.

## Requisitos
- Python 3.8 o superior
- Dependencias:
  - `kivy`: Para la interfaz gráfica.
  - `bcrypt`: Para hashear contraseñas.
  - `Pillow`: Para manejar imágenes.
- Sistema operativo: Windows, macOS o Linux (soporte para Android/iOS con empaquetado adicional).

## Estructura del Proyecto
```
tienda_kivy/
├── images/           # Carpeta para almacenar fotos de productos
├── tienda.db        # Base de datos SQLite
├── main.py          # Punto de entrada principal
├── database.py      # Lógica de base de datos
├── auth.py          # Lógica de autenticación
└── tienda.kv        # Diseño de la interfaz en Kivy
```

## Instalación
1. Clona o descarga el repositorio:
   ```bash
   git clone <URL-del-repositorio>
   cd tienda_kivy
   ```
2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Crea la carpeta `images/` en el directorio raíz:
   ```bash
   mkdir images
   ```

## Ejecución
1. Asegúrate de estar en el directorio del proyecto y que el entorno virtual esté activado (si lo usas).
2. Ejecuta la aplicación:
   ```bash
   python main.py
   ```
3. La aplicación se abrirá en una ventana de login. Regístrate, inicia sesión y usa el menú principal para gestionar categorías, marcas y productos.

## Despliegue
### Para Escritorio
Para distribuir la aplicación como un ejecutable independiente:
1. Instala PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Genera el ejecutable:
   ```bash
   pyinstaller --add-data "images;images" --add-data "tienda.kv;." --onefile main.py
   ```
3. Encuentra el ejecutable en la carpeta `dist/`.
4. Copia la carpeta `images/`, el archivo `tienda.db` (si existe) y `tienda.kv` a la misma carpeta que el ejecutable.
5. Ejecuta el archivo `.exe` (Windows) o el binario correspondiente (Linux/macOS).

### Para Android (Opcional)
Para empaquetar la aplicación para Android:
1. Instala Buildozer:
   ```bash
   pip install buildozer
   ```
2. Inicializa el proyecto Buildozer:
   ```bash
   buildozer init
   ```
3. Edita `buildozer.spec` para incluir dependencias (`kivy`, `bcrypt`, `Pillow`) y archivos adicionales (`images/`, `tienda.kv`, `tienda.db`).
4. Genera el APK:
   ```bash
   buildozer android debug
   ```
5. El APK estará en la carpeta `bin/`. Instálalo en un dispositivo Android.

## Notas Adicionales
- **Seguridad**: Las contraseñas se almacenan hasheadas con `bcrypt`. Para producción, considera usar una base de datos más robusta (como PostgreSQL) y autenticación con tokens.
- **Imágenes**: Las fotos de los productos deben estar en formatos `.png`, `.jpg` o `.jpeg` y se almacenan en la carpeta `images/`.
- **Base de datos**: Si `tienda.db` no existe, se creará automáticamente al iniciar la aplicación.
- **Pruebas**: Implementa pruebas unitarias y de integración para `database.py` y `auth.py` usando `unittest` o `pytest`.
- **Multiplataforma**: Kivy es ideal para móviles. Consulta la documentación de Buildozer para empaquetar para iOS.

## Contribuciones
Si deseas contribuir, crea un *pull request* con tus cambios. Asegúrate de incluir pruebas para cualquier nueva funcionalidad.
