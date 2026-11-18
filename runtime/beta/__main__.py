import sys
from .cli import main
from .engine import TransitionError

try:
    sys.exit(main())
except TransitionError as e:
    print(f"error: {e}", file=sys.stderr)
    sys.exit(2)
