import click
import uvicorn
import webbrowser
from threading import Timer

def auto_launch_browser(port: int) -> None:
    """
    Opens the system default web browser automatically to the application page.
    """
    webbrowser.open(f"http://localhost:{port}")

@click.group()
def main() -> None:
    """
    ⚡ CODEIT: Local Research-to-Notebook Compiler CLI Node.
    """
    pass

@main.command()
@click.option('--port', default=8080, help='Port to bind the local web interface server to.')
def serve(port: int) -> None:
    """
    Launches the FastAPI application engine locally under a lightweight Uvicorn server frame.
    """
    click.echo(f"🚀 Initializing Codeit Processing Suite Local Service Node on port {port}...")
    click.echo("💡 Ensuring local Ollama instance is active with model 'qwen2.5-coder:14b-instruct'...")
    
    # Fire browser initialization event wrapper exactly 1.5 seconds following stack stand up.
    Timer(1.5, auto_launch_browser, args=[port]).start()
    
    uvicorn.run("codeit.main:app", host="127.0.0.1", port=port, reload=False, log_level="info")

if __name__ == "__main__":
    main()
