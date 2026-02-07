import React, { useState, useRef, useEffect } from 'react';
import './Dashboard.css';
import camera from '../asset/camera.jpg';
import { generateCaption, getAuthSession } from '../api';

function Dashboard() {
  const [sentiment, setSentiment] = useState('');
  const [Length, setLength] = useState();
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [generatedCaption, setGeneratedCaption] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [isVideoReady, setIsVideoReady] = useState(false);

  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setSelectedImage(imageUrl);
  setSelectedFile(file);
  setGeneratedCaption('');
    }
  };

  const handleCaptureClick = () => {
    if (isCameraOpen) {
      const video = videoRef.current;
      if (!video) {
        alert('Error: Video element not found.');
        return;
      }

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);

      const imageUrl = canvas.toDataURL('image/png');
      setSelectedImage(imageUrl);

      // Convert capture to Blob/File so we can send it to backend
      canvas.toBlob((blob) => {
        if (blob) {
          const file = new File([blob], 'capture.png', { type: 'image/png' });
          setSelectedFile(file);
          setGeneratedCaption('');
        }
      }, 'image/png');

      stopCamera();
    } else {
      setIsCameraOpen(true); // This triggers video render
    }
  };

  const handleGenerateCaption = async () => {
    if (!selectedFile) {
      alert('Please upload or capture an image first.');
      return;
    }

    try {
      setIsGenerating(true);
      const { token, user } = getAuthSession();
      const res = await generateCaption({
        imageFile: selectedFile,
        sentiment,
        length: Length,
        userId: user?.id,
        token
      });
      setGeneratedCaption(res.caption || '');
    } catch (err) {
      alert(err.message || 'Failed to generate caption');
    } finally {
      setIsGenerating(false);
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    setIsCameraOpen(false);
    setIsVideoReady(false);
  };

  // Effect: when video is ready and camera should be on, attach stream
  useEffect(() => {
    const startCamera = async () => {
      try {
        if (!navigator.mediaDevices?.getUserMedia) {
          alert("Camera not supported on this browser.");
          return;
        }

        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          streamRef.current = stream;
        } else {
          console.warn("Video ref not ready.");
        }
      } catch (err) {
        console.error("Error accessing camera:", err);
        alert(`Camera error: ${err.message}`);
        setIsCameraOpen(false);
      }
    };

    if (isCameraOpen && isVideoReady) {
      startCamera();
    }
  }, [isCameraOpen, isVideoReady]);

  return (
    <div className="dashboard">
      <div className="dashboard-container">
        <h2 style={{ color: 'purple' }}>Image Capturing Dashboard</h2>

        <div style={{ position: 'absolute', top: '80px', right: '300px' }}>
          <h2 style={{ color: 'purple', marginBottom: '30px' }}>Caption Generation Options</h2>
          <label style={{ fontSize: '20px', color: 'purple',marginBottom: '30px' }}>Select Sentiment:</label>
          <select
            value={sentiment}
            onChange={(e) => setSentiment(e.target.value)}
            className='select'
            style={{
              width: '200px',
              height: '40px',
              padding: '10px',
              borderRadius: '10px',
              border: '1px solid #d1a5f0',
              fontSize: '15px',
              marginTop: '5px',
              display: 'block',
              marginBottom: '10px',
              color: '#d492d8',
              marginBottom: '20px'
            }}
          >
            <option value="" disabled>-- Select Mood --</option>
            <option value="Happy">😊 Happy</option>
            <option value="Sad">😞 Sad</option>
            <option value="Angry">😡 Angry</option>
            <option value="Excited">🤩 Excited</option>
            <option value="Calm">😌 Calm</option>
            <option value="Anxious">😰 Anxious</option>
            <option value="Confused">😕 Confused</option>
            <option value="Content">😌 Content</option>
            <option value="Motivated">💪 Motivated</option>
            <option value="Lonely">😔 Lonely</option>
            <option value="Tired">😴 Tired</option>
            <option value="Grateful">🙏 Grateful</option>
            <option value="Hopeful">🌟 Hopeful</option>
            <option value="Frustrated">😤 Frustrated</option>
            <option value="Bored">😑 Bored</option>
            <option value="Nostalgic">🥺 Nostalgic</option>
            <option value="Surprised">😲 Surprised</option>
            <option value="Scared">😱 Scared</option>
            <option value="Peaceful">🕊️ Peaceful</option>
            <option value="Inspired">✨ Inspired</option>
          </select>

          <label style={{ fontSize: '20px', color: 'purple' }}>Caption Length:</label>
          <input
            value={Length}
            onChange={(e) => setLength(e.target.value)}
            style={{
              width: '50px',
              height: '20px',
              padding: '10px',
              borderRadius: '10px',
              border: '1px solid #d1a5f0',
              fontSize: '15px',
              marginTop: '5px',
              display: 'block',
              marginBottom: '10px',
              color: '#d492d8'
            }}
          />
          <button className='but' onClick={handleGenerateCaption} disabled={isGenerating}>
            {isGenerating ? 'Generating...' : 'Generate Caption'}
          </button>
        </div>

        <div className="image-container">
          {isCameraOpen ? (
            <video
              ref={(el) => {
                videoRef.current = el;
                if (el) setIsVideoReady(true);
              }}
              autoPlay
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            />
          ) : (
            <img src={selectedImage || camera} alt="Placeholder" />
          )}
        </div>

        <div className="buttons">
          <input
            type="file"
            accept="image/*"
            style={{ display: 'none' }}
            ref={fileInputRef}
            onChange={handleFileChange}
          />
          <button className="button" onClick={handleUploadClick}>Upload Image</button>
          <button className="button" onClick={handleCaptureClick}>
            {isCameraOpen ? 'Take Photo' : 'Capture Image'}
          </button>
        </div>

        <h2 style={{ color: 'purple' }}>Generated Caption</h2>
        <div className="container" style={{ padding: '16px' }}>
          <div style={{ color: '#333', fontSize: '18px' }}>
            {generatedCaption || 'Your caption will appear here.'}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
