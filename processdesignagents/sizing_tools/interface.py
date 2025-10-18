from typing import Annotated

#Import each methods
from .preliminary import (
    prelim_basic_heat_exchanger_sizing, 
    prelim_shell_and_tube_heat_exchanger_sizing, 
    prelim_pressurized_vessel_sizing,
    prelim_vertical_pressurized_vessel_sizing,
    prelim_horizontal_pressurized_vessel_sizing,
    prelim_tank_sizing,
    prelim_pump_sizing,
    prelim_centrifugal_pump_sizing
)

#Import configuration
from .config import get_config

# Tools organized by equipment category
TOOLS_BY_CATEGORIES = {
    "heat_exchanger": {
        "description": "Size a shell-and-tube heat exchanger.",
        "tools": [
            "basic_heat_exchanger_sizing",
            "shell_and_tube_heat_exchanger_sizing",
        ]
    },
    "pressurized_vessel": {
        "description": "Size a pressurized vessel.",
        "tools": [
            "pressurized_vessel_sizing",
            "vertical_pressurized_vessel_sizing",
            "horizontal_pressurized_vessel_sizing",
            "tank_sizing"
        ]
    },
    "pump": {
        "description": "Size a pump.",
        "tools": [
            "pump_sizing",
            "centrifugal_pump_sizing",
        ]
    }
}

# Mapping of methods to their sizing methods implementation
SIZING_METHODS = {
    # basic_heat_exchanger_sizing
    "basic_heat_exchanger_sizing": {
        "preliminary": prelim_basic_heat_exchanger_sizing
    },
    # shell_and_tube_heat_exchanger_sizing
    "shell_and_tube_heat_exchanger_sizing": {
        "preliminary": prelim_shell_and_tube_heat_exchanger_sizing
    },
    # pressurized_vessel_sizing
    "pressurized_vessel_sizing": {
        "preliminary": prelim_pressurized_vessel_sizing
    },
    # vertical_pressurized_vessel_sizing
    "vertical_pressurized_vessel_sizing": {
        "preliminary": prelim_vertical_pressurized_vessel_sizing
    },
    # horizontal_pressurized_vessel_sizing
    "horizontal_pressurized_vessel_sizing": {
        "preliminary": prelim_horizontal_pressurized_vessel_sizing
    },
    # tank_sizing
    "tank_sizing": {
        "preliminary": prelim_tank_sizing
    },
    # pump_sizing
    "pump_sizing": {
        "preliminary": prelim_pump_sizing
    },
    # centrifugal_pump_sizing
    "centrifugal_pump_sizing": {
        "preliminary": prelim_centrifugal_pump_sizing
    }
}

def get_category_for_method(method: str) -> str:
    """Get the category that contains the specified method."""
    for category, info in TOOLS_BY_CATEGORIES.items():
        if method in info["tools"]:
            return category
    raise ValueError(f"Method '{method}' not found in any category")

def get_vendor(category: str, method: str = None) -> str:
    """Get the configured vendor for a data category or specific tool method.
    Tool-level configuration takes precedence over category-level.
    """
    config = get_config()
    
    # Check tool-level configuration first (if method provided)
    if method:
        tool_sizing = config.get("tool_sizing", {})
        if method in tool_sizing:
            return tool_sizing[method]

    # Fall back to category-level configuration
    return config.get("data_sizing", {}).get(category, "default")


def equipment_sizing(method: str, *args, **kwargs) -> str:
    """Route method calls to appropriate sizing implementation with fallback support."""
    category = get_category_for_method(method)
    method_config = get_vendor(category, method)

    primary_methods = [v.strip() for v in method_config.split(',')]

    if method not in SIZING_METHODS:
        raise ValueError(f"Method '{method}' not suppored.")
    
    # Get all available sizing methods for fallback
    all_available_methods = list(SIZING_METHODS[method].keys())
    
    # Create fallback method list: primary method first, the remaing methods as fallback
    fallback_vendors = primary_methods.copy()
    for method in all_available_methods:
        if method not in primary_methods:
            fallback_vendors.append(method)
    
    # Debug: Print fallback oreding
    primary_str = " → ".join(primary_methods)
    fallback_str = " → ".join(fallback_vendors)
    print(f"DEBUG: {method} - Primary: [{primary_str}], Fallback: [{fallback_str}]")

    # Track results and execution state
    results = []
    method_attemp_count = 0
    any_primanry_method_attempted = False
    successful_method = None
    
    for _method in fallback_vendors:
        if _method not in SIZING_METHODS[method]:
            if _method in primary_methods:
                print(f"INFO: Method '{_method}' not supported for method '{method}', falling back to next method.")
            continue
    
        method_impl = SIZING_METHODS[method][_method]
        is_primary_method = _method in primary_methods
        method_attemp_count += 1
        
        # Track if we attemped any primary method
        if is_primary_method:
            any_primanry_method_attempted = True

        # Debug: Print current attemp
        method_type = "PRIMARY" if is_primary_method else "FALLBACK"
        print(f"DEBUG: Attempting {method_type} method '{_method}' for {method} (attempt #{method_attemp_count})")
        
        # Handle list of methods for a _method
        if isinstance(method_impl, list):
            method_methods = [(impl, _method) for impl in method_impl]
            print(f"DEUBG: Method '{_method}' has multiple implementations: {len(method_methods)} functions")
        else:
            method_methods = [(method_impl, _method)]
        
        # Run methods for this _method
        method_results = []
        for impl_func, method_name in method_methods:
            try:
                print(f"DEBUG: Calling {impl_func.__name__} from '{method_name}'...")
                result = impl_func(*args, **kwargs)
                method_results.append(result)
                print(f"SUCCESS: {impl_func.__name__} from '{method_name}' completed successfully")
            except Exception as e:
                # Log error but continue with other implementations
                print(f"FAILED: {impl_func.__name__} from '{method_name}' failed with error: {e}")
                continue
            
        # Add this method's results
        if method_results:
            results.extend(method_results)
            successful_method = _method
            result_summary = f"Got {len(method_results)} results(s)"
            print(f"SUCCESS: {result_summary} for method '{method}'")
            
            # Stopping logic: Stop after first successful vendor for single-vendor configs
            # Multiple vendor configs (comma-separated) may want to collect from multiple sources
            if len(primary_methods) == 1:
                print(f"DEBUG: Stopping after successful method '{_method}' (single-vendor config)")
                break
        else:
            print(f"FAILED: No results for method '{method}'")
        
    # Final result summary
    if len(results) == 1:
        return results[0]
    else:
        # Convert all results to strings and concatenate
        return '\n'.join(str(result) for result in results)