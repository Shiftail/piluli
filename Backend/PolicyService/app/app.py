import logging
from typing import Any, Dict

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from app import config, schemes
from app.polices.requestenforcer import EnforceResult, RequestEnforcer

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-9s %(message)s"
)

app_config: config.Config = config.load_config()

policy_checker: RequestEnforcer = RequestEnforcer(
    app_config.policies_config_path, app_config.jwt_secret.get_secret_value()
)

class App(FastAPI):
    def openapi(self) -> Dict[str, Any]:
        scheme_builder = schemes.SchemeBuilder(super().openapi())

        for target in policy_checker.services:
            resp = httpx.get(target.openapi_scheme)
            scheme_builder.append(resp.json(), inject_token_in_swagger=target.inject_token_in_swagger)
        return scheme_builder.result


app = App()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)
@app.api_route("/{path_name:path}", methods=["GET", "DELETE", "PATCH", "POST", "PUT", "HEAD", "OPTIONS", "CONNECT", "TRACE"])
async def catch_all(request: Request, path_name: str):
    enforce_result: EnforceResult = policy_checker.enforce(request)

    # Если доступ не разрешен, проверим, была ли ошибка авторизации
    if not enforce_result.access_allowed:
        # Если токен не передан или невалиден, вернем 401 Unauthorized
        token_data = policy_checker._RequestEnforcer__extract_token_data(request)
        if token_data is None:
            return JSONResponse(content={'message': 'User not authorized'}, status_code=401)

        # Если доступ запрещен по политике, можно вернуть 403 (Forbidden), но это зависит от политики
        return JSONResponse(content={'message': 'Access denied'}, status_code=403)

    # Если доступ разрешен, проксируем запрос к целевому сервису
    print(enforce_result.redirect_service, path_name)

    client = httpx.AsyncClient(base_url=enforce_result.redirect_service)
    url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
    rp_req = client.build_request(request.method, url, headers=request.headers.raw, content=await request.body())
    rp_resp = await client.send(rp_req, stream=True)
    
    # Возвращаем ответ от целевого сервиса
    return StreamingResponse(
        rp_resp.aiter_raw(),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers
    )
