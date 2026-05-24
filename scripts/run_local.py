import argparse
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--start-year', type=int, default=2024)
parser.add_argument('--end-year', type=int, default=2025)
parser.add_argument('--states', nargs='+', default=['PA','NJ','NY','CA','TX'])
args = parser.parse_args()

cmd = [sys.executable, 'src/pipelines/usaspending_medallion_pipeline.py', '--start-year', str(args.start_year), '--end-year', str(args.end_year), '--states'] + args.states
subprocess.check_call(cmd)
print('Local refresh complete. Start Flask with: python app/flask_app.py')
