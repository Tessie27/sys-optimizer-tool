import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import shutil
import psutil
import time
from datetime import timedelta
import tempfile

# Set modern theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ModernSystemApp:
    def __init__(self):
        self.temp_folders = [
            tempfile.gettempdir(),
            os.path.expanduser('~\\AppData\\Local\\Temp'),
            os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\Temporary Internet Files'),
        ]
    
    def get_system_uptime(self):
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        uptime_str = str(timedelta(seconds=uptime_seconds))
        return uptime_str.split('.')[0]
    
    def get_system_info(self):
        # CPU and Memory
        cpu_percent = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Network
        net_io = psutil.net_io_counters()
        
        return {
            'uptime': self.get_system_uptime(),
            'cpu_usage': cpu_percent,
            'memory_usage': memory.percent,
            'memory_available': memory.available // (1024**3),
            'memory_total': memory.total // (1024**3),
            'disk_usage': disk.percent,
            'disk_free': disk.free // (1024**3),
            'disk_total': disk.total // (1024**3),
            'bytes_sent': net_io.bytes_sent // (1024**2),
            'bytes_recv': net_io.bytes_recv // (1024**2)
        }
    
    def clear_temp_files(self):
        cleaned_files = 0
        cleaned_size = 0
        errors = []
        
        for temp_folder in self.temp_folders:
            if os.path.exists(temp_folder):
                try:
                    for root, dirs, files in os.walk(temp_folder):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                if os.path.isfile(file_path):
                                    file_size = os.path.getsize(file_path)
                                    os.remove(file_path)
                                    cleaned_files += 1
                                    cleaned_size += file_size
                            except (PermissionError, OSError):
                                continue
                except (PermissionError, OSError):
                    errors.append(f"Could not access: {temp_folder}")
        
        return cleaned_files, cleaned_size // (1024**2), errors

