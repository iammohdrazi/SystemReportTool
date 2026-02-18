# System Report Tool

A comprehensive system monitoring and reporting tool built with Flask that provides real-time system information through a web interface and generates detailed system reports.

## Features

- **Real-time System Monitoring**: Monitor CPU, memory, disk, network, and battery status
- **Web Interface**: Clean, responsive web dashboard for viewing system information
- **Report Generation**: Generate detailed text-based system reports
- **Process Monitoring**: View top processes by CPU usage
- **Cross-platform**: Works on Windows, Linux, and macOS
- **Logging**: Comprehensive logging of system activities
- **Auto-refresh**: Configurable auto-refresh for real-time updates

## Versions

This repository contains multiple versions of the tool:
- `system_report_tool_v1.py` - Initial version with basic functionality
- `system_report_tool_v2.py` - Enhanced version with improved UI and additional features
- `system_report_tool_v3.py` - Latest version with advanced monitoring capabilities
- `cli/` - Command-line interface version for terminal usage

## Requirements

- Python 3.7+
- Flask
- psutil
- webbrowser (built-in)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd SystemReportTool
```

2. Install required packages:
```bash
pip install flask psutil
```

## Usage

### Web Interface Version

Run the latest version (v3):
```bash
python system_report_tool_v3.py
```

The application will start a web server and automatically open your default browser to view the dashboard.

### CLI Version

Navigate to the cli directory:
```bash
cd cli
python system_report.py
```

## Output

The tool generates:
- **Web Dashboard**: Real-time system information displayed in your browser
- **Log Files**: Stored in `log/` directory with detailed activity logs
- **System Reports**: Generated in `report/` directory as text files

## System Information Monitored

- **System Info**: OS, hostname, architecture, uptime
- **CPU**: Usage, core count, frequency
- **Memory**: Total, available, used, percentage
- **Disk**: Partitions, usage statistics
- **Network**: Interfaces, I/O statistics
- **Battery**: Status, percentage (if available)
- **Processes**: Top processes by CPU usage

## Configuration

- Default port: 5000
- Auto-refresh interval: 5 seconds (configurable)
- Log level: INFO
- Report format: Text file

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please see the LICENSE file for details.

## Troubleshooting

- **Port already in use**: Change the port in the script
- **Missing dependencies**: Ensure all requirements are installed
- **Permission issues**: Run with appropriate permissions for system access

## Author

System monitoring tool for comprehensive system analysis and reporting.
