"""Render existing Ox check results; never converts omissions or missing tools to approval."""
from pathlib import Path
import argparse
import json
import sys


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report',type=Path)
    args=parser.parse_args()
    try:
        doc=json.loads(args.report.read_text())
        results=doc['results']
        if not isinstance(results,list) or not results or doc.get('product_acceptance') is not False:
            raise ValueError('expected an Ox results document, excluding product acceptance')
        print('Check observations; no product approval.\n')
        print('| Command | State | Exit |\n| --- | --- | --- |')
        codes=[]
        for row in results:
            if not isinstance(row['argv'],list) or type(row['exit_code']) is not int:
                raise ValueError('invalid result')
            cmd=' '.join(row['argv']).replace('|','\\|').replace('\n',' ')
            state=str(row['state']).replace('|','\\|').replace('\n',' ')
            print(f"| {cmd} | {state} | {row['exit_code']} |")
            codes.append(row['exit_code'])
        for item in doc.get('omitted',[]): print('\nOmitted:',json.dumps(item,ensure_ascii=False))
        for item in doc.get('manual_evidence',[]): print('\nManual evidence:',item)
        code=next((x for x in codes if x),0)
        return code if code>=0 else 128-code
    except (OSError,ValueError,KeyError,TypeError) as error:
        print('Invalid report:',error,file=sys.stderr);return 2


if __name__=='__main__':sys.exit(main())
