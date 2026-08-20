class SynthNodeWidget(QFrame):
    """Editable modular node frame with a replaceable name/type field."""
    def __init__(self, name, x, y, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setLineWidth(2)
        self.resize(200, 130)
        self.move(x, y)
        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff; border: 1px solid #555; border-radius: 6px;")
        
        layout = QVBoxLayout(self)
        
        # Use QLineEdit for editing/replacing and set title_label as an alias if needed
        self.title_input = QLineEdit(name)
        self.title_input.setStyleSheet("background-color: #2a2a2a; color: #ffffff; border: 1px solid #666; padding: 2px;")
        self.title_label = self.title_input  # Backwards compatibility alias to prevent AttributeError
        layout.addWidget(self.title_input)
        
        ports_layout = QHBoxLayout()
        
        in_container = QVBoxLayout()
        lbl_in = QLabel("In")
        lbl_in.setStyleSheet("color: #aaa; border: none; font-size: 11px;")
        in_container.addWidget(lbl_in)
        self.in_port = PortWidget('in', self)
        in_container.addWidget(self.in_port)
        
        out_container = QVBoxLayout()
        lbl_out = QLabel("Out")
        lbl_out.setStyleSheet("color: #aaa; border: none; font-size: 11px;")
        out_container.addWidget(lbl_out)
        self.out_port = PortWidget('out', self)
        out_container.addWidget(self.out_port)
        
        ports_layout.addLayout(in_container)
        ports_layout.addLayout(out_container)
        layout.addLayout(ports_layout)

        self.dragging = False
        self.drag_position = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton and self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            if self.parent():
                self.parent().update()
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False
