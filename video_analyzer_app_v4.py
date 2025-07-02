import subprocess
import json
import os
import sys
import threading
import queue
import textwrap
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import matplotlib.pyplot as plt
import numpy as np

# --- The Model (Business Logic) ---
class VideoAnalysisEngine:
    # ... (No changes to __init__, _run_ffprobe, get_media_info, get_formatted_details_string, generate_bitrate_data) ...
    def __init__(self, file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file does not exist: {file_path}")
        self.file_path = file_path
        self.media_info = None
        self.target_stream = None
        self.stream_type = 'video'

    def _run_ffprobe(self, command):
        try:
            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True, encoding='utf-8', startupinfo=startupinfo
            )
            return process
        except FileNotFoundError:
            raise RuntimeError("ffprobe not found. Please ensure ffmpeg is installed and in your system's PATH.")
        except Exception as e:
            raise RuntimeError(f"Failed to start ffprobe: {e}")

    def get_media_info(self):
        command = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', self.file_path
        ]
        process = self._run_ffprobe(command)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise RuntimeError(f"ffprobe error getting info: {stderr.strip()}")
        self.media_info = json.loads(stdout)
        video_streams = [s for s in self.media_info.get('streams', []) if s['codec_type'] == 'video']
        audio_streams = [s for s in self.media_info.get('streams', []) if s['codec_type'] == 'audio']
        if video_streams:
            self.target_stream = video_streams[0]
            self.stream_type = 'video'
        elif audio_streams:
            self.target_stream = audio_streams[0]
            self.stream_type = 'audio'
        else:
            raise ValueError("No video or audio streams found in the file.")
        return self.media_info

    def get_formatted_details_string(self):
        if not self.media_info: return ""
        details = []
        fmt = self.media_info.get('format', {})
        duration = float(fmt.get('duration', 0))
        size_mb = float(fmt.get('size', 0)) / (1024*1024)
        bitrate_kbps = float(fmt.get('bit_rate', 0)) / 1000
        details.append(f"Duration: {duration:.2f}s  |  Size: {size_mb:.2f} MB  |  Overall Bitrate: {bitrate_kbps:.0f} kbps")
        v_stream = next((s for s in self.media_info.get('streams', []) if s['codec_type'] == 'video'), None)
        if v_stream:
            v_codec = v_stream.get('codec_name', 'N/A')
            v_res = f"{v_stream.get('width')}x{v_stream.get('height')}"
            v_bitrate = int(v_stream.get('bit_rate', '0')) / 1000 if v_stream.get('bit_rate') else 0
            details.append(f"Video: {v_codec.upper()}, {v_res}, ~{v_bitrate:.0f} kbps")
        else:
            details.append("Video: N/A")
        a_stream = next((s for s in self.media_info.get('streams', []) if s['codec_type'] == 'audio'), None)
        if a_stream:
            a_codec = a_stream.get('codec_name', 'N/A')
            a_rate = int(a_stream.get('sample_rate', '0')) / 1000
            a_ch = a_stream.get('channel_layout', f"{a_stream.get('channels', '?')} ch")
            a_bitrate = int(a_stream.get('bit_rate', '0')) / 1000 if a_stream.get('bit_rate') else 0
            details.append(f"Audio: {a_codec.upper()}, {a_rate:.1f} kHz, {a_ch}, ~{a_bitrate:.0f} kbps")
        else:
            details.append("Audio: N/A")
        return "\n".join(details)

    def generate_bitrate_data(self, progress_callback):
        duration_str = self.media_info.get('format', {}).get('duration', '0')
        total_duration = float(duration_str)
        if total_duration <= 0: return []
        stream_selector = 'v:0' if self.stream_type == 'video' else 'a:0'
        command = [
            'ffprobe', '-v', 'quiet', '-select_streams', stream_selector,
            '-show_entries', 'packet=pts_time,size', '-of', 'csv=p=0', self.file_path
        ]
        process = self._run_ffprobe(command)
        bitrate_data, interval, current_interval_end, interval_size, last_progress = ([], 1.0, 1.0, 0, -1)
        for line in process.stdout:
            try:
                pts_time_str, size_str = line.strip().split(',')
                if not pts_time_str or not size_str: continue
                pts_time, size = float(pts_time_str), int(size_str)
                if pts_time >= current_interval_end:
                    bitrate = (interval_size * 8) / (interval * 1000)
                    bitrate_data.append(bitrate)
                    interval_size = 0
                    current_interval_end += interval
                interval_size += size
                progress = int((pts_time / total_duration) * 100)
                if progress > last_progress:
                    progress_callback(progress)
                    last_progress = progress
            except (ValueError, IndexError): continue
        if interval_size > 0:
            bitrate_data.append((interval_size * 8) / (interval * 1000))
        process.wait()
        progress_callback(100)
        return bitrate_data

    # --- CORRECTED SECTION START ---
    def plot_bitrate_chart(self, bitrate_data, details_string):
        """Creates and saves a chart with a clean layout for media details."""
        if not bitrate_data:
            raise ValueError("No bitrate data was generated to plot.")
        
        # BUG FIX: The 'time_points' variable was missing. It is defined here.
        time_points = np.arange(len(bitrate_data))

        fig, ax = plt.subplots(figsize=(15, 8))
        ax.plot(time_points, bitrate_data, label=f'{self.stream_type.capitalize()} Bitrate (kbps)', color='royalblue')
        
        base_filename = os.path.basename(self.file_path)
        wrapped_title = textwrap.fill(base_filename, 80)
        fig.suptitle(f"Bitrate Analysis for:\n{wrapped_title}", fontsize=14, y=0.98)
        
        fig.subplots_adjust(top=0.85, bottom=0.1, left=0.07, right=0.95)

        fig.text(0.5, 0.9, details_string, 
                 ha='center', va='center', fontsize=9, 
                 bbox=dict(boxstyle='round,pad=0.5', fc='aliceblue', ec='lightsteelblue', lw=1))

        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Bitrate (kbps)')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)

        output_filename = f"bitrate_chart_{os.path.splitext(base_filename)[0]}.png"
        fig.savefig(output_filename)
        plt.close(fig)
        return output_filename
    # --- CORRECTED SECTION END ---

