import base64
import importlib
import json
import os
import urllib.error
import urllib.request
from dotenv import load_dotenv

load_dotenv(override=True)


def _get_hf_inference_client():
    try:
        module = importlib.import_module("huggingface_hub")
        return getattr(module, "InferenceClient", None)
    except Exception:
        return None


def _fallback_caption(sentiment="neutral", length="short"):
    base = "A beautiful moment captured."
    tone = (sentiment or "neutral").strip().lower()
    size = (length or "short").strip().lower()

    if tone in {"happy", "joyful", "excited"}:
        base = "A joyful moment full of warmth and energy."
    elif tone in {"sad", "melancholic", "lonely"}:
        base = "A quiet moment wrapped in emotion."
    elif tone in {"aesthetic", "calm", "peaceful"}:
        base = "An aesthetic frame with calm, balanced vibes."

    if size in {"short", "1", "one"}:
        return base
    if size in {"medium", "2", "two"}:
        return f"{base} It feels like a scene from a story you want to revisit."
    return f"{base} It captures details, mood, and memory in a way that lingers long after the moment passes."


def _normalize_length(length):
    value = (str(length).strip().lower() if length is not None else "short")
    if value in {"short", "medium", "long"}:
        return value

    try:
        num = int(value)
    except Exception:
        return "short"

    if num <= 1:
        return "short"
    if num == 2:
        return "medium"
    return "long"


def _stylize_caption(raw_caption, sentiment, normalized_length):
    caption = (raw_caption or "").strip()
    if not caption:
        return None

    tone = (sentiment or "neutral").strip().lower()
    prefix_map = {
        "happy": "Feeling on top of the world.",
        "joyful": "Pure joy in one frame.",
        "excited": "Energy turned all the way up.",
        "sad": "A soft moment that says a lot.",
        "melancholic": "A thoughtful pause in time.",
        "lonely": "A quiet frame with deep feeling.",
        "aesthetic": "Clean lines and perfect mood.",
        "calm": "Everything slows down here.",
        "peaceful": "Stillness done beautifully.",
    }

    prefix = prefix_map.get(tone)
    if prefix and not caption.lower().startswith(prefix.lower()):
        caption = f"{prefix} {caption}"

    if normalized_length == "short":
        return caption

    if normalized_length == "medium":
        return f"{caption} It feels like a scene worth staying in a little longer."

    return (
        f"{caption} Every detail adds to the atmosphere, turning a simple frame into a memory "
        "that lingers long after the moment passes."
    )


