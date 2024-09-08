import time
from fasthtml.common import *

app, rt = fast_app(
    hdrs=(
        Style("""
            body {
                padding-top: 2rem;
                width: 70%;
                margin: 0 auto;
            }
            input {
                width: 100%;
                padding: 10px;
                margin-top: 10px;
            }
            button {
                width: 100%;
                padding: 10px;
                margin-top: 10px;
                border: none;
                cursor: pointer;
            }
            .indicator {
                display: none;
            }
            .htmx-request .indicator {
                display: inline-block;
            }
            .button-content {
                display: inline-block;
            }
            .htmx-request .button-content {
                display: none;
            }
        """),
    )
)

STORED_CONTENT = ""


@app.get("/")
def home():
    return Titled(
        "Input Demo",
        Div(
            P(f"Stored content: {STORED_CONTENT}", id="content"),
            Form(
                Input(
                    type="text",
                    name="user_input",
                    placeholder="Enter some text",
                    id="user_input",
                    _required=True,
                    minlength=3,
                ),
                Button(
                    Span("Submit", _class="button-content"),
                    Span(
                        "Loading...",
                        aria_busy="true",
                        _class="indicator",
                    ),
                    type="submit",
                    id="submit_button",
                ),
                hx_post="/submit",
                hx_target="#content",
                hx_disabled_elt="#user_input, #submit_button",
            ),
        ),
    )


@app.post("/submit")
async def submit(request):
    global STORED_CONTENT
    form_data = await request.form()
    STORED_CONTENT = form_data.get("user_input", "")
    time.sleep(1)
    return f"Stored content: {STORED_CONTENT}"
