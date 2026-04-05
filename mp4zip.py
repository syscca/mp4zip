import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import threading
import re
import time

class MP4ZipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MP4 极限压缩工具 v1.0")
        self.root.geometry("600x450")
        
        self.file_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.compression_level = tk.IntVar(value=1) # 0: 标准, 1: 强力, 2: 极限
        self.use_qsv = tk.BooleanVar(value=True) # 默认开启 QSV
        self.is_compressing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 文件选择
        ttk.Label(main_frame, text="选择 MP4 视频文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.file_path, width=50).grid(row=1, column=0, padx=5)
        ttk.Button(main_frame, text="浏览...", command=self.browse_file).grid(row=1, column=1)
        
        # 压缩等级选择
        ttk.Label(main_frame, text="压缩强度 (强度越高，体积越小，处理越慢):").grid(row=2, column=0, sticky=tk.W, pady=(20, 5))
        radio_frame = ttk.Frame(main_frame)
        radio_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W)
        
        ttk.Radiobutton(radio_frame, text="标准 (H.264, 速度快)", variable=self.compression_level, value=0).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(radio_frame, text="强力 (H.265, 推荐)", variable=self.compression_level, value=1).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(radio_frame, text="极限 (H.265 Slow, 最小体积)", variable=self.compression_level, value=2).pack(side=tk.LEFT, padx=10)
        
        # 硬件加速选项
        ttk.Checkbutton(main_frame, text="开启英特尔核显加速 (QSV)", variable=self.use_qsv).grid(row=4, column=0, sticky=tk.W, pady=5)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20)
        
        # 状态显示
        self.status_label = ttk.Label(main_frame, text="准备就绪")
        self.status_label.grid(row=6, column=0, columnspan=2, pady=5)
        
        # 按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        self.start_btn = ttk.Button(btn_frame, text="开始压缩", command=self.start_compression_thread)
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        # 日志区域
        self.log_text = tk.Text(main_frame, height=8, width=70, state=tk.DISABLED, font=("Consolas", 9))
        self.log_text.grid(row=8, column=0, columnspan=2, pady=10)
        
    def browse_file(self):
        file = filedialog.askopenfilename(filetypes=[("MP4 视频", "*.mp4"), ("所有文件", "*.*")])
        if file:
            self.file_path.set(file)
            self.log(f"已选择文件: {file}")
            
    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def get_video_duration(self, file_path):
        try:
            cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            return float(result.stdout.strip())
        except:
            return 0

    def start_compression_thread(self):
        if not self.file_path.get():
            messagebox.showwarning("提示", "请先选择一个 MP4 文件！")
            return
        
        if self.is_compressing:
            return
            
        self.is_compressing = True
        self.start_btn.config(state=tk.DISABLED)
        threading.Thread(target=self.run_compression, daemon=True).start()

    def run_compression(self):
        input_file = self.file_path.get()
        file_dir = os.path.dirname(input_file)
        file_name = os.path.basename(input_file)
        name_no_ext = os.path.splitext(file_name)[0]
        output_file = os.path.join(file_dir, f"{name_no_ext}_compressed.mp4")
        
        # 确保输出文件名不冲突
        counter = 1
        while os.path.exists(output_file):
            output_file = os.path.join(file_dir, f"{name_no_ext}_compressed_{counter}.mp4")
            counter += 1

        duration = self.get_video_duration(input_file)
        
        # 压缩参数配置
        level = self.compression_level.get()
        use_qsv = self.use_qsv.get()
        
        if use_qsv:
            if level == 0: # 标准 QSV
                cmd = [
                    'ffmpeg', '-hwaccel', 'qsv', '-i', input_file,
                    '-c:v', 'h264_qsv', '-global_quality', '25', '-preset', 'slower',
                    '-c:a', 'aac', '-b:a', '128k',
                    '-y', output_file
                ]
                self.log("模式: 标准 (H.264 + QSV 加速)")
            elif level == 1: # 强力 QSV
                cmd = [
                    'ffmpeg', '-hwaccel', 'qsv', '-i', input_file,
                    '-c:v', 'hevc_qsv', '-global_quality', '28', '-preset', 'slower',
                    '-c:a', 'aac', '-b:a', '96k',
                    '-y', output_file
                ]
                self.log("模式: 强力 (H.265 + QSV 加速)")
            else: # 极限 QSV
                cmd = [
                    'ffmpeg', '-hwaccel', 'qsv', '-i', input_file,
                    '-c:v', 'hevc_qsv', '-global_quality', '32', '-preset', 'veryslow',
                    '-c:a', 'aac', '-b:a', '64k',
                    '-y', output_file
                ]
                self.log("模式: 极限 (H.265 + QSV 加速)")
        else:
            if level == 0: # 标准 CPU
                cmd = [
                    'ffmpeg', '-i', input_file,
                    '-c:v', 'libx264', '-crf', '23', '-preset', 'medium',
                    '-c:a', 'aac', '-b:a', '128k',
                    '-y', output_file
                ]
                self.log("模式: 标准 (H.264 CPU)")
            elif level == 1: # 强力 CPU
                cmd = [
                    'ffmpeg', '-i', input_file,
                    '-c:v', 'libx265', '-crf', '28', '-preset', 'medium',
                    '-c:a', 'aac', '-b:a', '96k',
                    '-y', output_file
                ]
                self.log("模式: 强力 (H.265 CPU)")
            else: # 极限 CPU
                cmd = [
                    'ffmpeg', '-i', input_file,
                    '-c:v', 'libx265', '-crf', '32', '-preset', 'slow',
                    '-c:a', 'aac', '-b:a', '64k',
                    '-y', output_file
                ]
                self.log("模式: 极限 (H.265 CPU Slow)")

        self.log(f"开始压缩: {file_name}")
        self.status_label.config(text="正在压缩中...")
        
        try:
            # 运行 ffmpeg 并解析进度
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8',
                errors='replace'
            )
            
            time_re = re.compile(r'time=(\d+):(\d+):(\d+\.\d+)')
            
            for line in process.stdout:
                match = time_re.search(line)
                if match and duration > 0:
                    hours, minutes, seconds = map(float, match.groups())
                    current_time = hours * 3600 + minutes * 60 + seconds
                    progress = min(100, (current_time / duration) * 100)
                    self.progress_var.set(progress)
                    self.root.update_idletasks()
            
            process.wait()
            
            if process.returncode == 0:
                old_size = os.path.getsize(input_file) / (1024 * 1024)
                new_size = os.path.getsize(output_file) / (1024 * 1024)
                self.log(f"压缩成功！")
                self.log(f"原始大小: {old_size:.2f} MB")
                self.log(f"压缩后大小: {new_size:.2f} MB")
                self.log(f"保存路径: {output_file}")
                self.status_label.config(text="压缩完成")
                self.progress_var.set(100)
                messagebox.showinfo("完成", f"视频压缩完成！\n体积减小: {((old_size-new_size)/old_size*100):.1f}%")
            else:
                self.log("压缩失败，请检查文件是否损坏。")
                self.status_label.config(text="压缩失败")
                
        except Exception as e:
            self.log(f"错误: {str(e)}")
            self.status_label.config(text="程序异常")
        
        self.is_compressing = False
        self.start_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = MP4ZipApp(root)
    root.mainloop()
