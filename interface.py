
class Progress():
    def __init__(self, progress_gui):
        self.progress_gui = progress_gui

    def update(self, completion_ratio):
        self.progress_gui.step_download(completion_ratio)
        
    def completed(self):
        self.progress_gui.download_complete()
