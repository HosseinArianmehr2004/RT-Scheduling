import os


def generate_html_from_logs():
    log_files = [
        "subsystem1_log.txt",
        "subsystem2_log.txt",
        "subsystem3_log.txt",
        "subsystem4_log.txt",
        "time_0.txt",  # می‌توانید این را برای فایل‌های زمان دیگر نیز اضافه کنید
        "time_1.txt",
        "time_2.txt",
        "time_3.txt",
        "time_4.txt",
        "time_5.txt",
        "time_6.txt",
        "time_7.txt",
        "time_8.txt",
        "time_9.txt",
    ]

    # Create HTML file to log output
    with open("./output/simulation_output.html", "w") as html_file:
        html_file.write("<html><head><title>Simulation Output</title></head><body>")
        html_file.write("<h1>Task Scheduler Output</h1>")

        for log_file in log_files:
            file_path = os.path.join("./output", log_file)
            if os.path.exists(file_path):
                html_file.write(f"<h2>{log_file}</h2>")
                html_file.write("<ul>")
                with open(file_path, "r") as f:
                    for line in f:
                        html_file.write(f"<li>{line.strip()}</li>")
                html_file.write("</ul>")
            else:
                html_file.write(f"<h2>{log_file} not found!</h2>")

        html_file.write("</body></html>")


if __name__ == "__main__":
    generate_html_from_logs()
