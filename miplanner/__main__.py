"""Main app module."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "backend.server:app",
        reload=True,
    )
