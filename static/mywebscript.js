let RunSentimentAnalysis = () => {
    const textToAnalyze = document.getElementById("textToAnalyze").value;

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && (this.status === 200 || this.status === 400)) {
            try {
                const response = JSON.parse(xhttp.responseText);
                displayEmotionTable(response);
            } catch (e) {
                document.getElementById("system_response").innerHTML = `<div class="alert alert-danger">Invalid response. Try again.</div>`;
            }
        }
    };
    xhttp.open("GET", `emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`, true);
    xhttp.send();
};

function displayEmotionTable(data) {
    const emojiMap = {
        anger: "😠",
        disgust: "🤢",
        fear: "😱",
        joy: "😊",
        sadness: "😢",
        surprise: "😲",
        love: "❤️"
    };

    let rows = '';
    for (let emotion in data) {
        if (emotion !== 'dominant_emotion') {
            rows += `
                <tr>
                    <td>${emojiMap[emotion] || ''} ${emotion}</td>
                    <td>${(data[emotion] * 100).toFixed(1)}%</td>
                </tr>
            `;
        }
    }

    let dominant = data['dominant_emotion'];
    let dominantEmoji = emojiMap[dominant] || '';
    
    document.getElementById("system_response").innerHTML = `
        <div class="text-center mb-4">
            <h3 class="text-primary">Dominant Emotion</h3>
            <h1 class="display-4 font-weight-bold">${dominantEmoji} ${dominant.toUpperCase()}</h1>
        </div>
        <table class="table table-striped table-bordered">
            <thead class="thead-dark">
                <tr>
                    <th>Emotion</th>
                    <th>Confidence</th>
                </tr>
            </thead>
            <tbody>
                ${rows}
            </tbody>
        </table>
    `;
}
