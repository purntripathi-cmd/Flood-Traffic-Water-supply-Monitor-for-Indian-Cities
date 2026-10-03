"""
Autonomous Standalone Weekly Civic Batch Scanner
Can be scheduled via Windows Task Scheduler or Linux Cron:
Usage:
  python scripts/weekly_civic_scanner.py --batch-size 4 --delay-seconds 1.0
  python scripts/weekly_civic_scanner.py --continuous --interval-hours 168
"""

import sys
import os
import time
import argparse

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils.scanner_daemon import run_batch_scan, get_scanner_status


def main():
    parser = argparse.ArgumentParser(description="Weekly Civic Scanner & Pincode Batch Processor")
    parser.add_argument("--batch-size", type=int, default=4, help="Number of pincodes to audit per batch chunk")
    parser.add_argument("--delay-seconds", type=float, default=1.0, help="Delay between batch chunks to avoid CPU spike")
    parser.add_argument("--city", type=str, default=None, help="Filter by city name (e.g. 'Bengaluru', 'Mumbai')")
    parser.add_argument("--continuous", action="store_true", help="Run indefinitely in background, checking weekly")
    parser.add_argument("--interval-hours", type=int, default=168, help="Hours between recurring scans if continuous")

    args = parser.parse_args()

    print("=" * 70)
    print("  AUTONOMOUS CIVIC AVOIDANCE SCANNER & PINCODE BATCH PROCESSOR")
    print("=" * 70)
    status = get_scanner_status()
    print(f"Current Telemetry: Last Run: {status.get('last_run_timestamp')} | Fresh: {status.get('is_fresh')}")

    while True:
        print(f"\n[SCANNER] Starting batch scan (Batch Size={args.batch_size}, Throttle={args.delay_seconds}s)...")
        
        def print_progress(current, total, msg):
            pct = round((current / total) * 100)
            print(f"[{pct:3d}%] ({current}/{total}) {msg}")

        result = run_batch_scan(
            batch_size=args.batch_size,
            delay_seconds=args.delay_seconds,
            city_filter=args.city,
            progress_callback=print_progress
        )

        print("\n[OK] Scan completed successfully!")
        print(f"  • Updated Records: {result['last_batch_records_updated']}")
        print(f"  • Next Scheduled Run: {result['next_scheduled_run']}")
        print(f"  • Data synced locally to data/chronic_avoidance_pincodes.csv")

        if not args.continuous:
            break

        print(f"\n[DAEMON] Sleeping for {args.interval_hours} hours until next weekly audit cycle...")
        time.sleep(args.interval_hours * 3600)


if __name__ == "__main__":
    main()
