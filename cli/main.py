from datetime import datetime
import typer
from pathlib import Path
from functools import wraps
from typing import List
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
from processdesignagents.default_config import DEFAULT_CONFIG
from cli.utils import *
from processdesignagents.agents.utils.json_tools import (
    convert_streams_json_to_markdown,
    convert_equipment_json_to_markdown,
    convert_risk_json_to_markdown,
)

console = Console()

app = typer.Typer(
    name="ProcessDesignAgents",
    help="ProcessDesignAgents CLI: Multi-Agents LLM Framework for Chemical Process Engineering Design.",
    add_completion=True,
)


# Create a deque to store recent messages with a maximum length
class MessageBuffer:
    def __init__(self, max_length=100):
        self.messages = deque(maxlen=max_length)
        self.tool_calls = deque(maxlen=max_length)
        self.current_report = None
        self.final_report = None  # Store the complete final report
        self.agents_status = {
            # Analyst Team
            "Process Requirement Analyst": "pending",
            "Design Basis Analyst": "pending",
            # Research Team
            "Innovative Researcher": "pending",
            "Conservative Researcher": "pending",
            "Concept Detailer": "pending",
            # Designer Team
            "Basic PFD Designer": "pending",
            "Stream Data Builder": "pending",
            "Equipment List Builder": "pending",
            "Stream Data Estimator": "pending",
            "Equipment Sizing Agent": "pending",
            # Lead Process Design Engineer
            "Safety Risk Analyst": "pending",
            "Project Manager": "pending"
        }
        self.current_agent = None
        self.report_sections = {
            "requirements": None,
            "research_concepts": None,
            "selected_concept_details": None,
            "design_basis": None,
            "basic_pfd": None,
            "basic_stream_data": None,
            "basic_hmb_results": None,
            "basic_equipment_template": None,
            "safety_risk_analyst_report": None,
            "project_manager_report": None,
        }
    
    def add_message(self, message_type, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.messages.append((timestamp, message_type, message))
        
    def add_tool_call(self, tool_call, agrs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tool_calls.append((timestamp, tool_call, agrs))
        
    def update_agent_status(self, agent, status):
        if agent in self.agents_status:
            self.agents_status[agent] = status
            self.current_agent = agent
            
    def update_report_section(self, section, report):
        if section in self.report_sections:
            if section in {"basic_stream_data", "basic_hmb_results"} and report:
                report = convert_streams_json_to_markdown(report)
            elif section == "basic_equipment_template" and report:
                report = convert_equipment_json_to_markdown(report)
            elif section == "safety_risk_analyst_report" and report:
                report = convert_risk_json_to_markdown(report)
            self.report_sections[section] = report
            self._update_current_report()
            
    def _update_current_report(self):
        # For the panel display, only show the most recently update section
        latest_section = None
        latest_content = None
        
        # Find the most recently updated section
        for section, report in self.report_sections.items():
            if report is not None:
                latest_section = section
                latest_content = report
                break

        if latest_section and latest_content:
            # Format the current section for display
            section_titles = {
                "requirements": "Process Requirements",
                "research_concepts": "Concept Portfolio",
                "selected_concept_details": "Selected Concept Detail",
                "design_basis": "Design Basis",
                "basic_pfd": "Basic Process Flow Diagram",
                "basic_stream_data": "Stream Data",
                "basic_hmb_results": "Heat & Material Balance",
                "basic_equipment_template": "Equipment Summary",
                "safety_risk_analyst_report": "Safety Risk Analyst Report",
                "project_manager_report": "Project Manager Report",
            }
            self.current_report = (
                f"### {section_titles[latest_section]}\n{latest_content}\n"
            )
        
        # Update the final complete report
        self._update_final_report()
        
    def _update_final_report(self):
        report_parts = []

        # Analyst Team Reports
        if any(
            self.report_sections[section]
            for section in [
                "requirements",
                "design_basis",
            ]
        ):
            report_parts.append("## Analyst Team Reports")
            if self.report_sections["requirements"]:
                report_parts.append(
                    f"### Process Requirements\n{self.report_sections['requirements']}"
                )
            if self.report_sections["design_basis"]:
                report_parts.append(
                    f"### Design Basis\n{self.report_sections['design_basis']}"
                )

        # Research Team Reports
        if any(
            self.report_sections[section]
            for section in [
                "research_concepts",
                "selected_concept_details",
            ]
        ):
            report_parts.append("## Research Team Reports")
            if self.report_sections["research_concepts"]:
                report_parts.append(
                    f"### Concept Portfolio\n{self.report_sections['research_concepts']}"
                )
            if self.report_sections["selected_concept_details"]:
                report_parts.append(
                    f"### Selected Concept Detail\n{self.report_sections['selected_concept_details']}"
                )

        # Designer Team Reports
        if any(
            self.report_sections[section]
            for section in [
                "basic_pfd",
                "basic_stream_data",
                "basic_hmb_results",
                "basic_equipment_template",
            ]
        ):
            report_parts.append("## Designer Team Reports")
            if self.report_sections["basic_pfd"]:
                report_parts.append(
                    f"### Basic Process Flow Diagram\n{self.report_sections['basic_pfd']}"
                )
            if self.report_sections["basic_stream_data"]:
                report_parts.append(
                    f"### Stream Data\n{self.report_sections['basic_stream_data']}"
                )
            if self.report_sections["basic_hmb_results"]:
                report_parts.append(
                    f"### Heat & Material Balance\n{self.report_sections['basic_hmb_results']}"
                )
            if self.report_sections["basic_equipment_template"]:
                report_parts.append(
                    f"### Equipment Summary\n{self.report_sections['basic_equipment_template']}"
                )

        # Lead Process Design Engineer Reports
        if any(
            self.report_sections[section]
            for section in [
                "safety_risk_analyst_report",
                "project_manager_report",
            ]
        ):
            report_parts.append("## Lead Process Design Engineer Reports")
            if self.report_sections["safety_risk_analyst_report"]:
                report_parts.append(
                    f"### Safety Risk Analyst Report\n{self.report_sections['safety_risk_analyst_report']}"
                )
            if self.report_sections["project_manager_report"]:
                report_parts.append(
                    f"### Project Manager Report\n{self.report_sections['project_manager_report']}"
                )

        self.final_report = "\n\n".join(report_parts) if report_parts else None

message_buffer = MessageBuffer()


def create_layout():
    """Create console layout for analysis display."""
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3),
    )
    layout["main"].split_column(
        Layout(name="upper", ratio=3), Layout(name="analysis", ratio=5)
    )
    layout["upper"].split_row(
        Layout(name="progress", ratio=2), Layout(name="messages", ratio=3)
    )
    return layout

