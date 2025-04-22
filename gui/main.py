import customtkinter as ctk
from lib.selectFile import select_file
from lib.audio_processing import process_audio_file
import os
import threading
from datetime import datetime, timedelta
from pydub.silence import split_on_silence
from pydub import AudioSegment
from CTkTable import *

data = {
    "file_url": '',
}

def process():
    def run_processing():
        # Disable buttons and reset UI
        process_button.configure(state='disabled', text="Processing...")
        open_button.configure(state='disabled')
        progress_bar.set(0)
        output_label.configure(text="Processing started...")

        try:
            # Load audio file
            audio = AudioSegment.from_file(data["file_url"])
            chunks = split_on_silence(audio, min_silence_len=500, silence_thresh=-40)
            
            # Clear previous output
            for widget in output_frame.winfo_children():
                widget.destroy()

            output_data = []
            start_time = datetime.now()
            total_chunks = len(chunks)

            # Process each chunk
            for index, chunk in enumerate(chunks, 1):
                # Update progress bar
                progress = (index / total_chunks) * 100
                progress_bar.set(progress / 100)
                output_label.configure(text=f"Processing chunk {index}/{total_chunks}")

                # Export chunk and process
                chunk.export("temp.wav", format="wav")
                text = process_audio_file("temp.wav", 'fr-FR')
                
                # Calculate timestamp
                duration = timedelta(seconds=chunk.duration_seconds)
                end_time = start_time + duration
                timestamp = end_time.strftime("%H:%M:%S")
                
                # Store results
                output_data.append((timestamp, text))
                start_time = end_time

            # Create results table
            table = CTkTable(master=output_frame, row=len(output_data), column=2, values=output_data)
            table.pack(expand=True, fill="both", padx=20, pady=20)

            # Clean up
            os.remove('temp.wav')
            
            # Update UI on completion
            progress_bar.set(1)
            output_label.configure(text="Processing completed!")

        except Exception as e:
            # Handle any errors
            output_label.configure(text=f"Error: {str(e)}")
            progress_bar.set(0)

        finally:
            # Re-enable buttons
            process_button.configure(text="Process", state='enabled')
            open_button.configure(state='enabled')

    # Run processing in a separate thread
    processing_thread = threading.Thread(target=run_processing)
    processing_thread.start()

def open_file():
    # Attempt to select a file
    file_path = select_file()
    # Update the data dictionary with the selected file path
    data.update({'file_url': file_path})
    # Update the button text to show the selected file path
    file_name = os.path.basename(file_path)
    open_button.configure(text=file_name)
    
    # Reset progress and output
    progress_bar.set(0)
    output_label.configure(text="File selected. Ready to process.")
    
    # Enable process button
    process_button.configure(state='normal')

# Set the appearance and theme
ctk.set_appearance_mode("dark")

# Create the main application window
app = ctk.CTk()
app.geometry("700x600")
app.title("Audio to Text Converter")

# Create a frame to hold the widgets
frame = ctk.CTkFrame(app)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Add a title label to the frame
title_label = ctk.CTkLabel(frame, text="Audio to Text Converter", font=("tahoma", 20))
title_label.pack(pady=10)

# Create the open file button
open_button = ctk.CTkButton(
    frame,
    text='Select File',
    command=open_file,
    font=("tahoma", 20)
)
open_button.pack(expand=True, pady=10)

# Create the process button
process_button = ctk.CTkButton(
    frame,
    text='Process',
    command=process,
    state="disabled",
    font=("tahoma", 20)
)
process_button.pack(expand=True, pady=10)

# Create a progress bar
progress_bar = ctk.CTkProgressBar(frame, width=400)
progress_bar.pack(pady=10)
progress_bar.set(0)  # Initial state

# Create a label to show processing status
output_label = ctk.CTkLabel(frame, text="", font=("tahoma", 16))
output_label.pack(pady=10)

# Create a scrollable frame for the output
output_frame = ctk.CTkScrollableFrame(frame)
output_frame.pack(pady=20, fill="both", expand=True)

# Run the application
app.mainloop()