# --- The Controller and View classes remain unchanged ---
class AnalysisWorker(threading.Thread):
    def __init__(self, file_paths, comm_queue):
        super().__init__()
        self.file_paths = file_paths
        self.queue = comm_queue

    def run(self):
        total_files = len(self.file_paths)
        for i, path in enumerate(self.file_paths):
            try:
                self.queue.put({
                    'type': 'batch_progress', 'current': i + 1, 'total': total_files,
                    'filename': os.path.basename(path)
                })
                engine = VideoAnalysisEngine(path)
                self.queue.put({'type': 'status', 'msg': 'Getting media metadata...'})
                engine.get_media_info()
                details_string = engine.get_formatted_details_string()
                self.queue.put({'type': 'status', 'msg': 'Analyzing packet data...'})
                def progress_callback(percent):
                    self.queue.put({'type': 'progress', 'value': percent})
                bitrate_data = engine.generate_bitrate_data(progress_callback)
                self.queue.put({'type': 'status', 'msg': 'Generating chart...'})
                output_path = engine.plot_bitrate_chart(bitrate_data, details_string)
                self.queue.put({'type': 'file_complete', 'path': output_path})
            except Exception as e:
                error_msg = f"Failed to process '{os.path.basename(path)}': {e}"
                self.queue.put({'type': 'error', 'msg': error_msg})
        self.queue.put({'type': 'batch_complete', 'total': total_files})

class VideoAnalyzerApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Media Bitrate Analyzer v4 | BY : RIFAT ") # Version updated
        self.geometry("700x450")
        self.comm_queue = queue.Queue()
        self.file_paths = []
        self.is_processing = False
        self._check_dependencies()
        self._create_widgets()
        self._setup_drag_and_drop()

    def _check_dependencies(self):
        try:
            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.Popen(['ffprobe', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)
        except FileNotFoundError:
            messagebox.showerror("Dependency Missing", "FFmpeg/ffprobe not found. Please install FFmpeg and ensure it's in your system's PATH.")
            self.destroy()
            sys.exit(1)

    def _create_widgets(self):
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        list_frame = ttk.LabelFrame(self.main_frame, text="Media Files to Analyze (Drag & Drop or Browse)")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        self.file_listbox.bind('<<ListboxSelect>>', self._on_selection_change)
        list_button_frame = ttk.Frame(self.main_frame)
        list_button_frame.pack(fill=tk.X, pady=(0, 5))
        self.select_all_button = ttk.Button(list_button_frame, text="Select All", command=lambda: self.file_listbox.select_set(0, tk.END))
        self.select_all_button.pack(side=tk.LEFT)
        self.deselect_all_button = ttk.Button(list_button_frame, text="Deselect All", command=lambda: self.file_listbox.select_clear(0, tk.END))
        self.deselect_all_button.pack(side=tk.LEFT, padx=5)
        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(fill=tk.X, pady=5)
        self.browse_button = ttk.Button(control_frame, text="Browse Files", command=self._browse_files)
        self.browse_button.pack(side=tk.LEFT, padx=(0,5))
        self.clear_button = ttk.Button(control_frame, text="Clear List", command=self._clear_list)
        self.clear_button.pack(side=tk.LEFT)
        self.analyze_button = ttk.Button(control_frame, text="Analyze Selected", command=self._start_analysis)
        self.analyze_button.pack(side=tk.RIGHT)
        self.analyze_button.config(state=tk.DISABLED)
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, pady=5, side=tk.BOTTOM)
        self.progress_bar = ttk.Progressbar(status_frame, orient='horizontal', mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=5)
        self.status_label = ttk.Label(status_frame, text="Add files by browsing or drag-and-drop.", anchor=tk.W)
        self.status_label.pack(fill=tk.X)

    def _setup_drag_and_drop(self):
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self._on_drop)

    def _on_drop(self, event):
        files = self.tk.splitlist(event.data)
        for f in files: self._add_file_to_list(f)
    
    def _browse_files(self):
        files = filedialog.askopenfilenames(title="Select Media Files", filetypes=[("All files", "*.*")])
        for f in files: self._add_file_to_list(f)
            
    def _add_file_to_list(self, file_path):
        if file_path not in self.file_paths:
            self.file_paths.append(file_path)
            self.file_listbox.insert(tk.END, os.path.basename(file_path))

    def _clear_list(self):
        self.file_paths.clear()
        self.file_listbox.delete(0, tk.END)
        self._on_selection_change()
        self.status_label.config(text="File list cleared.")

    def _on_selection_change(self, event=None):
        if self.file_listbox.curselection():
            self.analyze_button.config(state=tk.NORMAL)
        else:
            self.analyze_button.config(state=tk.DISABLED)
    
    def _start_analysis(self):
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select one or more files to analyze.")
            return
        if self.is_processing:
            messagebox.showwarning("Busy", "An analysis is already in progress.")
            return
        files_to_process = [self.file_paths[i] for i in selected_indices]
        self.is_processing = True
        self._toggle_controls(tk.DISABLED)
        self.progress_bar['value'] = 0
        self.worker = AnalysisWorker(files_to_process, self.comm_queue)
        self.worker.start()
        self.after(100, self._process_queue)

    def _process_queue(self):
        try:
            msg = self.comm_queue.get_nowait()
            msg_type = msg.get('type')
            if msg_type == 'batch_progress':
                self.status_label.config(text=f"Analyzing {msg['current']}/{msg['total']}: {msg['filename']}")
                self.progress_bar['value'] = 0
            elif msg_type == 'progress':
                self.progress_bar['value'] = msg['value']
            elif msg_type == 'status':
                current_status = self.status_label.cget("text").split('...')[0]
                self.status_label.config(text=f"{current_status}... {msg['msg']}")
            elif msg_type == 'file_complete':
                pass
            elif msg_type == 'error':
                messagebox.showerror("Processing Error", msg['msg'])
            elif msg_type == 'batch_complete':
                messagebox.showinfo("Success", f"Batch processing complete. Analyzed {msg['total']} files.")
                self.status_label.config(text=f"Finished processing {msg['total']} files.")
                self._analysis_finished()
            self.after(100, self._process_queue)
        except queue.Empty:
            if self.is_processing:
                self.after(100, self._process_queue)

    def _analysis_finished(self):
        self.is_processing = False
        self._toggle_controls(tk.NORMAL)
        self.progress_bar['value'] = 0

    def _toggle_controls(self, state):
        for button in [self.browse_button, self.clear_button, self.analyze_button, self.select_all_button, self.deselect_all_button]:
            button.config(state=state)
        self.file_listbox.config(state=state if state == tk.NORMAL else tk.DISABLED)
        if state == tk.NORMAL:
            self._on_selection_change()

if __name__ == "__main__":
    app = VideoAnalyzerApp()
    app.mainloop()