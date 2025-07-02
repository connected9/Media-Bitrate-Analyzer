
📊 Media Bitrate Analyzer
<div align="center">


![alt text](https://img.shields.io/badge/python-3.7+-blue.svg)


![alt text](https://img.shields.io/badge/license-MIT-green.svg)


![alt text](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey.svg)


![alt text](https://img.shields.io/badge/built%20with-Tkinter%20%26%20Matplotlib-orange.svg)

A user-friendly desktop GUI for generating detailed bitrate analysis charts for any video or audio file.

</div>


This tool leverages the power of FFmpeg/ffprobe to provide a deep insight into the encoding quality of your media files. It's designed for media professionals, developers, and enthusiasts who need a quick, reliable way to visualize variable bitrate data.

<br>

<div align="center">


A GIF or high-quality screenshot of the application in action would go here.

</div>

<br>

✨ Key Features

🖥️ Intuitive GUI: A clean and simple interface built with native Python libraries.

🖱️ Drag & Drop: Easily add files by dragging them onto the window.

📂 Batch Processing: Analyze multiple files at once with a clear progress display.

📈 Detailed Bitrate Charts: Generates a high-quality .png chart for each file, visualizing bitrate over time.

📝 Comprehensive Metadata: Charts include a dedicated header with crucial info:

File Duration, Size, and Overall Bitrate

Video Codec, Resolution, and Average Bitrate

Audio Codec, Sample Rate, Channel Layout, and Average Bitrate

⚡ Responsive & Non-Blocking: The multi-threaded architecture ensures the app never freezes, even with large files.

🌐 Universal File Support: Intelligently analyzes any format supported by your FFmpeg installation (.mp4, .mkv, .flac, etc.).

💪 Robust Error Handling: If a file fails, the app reports the error and seamlessly continues with the next file in the batch.

⚙️ Prerequisites

Before you begin, ensure you have the following installed and configured on your system.

Python 3.7+ and the pip package manager.

FFmpeg: This is the core engine for the analysis.

❗️ CRUCIAL: ffmpeg and ffprobe must be accessible from your system's command line (i.e., they are in the system's PATH).

Verify your installation by opening a terminal and running ffprobe -version. If it prints version information, you're all set!

Download from the official site: ffmpeg.org/download.html

🚀 Installation & Usage

Follow these simple steps to get the analyzer running.

Get the Code

Download the video_analyzer_app_v4.py script to a new folder on your computer.

Install Python Libraries

Open a terminal or command prompt and run the following command to install the required packages:

Generated bash
pip install matplotlib tkinterdnd2


Launch the Application

In your terminal, navigate to the folder where you saved the script and run:

Generated bash
python video_analyzer_app_v4.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Analyze Your Files

Add files using Drag & Drop or the "Browse Files" button.

Select the files you wish to process in the list (Ctrl+Click, Shift+Click, or "Select All").

Click "Analyze Selected".

View Your Results

A .png chart for each successfully processed file will be saved in the same folder as the script.

📊 The Output Chart

The generated chart is designed for clarity and provides a complete data snapshot.

<div align="center">


An example of a generated chart image would go here.

</div>


The chart includes:

Main Title: The full filename, wrapped intelligently to fit.

Details Header: A clean, boxed-off section with key metadata.

Plot Area: A graph of bitrate (kbps) vs. time (seconds).

🔧 How It Works: The Architecture

The application is built on a robust three-part architecture to ensure stability and responsiveness.

Generated code
+--------------------------+
User Interaction -> |  VideoAnalyzerApp (View) | -> Creates Worker
(Tkinter)         |  (Main GUI Thread)       |
                  +------------+-------------+
                               |
                               | (file list, queue)
                               v
                  +--------------------------+
                  |  AnalysisWorker (Thread) | -> Loops through files
                  +------------+-------------+
                               |
                               | (progress, results)
                               v (via Queue)
                  +--------------------------+
                  | VideoAnalysisEngine (Model)| -> Runs ffprobe, creates chart
                  |  (Runs in Worker Thread) |
                  +--------------------------+
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END

View (GUI): Handles all user interactions without performing any heavy work itself.

Controller (Worker Thread): Manages the analysis queue, processing one file at a time off the main thread to prevent the UI from freezing.

Model (Engine): Contains the core logic, executing ffprobe commands and using matplotlib to generate the output images.

⚠️ Troubleshooting

Encountered an issue? Here are solutions to common problems.

<details>
<summary><strong>Error: "ffprobe not found" or "Dependency Missing"</strong></summary>


Problem: The script cannot find the ffprobe executable.

Solution: You must add the directory containing ffmpeg.exe and ffprobe.exe to your system's PATH environment variable.

Windows: Search for "Edit the system environment variables", click "Environment Variables...", select the "Path" variable under "System variables", click "Edit...", "New", and paste the path to your FFmpeg bin folder (e.g., C:\ffmpeg\bin). Restart your terminal.

macOS/Linux: Edit your shell profile file (e.g., ~/.zshrc, ~/.bash_profile) and add the line: export PATH="/path/to/your/ffmpeg/bin:$PATH". Save the file and restart your terminal or run source ~/.zshrc.

</details>

<details>
<summary><strong>Error: "Permission denied" when saving the chart</strong></summary>


Problem: The script does not have permission to write files in its current location.

Solution: Make sure you are running the script from a directory where you have write permissions (e.g., your Desktop or Documents folder). Avoid running it from protected locations like C:\Program Files.

</details>

<details>
<summary><strong>Analysis is very slow the first time, then fast.</strong></summary>


Observation: The first file takes a long time, but analyzing it again is almost instant.

Explanation: This is normal and is due to File System Caching. The first time, your computer reads the file from the slow disk. Your operating system then keeps a copy in fast RAM. Subsequent analyses read from RAM, which is much faster. This is not a bug, but a feature of modern operating systems.

</details>

🤝 Contributing

Feedback, bug reports, and feature requests are welcome! Please feel free to open an issue if this project were hosted on a platform like GitHub.

📜 License

This project is licensed under the MIT License.

<details>
<summary>Click to view License</summary>

Generated code
MIT License

Copyright (c) 2023 [Your Name or Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END
</details>
