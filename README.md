# 🚀 System Optimizer Tool

A modern, portable system optimization utility built with Python and CustomTkinter. Monitor system resources, clean temporary files, and optimize your system performance - all without admin rights!

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 📊 System Monitoring
- **Real-time CPU Usage** - Live CPU utilization with progress visualization
- **Memory Tracking** - RAM usage and available memory display
- **Disk Space Analysis** - Storage usage and free space monitoring
- **Network Statistics** - Data sent/received tracking
- **System Uptime** - Current system uptime display

### 🧹 Cleaning Tools
- **Temporary Files Cleaner** - Remove junk files from multiple temp directories
- **Safe Cleaning** - No system files affected, permission error handling
- **Space Recovery** - Track how much disk space was freed

### ⚡ Performance Tools
- **Quick System Scan** - Health check for CPU, memory, and disk
- **Real-time Updates** - Automatic 5-second refresh cycles
- **Activity Logging** - Detailed operation log with color-coded messages

### 🎨 Modern Interface
- **Dark Theme** - Easy on the eyes modern UI
- **Scrollable Design** - Handles all screen sizes gracefully
- **Responsive Layout** - Adapts to window resizing
- **Progress Indicators** - Visual feedback for all operations

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Dependencies Installation
```bash
pip install customtkinter psutil
```

### Quick Start
```bash
# Download the script and run:
python system_optimizer.py
```

## 📦 Portable Usage

This application is designed to be completely portable:
- ✅ No installation required
- ✅ No admin rights needed
- ✅ No system modifications
- ✅ Single-file executable (when packaged)

## 🎯 Usage Guide

### System Overview Panel
- Monitor real-time system metrics at a glance
- Click **🔄 Refresh** for immediate updates
- Automatic updates every 5 seconds

### Quick Actions
1. **🧹 Clean Temporary Files**
   - Safely removes temp files from multiple locations
   - Shows files cleaned and space recovered
   - Handles permission errors gracefully

2. **🔍 Quick System Scan**
   - Performs system health check
   - Provides recommendations
   - Color-coded health indicators

### Advanced Tools
- Browser cache management
- Print spooler cleanup
- System reporting
- Process monitoring
- Network statistics
- Performance metrics

### Activity Log
- View all operations in real-time
- Color-coded message types
- Clear log functionality
- Auto-scroll to latest entries

## 🔧 Technical Details

### Supported Temp Locations
- System temp directory
- User AppData temp folders
- Windows temporary internet files
- *Easily extensible for more locations*

### System Requirements
- **RAM**: 512MB minimum
- **Storage**: 50MB free space
- **Permissions**: User-level access
- **OS**: Windows 10/11, Linux, macOS

### Safety Features
- Read-only system monitoring
- Safe file deletion with validation
- Permission error handling
- No registry modifications
- No system file access

## 🚨 Safety & Privacy

### 🔒 Security Guarantees
- **No Internet Access** - All operations are local
- **No Data Collection** - Complete privacy
- **No System Modifications** - Read-only except for temp files
- **Open Source** - Fully transparent code

### 🗑️ What Gets Cleaned
- Browser cache files
- Temporary application data
- Download cache files
- **No personal files affected**

## 🐛 Troubleshooting

### Common Issues

**"Permission Denied" Errors**
- Normal - indicates protected system files being skipped
- Application continues working normally

**High CPU Usage Display**
- Monitor running processes in Task Manager
- Use built-in quick scan for recommendations

**Temporary Files Not Cleaning**
- Some files may be in use by other applications
- Try closing other apps and retry

### Getting Help
1. Check the activity log for specific error messages
2. Ensure all dependencies are installed
3. Verify Python version compatibility

## 🛡️ Legal & Compliance

- **License**: MIT License
- **Privacy**: No data collection or telemetry
- **Safety**: No system modifications without user consent
- **Open Source**: Full code transparency

## 🔮 Future Enhancements

Planned features:
- [ ] Cross-platform temp file detection
- [ ] Startup program management
- [ ] Duplicate file finder
- [ ] Large file analyzer
- [ ] Automated maintenance scheduling

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional system monitors
- More cleaning options
- UI/UX enhancements
- Cross-platform compatibility

## 📄 License

MIT License - feel free to use, modify, and distribute.

---


