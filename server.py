"""
g4f OpenAI-compatible API server for CZAR agent fleet.
Forces Yqcloud as default provider — no HAR files or browser cookies needed.
Replaces ChatAnywhere with zero-cost free providers.
"""
import os
import logging
import g4f
from g4f.api import create_app
from g4f.config import AppConfig

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

PORT = int(os.environ.get("PORT", 8080))

# Force Yqcloud as the default provider for ALL requests.
# Yqcloud: no auth, no HAR files, supports multi-turn conversations.
# Without this, g4f tries Copilot/Bing which require browser cookies → Railway 422/401 errors.
AppConfig.provider = "Yqcloud"
logger.info("Default provider locked to: Yqcloud (no-auth, multi-turn)")
logger.info("Fallback order if Yqcloud fails: PollinationsAI → Blackbox → DeepInfra")

# Preferred no-auth providers for reference (used when model-specific routing kicks in)
PROVIDER_CHAIN = [
    g4f.Provider.Yqcloud,         # Primary: no auth, multi-turn, reliable
    g4f.Provider.PollinationsAI,  # Fallback 1: gpt-4o-mini, no auth
    g4f.Provider.Blackbox,        # Fallback 2: gpt-4o, fast
    g4f.Provider.DeepInfra,       # Fallback 3: deepseek-r1, llama-4-scout
]

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting g4f API on port {PORT}")
    logger.info(f"OpenAI-compatible endpoint: http://0.0.0.0:{PORT}/v1")
    logger.info(f"Models endpoint: http://0.0.0.0:{PORT}/v1/models")

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
