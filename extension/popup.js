document.addEventListener('DOMContentLoaded', function() {
  const submitButton = document.getElementById('submit');
  const statusDiv = document.getElementById('status');

  // TODO: Replace with your actual backend URL and API key
  const BACKEND_URL = 'https://your-railway-app.up.railway.app'; // Change this
  const API_KEY = 'your-api-key-here'; // Change this

  submitButton.addEventListener('click', async function() {
    const urlInput = document.getElementById('url');
    const labelInput = document.getElementById('label');

    const url = urlInput.value.trim();
    const label = labelInput.value.trim() || 'Unnamed competitor';

    if (!url) {
      statusDiv.textContent = 'Please enter a URL';
      statusDiv.style.color = 'red';
      return;
    }

    // Disable button and show loading
    submitButton.disabled = true;
    statusDiv.textContent = 'Submitting...';
    statusDiv.style.color = 'blue';

    try {
      const response = await fetch(`${BACKEND_URL}/extension/configure`, {
        method: 'POST',
        headers {
          'Content-Type': 'application/json',
          'X-API-Key': API_KEY
        },
        body: JSON.stringify({
          url: url,
          competitor_label: label,
          section_selector: 'body', // Default to whole page; user can change later
          check_interval_hours: 6
        })
      });

      if response.ok {
        const result = await response.json();
        statusDiv.textContent = `Success! Monitoring started for ${label}`;
        statusDiv.style.color = 'green';
        // Clear the form
        urlInput.value = '';
        labelInput.value = '';
      } else {
        const error = await response.json();
        statusDiv.textContent = `Error: ${error.detail || 'Unknown error'}`;
        statusDiv.style.color = 'red';
      }
    } catch (error) {
      statusDiv.textContent = `Network error: ${error.message}`;
      statusDiv.style.color = 'red';
    } finally {
      submitButton.disabled = false;
    }
  });
});