def update_display(layout, snippet_text=None):
    # Header with welcome message
    layout["header"].update(
        Panel(
            "[bold green]Welcome to ProcessDesignAgents CLI[/bold green]\n"
            "[dim]© [GCME EPT-PX](https://github.com/may3rd)[/dim]",
            title="Welcome to ProcessDesignAgents",
            border_style="green",
            padding=(1, 2),
            expand=True,
        )
    )
    
    # Progress panel showing agent status
    progress_table = Table(
        show_header=True,
        header_style="bold magenta",
        show_footer=False,
        box=box.SIMPLE_HEAD,  # Use simple header wih horizontal lines
        title=None,  # Remove the redundant Progress title
        padding=(0, 2),  # Add horizontal padding
        expand=True,  # Make table expand to fill available space
    )
    progress_table.add_column("Team", style="cyan", justify="center", width=20)
    progress_table.add_column("Agent", style="green", justify="center", width=20)
    progress_table.add_column("Status", style="green", justify="center", width=20)

    # Group agents by team
    teams = {
        "Analyst Team": ["Process Requirement Analyst", "Design Basis Analyst"],
        "Research Team": ["Innovative Researcher", "Conservative Researcher", "Concept Detailer"],
        "Designer Team": [
            "Basic PFD Designer",
            "Stream Data Builder",
            "Stream Data Estimator",
            "Equipment List Builder",
            "Equipment Sizing Agent",
        ],
        "Lead Process Design Engineer": ["Safety Risk Analyst", "Project Manager"],
    }
    
    for team, agents in teams.items():
        # Add first agent with team name
        first_agent = agents[0]
        status = message_buffer.agents_status.get(first_agent, "pending")
        if status == "in_progress":
            spinner = Spinner(
                "dots", text="[blue]in_progress[/blue]", style="bold cyan"
            )
            status_cell = spinner
        else:
            status_color = {
                "pending": "yellow",
                "completed": "green",
                "error": "red",
            }.get(status, "white")
            status_cell = f"[{status_color}]{status}[/{status_color}]"
        progress_table.add_row(team, first_agent, status_cell)
        
        # Add remaining agents in team
        for agent in agents[1:]:
            status = message_buffer.agents_status.get(agent, "pending")
            if status == "in_progress":
                spinner = Spinner(
                    "dots", text="[blue]in_progress[/blue]", style="bold cyan"
                )
                status_cell = spinner
            else:
                status_color = {
                    "pending": "yellow",
                    "completed": "green",
                    "error": "red",
                }.get(status, "white")
                status_cell = f"[{status_color}]{status}[/{status_color}]"
            progress_table.add_row("", agent, status_cell)

        # Add horizontal line after each team
        progress_table.add_row("-" * 20, "-" * 20, "-" * 20, style="dim")

    layout["progress"].update(
        Panel(progress_table, title="Progress", border_style="cyan", padding=(1, 2))    
    )
    
    # Messages panel showing recent messages and tool calls
    message_table = Table(
        show_header=True,
        header_style="bold magenta",
        show_footer=False,
        box=box.MINIMAL,  # Use simple header wih horizontal lines
        show_lines=True,
        padding=(0, 1),  # Add horizontal padding
        expand=True,  # Make table expand to fill available space
    )
    message_table.add_column("Time", style="cyan", justify="center", width=8)
    message_table.add_column("Type", style="green", justify="center", width=10)
    message_table.add_column(
        "Content", style="white", no_wrap=False, ratio=1
    )  # Make content column expand
    
    # Combine tool calls and message
    all_messages = []
    
    # Add tool calls
    for timestamp, tool_call, args in message_buffer.tool_calls:
        # Truncate tool call args if too long
        if isinstance(args, str) and len(args) > 100:
            args = args[:97] + "..."
        all_messages.append((timestamp, "Tool", f"{tool_call}: {args}"))
    
    # Add regular messages
    for timestamp, message_type, content in message_buffer.messages:
        # covert content to string if if it's not already
        content_str = content
        if isinstance(content, List):
            # Handle list of content blocks (Anthropic format)
            text_parts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
                    elif item.get("type") == "tool_use":
                        text_parts.append(f"[Tool: {item.get('name', 'unknown')}]")
                else:
                    text_parts.append(str(item))
            content_str = " ".join(text_parts)
        elif not isinstance(content, str):
            content_str = str(content)

        # Truncate message content if too long
        if len(content_str) > 200:
            content_str = content_str[:197] + "..."
        all_messages.append((timestamp, message_type, content_str))
    
    # Sort messages by timestamp
    all_messages.sort(key=lambda x: x[0])
    
    # Calculate how many messages we can show based on available space
    # Start with a resaonable number and adjust based on content length
    max_messages = 12
    
    # Get the last N messages that will fit in the panel
    recent_messages = all_messages[-max_messages:]
    
    # Add messages to table
    for timestamp, message_type, content in recent_messages:
        # Format content with word wrapping
        wrapped_content = Text(content, overflow="fold")
        message_table.add_row(timestamp, message_type, wrapped_content)
        
    if snippet_text:
        message_table.add_row("", "Spinner", snippet_text)
    
    # Add a footer to indicate if messages were truncated
    if len(all_messages) > max_messages:
        message_table.footer = (
            f"[dim]Showing last {max_messages} of {len(all_messages)} messages[/dim]"
        )

    layout["messages"].update(
        Panel(message_table, title="Messages & Tools", border_style="blue", padding=(1, 2))
    )
    
    # Analysis panel showing current report
    if message_buffer.current_report:
        layout["analysis"].update(
            Panel(
                Markdown(message_buffer.current_report),
                title="Current Report",
                border_style="green",
                padding=(1, 2),
            )
        )
    else:
        layout["analysis"].update(
            Panel(
                "[italic]Waiting for analysis report...[/italic]",
                title="Current Report",
                border_style="green",
                padding=(1, 2),
            )
        )
    
    # Footer with statistics
    tool_calls_count = len(message_buffer.tool_calls)
    llm_calls_count = sum(
        1 for _, message_type, _ in message_buffer.messages if message_type == "Reasoning"
    )
    reports_count = sum(
        1 for content in message_buffer.report_sections.values() if content is not None
    )

    status_table = Table(show_header=False, box=None, padding=(0, 2), expand=True)
    status_table.add_column("Stats", justify="center")
    status_table.add_row(
        f"Tool Calls: {tool_calls_count} | LLM Calls: {llm_calls_count} | Generated Reports: {reports_count}"
    )
    
    layout["footer"].update(Panel(status_table, border_style="grey50"))

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
        title="Welcome to ProcessDesignAgents",
        subtitle="Multi-Agents LLM Process Design Framework",
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
            "Step 1: Problem Statement", "Enter the problem to analyze", "Design column separate methanal and water"
        )
    )
    
    problem_statement = get_problem_statement(console)
    
    # Step 2: Thinking agents
    console.print(
        create_question_box(
            "Step 2: Thinking Agents", "Select your thinking agents for analysis"
        )
    )
    selected_shallow_thinker = select_shallow_thinking_agent(console)
    selected_deep_thinker = select_deep_thinking_agent(console)
    
    return {
        "problem_statement": problem_statement,
        "quick_think_llm": selected_shallow_thinker,
        "deep_think_llm": selected_deep_thinker
    }
    
