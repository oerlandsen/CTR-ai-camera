class TelegramManager:

    def __init__(self) -> None:
        self.alarm_frames = 0
        self.alarm = False

    def analyze(self, ai_result):
        if ai_result.alarm:
            self.alarm = True
            self.alarm_frames += 1
        
        if self.alarm and self.alarm_frames == 100:
            self.send_message()
            self.alarm_frames = 0
       
        if not ai_result.alarm:
            self.alarm = False
            self.alarm_frames = 0
