from fastapi import FastAPI, HTTPException, Body
from translate import load_model, translate
import logging
import time
from functools import lru_cache
from typing import List
import uuid

# 1. Logger mejorado (registra artículo original y traducción)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("translation.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 2. Configuración de procesamiento
class Config:
    CHUNK_SIZE = 800  # Tamaño máximo por chunk
    MAX_DELAY = 0.05  # Delay entre chunks (50ms)
    MAX_CONCURRENT_REQUESTS = 1  # ¡Nuevo! Procesar una solicitud a la vez

app = FastAPI(title="Traductor Técnico NLLB (Serializado)")
request_queue = []  # Cola para procesamiento serializado

# 3. Carga del modelo (igual que antes)
model, tokenizer = None, None
def load_models():
    global model, tokenizer
    model, tokenizer = load_model()
    translate("Model warming up", model, tokenizer, "eng_Latn", "spa_Latn")
    logger.info("Modelo cargado y listo")

# 4. Cache de traducciones (mejorado)
@lru_cache(maxsize=5000)
def cached_translate(text: str, source: str, target: str) -> str:
    return translate(text, model, tokenizer, source, target)

# 5. Endpoint principal (ahora serializado)
@app.post("/translate")
async def translate_endpoint(
    text: str = Body(...),
    target: str = Body("spa_Latn"),
    source: str = Body("eng_Latn")
):
    start_time = time.time()
    request_id = str(uuid.uuid4())[:8]  # ID único para tracking
    
    try:
        # Esperar si hay solicitudes en proceso
        while len(request_queue) >= Config.MAX_CONCURRENT_REQUESTS:
            time.sleep(0.1)
        
        request_queue.append(request_id)
        logger.info(f"[{request_id}] Inicio | Artículo: '{text[:50]}...' | Chars: {len(text)}")

        # Procesamiento por chunks (adaptativo)
        if len(text) <= Config.CHUNK_SIZE:
            translated = cached_translate(text, source, target)
            chunks_used = 1
        else:
            chunks = [text[i:i+Config.CHUNK_SIZE] for i in range(0, len(text), Config.CHUNK_SIZE)]
            translated_chunks = []
            for i, chunk in enumerate(chunks):
                translated_chunks.append(cached_translate(chunk, source, target))
                if i < len(chunks) - 1:
                    time.sleep(Config.MAX_DELAY)
            translated = "".join(translated_chunks)
            chunks_used = len(chunks)

        # Registro completo en logs
        logger.info(
            f"[{request_id}] Fin | "
            f"Tiempo: {time.time() - start_time:.2f}s | "
            f"Chars: {len(text)} | "
            f"Chunks: {chunks_used}\n"
            f"Original: {text[:100]}...\n"
            f"Traducido: {translated[:100]}..."
        )

        return {
            "choices": [{
                "message": {
                    "content": translated
                }
            }]
        }

    except Exception as e:
        logger.error(f"[{request_id}] Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    finally:
        if request_id in request_queue:
            request_queue.remove(request_id)

if __name__ == "__main__":
    load_models()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)