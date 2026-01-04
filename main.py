import os

from log_automation import (
    copy_log_files,
    extract_error_messages,
    format_log_entries
)


def main():
    source_dir = "logs_source"
    destination_dir = "logs_dest"
    output_dir = "output"

    os.makedirs(output_dir, exist_ok=True)

    copied_files = copy_log_files(source_dir, destination_dir)

    all_errors = []
    all_formatted_logs = []

    for log_file in copied_files:
        all_errors.extend(extract_error_messages(log_file))
        all_formatted_logs.extend(format_log_entries(log_file))

    # Write error logs
    error_log_path = os.path.join(output_dir, "error_logs.txt")
    with open(error_log_path, "w") as file:
        for error in all_errors:
            print(error)
            file.write(error + "\n")

    # Write formatted logs
    formatted_log_path = os.path.join(output_dir, "formatted_logs.txt")
    with open(formatted_log_path, "w") as file:
        for entry in all_formatted_logs:
            file.write(entry + "\n")

    print("\nLog processing completed successfully.")


if __name__ == "__main__":
    main()
