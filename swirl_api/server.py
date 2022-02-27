from fastapi import FastAPI


app = FastAPI(debug=True)


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.get("/api/v1/swirl/calculate/{expr}")
async def calculate(expr: str):
    return {"result": eval(f"{expr}")}
