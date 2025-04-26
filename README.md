# ebook-translator-nllb\n\nMotor de traducción para libros técnicos (Inglés → Español) usando NLLB y Fine-tuning.

# Ebook Translator NLLB

## Descripción

Proyecto para desarrollar una solución local de traducción de libros electrónicos basada en el modelo NLLB (No Language Left Behind) de Meta.  
El objetivo es facilitar la traducción de grandes volúmenes de texto sin depender de servicios de terceros ni de APIs comerciales.

---

## Estructura del Proyecto

- `/etapa-1/`: Desarrollo inicial de la API local con FastAPI y primer integración con Calibre.
- (Futuro) `/etapa-2/`: Optimización de performance y mejoras de funcionalidades.

---

## Estado Actual

- [x] API local desarrollada.
- [x] Traducción de libros grandes funcional.
- [x] Integración con Calibre.
- [ ] Mejoras de velocidad y configuración dinámica de parámetros (próximamente).

---

## Instalación general

1. Clonar el repositorio.
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Iniciar el servidor:
   ```bash
   cd etapa-1
   uvicorn main:app --reload
   ```

---

## Créditos

- Modelo: [NLLB-200 distilled 600M](https://huggingface.co/facebook/nllb-200-distilled-600M)
- Framework: [FastAPI](https://fastapi.tiangolo.com/)
- Integración: Plugin [Ebook Translator](https://github.com/your-plugin-link) de Calibre.

---

## Licencia

MIT License (o definir licencia de uso).
