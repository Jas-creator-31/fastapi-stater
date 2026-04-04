from fastapi import FastAPI, Request
# from typing import Optional
from user_agents import parse
from src.features.auth.models import UserAgentInfo
from src.core.context.request_context import RequestContext, request_metadata_context

def register_middleware(app: FastAPI):
    
    @app.middleware('http')
    async def request_metadata(
        req: Request, 
        call_next, 
    ):
        user_agent = req.headers.get('user-agent', "")
        raw_ua = parse(user_agent)
        client_ip: str = req.headers.get("x-forwarded-for", req.client.host) # type: ignore

        ua = UserAgentInfo(
                browser=raw_ua.browser.family,
                device=raw_ua.device.family,
                os=raw_ua.os.family,
                is_mobile=raw_ua.is_mobile
            )

        new_metadata = RequestContext(client_ip=client_ip, user_agent=ua)
        token = request_metadata_context.set(new_metadata)

        try: 
            return await call_next(req)
        
        finally:
            request_metadata_context.reset(token)
