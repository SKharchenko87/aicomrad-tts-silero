document.addEventListener('DOMContentLoaded', () => {
    const languageSelect = document.getElementById('language-select');
    const speakerSelect = document.getElementById('speaker-select');
    const textInput = document.getElementById('text-input');
    const charCurrent = document.getElementById('char-current');
    const synthesizeBtn = document.getElementById('synthesize-btn');
    const resultArea = document.getElementById('result-area');
    const audioPlayer = document.getElementById('audio-player');
    const downloadBtn = document.getElementById('download-btn');
    const loader = document.querySelector('.loader');
    const btnText = document.querySelector('.btn-text');

    let speakersData = {};

    // Function to update speaker options based on selected language
    function updateSpeakers(lang) {
        speakerSelect.innerHTML = '';
        const speakers = speakersData[lang] || [];

        if (speakers.length === 0) {
            const option = document.createElement('option');
            option.textContent = 'No speakers available';
            option.disabled = true;
            speakerSelect.appendChild(option);
            return;
        }

        speakers.forEach(speaker => {
            const option = document.createElement('option');
            option.value = speaker;
            option.textContent = speaker.charAt(0).toUpperCase() + speaker.slice(1);
            speakerSelect.appendChild(option);
        });

        // Select first speaker by default
        if (speakers.length > 0) {
            speakerSelect.value = speakers[0];
        }
    }

    // Fetch speakers
    fetch('/api/speakers')
        .then(response => response.json())
        .then(data => {
            speakersData = data.speakers;
            // Initialize with default language (ru)
            updateSpeakers(languageSelect.value);
        })
        .catch(err => {
            console.error('Failed to load speakers:', err);
            speakerSelect.innerHTML = '<option disabled>Error loading speakers</option>';
        });

    // Handle language change
    languageSelect.addEventListener('change', (e) => {
        updateSpeakers(e.target.value);
    });

    // Character count
    textInput.addEventListener('input', () => {
        charCurrent.textContent = textInput.value.length;
    });

    // Synthesize
    synthesizeBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        const speaker = speakerSelect.value;
        const language = languageSelect.value;

        if (!text) {
            alert('Please enter some text.');
            return;
        }

        // UI Loading State
        synthesizeBtn.disabled = true;
        btnText.textContent = 'Generating...';
        loader.classList.remove('hidden');
        resultArea.classList.add('hidden');

        try {
            const response = await fetch('/api/synthesize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    speaker: speaker,
                    language: language
                })
            });

            if (!response.ok) {
                throw new Error('Synthesis failed');
            }

            const blob = await response.blob();
            const url = URL.createObjectURL(blob);

            audioPlayer.src = url;
            downloadBtn.href = url;

            // Auto play
            audioPlayer.play().catch(e => console.log("Auto-play prevented:", e));

            resultArea.classList.remove('hidden');
        } catch (error) {
            console.error(error);
            alert('Error generating speech. Please try again.');
        } finally {
            synthesizeBtn.disabled = false;
            btnText.textContent = 'Generate Speech';
            loader.classList.add('hidden');
        }
    });
});
