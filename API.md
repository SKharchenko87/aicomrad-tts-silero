# Silero TTS API Documentation

## Запуск сервиса

### Базовый запуск

```bash
docker run -p 5000:5000 silero-tts
```

При первом запуске модели будут загружены автоматически (~500MB для русской модели, ~100MB для английской).

### Запуск с примонтированными моделями

Чтобы избежать повторной загрузки моделей при каждом запуске контейнера, вы можете примонтировать директорию с предзагруженными моделями:

```bash
# Создайте директорию для моделей
mkdir models

# Скачайте модели вручную
curl -L https://models.silero.ai/models/tts/ru/v5_ru.pt -o models/model_ru.pt
curl -L https://models.silero.ai/models/tts/en/v3_en.pt -o models/model_en.pt

# Запустите контейнер с примонтированными моделями
docker run -p 5000:5000 -v $(pwd)/models:/models silero-tts
```

**Windows (PowerShell):**
```powershell
# Создайте директорию для моделей
mkdir models

# Скачайте модели
Invoke-WebRequest -Uri "https://models.silero.ai/models/tts/ru/v5_ru.pt" -OutFile "models/model_ru.pt"
Invoke-WebRequest -Uri "https://models.silero.ai/models/tts/en/v3_en.pt" -OutFile "models/model_en.pt"

# Запустите контейнер
docker run -p 5000:5000 -v ${PWD}/models:/models silero-tts
```

При запуске с примонтированными моделями сервис будет использовать их вместо загрузки.

## API Endpoints

### 1. Получить список доступных спикеров

**GET** `/api/speakers`

**Ответ:**
```json
{
  "speakers": {
    "ru": ["aidar", "baya", "kseniya", "xenia", "eugene", "random"],
    "en": ["en_0", "en_1", "en_2", "en_3", "en_4", "en_5", ...]
  }
}
```

### 2. Синтезировать речь

**POST** `/api/synthesize`

**Заголовки:**
```
Content-Type: application/json
```

**Тело запроса:**
```json
{
  "text": "Текст для синтеза",
  "language": "ru",
  "speaker": "xenia"
}
```

**Параметры:**
- `text` (обязательный) - текст для синтеза (максимум 1000 символов)
- `language` (обязательный) - язык модели: `"ru"` или `"en"`
- `speaker` (опциональный) - имя спикера, по умолчанию `"xenia"` для русского

**Ответ:**
- Аудио файл в формате WAV (48kHz)
- Content-Type: `audio/wav`

## Примеры использования

### Python

```python
import requests

# Русский язык
response = requests.post('http://localhost:5000/api/synthesize', json={
    'text': 'Привет, это тест синтеза речи',
    'language': 'ru',
    'speaker': 'xenia'
})

with open('output_ru.wav', 'wb') as f:
    f.write(response.content)

# Английский язык
response = requests.post('http://localhost:5000/api/synthesize', json={
    'text': 'Hello, this is a test of speech synthesis',
    'language': 'en',
    'speaker': 'en_0'
})

with open('output_en.wav', 'wb') as f:
    f.write(response.content)
```

### cURL

```bash
# Русский язык
curl -X POST http://localhost:5000/api/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text":"Привет мир","language":"ru","speaker":"xenia"}' \
  --output output.wav

# Английский язык
curl -X POST http://localhost:5000/api/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world","language":"en","speaker":"en_0"}' \
  --output output.wav
```

### JavaScript (Node.js)

```javascript
const fs = require('fs');

async function synthesize(text, language, speaker) {
  const response = await fetch('http://localhost:5000/api/synthesize', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text, language, speaker })
  });

  const buffer = await response.arrayBuffer();
  fs.writeFileSync('output.wav', Buffer.from(buffer));
}

// Использование
synthesize('Привет мир', 'ru', 'xenia');
synthesize('Hello world', 'en', 'en_0');
```

### JavaScript (Browser)

```javascript
async function synthesize(text, language, speaker) {
  const response = await fetch('http://localhost:5000/api/synthesize', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text, language, speaker })
  });

  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  
  // Воспроизвести
  const audio = new Audio(url);
  audio.play();
  
  // Или скачать
  const a = document.createElement('a');
  a.href = url;
  a.download = 'speech.wav';
  a.click();
}
```

## Важные замечания

1. **Числа**: Модель не произносит цифры. Преобразуйте числа в текст перед отправкой:
   - ❌ "У меня пять яблок" → "У меня яблок"
   - ✅ "У меня пять яблок" → "У меня пять яблок"

2. **Длинные тексты**: Тексты автоматически разбиваются на части по 1000 символов и склеиваются в один аудиофайл.

3. **Кэширование**: Одинаковые запросы кэшируются на сервере для ускорения повторных запросов.

4. **Первый запрос**: При первом запросе на английском языке модель будет загружена (может занять время).

## Коды ошибок

- `400` - Неверные параметры запроса (например, пустой текст)
- `500` - Ошибка синтеза (проверьте логи сервера)