class ScrollableModernGUI:
    def __init__(self):
        self.app = ModernSystemApp()
        self.setup_window()
        self.create_scrollable_interface()
        self.start_updates()
    
    def setup_window(self):
        self.root = ctk.CTk()
        self.root.title("🚀 System Optimizer Pro")
        self.root.geometry("900x600")  # Smaller default size to demonstrate scrolling
        self.root.minsize(850, 500)
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
    
    def create_scrollable_interface(self):
        # Create main container
        main_container = ctk.CTkFrame(self.root, corner_radius=0)
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Create a canvas and scrollbar for vertical scrolling
        self.canvas = tk.Canvas(main_container, bg='#2b2b2b', highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(main_container, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas, corner_radius=0)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=20)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=20)
        
        # Bind mouse wheel to canvas
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)
        
        # Create all widgets in the scrollable frame
        self.create_header()
        self.create_stats_section()
        self.create_actions_section()
        self.create_advanced_section()
        self.create_log_section()
    
    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def create_header(self):
        header_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Title and subtitle
        title = ctk.CTkLabel(header_frame, 
                           text="🚀 System Optimizer Pro", 
                           font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(side="left")
        
        subtitle = ctk.CTkLabel(header_frame, 
                              text="Portable System Utility • No Admin Rights Required",
                              font=ctk.CTkFont(size=12),
                              text_color="gray")
        subtitle.pack(side="left", padx=(10, 0), pady=(5, 0))
        
        # Refresh button
        self.refresh_btn = ctk.CTkButton(header_frame, 
                                       text="🔄 Refresh", 
                                       width=100,
                                       command=self.refresh_all,
                                       font=ctk.CTkFont(size=12))
        self.refresh_btn.pack(side="right")
    
    def create_stats_section(self):
        stats_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        # Section title
        ctk.CTkLabel(stats_frame, text="📊 System Overview", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Stats grid
        grid_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Row 1
        row1 = ctk.CTkFrame(grid_frame, fg_color="transparent")
        row1.pack(fill="x", pady=5)
        
        self.uptime_label = self.create_stat_card(row1, "⏰ System Uptime", "Loading...", 0)
        self.cpu_label = self.create_stat_card(row1, "⚡ CPU Usage", "Loading...", 1)
        self.memory_label = self.create_stat_card(row1, "💾 Memory", "Loading...", 2)
        
        # Row 2
        row2 = ctk.CTkFrame(grid_frame, fg_color="transparent")
        row2.pack(fill="x", pady=5)
        
        self.disk_label = self.create_stat_card(row2, "💽 Disk Usage", "Loading...", 0)
        self.net_sent_label = self.create_stat_card(row2, "📤 Data Sent", "Loading...", 1)
        self.net_recv_label = self.create_stat_card(row2, "📥 Data Received", "Loading...", 2)
    
    def create_stat_card(self, parent, title, value, column):
        card = ctk.CTkFrame(parent, corner_radius=8, height=80)
        card.pack(side="left", fill="x", expand=True, padx=5)
        
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 0))
        value_label = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=14))
        value_label.pack(pady=(5, 10))
        
        return value_label
    
    def create_actions_section(self):
        actions_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        actions_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(actions_frame, text="🛠️ Quick Actions", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.clean_btn = ctk.CTkButton(buttons_frame, 
                                     text="🧹 Clean Temporary Files", 
                                     command=self.clean_temp_files,
                                     font=ctk.CTkFont(size=13),
                                     height=40,
                                     fg_color="#E74C3C",
                                     hover_color="#C0392B")
        self.clean_btn.pack(side="left", padx=(0, 10))
        
        self.quick_scan_btn = ctk.CTkButton(buttons_frame, 
                                          text="🔍 Quick System Scan", 
                                          command=self.quick_scan,
                                          font=ctk.CTkFont(size=13),
                                          height=40)
        self.quick_scan_btn.pack(side="left", padx=10)
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(actions_frame, height=20, corner_radius=10)
        self.progress.pack(fill="x", padx=15, pady=(10, 15))
        self.progress.set(0)
        
        # Progress label
        self.progress_label = ctk.CTkLabel(actions_frame, text="Ready", text_color="gray")
        self.progress_label.pack(pady=(0, 10))
    
    def create_advanced_section(self):
        """Additional section to demonstrate scrolling"""
        advanced_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        advanced_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(advanced_frame, text="⚙️ Advanced Tools", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Advanced buttons grid
        grid_frame = ctk.CTkFrame(advanced_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Row 1
        row1 = ctk.CTkFrame(grid_frame, fg_color="transparent")
        row1.pack(fill="x", pady=5)
        
        btn1 = ctk.CTkButton(row1, text="📁 Browser Cache", height=35,
                           command=lambda: self.log_message("📁 Browser cache cleanup clicked", "#3498DB"))
        btn1.pack(side="left", padx=5, expand=True, fill="x")
        
        btn2 = ctk.CTkButton(row1, text="🖨️ Print Spooler", height=35,
                           command=lambda: self.log_message("🖨️ Print spooler cleanup clicked", "#3498DB"))
        btn2.pack(side="left", padx=5, expand=True, fill="x")
        
        btn3 = ctk.CTkButton(row1, text="📊 System Report", height=35,
                           command=lambda: self.log_message("📊 System report generated", "#3498DB"))
        btn3.pack(side="left", padx=5, expand=True, fill="x")
        
        # Row 2
        row2 = ctk.CTkFrame(grid_frame, fg_color="transparent")
        row2.pack(fill="x", pady=5)
        
        btn4 = ctk.CTkButton(row2, text="🔍 Process Monitor", height=35,
                           command=lambda: self.log_message("🔍 Process monitor opened", "#3498DB"))
        btn4.pack(side="left", padx=5, expand=True, fill="x")
        
        btn5 = ctk.CTkButton(row2, text="🌐 Network Stats", height=35,
                           command=lambda: self.log_message("🌐 Network statistics shown", "#3498DB"))
        btn5.pack(side="left", padx=5, expand=True, fill="x")
        
        btn6 = ctk.CTkButton(row2, text="⚡ Performance", height=35,
                           command=lambda: self.log_message("⚡ Performance metrics displayed", "#3498DB"))
        btn6.pack(side="left", padx=5, expand=True, fill="x")
    
    def create_log_section(self):
        log_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        log_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        # Log header with clear button
        log_header = ctk.CTkFrame(log_frame, fg_color="transparent")
        log_header.pack(fill="x", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(log_header, text="📝 Activity Log", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
        
        clear_btn = ctk.CTkButton(log_header, text="Clear Log", width=80,
                                command=self.clear_log,
                                font=ctk.CTkFont(size=12))
        clear_btn.pack(side="right")
        
        # Log text area
        self.log_text = ctk.CTkTextbox(log_frame, 
                                     font=ctk.CTkFont(family="Consolas", size=12),
                                     wrap="word",
                                     corner_radius=8,
                                     height=200)  # Fixed height for log area
        self.log_text.pack(fill="x", padx=15, pady=(0, 15))
    
    def clear_log(self):
        self.log_text.delete("1.0", "end")
        self.log_message("📝 Log cleared", "#95A5A6")
    
    def log_message(self, message, color=None):
        tag = f"color_{hash(message)}"
        if color:
            self.log_text.tag_config(tag, foreground=color)
            self.log_text.insert("end", f"{message}\n", tag)
        else:
            self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.root.update()
    
    def refresh_all(self):
        self.log_message("🔄 Refreshing system information...", "#3498DB")
        self.update_system_info()
    
    def update_system_info(self):
        def update_thread():
            try:
                info = self.app.get_system_info()
                
                # Update all labels
                self.uptime_label.configure(text=info['uptime'])
                self.cpu_label.configure(text=f"{info['cpu_usage']}%")
                self.memory_label.configure(text=f"{info['memory_usage']}% ({info['memory_available']}GB free)")
                self.disk_label.configure(text=f"{info['disk_usage']}% ({info['disk_free']}GB free)")
                self.net_sent_label.configure(text=f"{info['bytes_sent']} MB")
                self.net_recv_label.configure(text=f"{info['bytes_recv']} MB")
                
                # Update progress for CPU
                self.progress.set(info['cpu_usage'] / 100)
                
            except Exception as e:
                self.log_message(f"❌ Error updating system info: {str(e)}", "#E74C3C")
        
        threading.Thread(target=update_thread, daemon=True).start()
    
    def clean_temp_files(self):
        def cleanup_thread():
            self.clean_btn.configure(state="disabled")
            self.progress_label.configure(text="Cleaning temporary files...")
            
            # Animated progress
            for i in range(101):
                self.progress.set(i/100)
                time.sleep(0.01)
            
            files, size, errors = self.app.clear_temp_files()
            
            self.progress.set(0)
            self.clean_btn.configure(state="normal")
            self.progress_label.configure(text="Ready")
            
            self.log_message(f"✅ Successfully cleaned {files} files", "#27AE60")
            self.log_message(f"💾 Freed {size} MB of disk space", "#27AE60")
            
            if errors:
                self.log_message(f"⚠️  {len(errors)} items could not be cleaned", "#F39C12")
            
            self.update_system_info()
            messagebox.showinfo("Cleanup Complete", 
                              f"Cleaned {files} files\nFreed {size} MB of space")
        
        self.log_message("🧹 Starting temporary files cleanup...", "#3498DB")
        threading.Thread(target=cleanup_thread, daemon=True).start()
    
    def quick_scan(self):
        def scan_thread():
            self.quick_scan_btn.configure(state="disabled")
            self.progress_label.configure(text="Performing quick scan...")
            
            # Simulate scanning process
            for i in range(101):
                self.progress.set(i/100)
                time.sleep(0.02)
            
            info = self.app.get_system_info()
            self.progress.set(0)
            self.quick_scan_btn.configure(state="normal")
            self.progress_label.configure(text="Ready")
            
            # Log scan results
            self.log_message("🔍 Quick Scan Results:", "#9B59B6")
            self.log_message(f"   CPU Health: {'✅ Good' if info['cpu_usage'] < 80 else '⚠️ High Usage'}")
            self.log_message(f"   Memory Health: {'✅ Good' if info['memory_usage'] < 85 else '⚠️ High Usage'}")
            self.log_message(f"   Disk Health: {'✅ Good' if info['disk_usage'] < 90 else '⚠️ Nearly Full'}")
            self.log_message("✅ Quick scan completed", "#27AE60")
        
        self.log_message("🔍 Starting quick system scan...", "#9B59B6")
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def start_updates(self):
        # Initial update
        self.update_system_info()
        
        # Set up periodic updates
        def periodic_update():
            while True:
                time.sleep(5)
                self.update_system_info()
        
        threading.Thread(target=periodic_update, daemon=True).start()

def main():
    app = ScrollableModernGUI()
    app.root.mainloop()

if __name__ == "__main__":
    main()