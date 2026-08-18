import random

# ==========================================
# 1. INSTRUMENT PRESETS & CONFIGURATION
# ==========================================
# Replace these strings with your actual instrument IDs, patch names, or synth engine references
USER_INSTRUMENT_POOL = [
    "NITROUS_O_Lead_Synth",
    "Sub_Bass_Custom",
    "Arp_Pluck_01",
    "Atmospheric_Pad"
]

def generate_random_song_parameters(
    instruments_pool=None,
    max_steps=32,
    max_notes_per_step=3,
    duration_bounds=(0.125, 2.0)
):
    """
    Generates structured, randomized song parameters within a sane operational limit.
    Utilizes bounded spatial coordinates (x, y, z logic mapping) applied to musical parameters.
    """
    if instruments_pool is None:
        instruments_pool = USER_INSTRUMENT_POOL

    # Sane limits for structural integrity (1 to 4 instruments active)
    selected_instruments = random.sample(
        instruments_pool,
        k=random.randint(1, min(4, len(instruments_pool)))
    )

    song_structure = {}

    for instrument in selected_instruments:
        # Determine active steps using spatial bounds (x, y, z mapping concept)
        step_count = random.randint(8, max_steps)
        sequence = []

        for step in range(step_count):
            # Mapping notes within a controlled melodic range (MIDI notes 36 to 84)
            active_notes_count = random.randint(1, max_notes_per_step)
            notes = [random.randint(36, 84) for _ in range(active_notes_count)]

            # Duration bounded within sensible rhythmic values (sixteenth note to half note)
            duration = round(random.choice([0.125, 0.25, 0.5, 1.0, 1.5, 2.0]), 3)

            sequence.append({
                "step": step + 1,
                "notes": notes,
                "duration": duration,
                "velocity": random.randint(60, 127)
            })

        song_structure[instrument] = {
            "total_steps": step_count,
            "sequence": sequence
        }

    return song_structure


# ==========================================
# 2. AUDIO ENGINE & SYNTH HANDLER MAPPING
# ==========================================
def trigger_synth_notes(instrument_name, notes, duration, velocity):
    """
    Placeholder handler function to map generated sequence data
    directly into your software synth engine or MIDI stream.
    """
    # TODO: Replace print statements with calls to your actual synthesis/audio pipeline
    print(f"-> [Trigger] Synth: {instrument_name} | Notes: {notes} | Dur: {duration}s | Vel: {velocity}")


def play_generated_sequence(song_data):
    """
    Iterates through the generated song structure and dispatches events.
    """
    for instrument, data in song_data.items():
        print(f"\nInstrument: {instrument} | Total Steps: {data['total_steps']}")
        for event in data["sequence"]:
            trigger_synth_notes(
                instrument_name=instrument,
                notes=event["notes"],
                duration=event["duration"],
                velocity=event["velocity"]
            )


# ==========================================
# 3. EXECUTION / BUTTON TRIGGER HOOK
# ==========================================
def on_random_song_button_clicked():
    """
    Main hook function tied to your UI 'Random Song' button.
    """
    print("=== Random Song Button Triggered ===")

    # Generate the structured parameters using your custom presets
    new_song_data = generate_random_song_parameters(instruments_pool=USER_INSTRUMENT_POOL)

    # Pass the output directly to the playback/mapping engine
    play_generated_sequence(new_song_data)

    return new_song_data


if __name__ == "__main__":
    # Simulate a button press execution
    on_random_song_button_clicked()
