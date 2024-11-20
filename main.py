from fastapi import FastAPI
from contas_a_pagar_e_receber.routes.contas_a_pagar_e_receber_router import router
import uvicorn


app = FastAPI()


@app.get("/")
def fast_api() -> str:
    """API no AR XD"""
    return "Hello, FastAPI. Here We Go!!!"


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
