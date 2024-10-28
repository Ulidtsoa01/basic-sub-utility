import argparse
from pathlib import Path
import ass
import srt
from datetime import datetime, timedelta

ARGUMENTS = {
    "shift": {
        "flags": ["-s", "--shift"],
        "kwargs": {
            "default": None,
            "required": False,
            "type": str,
            "help": "Shift the times of the subtitles by the given seconds",
        },
    },
    "start": {
        "flags": ["--start"],
        "kwargs": {
            "default": None,
            "required": False,
            "type": str,
            "help": (
                "Dialogue event must begin at or after this time for changes to apply."
                "Duration format is `HH:MM:SS.ssss`"
            ),
        },
    },
    "end": {
        "flags": ["--end"],
        "kwargs": {
            "default": None,
            "required": False,
            "type": str,
            "help": (
                "Dialogue event must be before or at this time for changes to apply."
                "Duration format is `HH:MM:SS.ssss`"
            ),
        },
    },
    "remove_start": {
        "flags": ["-rs", "--remove_start"],
        "kwargs": {
            "default": None,
            "required": False,
            "type": str,
            "help": (
                "All dialogue events after this duration or until remove_end are removed."
                "Duration format is `HH:MM:SS.ssss`"
            ),
        },
    },
    "remove_end": {
        "flags": ["-re", "--remove_end"],
        "kwargs": {
            "default": None,
            "required": False,
            "type": str,
            "help": (
                "All dialogue events before this duration or stopping at remove_start are removed."
                "Duration format is `HH:MM:SS.ssss`"
            ),
        },
    },
}


def get_args():
    parser = argparse.ArgumentParser(description="Basic utilities for subtitles")
    parser.add_argument("file", type=Path, help="path to the subtitle file")
    for arg in ARGUMENTS.values():
        parser.add_argument(*arg["flags"], **arg["kwargs"])
    args = parser.parse_args()
    return args

def run_ass():
    with open(filePath.resolve(), 'r', encoding='utf-8-sig') as f:
      doc = ass.parse(f)
      f.close()
    
    for i in range(len(doc.events)):
        if start_time and start_time > doc.events[i].start:
            continue
        if end_time and end_time < doc.events[i].end:
            continue
        if shift_time:
            doc.events[i].start += shift_time
            # print(1, doc.events[i].end)
            doc.events[i].end += shift_time
            # print(2, doc.events[i].end)

    new_file = filePath.parent / (filePath.stem + "_modified" + filePath.suffix)
    with open(new_file, "w" , encoding='utf_8_sig') as f:
        doc.dump_file(f)

def run_srt():
    with open(filePath.resolve(), 'r', encoding='utf-8-sig') as f:
      lines = f.read()
      doc = list(srt.parse(lines))
      f.close()
    
    for i in range(len(doc)):
        if start_time and start_time > doc[i].start:
            continue
        if end_time and end_time < doc[i].end:
            continue
        if shift_time:
            doc[i].start += shift_time
            print(1, doc[i].end)
            doc[i].end += shift_time
            print(2, doc[i].end)

    new_file = filePath.parent / (filePath.stem + "_modified" + filePath.suffix)
    with open(new_file, "w" , encoding='utf_8_sig') as f:
        srtblock = srt.compose(doc)
        f.write(srtblock)
        f.close()

if __name__ == "__main__":
    args = get_args()
    filePath = Path(args.file)
    
    shift_time = False
    start_time = False
    end_time = False
    def convert_HHMMSSssss(str):
        t = str.split(".")
        dt = datetime.strptime(t[0], "%H:%M:%S")
        td = timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second, microseconds=int(t[1])*100)
        return td
    if args.shift:
        shift_time = timedelta(seconds=float(args.shift))
    if args.start:
        start_time = convert_HHMMSSssss(args.start)
    if args.end:
        end_time = convert_HHMMSSssss(args.end)
    
    if filePath.suffix == ".ass":
        run_ass()
    elif filePath.suffix == ".srt":
        run_srt()

    
# python .\basic-sub-utility.py "C:\Coding\.extract\test.srt" -s 1.5 --start 00:00:01.1234 --end 00:00:33.1234