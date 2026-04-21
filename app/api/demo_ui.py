from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["demo-ui"])


@router.get("/demo/login", response_class=HTMLResponse)
def login_page():
    return """
    <html>
        <body>
            <h2>Login Page</h2>
            <form action="/demo/login" method="post">
                <input type="text" name="username" placeholder="Username" />
                <input type="password" name="password" placeholder="Password" />
                <button type="submit">Login</button>
            </form>
        </body>
    </html>
    """


@router.post("/demo/login", response_class=HTMLResponse)
def login_submit(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "admin":
        return "<h3>Login successful</h3>"
    return "<h3 style='color:red;'>Login failed</h3>"