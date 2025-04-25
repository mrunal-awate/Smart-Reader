// Wait for the DOM to be fully loaded before binding the form submit
document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('upload-form');
  const extractedTextElement = document.getElementById('extracted-text');
  const audioPlayer = document.getElementById('audio-player');
  const audioSource = document.getElementById('audio-source');

  form.addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the default form submission behavior

    // Get form data
    const formData = new FormData(form);

    // Create an AJAX request to send the form data to the backend
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);

    xhr.onload = function() {
      if (xhr.status === 200) {
        // Parse the response from the server
        const response = JSON.parse(xhr.responseText);

        // Display extracted text on the page
        extractedTextElement.textContent = response.text;

        // Set the audio source and make the player ready
        audioSource.src = response.audio_url;
        audioPlayer.load();
        audioPlayer.play();
      } else {
        extractedTextElement.textContent = 'An error occurred while processing the image.';
      }
    };

    // Handle network errors
    xhr.onerror = function() {
      extractedTextElement.textContent = 'Network error. Please try again later.';
    };

    // Send the form data as multipart/form-data
    xhr.send(formData);
  });
});
