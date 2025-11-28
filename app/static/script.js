document.addEventListener('DOMContentLoaded', () => {
    const speakerSelect = document.getElementById('speaker-select');
    const textInput = document.getElementById('text-input');
    const charCurrent = document.getElementById('char-current');
    const synthesizeBtn = document.getElementById('synthesize-btn');
    const resultArea = document.getElementById('result-area');
    const audioPlayer = document.getElementById('audio-player');
    const downloadBtn = document.getElementById('download-btn');
    const loader = document.querySelector('.loader');
    const btnText = document.querySelector('.btn-text');

    // Fetch speakers
    fetch('/api/speakers')
        .then(response => response.json())
        .then(data => {
            speakerSelect.innerHTML = '';
            data.speakers.forEach(speaker => {
                const option = document.createElement('option');
                option.value = speaker;
                option.textContent = speaker.charAt(0).toUpperCase() + speaker.slice(1);
                if (speaker === 'xenia') option.selected = true;
                speakerSelect.appendChild(option);
            });
        })
        .catch(err => {
            console.error('Failed to load speakers:', err);
            speakerSelect.innerHTML = '<option disabled>Error loading speakers</option>';
        });

    // Character count
    textInput.addEventListener('input', () => {
        charCurrent.textContent = textInput.value.length;
    });

    // Synthesize
    synthesizeBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        const speaker = speakerSelect.value;

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
                    speaker: speaker
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
