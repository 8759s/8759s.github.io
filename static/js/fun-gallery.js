(() => {
  const gallery = document.querySelector('.fun-grid');
  if (!gallery || gallery.dataset.speechReady === 'true') return;
  gallery.dataset.speechReady = 'true';

  const buttons = [...gallery.querySelectorAll('.fun-play')];
  const speech = window.speechSynthesis;
  let activeButton = null;
  let activeUtterance = null;

  const resetButton = (button) => {
    if (!button) return;
    button.setAttribute('aria-pressed', 'false');
    button.querySelector('span').textContent = 'Listen';
  };

  const stop = () => {
    if (speech) speech.cancel();
    resetButton(activeButton);
    activeButton = null;
    activeUtterance = null;
  };

  if (!speech || typeof window.SpeechSynthesisUtterance === 'undefined') {
    buttons.forEach((button) => {
      button.disabled = true;
      button.title = 'Speech playback is not available in this browser.';
    });
  } else {
    buttons.forEach((button) => {
      button.addEventListener('click', () => {
        if (activeButton === button) {
          stop();
          return;
        }

        stop();
        const card = button.closest('.fun-card');
        const name = card.querySelector('h2').textContent.trim();
        const description = card.querySelector('.fun-description').textContent.trim();
        const utterance = new SpeechSynthesisUtterance(`${name}. ${description}`);
        utterance.lang = 'en-US';
        utterance.rate = 0.92;
        utterance.pitch = 1.02;

        activeButton = button;
        activeUtterance = utterance;
        button.setAttribute('aria-pressed', 'true');
        button.querySelector('span').textContent = 'Stop';

        const finish = () => {
          // A canceled utterance can report its error after a new card starts.
          if (activeUtterance !== utterance) return;
          resetButton(button);
          activeButton = null;
          activeUtterance = null;
        };
        utterance.addEventListener('end', finish, { once: true });
        utterance.addEventListener('error', finish, { once: true });
        speech.speak(utterance);
      });
    });
  }

  gallery.querySelectorAll('.fun-card').forEach((card) => {
    const photos = [...card.querySelectorAll('.fun-photo')];
    const thumbnails = [...card.querySelectorAll('.fun-thumbnail')];
    thumbnails.forEach((thumbnail) => {
      thumbnail.addEventListener('click', () => {
        const selectedIndex = thumbnail.dataset.photoIndex;
        photos.forEach((photo) => {
          photo.hidden = photo.dataset.photoIndex !== selectedIndex;
        });
        thumbnails.forEach((candidate) => {
          candidate.setAttribute('aria-pressed', String(candidate === thumbnail));
        });
      });
    });
  });

  window.addEventListener('pagehide', stop);
})();
