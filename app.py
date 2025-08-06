import uvicorn
# from src.main import app

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="localhost", port=8000, reload=True)