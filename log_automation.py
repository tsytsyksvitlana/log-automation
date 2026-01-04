import os
import re
import shutil
from typing import List
from datetime import datetime


APACHE_PATTERN = re.compile(
    r"\[(?P<timestamp>.+?)\]\s+\[(?P<level>\w+)\]\s+(?P<message>.*)",
    re.IGNORECASE
)

HADOOP_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2},\d+)\s+"
    r"(?P<level>INFO|ERROR|WARN|FATAL)\s+"
    r"\[(?P<thread>.*?)\]\s+"
    r"(?P<class>[\w\.]+):\s+(?P<message>.*)"
)

SPARK_PATTERN = re.compile(
    r"(?P<timestamp>\d{2}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>INFO|ERROR|WARN|FATAL)\s+"
    r"(?P<class>[\w\.]+):\s+(?P<message>.*)"
)

LOG_PATTERNS = [APACHE_PATTERN, HADOOP_PATTERN, SPARK_PATTERN]
LEVEL_MAPPING = {
    "notice": "INFO",
    "info": "INFO",
    "warn": "WARN",
    "error": "ERROR",
    "fatal": "FATAL"
}



def copy_log_files(source_dir: str, destination_dir: str) -> List[str]:
    """
    Copies all log files from source directory to destination directory.
    """
    os.makedirs(destination_dir, exist_ok=True)
    copied_files = []

    for filename in os.listdir(source_dir):
        if filename.endswith((".log", ".txt")):
            src = os.path.join(source_dir, filename)
            dst = os.path.join(destination_dir, filename)
            shutil.copy2(src, dst)
            copied_files.append(dst)

    return copied_files


def normalize_timestamp(ts: str) -> str:
    for fmt in ("%a %b %d %H:%M:%S %Y",  # Apache
                "%Y-%m-%d %H:%M:%S,%f",  # Hadoop
                "%y/%m/%d %H:%M:%S"):    # Spark
        try:
            dt = datetime.strptime(ts, fmt)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    return ts


def extract_error_messages(file_path: str) -> List[str]:
    """
    Extracts ERROR / WARN / FATAL messages from log files.
    """
    errors = []
    with open(file_path) as file:
        for line in file:
            for pattern in LOG_PATTERNS:
                match = pattern.search(line)
                if match:
                    level = match.group("level").lower()
                    level = LEVEL_MAPPING.get(level, level.upper())
                    if level in {"ERROR", "WARN", "FATAL"}:
                        ts = normalize_timestamp(match.group("timestamp"))
                        errors.append(f"[{ts}] {level} - {match.group('message')}")
                    break
    return errors


def format_log_entries(file_path: str) -> List[str]:
    """
    Formats log entries into a unified format.
    """
    formatted_logs = []
    with open(file_path) as file:
        for line in file:
            for pattern in LOG_PATTERNS:
                match = pattern.search(line)
                if match:
                    level = match.group("level").lower()
                    level = LEVEL_MAPPING.get(level, level.upper())
                    ts = normalize_timestamp(match.group("timestamp"))
                    formatted_logs.append(f"[{ts}] {level} - {match.group('message')}")
                    break
    return formatted_logs

