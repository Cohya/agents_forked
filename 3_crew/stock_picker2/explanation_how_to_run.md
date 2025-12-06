run with the commend: crewai run

this is exactly like to run this following code 
#!/usr/bin/env python
"""
Run CrewAI crew manually with tracing.
"""

#!/usr/bin/env python
"""
Run CrewAI crew manually with tracing.
"""

```
import os
import sys
import warnings
from importlib import import_module

# Optional: suppress warnings from libraries like pysbd
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Disable telemetry / tracing if needed
os.environ["CREWAI_TRACE_ENABLED"] = "false"
os.environ["CREWAI_TELEMETRY_DISABLED"] = "true"

# ---- Step 1: Load your project folder ----
from crewai.project.utils import find_crewai_project

project_path = find_crewai_project()
if not project_path:
    raise RuntimeError("Cannot find CrewAI project folder.")
sys.path.append(str(project_path))

# ---- Step 2: Import crew.py and get Crew instance ----
crew_module = import_module("crew")  # make sure crew.py is in project root
crew_instance = getattr(crew_module, "crew", None)
if crew_instance is None:
    # fallback: if crew.py defines a Crew class
    crew_instance = getattr(crew_module, "Crew", None)
if crew_instance is None:
    raise RuntimeError("Cannot find crew() or Crew class in crew.py")

# If crew_instance is a class, instantiate it
if isinstance(crew_instance, type):
    crew_instance = crew_instance()

# ---- Step 3: Initialize tracing ----
try:
    from crewai.events.tracing import EphemeralTraceBatch
    trace_batch = EphemeralTraceBatch.create()
except Exception as e:
    trace_batch = None
    print(f"[Warning] Tracing initialization failed: {e}")

# ---- Step 4: Execute the crew ----
try:
    result = crew_instance.run() if hasattr(crew_instance, "run") else crew_instance.kickoff()
except Exception as e:
    raise RuntimeError(f"Error running crew: {e}")

# ---- Step 5: Finalize tracing ----
if trace_batch:
    try:
        trace_batch.upload()
    except Exception as e:
        print(f"[Warning] Trace upload failed (404 is expected if disabled): {e}")

# ---- Step 6: Print result ----
print("\n=== Crew Result ===\n")
print(result)
```

