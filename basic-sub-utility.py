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

class ASS():
    def open(self):
        with open(filePath.resolve(), 'r', encoding='utf-8-sig') as f:
            doc = ass.parse(f)
            f.close()
        return doc
    
    def output(self, doc):
        new_file = filePath.parent / (filePath.stem + "_modified" + filePath.suffix)
        with open(new_file, "w" , encoding='utf_8_sig') as f:
            doc.dump_file(f)
            f.flush()
            f.close()
    
    def get_events(self, doc):
        return doc.events
    
    def set_events(self, doc, events):
        doc.events = events
        return doc


class SRT():
    def open(self):
        with open(filePath.resolve(), 'r', encoding='utf-8-sig') as f:
            lines = f.read()
            doc = list(srt.parse(lines))
            f.close()
        return doc
    
    def output(self, doc):
        new_file = filePath.parent / (filePath.stem + "_modified" + filePath.suffix)
        with open(new_file, "w" , encoding='utf_8_sig') as f:
            srtblock = srt.compose(doc)
            f.write(srtblock)
            f.flush()
            f.close()

    def get_events(self, doc):
        return doc
    
    def set_events(self, _, events):
        return events


def run_both(ext):
    sub = ""
    if ext == ".ass":
        sub = ASS()
    if ext == ".srt":
        sub = SRT()
    
    doc = sub.open()
    events = sub.get_events(doc)
    for i in range(len(events)):
        if args.start is not None and start_time > events[i].start:
            continue
        if args.end is not None and end_time < events[i].end:
            continue
        if args.shift is not None:
            events[i].start += shift_time
            events[i].end += shift_time
    
    if args.remove_start is not None:
        events = list(filter(lambda x: x.start < remove_st, events))
    if args.remove_end is not None:
        events = list(filter(lambda x: x.end > remove_et, events))

    doc = sub.set_events(doc, events)
    sub.output(doc)


def get_args():
    parser = argparse.ArgumentParser(description="Basic utilities for subtitles")
    parser.add_argument("file", type=Path, help="path to the subtitle file")
    for arg in ARGUMENTS.values():
        parser.add_argument(*arg["flags"], **arg["kwargs"])
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()
    filePath = Path(args.file)
    
    shift_time = False
    start_time = False
    end_time = False
    remove_st = False
    remove_et = False
    def convert_HHMMSSssss(str):
        t = str.split(".")
        dt = datetime.strptime(t[0], "%H:%M:%S")
        td = timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second, microseconds=int(t[1])*100)
        return td
    if args.shift is not None:
        shift_time = timedelta(seconds=float(args.shift))
    if args.start is not None:
        start_time = convert_HHMMSSssss(args.start)
    if args.end is not None:
        end_time = convert_HHMMSSssss(args.end)
    if args.remove_start is not None:
        remove_st = convert_HHMMSSssss(args.remove_start)
    if args.remove_end is not None:
        remove_et = convert_HHMMSSssss(args.remove_end)
    run_both(filePath.suffix)