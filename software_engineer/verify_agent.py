import sys
import os

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from software_engineer.agent import software_engineer
    print("Successfully imported software_engineer agent.")
    
    print(f"Agent Name: {software_engineer.name}")
    print(f"Agent Model: {software_engineer.model}")
    
    print("\nTools:")
    for tool in software_engineer.tools:
        # Check if it's a FunctionTool (which wraps the function) or the function itself if not yet wrapped
        # In ADK Python, passing functions to tools=[] automatically wraps them in FunctionTool
        tool_name = getattr(tool, 'name', str(tool))
        print(f"- {tool_name}")
        
    expected_tools = ['create_file', 'execute_python_file', 'run_command', 'query_codebase']
    
    # Simple check to see if our expected tools are present by name
    # Note: The actual tool name might be derived from the function name
    found_tools = [getattr(tool, 'name', getattr(tool, '__name__', str(tool))) for tool in software_engineer.tools]
    
    missing = [t for t in expected_tools if t not in found_tools]
    
    if not missing:
        print("\nAll expected tools are present.")
    else:
        print(f"\nMissing tools: {missing}")
        print(f"Found tools: {found_tools}")

except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
