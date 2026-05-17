# Real-Time Face Recognition & Emotion Analysis System

## Overview

This project is a production-style realtime AI system that performs:

- Face detection
- Face recognition
- Emotion analysis
- Live biometric enrollment
- Realtime websocket inference streaming
- Multi-face tracking
- Cloud deployment

The system was designed as an end-to-end ML engineering project focused not only on model inference, but also on realtime systems architecture, backend engineering, frontend orchestration, deployment, and production tradeoff analysis.

---

# Features

## Realtime Face Detection

- MediaPipe-based face detection
- Optimized for realtime performance
- Bounding-box tracking overlay
- Multiple face support

---

## Face Recognition

- DeepFace FaceNet embeddings
- Multi-sample biometric enrollment
- Cosine similarity matching
- Persistent per-track identity state

---

## Emotion Analysis

- DeepFace emotion classification
- Emotion confidence scoring
- Temporal emotion smoothing
- Per-track emotion state management

---

## Live Enrollment System

The original image-upload enrollment flow was replaced with a guided biometric enrollment experience.

Users:

1. Enter a name
2. Start enrollment
3. Perform guided head movements and expressions
4. Automatically capture multiple samples
5. Generate robust face embeddings

This significantly improved recognition robustness while also creating a more production-style user experience.

---

## Realtime WebSocket Streaming

The frontend streams webcam frames to the backend using WebSockets.

Benefits:

- Lower latency
- Reduced HTTP overhead
- Smoother realtime experience
- Better UI responsiveness

---

## Face Tracking

Implemented lightweight centroid-based tracking.

Features:

- Persistent track IDs
- Per-face recognition persistence
- Per-face emotion persistence
- Reduced inference recomputation
- Stable UI overlays

Example overlay:

```text
#0 | Omkar
happy | 91%
```

---

## Cloud Deployment

Frontend and backend were deployed as independent services.

### Frontend

- React + Vite
- Hosted on Vercel

### Backend

- FastAPI
- Dockerized ML inference pipeline
- Hosted on AWS EC2

### Database

- PostgreSQL
- Containerized with Docker Compose

### Secure Networking

Cloudflare Tunnel was used to:

- Enable HTTPS/WSS communication
- Avoid manual SSL setup
- Avoid Nginx configuration
- Enable secure websocket connectivity

---

# Tech Stack

## Frontend

- React
- Vite
- Tailwind CSS
- WebSocket API
- HTML Canvas overlays

---

## Backend

- FastAPI
- WebSockets
- OpenCV
- MediaPipe
- DeepFace
- TensorFlow
- PostgreSQL

---

## Infrastructure

- Docker
- Docker Compose
- AWS EC2
- Cloudflare Tunnel
- Vercel

---

# System Architecture

```text
Frontend (Vercel)
        ↓ HTTPS/WSS
Cloudflare Tunnel
        ↓
AWS EC2 Instance
 ├── FastAPI Backend
 ├── ML Inference Pipeline
 ├── WebSocket Streaming
 ├── PostgreSQL
 └── Docker Compose
```

---

# ML Pipeline

```text
Webcam Frame
     ↓
WebSocket Stream
     ↓
Face Detection
     ↓
Face Tracking
     ↓
Face Recognition
     ↓
Emotion Analysis
     ↓
Frontend Overlay Rendering
```

---

# Performance Optimizations

Several optimizations were introduced during development.

## Detection Optimization

### MTCNN → MediaPipe Migration

MTCNN was initially used for face detection but later replaced with MediaPipe due to significantly lower detection latency.

### Benchmark Comparison

| Detector  | Detection Time |
| --------- | -------------- |
| MTCNN     | ~70ms          |
| MediaPipe | ~6ms           |

This substantially improved realtime responsiveness.

---

## Frame Scaling

Frames were resized before detection to reduce computation.

---

## Interval-Based Inference

Detection, recognition, and emotion analysis were executed at configurable intervals instead of every frame.

---

## Emotion Smoothing

Emotion predictions were stabilized using short rolling history windows.

---

## Tracking-Based Persistence

Tracking allowed recognition and emotion state reuse across frames.

Benefits:

- Lower compute usage
- Reduced UI flickering
- Smoother identity persistence

---

# Engineering Challenges

## WebSocket + HTTPS Compatibility

Because the frontend was hosted on HTTPS, browsers blocked insecure websocket connections.

Solution:

- Cloudflare Tunnel
- WSS support
- Secure backend exposure

---

## Infrastructure Constraints

The system was deployed on a small AWS EC2 instance:

- t3.micro
- 1 GB RAM

The combined workload of:

- TensorFlow
- DeepFace
- MediaPipe
- WebSocket streaming
- PostgreSQL
- Docker containers

created significant resource pressure.

Observed issues:

- SSH disconnects
- WebSocket interruptions
- Cloudflare tunnel instability
- Memory exhaustion

At this stage the deployment architecture had already been validated successfully, so further optimization work was intentionally deferred.

---

# Future Improvements

Potential future upgrades include:

- Async inference queues
- GPU inference
- ONNX optimization
- Redis-based frame buffering
- Kubernetes deployment
- Advanced tracking systems (DeepSORT / ByteTrack)
- Liveness detection
- Face embedding caching

---

# Key Learnings

This project evolved from a simple ML demo into a production-style AI system.

Major engineering learnings included:

- Realtime inference architecture
- WebSocket systems
- Backend modularization
- Cloud deployment
- Dockerized ML services
- Infrastructure debugging
- Production tradeoff analysis
- Tracking-based state management

---

# Final Outcome

The project successfully demonstrates:

- Applied computer vision engineering
- ML systems architecture
- Realtime streaming systems
- Full-stack AI integration
- Cloud deployment workflows
- Production engineering tradeoffs

The project intentionally stopped after validating deployment and systems architecture in order to prioritize breadth across future AI engineering projects rather than over-investing into scaling a single application.
