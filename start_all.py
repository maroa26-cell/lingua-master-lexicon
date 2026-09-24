import subprocess

apps = [
    "lexicon_admin.py",
    "lexicon_api.py",
    "lexicon_health.py",
    "lexicon_stats_v5.py"
]

for app in apps:
    subprocess.Popen(["python", app])
    print(f"Started {app}")
