"""Diagnose connectivity to an Ellisys analyzer Remote Control server.

Usage: python probe.py [host] [port]     (defaults: localhost 12345)

Exit codes: 0 = connected (prints app info or TCP-only OK), 2 = TCP unreachable,
3 = SDK connect failed despite TCP being open.
Works with any Python; uses the SDK only if it is installed.
"""
import socket
import sys

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 12345

# Stage 1: raw TCP reachability (no SDK needed).
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3.0)
try:
    s.connect((host, port))
except OSError as exc:
    print(f"UNREACHABLE: no TCP listener at {host}:{port} ({exc}).")
    print("-> Is the Ellisys analyzer application running on that machine?")
    print("-> Is the Remote Control plugin installed and enabled (see the User Guide)?")
    print("-> Is the port right (default 12345)? Firewall?")
    sys.exit(2)
finally:
    s.close()
print(f"TCP OK: {host}:{port} is listening.")

# Stage 2: real SDK handshake, if the SDK is available in this interpreter.
try:
    import ellisys_analysis_automation as ea
except ImportError:
    print("SDK not importable in THIS interpreter -- TCP-level check only.")
    print("-> Run scripts/setup_env.py, then re-run with the venv interpreter")
    print("   (.venv/bin/python on Linux/macOS, .venv\\Scripts\\python.exe on Windows)")
    sys.exit(0)

try:
    with ea.connect(host, port) as analyzer:
        info = analyzer.app_info()
        print(f"CONNECTED: {info}")
        print(f"recording={analyzer.is_recording} loading={analyzer.is_loading}")
        names = analyzer.overviews()
        print(f"overviews={names}")
except ea.RemoteControlError as exc:
    print(f"SDK CONNECT FAILED despite open TCP port: {exc}")
    print("-> The listener may not be the Remote Control server (wrong port/service).")
    sys.exit(3)
