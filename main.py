from app.config.config import load_config
from app.factory import create_app

config = load_config()
app = create_app(config)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=config.server.host, port=config.server.port, reload=True)
