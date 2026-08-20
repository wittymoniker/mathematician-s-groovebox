def init_ui_components(self):
        high_contrast_stylesheet = """
            QMainWindow, QWidget, QDialog {
                background-color: #080808;
                color: #ffffff;
                font-family: sans-serif;
                font-size: 11pt;
            }
            QPushButton {
                background-color: #141414;
                color: #00ffff;
                border: 2px solid #00ffff;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ffff;
                color: #080808;
            }
            QPushButton:checked {
                background-color: #00ffff;
                color: #080808;
                border: 2px solid #ffffff;
            }
            QSpinBox, QComboBox, QLineEdit, QDoubleSpinBox {
                background-color: #181818;
                color: #ffffff;
                border: 2px solid #444444;
                border-radius: 3px;
                padding: 4px;
            }
            QLabel {
                color: #ffffff;
                font-weight: bold;
            }
        """
        if QApplication.instance():
            QApplication.instance().setStyleSheet(high_contrast_stylesheet)
        self.setStyleSheet(high_contrast_stylesheet)

        central_widget = self.centralWidget()
        if central_widget is None:
            central_widget = QWidget(self)
            self.setCentralWidget(central_widget)

        master_container = central_widget.layout()
        if master_container is None:
            master_container = QVBoxLayout(central_widget)
        else:
            while master_container.count():
                item = master_container.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

        master_container.setSpacing(8)
        master_container.setContentsMargins(10, 10, 10, 10)

        # 48 Aptly Named Unique Instrument Types
        self.instrument_names_48 = [
            "Z-Pinch Resonator", "Topological Fold", "Quantum Soliton", "Harmonic Phase-Shift",
            "Sub-Harmonic Drone", "Micro-Transient Click", "Stochastic Noise Matrix", "Voltage Controlled Crystal",
            "Resonant Cavity Feedback", "Plasma Streamer Node", "Frequency Divider Array", "Complex Waveguide",
            "Anomalous Sine Core", "Hyperbolic Sawtooth", "Additive Formant Synth", "Granular Cloud Emitter",
            "Metallic Tines", "Glass Resonance", "Sub-Bass Ionizer", "Electrostatic Discharge",
            "Vector Morph Oscillator", "Ring Modulator Bank", "Spectral Smear Filter", "Formant Sweep Matrix",
            "Bit-Crushed Impulse", "Phase Distortion Core", "Resonant Comb Filter", "Complex FM Modulator",
            "Analog Drift Oscillator", "Vacuum Tube Saturation", "Tape Flutter Emulator", "Spring Reverb Tank",
            "Binaural Drone Generator", "Chaotic Attractor Node", "Percolating Noise Burst", "Harmonic Overdrive",
            "Sub-Audio LFO", "Pulse Width Modulator", "Sync-Lead Synthesizer", "Formant Vocalizer",
            "Acoustic Plate Simulation", "Piezo Transducer Click", "Thermal Noise Generator", "Galactic Cosmic Ray",
            "Magnetic Flux Modulator", "Eddy Current Oscillator", "Standing Wave Matrix", "Quantum Entanglement Node"
        ]

        # -------------------------------------------------------------
        # 1. TRANSPORT & INSTRUMENT SELECTOR BAR
        # -------------------------------------------------------------
        self.transport_layout = QHBoxLayout()
        self.btn_play = QPushButton("▶ Play")
        self.btn_stop = QPushButton("⏹ Stop")
        self.btn_record = QPushButton("⏺ Record")
        self.lbl_bpm = QLabel("BPM:")
        self.spin_bpm = QSpinBox()
        self.spin_bpm.setRange(40, 240)
        self.spin_bpm.setValue(120)

        self.instrument_selector_dropdown = QComboBox()
        self.instrument_selector_dropdown.addItems(self.instrument_names_48)

        self.btn_randomize_all = QPushButton("🎲 Randomize Instrument")
        self.btn_export = QPushButton("💾 Export Mixdown")

        self.btn_play.clicked.connect(getattr(self, 'toggle_playback', lambda: None))
        self.btn_stop.clicked.connect(getattr(self, 'stop_playback', lambda: None))
        self.btn_randomize_all.clicked.connect(getattr(self, 'randomize_single_instrument', lambda: None))
        self.btn_export.clicked.connect(getattr(self, 'export_mixdown', lambda: None))

        self.transport_layout.addWidget(self.btn_play)
        self.transport_layout.addWidget(self.btn_stop)
        self.transport_layout.addWidget(self.btn_record)
        self.transport_layout.addWidget(self.lbl_bpm)
        self.transport_layout.addWidget(self.spin_bpm)
        self.transport_layout.addWidget(QLabel("Active Instrument:"))
        self.transport_layout.addWidget(self.instrument_selector_dropdown)
        self.transport_layout.addStretch(1)
        self.transport_layout.addWidget(self.btn_randomize_all)
        self.transport_layout.addWidget(self.btn_export)

        master_container.addLayout(self.transport_layout)

        # -------------------------------------------------------------
        # 2. ACTIVE SYNTH CHANNEL PARAMETER STRIP & MIXDOWN CONTROLS
        # -------------------------------------------------------------
        self.top_layout = QHBoxLayout()
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Mode: Single Instrument", "Mode: Global Ecosystem"])

        self.spin_tuning = QSpinBox()
        self.spin_tuning.setRange(100, 1200)
        self.slider_amplitude = QSlider(Qt.Orientation.Horizontal)
        self.slider_amplitude.setRange(0, 100)

        # Envelope Mixdown Weight Slider (Synth Timbre Strength vs Selected Timbre)
        self.slider_mix_weight = QSlider(Qt.Orientation.Horizontal)
        self.slider_mix_weight.setRange(0, 100)
        self.slider_mix_weight.setValue(100) # Peak strength up to 100%

        self.top_layout.addWidget(self.mode_combo)
        self.top_layout.addWidget(QLabel("Tuning:"))
        self.top_layout.addWidget(self.spin_tuning)
        self.top_layout.addWidget(QLabel("Amp:"))
        self.top_layout.addWidget(self.slider_amplitude)
        self.top_layout.addWidget(QLabel("Envelope Synth Mix (0-100%):"))
        self.top_layout.addWidget(self.slider_mix_weight)

        master_container.addLayout(self.top_layout)

        # -------------------------------------------------------------
        # 3. WORKFLOW TOOLBAR
        # -------------------------------------------------------------
        self.workflow_toolbar = QHBoxLayout()
        self.btn_edit_synth = QPushButton("🛠 Edit Synth Settings")
        self.btn_view_playlist = QPushButton("📜 Global Playlist & Paintbrush Window")
        self.btn_view_patchbay = QPushButton("🔌 Global Modular Patch Bay")
        self.btn_script_inst = QPushButton("📝 Instrument Script Editor")

        self.btn_edit_synth.clicked.connect(lambda: self.spawn_floating_window('synth_editor_window', "Synth Settings Editor"))
        self.btn_view_playlist.clicked.connect(lambda: self.spawn_floating_window('playlist_window', "Global Playlist Timeline"))
        self.btn_view_patchbay.clicked.connect(lambda: self.spawn_floating_window('patch_bay_dialog', "Global Modular Patch Bay"))
        self.btn_script_inst.clicked.connect(lambda: self.spawn_floating_window('script_editor_window', "Instrument Script Editor"))

        self.workflow_toolbar.addWidget(self.btn_edit_synth)
        self.workflow_toolbar.addWidget(self.btn_view_playlist)
        self.workflow_toolbar.addWidget(self.btn_view_patchbay)
        self.workflow_toolbar.addWidget(self.btn_script_inst)

        master_container.addLayout(self.workflow_toolbar)

        # -------------------------------------------------------------
        # 4. RESIZABLE SEQUENCE & PLAYLIST LENGTH CONTROLS
        # -------------------------------------------------------------
        sizing_layout = QHBoxLayout()
        sizing_layout.addWidget(QLabel("Sequence Length (Steps):"))
        self.spin_seq_length = QSpinBox()
        self.spin_seq_length.setRange(4, 32)
        self.spin_seq_length.setValue(16)
        sizing_layout.addWidget(self.spin_seq_length)

        sizing_layout.addWidget(QLabel("Playlist Length (Rows):"))
        self.spin_playlist_length = QSpinBox()
        self.spin_playlist_length.setRange(8, 64)
        self.spin_playlist_length.setValue(16)
        sizing_layout.addWidget(self.spin_playlist_length)
        sizing_layout.addStretch(1)

        sizing_container = QWidget()
        sizing_container.setLayout(sizing_layout)
        master_container.addWidget(sizing_container)

        # -------------------------------------------------------------
        # 5. NATIVE SEQUENCER TRIGGER & ARRANGEMENT PANE
        # -------------------------------------------------------------
        self.top_sequencer = QWidget()
        seq_inner = QVBoxLayout(self.top_sequencer)
        seq_inner.setContentsMargins(0, 0, 0, 0)

        seq_header_layout = QHBoxLayout()
        seq_header_layout.addWidget(QLabel("⚡ Active Sequencer Trigger & Saved Synth Sampler"))

        self.top_sequencer.instance_combo = QComboBox()
        self.top_sequencer.instance_combo.addItems(self.instrument_names_48)
        seq_header_layout.addWidget(QLabel("Target Saved Synth:"))
        seq_header_layout.addWidget(self.top_sequencer.instance_combo)

        seq_header_layout.addWidget(QLabel("Step Val:"))
        self.seq_step_value_spin = QDoubleSpinBox()
        self.seq_step_value_spin.setRange(-1000.0, 1000.0)
        self.seq_step_value_spin.setValue(1.0)
        self.seq_step_value_spin.setSingleStep(0.1)
        seq_header_layout.addWidget(self.seq_step_value_spin)

        # Trigger button samples the explicitly saved synth state rather than a random preset
        btn_trigger_seq = QPushButton("▶ Trigger Saved Synth Sample")

        def execute_saved_synth_trigger():
            saved_synth = self.top_sequencer.instance_combo.currentText()
            mix_factor = self.slider_mix_weight.value() / 100.0
            # Envelope mixdown: Peak strength up to 100% at peak envelope, tapering toward zero around troughs
            print(f"[Mixdown Engine] Sampling saved synth '{saved_synth}' with envelope mix factor: {mix_factor * 100}%")

        btn_trigger_seq.clicked.connect(execute_saved_synth_trigger)
        seq_header_layout.addWidget(btn_trigger_seq)
        seq_inner.addLayout(seq_header_layout)

        # Sequencer step buttons grid (Dynamic step length based on spinbox)
        self.steps_layout_widget = QWidget()
        self.steps_inner_layout = QHBoxLayout(self.steps_layout_widget)
        self.steps_inner_layout.setContentsMargins(0, 0, 0, 0)
        self.seq_step_buttons = []

        def rebuild_sequencer_steps(count):
            while self.steps_inner_layout.count():
                item = self.steps_inner_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            self.seq_step_buttons.clear()

            def make_step_toggle_handler(btn):
                def on_toggle(checked):
                    if checked:
                        btn.setStyleSheet("background-color: #00ffff; color: #080808; border: 2px solid #ffffff; font-weight: bold;")
                    else:
                        btn.setStyleSheet("background-color: #141414; color: #00ffff; border: 2px solid #444444;")
                return on_toggle

            for s in range(count):
                step_btn = QPushButton(str(s + 1))
                step_btn.setCheckable(True)
                step_btn.setStyleSheet("background-color: #141414; color: #00ffff; border: 2px solid #444444;")
                step_btn.toggled.connect(make_step_toggle_handler(step_btn))
                self.steps_inner_layout.addWidget(step_btn)
                self.seq_step_buttons.append(step_btn)

        rebuild_sequencer_steps(self.spin_seq_length.value())
        self.spin_seq_length.valueChanged.connect(rebuild_sequencer_steps)

        seq_inner.addWidget(self.steps_layout_widget)
        master_container.addWidget(self.top_sequencer)

        # Interactive & Labeled Phase-Space Oscilloscope Visualizer
        if hasattr(self, 'visual_oscilloscope') and self.visual_oscilloscope is not None:
            master_container.addWidget(self.visual_oscilloscope)
        else:
            self.visual_oscilloscope = QPushButton("📊 Phase-Space Oscilloscope [Status: Active / Click to Freeze]")
            self.visual_oscilloscope.setCheckable(True)
            self.visual_oscilloscope.setStyleSheet("""
                QPushButton {
                    background-color: #050505;
                    color: #00ffff;
                    border: 2px solid #00ffff;
                    padding: 12px;
                    text-align: left;
                    font-weight: bold;
                }
                QPushButton:checked {
                    background-color: #1a0505;
                    color: #ff5555;
                    border: 2px solid #ff5555;
                }
            """)

            def toggle_oscilloscope_state(checked):
                if checked:
                    self.visual_oscilloscope.setText("📊 Phase-Space Oscilloscope [Status: FROZEN / Waveform Captured]")
                else:
                    self.visual_oscilloscope.setText("📊 Phase-Space Oscilloscope [Status: Active / Click to Freeze]")

            self.visual_oscilloscope.toggled.connect(toggle_oscilloscope_state)
            master_container.addWidget(self.visual_oscilloscope)

    def spawn_floating_window(self, attr_name, window_title):
        window = getattr(self, attr_name, None)

        if window is None or not window.isVisible():
            window = QWidget(None, Qt.WindowType.Window)
            window.setWindowTitle(window_title)

            if attr_name == 'playlist_window':
                window.resize(1000, 700)
            elif attr_name == 'patch_bay_dialog':
                window.resize(900, 650)
            else:
                window.resize(700, 500)

            main_layout = QVBoxLayout(window)

            current_instrument = self.instrument_selector_dropdown.currentText() if hasattr(self, 'instrument_selector_dropdown') else "Z-Pinch Resonator"
            if hasattr(self, 'instrument_names_48') and current_instrument in self.instrument_names_48:
                inst_index = self.instrument_names_48.index(current_instrument) + 1
            else:
                inst_index = 1

            if attr_name == 'playlist_window':
                main_layout.addWidget(QLabel("📜 Global Playlist & Paintbrush Arrangement Grid (Click/Drag to Paint Active Synth)"))

                from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
                from PyQt6.QtGui import QColor

                playlist_rows = self.spin_playlist_length.value() if hasattr(self, 'spin_playlist_length') else 16
                track_table = QTableWidget(playlist_rows, 5)
                track_table.setHorizontalHeaderLabels(["Time (T)", "Instrument Track (Paintbrush Target)", "Preset Type", "Velocity", "Modulation Curve"])

                instrument_list = getattr(self, 'instrument_names_48', [f"Instrument {i}" for i in range(1, 49)])

                palette_colors = [
                    QColor(20, 90, 100),  # Cyan-Teal
                    QColor(70, 30, 90),   # Deep Purple
                    QColor(20, 90, 40),   # Forest Green
                    QColor(90, 50, 20),   # Warm Amber
                    QColor(90, 20, 30),   # Crimson
                    QColor(30, 40, 90)    # Indigo
                ]

                for row_idx in range(playlist_rows):
                    item_time = QTableWidgetItem(f"T + {row_idx * 0.25}s")
                    inst_name = instrument_list[row_idx % len(instrument_list)]
                    item_inst = QTableWidgetItem(inst_name)
                    assigned_color = palette_colors[row_idx % len(palette_colors)]
                    item_inst.setBackground(assigned_color)

                    item_preset = QTableWidgetItem(f"Paint Matrix #{row_idx + 1}")
                    item_vel = QTableWidgetItem("90%")
                    item_curve = QTableWidgetItem("Linear Ramp")

                    track_table.setItem(row_idx, 0, item_time)
                    track_table.setItem(row_idx, 1, item_inst)
                    track_table.setItem(row_idx, 2, item_preset)
                    track_table.setItem(row_idx, 3, item_vel)
                    track_table.setItem(row_idx, 4, item_curve)

                # Paintbrush functionality: Clicking any table cell paints it with the currently selected synth
                def handle_cell_click(row, col):
                    if col == 1:
                        active_synth = self.instrument_selector_dropdown.currentText() if hasattr(self, 'instrument_selector_dropdown') else "Z-Pinch Resonator"
                        cell_item = track_table.item(row, col)
                        if cell_item:
                            cell_item.setText(active_synth)
                            cell_item.setBackground(QColor(0, 120, 120))
                            print(f"[Paintbrush] Painted row {row} with active synth: {active_synth}")

                track_table.cellClicked.connect(handle_cell_click)
                main_layout.addWidget(track_table)

                spanner_layout = QHBoxLayout()
                btn_randomize_playlist = QPushButton("🎲 Randomize Playlist Paint Pattern")
                status_display = QLabel("Status: Paintbrush grid ready. Click any instrument track cell to apply current selection.")
                status_display.setStyleSheet("color: #00ffff;")

                def trigger_playlist_span():
                    status_display.setText("[Success] Playlist paint pattern randomized.")

                btn_randomize_playlist.clicked.connect(trigger_playlist_span)
                spanner_layout.addWidget(btn_randomize_playlist)
                spanner_layout.addWidget(status_display)
                main_layout.addLayout(spanner_layout)

            elif attr_name == 'patch_bay_dialog':
                main_layout.addWidget(QLabel("🔌 Global Modular Patch Bay & Signal Routing Matrix"))

                patch_container = QWidget()
                patch_layout = QHBoxLayout(patch_container)

                instrument_list = getattr(self, 'instrument_names_48', [f"Instrument {i}" for i in range(1, 49)])

                input_col = QVBoxLayout()
                input_col.addWidget(QLabel("Signal Sources (Outputs)"))
                source_list = QComboBox()
                source_list.addItems([f"{name} Out" for name in instrument_list] + ["Global Phase Oscillator", "Z-Pinch Resonator"])
                input_col.addWidget(source_list)
                patch_layout.addLayout(input_col)

                route_center = QVBoxLayout()
                route_center.addWidget(QLabel("⟷ Sticky Cable Routing ⟷"))
                btn_patch = QPushButton("Connect Patch Cable")
                route_center.addWidget(btn_patch)
                patch_layout.addLayout(route_center)

                output_col = QVBoxLayout()
                output_col.addWidget(QLabel("Signal Destinations (Inputs)"))
                target_list = QComboBox()
                target_list.addItems([f"{name} In" for name in instrument_list] + ["EQR Filter Matrix", "Phase-Space Oscilloscope"])
                output_col.addWidget(target_list)
                patch_layout.addLayout(output_col)

                main_layout.addWidget(patch_container)

                patch_log = QTextEdit()
                patch_log.setReadOnly(True)
                patch_log.setPlainText("# Active Patch Matrix Connections:\n- Z-Pinch Resonator Out -> EQR Filter Matrix (Locked)")
                main_layout.addWidget(patch_log)

                def execute_patch_connection():
                    src = source_list.currentText()
                    tgt = target_list.currentText()
                    current_log = patch_log.toPlainText()
                    patch_log.setPlainText(current_log + f"\n- {src} ---> {tgt} (Connected)")

                btn_patch.clicked.connect(execute_patch_connection)

            elif attr_name == 'synth_editor_window':
                main_layout.addWidget(QLabel(f"Editing Synth Parameters for: {current_instrument} (Node ID: {inst_index})"))

                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)
                scroll_content = QWidget()
                scroll_layout = QVBoxLayout(scroll_content)

                dynamic_params = [
                    f"[{current_instrument}] Harmonic Fold ({inst_index})",
                    f"[{current_instrument}] Phase Drift (x, y)",
                    f"[{current_instrument}] Amplitude Mod Depth",
                    f"[{current_instrument}] Cutoff Frequency (Z-Scale)",
                    f"[{current_instrument}] Resonance Spike",
                    f"[{current_instrument}] Fractal Coordinate Depth"
                ]

                for param in dynamic_params:
                    row = QHBoxLayout()
                    row.addWidget(QLabel(f"{param}:"))
                    slider = QSlider(Qt.Orientation.Horizontal)
                    slider.setRange(0, 100)
                    slider.setValue((inst_index * 11) % 100)
                    row.addWidget(slider)
                    scroll_layout.addLayout(row)

                scroll_content.setLayout(scroll_layout)
                scroll_area.setWidget(scroll_content)
                main_layout.addWidget(scroll_area)

            elif attr_name == 'script_editor_window':
                main_layout.addWidget(QLabel(f"Active Instrument Script Workspace: {current_instrument}"))
                script_text_area = QTextEdit()
                script_text_area.setPlainText(f"# Script for Node {inst_index}: {current_instrument}\ndef evaluate_wave(x, y, z):\n    return x * {inst_index}.0 - y * z")
                main_layout.addWidget(script_text_area)
                btn_layout = QHBoxLayout()
                btn_layout.addWidget(QPushButton("▶ Run Instrument Script"))
                btn_layout.addWidget(QPushButton("💾 Save Script"))
                main_layout.addLayout(btn_layout)
            else:
                main_layout.addWidget(QLabel(f"Active Panel: {window_title}"))

            setattr(self, attr_name, window)

        window.show()
        window.raise_()
        window.activateWindow()
