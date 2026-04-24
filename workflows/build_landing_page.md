# Workflow: Build & Deploy Landing Page

## Objetivo
Generar y publicar la landing page de Kraft Coffee en un servicio cloud accesible públicamente.

## Inputs requeridos
- `brand_assets/Logo.webp` — Logo del café
- `brand_assets/Menu.png` — Imagen del menú
- `brand_assets/Fotos- recursos/` — Fotos de productos
- `brand_assets/LInk.txt` — Link de Google Maps
- Destino de deploy (Netlify / GitHub Pages / Vercel / FTP)

## Outputs
- URL pública de la landing page (entregada al usuario)

## Pasos

### 1. Verificar assets
Confirmar que todos los archivos de `brand_assets/` están presentes antes de continuar.

### 2. Generar el HTML
El archivo `index.html` en la raíz del proyecto es el entregable estático.
Construido con: HTML + CSS (inline) + JS mínimo. Sin dependencias externas salvo Google Fonts.

### 3. Validar localmente
Abrir `index.html` en el navegador para verificar que todas las secciones cargan correctamente:
- Navbar y hamburger mobile
- Hero con foto de fondo
- Sección Nosotros con imágenes
- Grilla de Menú
- Galería de fotos
- Sección Ubicación con mapa embebido
- Footer

### 4. Deploy al servicio cloud
Ejecutar el tool correspondiente según el destino elegido:

**Netlify:**
```
python tools/deploy_netlify.py
```
Requiere: `NETLIFY_AUTH_TOKEN` y `NETLIFY_SITE_ID` en `.env`

**GitHub Pages:**
```
python tools/deploy_github_pages.py
```
Requiere: `GITHUB_TOKEN` y `GITHUB_REPO` en `.env`

### 5. Verificar URL pública
Confirmar que la URL devuelta carga la página correctamente y las imágenes se ven bien.

## Edge cases
- Si las imágenes no cargan en producción: verificar que los paths relativos (`brand_assets/...`) se respetan en el deploy
- Si el mapa de Google no carga: puede requerir API Key para embeds en dominios de producción

## Estado actual
- [x] Assets recopilados
- [x] index.html generado
- [ ] Deploy configurado — **pendiente: definir destino con el usuario**
