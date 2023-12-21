import pyaudio as pa
from vosk import Model, KaldiRecognizer, SetLogLevel
import json
import subprocess

class SpeechToTextEngine:
    def __init__(self, model_path, model_name, lang, save_textfile_dir):
        self.model_path = model_path
        self.model_name = model_name
        self.lang = lang
        self.save_textfile_dir = save_textfile_dir

    def configure(self):
        model = Model(model_path=self.model_path, model_name=self.model_name, lang=self.lang)

        SetLogLevel(0)
        p = pa.PyAudio()
        mic_index = 3
        stream = p.open(format=pa.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000, input_device_index=mic_index)
        stream.start_stream()

        rec = KaldiRecognizer(model, 16000)
        rec.SetWords(True)
        rec.SetPartialWords(True)

        recognized_text = ""
        return stream, rec, recognized_text

    def listen_for_wake_word(self, stream):
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            rec.AcceptWaveform(data)
            partial_result = rec.PartialResult()

            if partial_result:
                partial_text = json.loads(partial_result).get("partial", "")
                print("Partial Result:", partial_text)

                if "wake up" in partial_text.lower():
                    print("Wake up detected! Listening for command...")
                    return True

    def listen_for_command(self, stream):
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            rec.AcceptWaveform(data)
            partial_result = rec.PartialResult()

            if partial_result:
                partial_text = json.loads(partial_result).get("partial", "")
                print("Partial Result:", partial_text)

                # Check for specific commands or phrases
                if "stop listening" in partial_text.lower():
                    print("Stop listening command detected. Stopping...")
                    return False

                # Handle other commands based on your requirements
                if "open browser" in partial_text.lower():
                    print("Opening the browser...")
                    subprocess.run(["start", "https://www.google.com"])

    def real_time_listen(self):
        stream, rec, recognized_text = self.configure()
        try:
            while True:
                # Listen for the wake-up word
                if self.listen_for_wake_word(stream):
                    # Listen for a command
                    if not self.listen_for_command(stream):
                        break  # Stop listening if requested

        except KeyboardInterrupt:
            print("KeyboardInterrupt: Stopping real-time listening")

        # Save the recognized text to a file
        with open(self.save_textfile_dir, "w") as output_file:
            output_file.write(recognized_text)

        stream.stop_stream()
        stream.close()
        p.terminate()

        print(f"Recognized text saved to: {self.save_textfile_dir}")

def main():
    model_path = "D:\\vizuosense_mine\\STT\\Resources\\vosk-model-small-en-us-0.15"
    model_name = "vosk-model-small-en-us-0.15"
    language = "small-en-us"
    save_textfile_dir = "D:\\vizuosense_mine\\STT\\Resources\\test.txt"
    stt_engine = SpeechToTextEngine(model_path, model_name, language, save_textfile_dir)
    stt_engine.real_time_listen()

if __name__ == "__main__":
    main()
