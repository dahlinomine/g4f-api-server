"""
g4f OpenAI-compatible API server for CZAR agent fleet.
No HAR files, no browser cookies — pure free providers only.
Replaces ChatAnywhere with zero-cost, no-auth providers.
"""
import os
import logging
import g4f
from g4f.api import create_app
from g4f.config import AppConfig

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

PORT = int(os.environ.get("PORT", 8080))

# PollinationsAI: confirmed working, no auth, <2s response, model: openai-fast
# Yqcloud was timing out (>30s) on Railway as of 2026-03-23.
# Without this, g4f routes to Copilot/Bing which need HAR cookies → 422/401 on Railway.
AppConfig.provider = "PollinationsAI"
logger.info("Default provider locked to: PollinationsAI (no-auth, fast)")
logger.info("Fallback chain: Qwen_Qwen_3 → DeepInfra → Groq")

# No-auth provider chain (reference — AppConfig.provider handles default routing)
PROVIDER_CHAIN = [
    g4f.Provider.PollinationsAI,  # Primary: no auth, <2s, model: openai-fast
    g4f.Provider.Qwen_Qwen_3,    # Fallback 1: qwen-3-235b, 32K ctx, no auth
    g4f.Provider.DeepInfra,      # Fallback 2: MiniMax-M2.5, no auth
    g4f.Provider.Groq,           # Fallback 3: gpt-oss-120b, no auth
]

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting g4f API on port {PORT}")
    logger.info(f"OpenAI-compatible endpoint: http://0.0.0.0:{PORT}/v1")
    logger.info(f"Models endpoint: http://0.0.0.0:{PORT}/v1/models")

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
