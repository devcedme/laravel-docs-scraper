from rich.console import Console

console = Console()

def log_success(message):
    console.print(f"[bold green]{message}[/bold green]")

def log_warning(message):
    console.print(f"[bold yellow]{message}[/bold yellow]")

def log_error(message):
    console.print(f"[bold red]{message}[/bold red]")

def log_info(message):
    console.print(f"[cyan]{message}[/cyan]")

def log(message):
    console.print(message)
