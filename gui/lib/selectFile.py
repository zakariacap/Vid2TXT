from tkinter import filedialog as fd

def select_file():
    filetypes = (
        ('Video and Audio Files', '*.m4a *.mkv *.mp4 *.avi *.mov *.wav *.mp3'),
        ('All Files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes
    )

    if filename:  # If a file is selected, return its path
        return filename
    else:  # Raise an error if no file is selected
        raise FileNotFoundError("No file was selected.")