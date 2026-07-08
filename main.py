from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import time
import uuid

app = FastAPI()

EMAIL = "24f2008116@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-5ejaba.example.com"


@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    start_time = time.time()

    if request.method == "OPTIONS":
        response = Response(status_code=204)
    else:
        response = await call_next(request)

    process_time = time.time() - start_time

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{process_time:.6f}"

    origin = request.headers.get("Origin")

    if origin == ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = origin

    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"

    return response


@app.get("/stats")
async def stats(values: str = ""):
    try:
        nums = [int(x) for x in values.split(",") if x.strip()]
    except:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid values"}
        )

    if not nums:
        return JSONResponse(
            status_code=400,
            content={"error": "No values"}
        )

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": round(sum(nums) / len(nums), 6)
    }
