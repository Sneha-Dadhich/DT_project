let speech = new SpeechSynthesisUtterance();
let voices = [];
let voiceSelect = document.querySelector("select");
window.speechSynthesis.onvoiceschanged = () => {
    voices = window.speechSynthesis.getVoices();
    speech.voice = voices[0];
    voices.forEach((voice, i) => (voiceSelect.options[i] = new Option(voice.name, i)));
};

voiceSelect.addEventListener("change", () => {
    speech.voice = voices[voiceSelect.value];
});

let audioContext;
let recorder;
let audioChunks = [];

document.querySelector("button").addEventListener("click", () => {
    speech.text = document.querySelector("textarea").value;
    window.speechSynthesis.speak(speech);

    // Start recording
    startRecording();
});

function startRecording() {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        let input = audioContext.createMediaStreamSource(stream);
        recorder = new Recorder(input);
        recorder.record();
        speech.onend = stopRecording;
    });
}

function stopRecording() {
    recorder.stop();
    recorder.exportWAV(convertToMP3);
}

function convertToMP3(blob) {
    let reader = new FileReader();
    reader.onload = (event) => {
        let buffer = event.target.result;
        audioContext.decodeAudioData(buffer, (audioBuffer) => {
            let samples = audioBuffer.getChannelData(0);
            let mp3Blob = encodeMP3(samples);
            saveRecording(mp3Blob);
        });
    };
    reader.readAsArrayBuffer(blob);
}

function encodeMP3(samples) {
    let buffer = [];
    let mp3encoder = new lamejs.Mp3Encoder(1, 44100, 128); // 1 channel, 44.1kHz, 128kbps
    let sampleBlockSize = 1152;
    for (let i = 0; i < samples.length; i += sampleBlockSize) {
        let sampleChunk = samples.subarray(i, i + sampleBlockSize);
        let mp3buf = mp3encoder.encodeBuffer(sampleChunk);
        if (mp3buf.length > 0) {
            buffer.push(new Int8Array(mp3buf));
        }
    }
    let mp3buf = mp3encoder.flush();
    if (mp3buf.length > 0) {
        buffer.push(new Int8Array(mp3buf));
    }
    return new Blob(buffer, { type: 'audio/mp3' });
}

function saveRecording(blob) {
    let url = URL.createObjectURL(blob);
    let a = document.createElement("a");
    a.style.display = "none";
    a.href = url;
    a.download = "speech.mp3";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}
