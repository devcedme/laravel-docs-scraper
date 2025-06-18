import os
import sys
import re
import time

from rich.live import Live
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn

from scraper import get_available_versions, get_doc_links, scrape_and_save
from ui import prompt_for_version
from logger import log_info, log_success, log_warning, log_error, console

def run_scraper():
    # 1. Fetch available versions
    log_info("Searching for available Laravel versions...")
    versions = get_available_versions()
    if not versions:
        log_error("Could not find any versions. Aborting.")
        return
    log_success(f"Found {len(versions)} versions.")

    # 2. Prompt user for the desired version
    selected_version = prompt_for_version(versions)
    if not selected_version:
        log_warning("\nNo version selected. Exiting program.")
        return
        
    base_url = selected_version['url']
    
    # 3. Create a dynamic folder name based on the version
    version_slug_match = re.search(r'/docs/([^/]+)', base_url)
    if not version_slug_match:
        log_error(f"Error: Could not extract version slug from URL: {base_url}")
        return
        
    version_slug = version_slug_match.group(1)
    
    parent_dir = "docs"
    output_dir = os.path.join(parent_dir, version_slug)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    log_info(f"\nFiles will be saved in the '{output_dir}' folder.")

    # 4. Collect links for the selected version
    links = get_doc_links(base_url)
    if not links:
        log_error("No links to scrape found. Aborting.")
        return
    log_success(f"Found {len(links)} documentation pages.")
        
    # 5. Set up and run the scraping process within a live display
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None, style="bold cyan", complete_style="bold green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("({task.completed} of {task.total})"),
        console=console,
    )
    
    with Live(progress, vertical_overflow="visible", screen=False) as live:
        try:
            task_id = progress.add_task(f"Scraping v{version_slug}", total=len(links))

            for link in links:
                scrape_and_save(link, output_dir)
                progress.update(task_id, advance=1)
                time.sleep(0.1)
            
            live.stop()
            log_success(f"\nScraping complete!")
            log_success(f"All files for version '{version_slug}' have been saved in the '{output_dir}' folder.")

        except KeyboardInterrupt:
            live.stop()
            log_warning("\n\nScraping process canceled by user. Exiting program.")
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

if __name__ == "__main__":
    run_scraper()
