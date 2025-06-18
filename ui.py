import questionary

def prompt_for_version(versions):
    # Prompts the user with an interactive list of versions.
    version_choices = [v['name'] for v in versions]

    selected_name = questionary.select(
        "Please select a version to scrape (Arrow keys to navigate, Enter to confirm):",
        choices=version_choices
    ).ask()

    # If user cancels the scraping process, the result is None
    if selected_name is None:
        return None

    # Find and return the full dictionary for the selected version
    for version in versions:
        if version['name'] == selected_name:
            return version
    
    return None
