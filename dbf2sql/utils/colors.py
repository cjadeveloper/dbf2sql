import click


def show_all_click_colors() -> None:

    all_colors = (
        "black",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
        "bright_black",
        "bright_red",
        "bright_green",
        "bright_yellow",
        "bright_blue",
        "bright_magenta",
        "bright_cyan",
        "bright_white",
    )

    for color in all_colors:
        click.echo(click.style(f"Colored {color}", fg=color))
    for color in all_colors:
        click.echo(click.style(f"Colored {color} and bold", fg=color, bold=True))
    for color in all_colors:
        click.echo(click.style(f"Reverse colored {color}", fg=color, reverse=True))
