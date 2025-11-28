import urllib.request
import json
import os
import sys

API_URL = "http://localhost:5000/api/synthesize"

def test_synthesis(text, language, speaker, filename):
    print(f"Testing {language} synthesis with speaker {speaker}...")
    payload = {
        "text": text,
        "language": language,
        "speaker": speaker
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(API_URL, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                content = response.read()
                with open(filename, 'wb') as f:
                    f.write(content)
                print(f"SUCCESS: Saved to {filename}")
            else:
                print(f"FAILED: {response.status}")
    except urllib.error.HTTPError as e:
        print(f"ERROR: {e.code} - {e.reason}")
        print(e.read().decode())
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    # Test English
    test_synthesis("Hello, this is a test of English synthesis.", "en", "en_0", "test_en.wav")
    
    # Test Russian
    test_synthesis("Привет, это проверка русского синтеза.", "ru", "xenia", "test_ru.wav")
