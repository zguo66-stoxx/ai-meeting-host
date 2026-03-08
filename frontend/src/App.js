import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = 'http://localhost:8000';

function App() {
  const [meetingActive, setMeetingActive] = useState(false);
  const [agenda, setAgenda] = useState(null);
  const [currentTopic, setCurrentTopic] = useState(null);
  const [transcription, setTranscription] = useState([]);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [botMessage, setBotMessage] = useState('');
  
  const mediaRecorder = useRef(null);
  const audioChunks = useRef([]);
  const audioContext = useRef(null);
  const audioElement = useRef(null);

  // Load meeting agenda on mount
  useEffect(() => {
    loadAgenda();
  }, []);

  const loadAgenda = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/agenda`);
      setAgenda(response.data);
    } catch (error) {
      console.error('Failed to load agenda:', error);
    }
  };

  const startMeeting = async () => {
    try {
      await axios.post(`${API_BASE}/api/meeting/start`);
      setMeetingActive(true);
      startListening();
      
      // Automatically speak the opening
      setTimeout(() => speakOpening(), 1000);
    } catch (error) {
      console.error('Failed to start meeting:', error);
    }
  };

  const stopMeeting = async () => {
    try {
      await axios.post(`${API_BASE}/api/meeting/stop`);
      setMeetingActive(false);
      stopListening();
    } catch (error) {
      console.error('Failed to stop meeting:', error);
    }
  };

  const startListening = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      mediaRecorder.current = new MediaRecorder(stream);
      
      mediaRecorder.current.ondataavailable = (event) => {
        audioChunks.current.push(event.data);
      };
      
      mediaRecorder.current.onstop = async () => {
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/wav' });
        audioChunks.current = [];
        
        // Send to backend for transcription
        const formData = new FormData();
        formData.append('audio', audioBlob, 'audio.wav');
        
        try {
          const response = await axios.post(`${API_BASE}/api/transcribe`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
          
          if (response.data.transcription) {
            setTranscription(prev => [...prev, {
              text: response.data.transcription,
              timestamp: new Date().toLocaleTimeString()
            }]);
          }
        } catch (error) {
          console.error('Transcription error:', error);
        }
        
        // Continue recording if still listening
        if (isListening && meetingActive) {
          mediaRecorder.current.start();
          setTimeout(() => mediaRecorder.current.stop(), 5000); // 5 second chunks
        }
      };
      
      mediaRecorder.current.start();
      setTimeout(() => mediaRecorder.current.stop(), 5000);
      setIsListening(true);
      
    } catch (error) {
      console.error('Microphone access error:', error);
      alert('Please allow microphone access');
    }
  };

  const stopListening = () => {
    if (mediaRecorder.current && mediaRecorder.current.state !== 'inactive') {
      mediaRecorder.current.stop();
      mediaRecorder.current.stream.getTracks().forEach(track => track.stop());
    }
    setIsListening(false);
  };

  const playAudio = (base64Audio) => {
    try {
      const audioData = atob(base64Audio);
      const arrayBuffer = new ArrayBuffer(audioData.length);
      const view = new Uint8Array(arrayBuffer);
      
      for (let i = 0; i < audioData.length; i++) {
        view[i] = audioData.charCodeAt(i);
      }
      
      const blob = new Blob([arrayBuffer], { type: 'audio/mpeg' });
      const url = URL.createObjectURL(blob);
      
      if (audioElement.current) {
        audioElement.current.pause();
      }
      
      audioElement.current = new Audio(url);
      audioElement.current.play();
      
      audioElement.current.onended = () => {
        setIsSpeaking(false);
        URL.revokeObjectURL(url);
      };
      
    } catch (error) {
      console.error('Audio playback error:', error);
      setIsSpeaking(false);
    }
  };

  const speakOpening = async () => {
    setIsSpeaking(true);
    try {
      const response = await axios.post(`${API_BASE}/api/speak/opening`);
      setBotMessage(response.data.text);
      playAudio(response.data.audio);
      
      // Update current topic
      updateMeetingStatus();
    } catch (error) {
      console.error('Speak error:', error);
      setIsSpeaking(false);
    }
  };

  const speakNextTopic = async () => {
    setIsSpeaking(true);
    try {
      const response = await axios.post(`${API_BASE}/api/speak/next-topic`);
      setBotMessage(response.data.text);
      playAudio(response.data.audio);
      
      // Update current topic
      updateMeetingStatus();
    } catch (error) {
      console.error('Speak error:', error);
      setIsSpeaking(false);
    }
  };

  const speakTransition = async () => {
    setIsSpeaking(true);
    try {
      const response = await axios.post(`${API_BASE}/api/speak/transition`);
      setBotMessage(response.data.text);
      playAudio(response.data.audio);
      
      // Update current topic
      updateMeetingStatus();
    } catch (error) {
      console.error('Speak error:', error);
      setIsSpeaking(false);
    }
  };

  const speakSmart = async () => {
    setIsSpeaking(true);
    try {
      const response = await axios.post(`${API_BASE}/api/speak/smart`, {
        message: "Provide a helpful comment based on the discussion"
      });
      setBotMessage(response.data.text);
      playAudio(response.data.audio);
    } catch (error) {
      console.error('Speak error:', error);
      setIsSpeaking(false);
    }
  };

  const updateMeetingStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/meeting/status`);
      setCurrentTopic(response.data.current_topic);
    } catch (error) {
      console.error('Status update error:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎙️ AI Meeting Host</h1>
        {agenda && <h2>{agenda.title}</h2>}
      </header>

      <main className="App-main">
        {!meetingActive ? (
          <div className="start-screen">
            <button className="btn-start" onClick={startMeeting}>
              Start Meeting
            </button>
            
            {agenda && (
              <div className="agenda-preview">
                <h3>Agenda</h3>
                <ul>
                  {agenda.topics.map((topic, index) => (
                    <li key={index}>
                      <strong>{topic.title}</strong> - {topic.lead} ({topic.duration_minutes} min)
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ) : (
          <div className="meeting-screen">
            <div className="status-bar">
              <div className="status-item">
                <span className={`indicator ${isListening ? 'active' : ''}`}></span>
                {isListening ? 'Listening...' : 'Not Listening'}
              </div>
              <div className="status-item">
                <span className={`indicator ${isSpeaking ? 'speaking' : ''}`}></span>
                {isSpeaking ? 'Speaking...' : 'Silent'}
              </div>
            </div>

            {currentTopic && (
              <div className="current-topic">
                <h3>Current Topic</h3>
                <h2>{currentTopic.title}</h2>
                <p>Led by: {currentTopic.lead} • {currentTopic.duration_minutes} minutes</p>
              </div>
            )}

            {botMessage && (
              <div className="bot-message">
                <strong>Bot says:</strong>
                <p>{botMessage}</p>
              </div>
            )}

            <div className="controls">
              <button 
                className="btn-speak-main"
                onClick={speakNextTopic}
                disabled={isSpeaking}
              >
                🎤 SPEAK<br/><small>(Next Topic)</small>
              </button>
              
              <div className="control-row">
                <button 
                  className="btn-control"
                  onClick={speakTransition}
                  disabled={isSpeaking}
                >
                  ➡️ Transition
                </button>
                
                <button 
                  className="btn-control"
                  onClick={speakSmart}
                  disabled={isSpeaking}
                >
                  🤖 Smart Response
                </button>
                
                <button 
                  className="btn-control btn-stop"
                  onClick={stopMeeting}
                >
                  ⏹️ Stop Meeting
                </button>
              </div>
            </div>

            <div className="transcription">
              <h3>Live Transcription</h3>
              <div className="transcription-list">
                {transcription.length === 0 ? (
                  <p className="empty-state">Waiting for audio...</p>
                ) : (
                  transcription.map((item, index) => (
                    <div key={index} className="transcription-item">
                      <span className="timestamp">{item.timestamp}</span>
                      <span className="text">{item.text}</span>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
