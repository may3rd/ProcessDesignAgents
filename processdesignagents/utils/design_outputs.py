import pandas as pd
import graphviz
from typing import Dict, Any
import numpy as np  # For any lingering type conversions

def generate_hmb(flowsheet: Dict[str, Any], validation_results: Dict[str, Any]) -> pd.DataFrame:
    """Generate Heat and Material Balance table."""
    # Placeholder data derived from state (customize based on simulation)
    hmb_data = {
        'Stream': ['Ethane Feed', 'Reactor Outlet', 'Product Ethylene', 'Byproducts'],
        'Mass Flow (kg/h)': [1000, 1000, round(validation_results.get('optimized_yield', 90.8)), 92],
        'Temperature (°C)': [25, 1200, 100, 100],
        'Enthalpy (kJ/h)': [0, 1500000, 90000, 1410000]  # Derived from energy estimates
    }
    return pd.DataFrame(hmb_data)

def generate_pfd(flowsheet: Dict[str, Any], validation_results: Dict[str, Any]) -> graphviz.Digraph:
    """Generate preliminary PFD as Graphviz DOT graph."""
    dot = graphviz.Digraph(comment='Preliminary PFD')
    for unit in flowsheet.get('units', []):
        dot.node(unit['name'], f"{unit['type']}\n{unit['specs']}")
    for conn in flowsheet.get('connections', []):
        dot.edge(conn['from'], conn['to'])
    # Add feed and product nodes
    dot.node('Feed', 'Ethane Feed\n1000 kg/h')
    dot.node('Prod', f'Ethylene Product\nYield {validation_results.get("optimized_yield", 90.8)}%')
    dot.edge('Feed', flowsheet['units'][0]['name'] if flowsheet.get('units') else 'R1')
    dot.edge(flowsheet['units'][-1]['name'] if flowsheet.get('units') else 'S1', 'Prod')
    return dot

def generate_equipment_list(flowsheet: Dict[str, Any]) -> pd.DataFrame:
    """Generate equipment list."""
    equipment = []
    for unit in flowsheet.get('units', []):
        equipment.append({
            'Unit': unit['name'],
            'Type': unit['type'],
            'Specs': str(unit['specs'])
        })
    return pd.DataFrame(equipment)