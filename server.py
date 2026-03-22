"""
g4f OpenAI-compatible API server for CZAR agent fleet.
Replaces ChatAnywhere with zero-cost free providers.
"""
import os
import asyncio
import logging
from g4f.api import create_app

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

PORT = int(os.environ.get("PORT", 8080))

# Preferred providers for CZAR workload (large context, no auth)
PREFERRED_PROVIDERS = [
    "Qwen_Qwen_3",          # qwen-3-235b — best free, 32K ctx
    "DeepInfra",             # deepseek-r1, llama-4-scout
    "Blackbox",              # gpt-4o, claude-3.7 — fast
    "PollinationsAI",        # gpt-4o-mini — reliable fallback
]

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting g4f API on port {PORT}")
    logger.info(f"OpenAI-compatible endpoint: http://0.0.0.0:{PORT}/v1")
    logger.info(f"Models endpoint: http://0.0.0.0:{PORT}/v1/models")
    
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
