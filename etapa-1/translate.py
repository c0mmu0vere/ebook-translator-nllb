from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch


def load_model():
    """Carga modelo NLLB-200 distilled 600M."""
    model_name = "facebook/nllb-200-distilled-600M"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    if torch.cuda.is_available():
        model = model.to("cuda")
    return model, tokenizer


def translate(text, model, tokenizer, source_lang="eng_Latn", target_lang="spa_Latn"):
    """Traduce texto usando el modelo."""
    try:
        tokenizer.src_lang = source_lang
        inputs = tokenizer(text, return_tensors="pt",
                            truncation=True, padding=True)

        if torch.cuda.is_available():
            inputs = {k: v.to("cuda") for k, v in inputs.items()}

        # Importante: usamos convert_tokens_to_ids
        translated = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids(target_lang),
            max_new_tokens=1000
        )
        return tokenizer.batch_decode(translated, skip_special_tokens=True)[0]

    except Exception as e:
        return f"Error en traducción: {str(e)}"


if __name__ == "__main__":
    model, tokenizer = load_model()
    test_text = "When deploying a microservice architecture, consider using service mesh like Istio for traffic management between pods in your Kubernetes cluster, while ensuring zero-trust security with mutual TLS authentication."
    print(f"Original: {test_text}")
    print(f"Traducido: {translate(test_text, model, tokenizer)}")