def _huggingface_caption(image_bytes, sentiment, normalized_length):
    hf_url = os.getenv("HUGGINGFACE_API_URL", "").strip()
    hf_router_url = os.getenv("HUGGINGFACE_ROUTER_API_URL", "").strip()
    configured_models = os.getenv(
        "HUGGINGFACE_MODELS",
        "Salesforce/blip-image-captioning-base,nlpconnect/vit-gpt2-image-captioning,Salesforce/blip-image-captioning-large",
    ).strip()
    hf_token = os.getenv("HUGGINGFACE_API_KEY", "").strip()

    model_ids = [m.strip() for m in configured_models.split(",") if m.strip()]

    inference_client_cls = _get_hf_inference_client()
    if inference_client_cls is not None:
        client = inference_client_cls(api_key=hf_token or None)
        for model_id in model_ids:
            try:
                result = client.image_to_text(image=image_bytes, model=model_id)
                generated_text = None

                if isinstance(result, str):
                    generated_text = result.strip()
                elif isinstance(result, dict):
                    generated_text = (result.get("generated_text") or "").strip()
                elif isinstance(result, list) and result:
                    generated_text = (result[0].get("generated_text") or "").strip()

                if generated_text:
                    return _stylize_caption(generated_text, sentiment, normalized_length)
            except Exception as e:
                print(f"[caption] Hugging Face client model failed ({model_id}): {type(e).__name__}: {e}")

    headers = {"Content-Type": "application/octet-stream"}
    if hf_token:
        headers["Authorization"] = f"Bearer {hf_token}"

    # Allow explicit single URL overrides while still keeping model-based fallback.
    endpoints = []
    if hf_url:
        endpoints.append(hf_url)
    if hf_router_url and hf_router_url != hf_url:
        endpoints.append(hf_router_url)

    for model_id in model_ids:
        api_endpoint = f"https://api-inference.huggingface.co/models/{model_id}"
        router_endpoint = f"https://router.huggingface.co/hf-inference/models/{model_id}"
        if api_endpoint not in endpoints:
            endpoints.append(api_endpoint)
        if router_endpoint not in endpoints:
            endpoints.append(router_endpoint)

    last_error = None
    for endpoint in endpoints:
        req = urllib.request.Request(
            endpoint,
            data=image_bytes,
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read().decode("utf-8")
                data = json.loads(raw)

                if isinstance(data, dict) and data.get("error"):
                    raise RuntimeError(data.get("error"))

                if not isinstance(data, list) or not data:
                    return None

                generated_text = (data[0].get("generated_text") or "").strip()
                return _stylize_caption(generated_text, sentiment, normalized_length)
        except urllib.error.HTTPError as e:
            last_error = e
            if e.code in {404, 410}:
                continue
            raise

    if last_error is not None:
        raise last_error

    return None


def _ollama_caption(image_bytes, mime_type, sentiment, normalized_length):
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434").rstrip("/")
    ollama_model = os.getenv("OLLAMA_MODEL", "llava")
    endpoint = f"{ollama_url}/api/generate"
    b64 = base64.b64encode(image_bytes).decode("utf-8")

    prompt = (
        "You are an Instagram caption assistant. "
        f"Write one {normalized_length} caption with a {sentiment} tone. "
        "No hashtags. Keep it natural and original."
    )

    payload = {
        "model": ollama_model,
        "prompt": prompt,
        "images": [b64],
        "stream": False,
    }

    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        text = (data.get("response") or "").strip()
        return text or None


def generate_caption(image_bytes, mime_type="image/jpeg", sentiment="neutral", length="short"):
    """Generate a caption using free providers with deterministic fallback."""
    normalized_length = _normalize_length(length)
    provider = os.getenv("CAPTION_PROVIDER", "huggingface").strip().lower()

    if not image_bytes:
        print("[caption] Using fallback: empty image payload")
        return _fallback_caption(sentiment=sentiment, length=normalized_length)

    if provider in {"ollama", "auto"}:
        try:
            text = _ollama_caption(image_bytes, mime_type, sentiment, normalized_length)
            if text:
                return text
        except urllib.error.URLError as e:
            print(f"[caption] Ollama unavailable: {type(e).__name__}: {e}")
        except Exception as e:
            print(f"[caption] Ollama failed: {type(e).__name__}: {e}")

    if provider == "ollama":
        print("[caption] Using fallback: CAPTION_PROVIDER=ollama but Ollama request failed")
        return _fallback_caption(sentiment=sentiment, length=normalized_length)

    try:
        text = _huggingface_caption(image_bytes, sentiment, normalized_length)
        if text:
            return text
        print("[caption] Using fallback: Hugging Face returned empty result")
        return _fallback_caption(sentiment=sentiment, length=normalized_length)
    except urllib.error.HTTPError as e:
        reason = None
        try:
            reason = e.read().decode("utf-8")
        except Exception:
            reason = str(e)
        print(f"[caption] Hugging Face HTTP error: {e.code}: {reason}")
        return _fallback_caption(sentiment=sentiment, length=normalized_length)
    except Exception as e:
        print(f"[caption] Using fallback: Hugging Face request failed: {type(e).__name__}: {e}")
        return _fallback_caption(sentiment=sentiment, length=normalized_length)