"""Convenience launcher: uvicorn backend.main:app using HOST/PORT from .env."""

from __future__ import annotations

import os

import uvicorn

from backend.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
        reload=False,
    )