def get_problem_statement(console: Console):
    """Get problem statement from user input."""
    return typer.prompt("", default="Design column separate methanal and water")


def display_complete_report(final_state):
    """Display the complete analysis report using Rich panels."""
    console.print("\n[bold green]Complete Analysis Report[/bold green]\n")

    team_sections = [
        (
            "Analyst Team Reports",
            [
                ("requirements", "Process Requirements"),
                ("design_basis", "Design Basis"),
            ],
        ),
        (
            "Research Team Reports",
            [
                ("research_concepts", "Concept Portfolio"),
                ("selected_concept_details", "Selected Concept Detail"),
            ],
        ),
        (
            "Designer Team Reports",
            [
                ("basic_pfd", "Basic Process Flow Diagram"),
                ("basic_stream_data", "Stream Data"),
                ("basic_hmb_results", "Heat & Material Balance"),
                ("basic_equipment_template", "Equipment Summary"),
            ],
        ),
        (
            "Lead Process Design Engineer Reports",
            [
                ("safety_risk_analyst_report", "Safety Risk Analyst Report"),
                ("project_manager_report", "Project Manager Report"),
            ],
        ),
    ]

    found_any = False

    for team_title, sections in team_sections:
        rendered_sections = []
        for key, title in sections:
            report_content = final_state.get(key) or message_buffer.report_sections.get(key)
            if report_content:
                rendered_sections.append(
                    Panel(
                        Markdown(report_content),
                        title=title,
                        border_style="blue",
                        padding=(1, 2),
                    )
                )
        
        if rendered_sections:
            found_any = True
            # Combine sections either stacked or as columns depending on count
            if len(rendered_sections) == 1:
                content = rendered_sections[0]
            else:
                content = Columns(rendered_sections, expand=True)
            console.print(
                Panel(
                    content,
                    title=team_title,
                    border_style="green",
                    padding=(1, 2),
                )
            )

    if not found_any:
        console.print(
            Panel(
                "No reports were generated.",
                border_style="red",
                padding=(1, 2),
            )
        )

