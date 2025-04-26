# Etapa 1 - Ebook Translator NLLB

## Descripción

Primera etapa del proyecto "Ebook Translator NLLB".  
En esta etapa se desarrolló una API local usando FastAPI que permite traducir libros electrónicos de manera eficiente utilizando un modelo de Meta NLLB (`nllb-200-distilled-600M`).  
La API se integra con el plugin "Ebook Translator" de Calibre para realizar traducciones directas.

---

## Funcionalidades implementadas

- Carga del modelo de traducción NLLB.
- Servidor API local (`localhost:8000`) para recibir texto y devolver traducciones.
- Gestión de traducciones por chunk para soportar textos grandes.
- Logs de actividad y errores para control del proceso.
- Integración con Calibre usando el plugin Ebook Translator.

---

## Requisitos

- Python 3.10+
- FastAPI
- Uvicorn
- Transformers
- PyTorch
- CUDA (opcional para acelerar procesamiento)

---

## Uso

1. Iniciar el servidor local:
   ```bash
   uvicorn main:app --reload
   ```

2. Configurar Calibre para apuntar a:
   ```
   http://localhost:8000/translate
   ```

3. Iniciar la traducción desde Calibre.

---

## Checklist de Buenas Prácticas para traducir libros grandes

### Antes de traducir:

- [ ] Guardar backup del libro original.
- [ ] Confirmar que el servidor FastAPI está corriendo.
- [ ] Confirmar que el modelo está usando CUDA (si está disponible).
- [ ] Configurar correctamente los idiomas en Calibre.

### Durante la traducción:

- [ ] Monitorear uso de CPU/GPU.
- [ ] Evitar tareas pesadas en paralelo.
- [ ] Revisar logs periódicamente.

### Después de traducir:

- [ ] Validar la calidad de la traducción.
- [ ] Corregir manualmente errores menores.
- [ ] Guardar el archivo traducido aparte.
- [ ] Documentar tiempos y observaciones.

---

## Estado del Proyecto

✅ Funcionalidad completa para traducir libros grandes localmente.  
⚡ Preparado para optimizaciones futuras en Etapa 2.
