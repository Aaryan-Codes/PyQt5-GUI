class DarkTheme:
    COLORS = {
        "primary": "#1E1E1E",       # Darker background for better contrast
        "secondary": "#252526",     # Widget background
        "accent": "#007ACC",        # Muted blue accent
        "text_primary": "#404040",  # Brighter primary text
        "text_secondary": "#858585",# Secondary text
        "border": "#3C3C3C",        # Consistent border color
        "warning": "#CE9178",       # Soft orange
        "success": "#608B4E",       # Muted green
        "critical": "#D16969",       # Soft red
        "heading": "#2A9FD6",       # Muted blue
    }
    
    STYLESHEET = f"""
    QWidget {{
        background-color: {COLORS["primary"]};
        color: {COLORS["text_primary"]};
        font-family: "Segoe UI", sans-serif;
        selection-background-color: {COLORS["accent"]};
    }}
    
    QGroupBox {{
        border: 1px solid {COLORS["border"]};
        border-radius: 4px;
        margin-top: 1ex;
        margin-bottom: 1ex;
        padding-top: 2ex;
        background-color: {COLORS["secondary"]};
        font: bold 14px;
    }}
    
    QGroupBox::title {{
        color: {COLORS["heading"]};
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
        font: bold 14px;
        text-transform: uppercase;
    }}
    
    QGroupBox#PositionWidget {{
        border: 2px solid {COLORS["border"]} !important;
    }}
    
    QLabel {{
        color: {COLORS["text_primary"]};
        font: 12px;
    }}
    
    QProgressBar {{
        border: 1px solid {COLORS["border"]};
        border-radius: 4px;
        background: {COLORS["secondary"]};
        text-align: center;
        color: {COLORS["text_primary"]};
    }}
    
    QProgressBar::chunk {{
        background-color: {COLORS["accent"]};
        border-radius: 4px;
    }}
    
    /* Status indicators */
    .success {{
        color: {COLORS["success"]};
        background-color: rgba(96, 139, 78, 0.15);
    }}
    
    .warning {{
        color: {COLORS["warning"]};
        background-color: rgba(206, 145, 120, 0.15);
    }}
    
    .critical {{
        color: {COLORS["critical"]};
        background-color: rgba(209, 105, 105, 0.15);
    }}
    
    /* Specific widget overrides */
    MotorWidget, BatteryWidget, GPSWidget {{
        qproperty-alignment: AlignCenter;
    }}
    
    SensorWidget {{
        border-color: {COLORS["accent"]};
    }}
    """