def update_research_team_status(status):
    """Update status for all research team agents."""
    research_team = [
        "Innovative Researcher",
        "Conservative Researcher",
        "Concept Detailer",
        "Design Basis Analyst",
        "Basic PFD Designer",
        "Stream Data Builder",
        "Equipment List Builder",
        "Stream Data Estimator",
        "Equipment Sizing Agent",
        "Safety Risk Analyst",
        "Project Manager",
    ]
    for agent in research_team:
        message_buffer.update_agent_status(agent, status)

def extract_content_string(content):
    """Extract string content from various message formats."""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        # Handle Anthropic's list format
        text_parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get('type') == 'text':
                    text_parts.append(item.get('text', ''))
                elif item.get('type') == 'tool_use':
                    text_parts.append(f"[Tool: {item.get('name', 'unknown')}]")
            else:
                text_parts.append(str(item))
        return ' '.join(text_parts)
    else:
        return str(content)

def run_analysis():
    # First get all user selections
    selections = get_user_selections()

    # Create config with selected parameter from selections
    config = DEFAULT_CONFIG.copy()
    config["quick_think_llm"] = selections["quick_think_llm"]
    config["deep_think_llm"] = selections["deep_think_llm"]

    graph = ProcessDesignGraph(debug=True, config=config)

    analysis_date = datetime.now().strftime("%Y%m%d_%H%M")
    results_dir = Path(config["results_dir"]) / analysis_date
    results_dir.mkdir(parents=True, exist_ok=True)
    report_dir = results_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    log_file = results_dir / "message_tool.log"
    log_file.touch(exist_ok=True)
    
    def save_message_decorator(obj, func_name):
        func = getattr(obj, func_name)
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            timestamp, message_type, content = obj.messages[-1]
            content = content.replace("\n", " ")
            with open(log_file, "a") as f:
                f.write(f"{timestamp}, {message_type}, {content}\n")
        return wrapper
    
    def save_tool_decorator(obj, func_name):
        func = getattr(obj, func_name)
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            timestamp, tool_name, args = obj.tool_calls[-1]
            args_str = ", ".join(f"{k}={v}" for k, v in args.items())
            with open(log_file, "a") as f:
                f.write(f"{timestamp}, [Tool Call] {tool_name}({args_str})\n")
        return wrapper
    
    def save_report_section_decorator(obj, func_name):
        func = getattr(obj, func_name)
        @wraps(func)
        def wrapper(section_name, content):
            func(section_name, content)
            if section_name in obj.report_sections and obj.report_sections[section_name] is not None:
                content = obj.report_sections[section_name]
                if content:
                    file_name = f"{section_name}.md"
                    with open(report_dir / file_name, "w") as f:
                        f.write(content)
        return wrapper
    
    message_buffer.add_message = save_message_decorator(message_buffer, "add_message")
    message_buffer.add_tool_call = save_tool_decorator(message_buffer, "add_tool_call")
    message_buffer.update_report_section = save_report_section_decorator(message_buffer, "update_report_section")
    
    # Now start the display layout
    layout = create_layout()

    with Live(layout, refresh_per_second=4) as live:
        # Initial display
        update_display(layout)
        
        # Add initial messages
        message_buffer.add_message("System", f"Problem: {selections['problem_statement']}")
        update_display(layout)
        
        # Reset agent status
        for agent in message_buffer.agents_status:
            message_buffer.update_agent_status(agent, "pending")
        
        # Reset report sections
        for section in message_buffer.report_sections:
            message_buffer.update_report_section(section, None)
        message_buffer.current_agent = None
        message_buffer.final_report = None
        
        # Update agent status to in_progress for the first analyst
        first_analyst = "Process Requirement Analyst"
        message_buffer.update_agent_status(first_analyst, "in_progress")
        update_display(layout)
        
        # Create spinner text
        spinner_text = (
            f"Analyzing the problem..."
        )
        update_display(layout, spinner_text)
        
        # Initialize state and get graph args
        init_agent_state = graph.propagator.create_initial_state(
            selections["problem_statement"]
        )
        args = graph.propagator.get_graph_args()
        
        # Stream the analysis
        trace = []
        for chunk in graph.graph.stream(init_agent_state, **args):
            if len(chunk.get("messages", [])) > 0:
                # Get the last message from the chunk
                last_message = chunk["messages"][-1]
                
                # Extract message content and type
                if hasattr(last_message, "content"):
                    content = extract_content_string(last_message.content)
                    msg_type = "Reasoning"
                else:
                    content = str(last_message)
                    msg_type = "System"
                
                # Add message to buffer
                message_buffer.add_message(msg_type, content)
                
                # If it's a tool call, add it to tool calls
                if hasattr(last_message, "tool_calls"):
                    for tool_call in last_message.tool_calls:
                        # Handle both dictionary and object tool calls
                        if isinstance(tool_call, dict):
                            message_buffer.add_tool_call(
                                tool_call["name"], tool_call["args"]
                            )
                        else:
                            message_buffer.add_tool_call(
                                tool_call.name, tool_call.args
                            )
                
                # Update reports and agent status based on chunk content
                # Analyst Team Outputs
                if chunk.get("requirements"):
                    message_buffer.update_report_section("requirements", chunk["requirements"])
                    message_buffer.update_agent_status("Process Requirement Analyst", "completed")
                    message_buffer.update_agent_status("Innovative Researcher", "in_progress")

                if chunk.get("design_basis"):
                    message_buffer.update_report_section("design_basis", chunk["design_basis"])
                    message_buffer.update_agent_status("Design Basis Analyst", "completed")
                    message_buffer.update_agent_status("Basic PFD Designer", "in_progress")

                # Research Team Outputs
                if chunk.get("research_concepts"):
                    message_buffer.update_report_section("research_concepts", chunk["research_concepts"])
                    if message_buffer.agents_status.get("Innovative Researcher") != "completed":
                        message_buffer.update_agent_status("Innovative Researcher", "completed")
                        message_buffer.update_agent_status("Conservative Researcher", "in_progress")
                    else:
                        message_buffer.update_agent_status("Conservative Researcher", "completed")
                        if "Concept Detailer" in message_buffer.agents_status:
                            message_buffer.update_agent_status("Concept Detailer", "in_progress")

                if chunk.get("selected_concept_details"):
                    message_buffer.update_report_section(
                        "selected_concept_details", chunk["selected_concept_details"]
                    )
                    if "Concept Detailer" in message_buffer.agents_status:
                        message_buffer.update_agent_status("Concept Detailer", "completed")
                    message_buffer.update_agent_status("Design Basis Analyst", "in_progress")

                # Designer Team Outputs
                if chunk.get("basic_pfd"):
                    message_buffer.update_report_section("basic_pfd", chunk["basic_pfd"])
                    message_buffer.update_agent_status("Basic PFD Designer", "completed")
                    message_buffer.update_agent_status("Stream Data Builder", "in_progress")

                if chunk.get("basic_stream_data"):
                    message_buffer.update_report_section("basic_stream_data", chunk["basic_stream_data"])
                    if message_buffer.agents_status.get("Stream Data Builder") != "completed":
                        message_buffer.update_agent_status("Stream Data Builder", "completed")
                        message_buffer.update_agent_status("Stream Data Estimator", "in_progress")
                    else:
                        message_buffer.update_agent_status("Stream Data Estimator", "completed")
                        message_buffer.update_agent_status("Equipment List Builder", "in_progress")

                if chunk.get("basic_hmb_results"):
                    message_buffer.update_report_section("basic_hmb_results", chunk["basic_hmb_results"])
                    message_buffer.update_agent_status("Stream Data Estimator", "completed")
                    message_buffer.update_agent_status("Equipment List Builder", "in_progress")

                if chunk.get("basic_equipment_template"):
                    message_buffer.update_report_section(
                        "basic_equipment_template", chunk["basic_equipment_template"]
                    )
                    if message_buffer.agents_status.get("Equipment List Builder") != "completed":
                        message_buffer.update_agent_status("Equipment List Builder", "completed")
                        message_buffer.update_agent_status("Equipment Sizing Agent", "in_progress")
                    else:
                        message_buffer.update_agent_status("Equipment Sizing Agent", "completed")
                        message_buffer.update_agent_status("Safety Risk Analyst", "in_progress")

                # Lead Team Outputs
                if chunk.get("safety_risk_analyst_report"):
                    message_buffer.update_report_section(
                        "safety_risk_analyst_report", chunk["safety_risk_analyst_report"]
                    )
                    message_buffer.update_agent_status("Safety Risk Analyst", "completed")
                    message_buffer.update_agent_status("Project Manager", "in_progress")

                if chunk.get("project_manager_report"):
                    message_buffer.update_report_section(
                        "project_manager_report", chunk["project_manager_report"]
                    )
                    message_buffer.update_agent_status("Project Manager", "completed")
                
                # Update display
                update_display(layout)
            
            trace.append(chunk)

        # Display final report
        final_state = trace[-1]
        
        # Update all agent statuses to completed
        for agent in message_buffer.agents_status:
            message_buffer.update_agent_status(agent, "completed")
        
        message_buffer.add_message(
            "Analysis", "Completed!"
        )
        
        # Update final report section
        for section in message_buffer.report_sections.keys():
            if section in final_state:
                message_buffer.update_report_section(section, final_state[section])
    
        # Display the complete Final report
        display_complete_report(final_state)
        
        update_display(layout)
        
        
@app.command()
def main():
    run_analysis()

if __name__ == "__main__":
    app()
