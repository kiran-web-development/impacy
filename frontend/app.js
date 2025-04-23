document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById('imageInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const imagePreview = document.getElementById('imagePreview');
    const resultsDiv = document.getElementById('results');

    // Preview image when selected
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                imagePreview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle image analysis
    analyzeBtn.addEventListener('click', async () => {
        const file = imageInput.files[0];
        if (!file) {
            alert('Please select an image first');
            return;
        }

        const formData = new FormData();
        formData.append('image', file);

        try {
            resultsDiv.innerHTML = 'Analyzing image...';
            const response = await fetch('http://localhost:5000/api/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Analysis failed');
            }

            const result = await response.json();
            resultsDiv.innerHTML = `
                <h3>Analysis Results:</h3>
                <pre>${JSON.stringify(result, null, 2)}</pre>
            `;
        } catch (error) {
            resultsDiv.innerHTML = `Error: ${error.message}`;
        }
    });
});