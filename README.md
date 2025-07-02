Media Bitrate Analyzer
A user-friendly, robust desktop GUI application for analyzing the bitrate of video and audio files. This tool leverages the power of FFmpeg/ffprobe to generate detailed, easy-to-read bitrate charts, making it ideal for media professionals, developers, and enthusiasts who need to inspect the quality and encoding characteristics of their files.
The application is built with Python and Tkinter, featuring a responsive, non-blocking interface that can handle large files and batch operations without freezing.
(A screenshot of the main application window with files loaded and ready for analysis)
Key Features
Intuitive Graphical User Interface: A clean and simple UI built with Python's standard Tkinter library.
Drag & Drop and File Browser: Easily add files by dragging them onto the window or by using the traditional "Browse" dialog.
Batch Processing: Analyze multiple files at once. Select one, many, or all files in the list for sequential processing.
Detailed Bitrate Chart: For each file, a high-quality .png chart is generated, visualizing the variable bitrate over time.
Comprehensive Media Details: The generated chart includes a dedicated header section with crucial metadata:
File Duration, Size, and Overall Bitrate
Video Codec, Resolution, and Average Bitrate
Audio Codec, Sample Rate, Channel Layout, and Average Bitrate
Responsive & Non-Blocking: Thanks to a multi-threaded architecture, the application remains fully responsive during analysis. A progress bar provides real-time feedback for the current file.
Broad File Support: Intelligently analyzes the primary video or audio stream of any container format supported by your FFmpeg installation (e.g., .mp4, .mkv, .mov, .avi, .webm, .flac, .mp3, etc.).
Robust Error Handling: If a file is corrupted or cannot be processed, the application will report the error and seamlessly continue to the next file in the batch.
Cross-Platform: Runs on Windows, macOS, and Linux, wherever Python and FFmpeg are available.
Prerequisites
Before running the application, you must have the following installed on your system:
Python 3.7+
FFmpeg: The core of the analysis.
Crucial: ffmpeg and ffprobe must be installed and accessible from your system's command line (i.e., they must be in your system's PATH).
You can verify this by opening a terminal or command prompt and typing ffprobe -version. If it returns version information, you are ready.
Download FFmpeg from the official site: https://ffmpeg.org/download.html
Installation
Get the Code:
Clone this repository or download the video_analyzer_app_v4.py script to a local directory.
Install Python Dependencies:
The application requires two common Python libraries. Open your terminal or command prompt and install them using pip:
Generated bash
pip install matplotlib tkinterdnd2
Use code with caution.
Bash
Usage
Launch the Application:
Navigate to the directory containing the script in your terminal and run it:
Generated bash
python video_analyzer_app_v4.py
Use code with caution.
Bash
Add Files:
Drag and Drop: Drag one or more media files from your file explorer directly onto the application window.
Browse: Click the "Browse Files" button to open a standard file selection dialog.
Select Files for Analysis:
Single File: Click on a file in the list.
Multiple Files: Use Ctrl+Click (or Cmd+Click on macOS) to select multiple individual files, or Shift+Click to select a range.
All Files: Click the "Select All" button.
Start the Analysis:
Click the "Analyze Selected" button. The process will begin.
Monitor Progress:
The status bar at the bottom will show the overall batch progress (e.g., "Analyzing 2/5...").
The progress bar will show the analysis progress for the current file.
The UI will remain fully usable during this time.
Find the Output:
Once the analysis for a file is complete, a .png chart named bitrate_chart_[your_filename].png will be saved in the same directory where the script is located. A dialog box will confirm when the entire batch is complete.
The Output Chart
The generated PNG file provides a clear and detailed overview of the media file's bitrate.
The chart is composed of three main sections:
Main Title: The full name of the analyzed media file, automatically wrapped to fit.
Details Header: A clean, boxed-off section containing key metadata.
| Detail | Description |
| :--- | :--- |
| Duration | Total runtime of the file in seconds. |
| Size | Total size of the file in megabytes. |
| Overall Bitrate| The average bitrate of the entire file (video + audio + overhead). |
| Video | The video codec, resolution, and average video stream bitrate. |
| Audio | The audio codec, sample rate, channel layout, and average audio stream bitrate. |
Plot Area: A graph showing the calculated bitrate in kilobits per second (kbps) on the y-axis against time in seconds on the x-axis.
How It Works (Technical Overview)
The application is designed for robustness and a smooth user experience using a modern architecture.
Frontend (View): The GUI is built with Tkinter and the tkinterdnd2 library for drag-and-drop support. It is responsible only for displaying information and capturing user input.
Backend (Model): The VideoAnalysisEngine class contains all the business logic. It calls ffprobe subprocesses to extract media information and packet data, parses the output, and uses matplotlib to generate the final chart.
Concurrency (Controller): An AnalysisWorker class running on a separate threading.Thread prevents the GUI from freezing during I/O-heavy operations. It communicates safely with the main UI thread using a queue.Queue to provide progress updates and results. This separation of concerns ensures the application is always responsive.
License
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
copies of the, and to permit persons to whom the Software is
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
Use code with caution.
</details>
