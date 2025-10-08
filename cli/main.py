import datetime
import typer
from pathlib import Path
from rich.console import Console

from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live
from rich.columns import Columns
from rich.markdown import Markdown
from rich.layout import Layout
from rich.text import Text
from rich.live import Live
from rich.table import Table
from collections import deque
import time
from rich.tree import Tree
from rich import box
from rich.align import Align
from rich.rule import Rule

from processdesignagents.graph.process_design_graph import ProcessDesignGraph
from processdesignagents.default_config import DEFAULT_CONNFIG
from cli.utils import *

console = Console()

app = typer.Typer(
    name="ProcessDesignAgents",
    help="ProcessDesignAgents CLI: Multi-Agents LLM Framework for Chemical Process Engineering Design.",
    add_completion=True,
)

def get_user_selections():
    """Get all user selections before starting the analysis display."""
    # Display ASCII art welcome message
    with open("./cli/static/welcome.txt", "r") as f:
        welcome_ascii = f.read()

    # Create welcome box content
    welcome_content = f"{welcome_ascii}\n"
    welcome_content += "[bold green]ProcessDesignAgents: Multi-Agents LLM Framework for Chemical Process Engineering Design - CLI[/bold green]\n\n"
    welcome_content += "[bold]Workflow Steps:[/bold]\n"
    welcome_content += "I. Analyst Team → II. Research Team → III. Designer Team → IV. Lead Process Design Engineer\n\n"
    welcome_content += (
        "[dim]Built by [E-PT-PX] inspired by (https://github.com/TauricResearch)[/dim]"
    )
    
    # Create and center the welcome box
    welcome_box = Panel(
        welcome_content,
        border_style="green",
        padding=(1, 2),
        title="Welcome to TradingAgents",
        subtitle="Multi-Agents LLM Financial Trading Framework",
    )
    console.print(Align.center(welcome_box))
    console.print()  # Add a blank line after the welcome box

    # Create a boxed questionnaire for each step
    def create_question_box(title, prompt, default=None):
        box_content = f"[bold]{title}[/bold]\n"
        box_content += f"[dim]{prompt}[/dim]"
        if default:
            box_content += f"\n[dim]Default: {default}[/dim]"
        return Panel(box_content, border_style="blue", padding=(1, 2))

    # Step 1: Ticker symbol
    console.print(
        create_question_box(
            "Step 1: Problem Statement", "Enter the problem to analyze", "Design process system"
        )
    )
    
    problem_statement = get_problem_statement()
    
    # Step 2: Thinking agents
    console.print(
        create_question_box(
            "Step 2: Thinking Agents", "Select your thinking agents for analysis"
        )
    )
    selected_shallow_thinker = select_shallow_thinking_agent()
    selected_deep_thinker = select_deep_thinking_agent()
    
    return {
        "problem_statement": problem_statement,
        "quick_think_llm": selected_shallow_thinker,
        "deep_think_llm": selected_deep_thinker
    }

def run_analysis():
    # First get all user selections
    selections = get_user_selections()

    # Create config with selected parameter from selections
    config = DEFAULT_CONNFIG.copy()
    config["quick_think_llm"] = selections["quick_think_llm"]
    config["deep_think_llm"] = selections["deep_think_llm"]

    graph = ProcessDesignGraph(debug=True, config=config)
    
@app.command()
def main():
    run_analysis()

if __name__ == "__main__":
    app()