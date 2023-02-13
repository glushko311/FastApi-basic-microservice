import os
import uvicorn


class DotEnvNotExistException(FileNotFoundError):
    pass


if __name__ == "__main__":
    env_file_dir = os.path.join(os.path.abspath(os.curdir), ".env")
    a = os.path.exists(env_file_dir)
    if not os.path.exists(env_file_dir):
        raise DotEnvNotExistException(f".env file not found by path {env_file_dir}")
    uvicorn.run('src.app:app', host="0.0.0.0", port=8000, reload=True)

