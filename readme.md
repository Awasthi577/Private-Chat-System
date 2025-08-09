# Mental 3D Model Viewer

This project is a Three.js-based 3D model viewer that loads multiple 3D models (from URLs) and displays them in a mosaic grid with individual animations. It also includes UI links to help you understand how the code works.

---

##  Features
- Loads 3D models from provided URLs (GLTF/GLB format).
- Displays models in a mosaic-like grid layout.
- Assigns **unique animations** to each model (no more same-animation issue).
- Clickable UI links to learn about Three.js and model loading.
- Uses placeholder images for thumbnails.

---

## Installation
1. Clone this repository or copy the files into a folder.
2. Make sure you have a local server to run it (Three.js requires files to be served via HTTP, not opened directly in the browser).
   - You can quickly run one using:
     ```bash
     # Python 3
     python -m http.server 8000
     
     # Node.js
     npx http-server .
     ```
3. Open `index.html` in your browser via the local server.

---

##  How It Works
1. **Scene Setup** – Creates a Three.js scene, camera, and renderer.
2. **Model Loading** – Uses `GLTFLoader` to fetch models from URLs.
3. **Mosaic Layout** – Each model is placed in a grid using an X/Z offset.
4. **Unique Animations** – Each model gets a slightly different rotation speed or animation clip to avoid identical movements.
5. **UI Links** – Helpful links are placed on the page to guide new developers.

---

## File Structure

/project
│── index.html # Main entry file
│── script.js # Three.js logic
│── style.css # Styling for UI
│── README.md # This file


---

## Example Code Snippet

// Loading models with unique animations
modelData.forEach((model, i) => {
  loader.load(model.url, gltf => {
    const obj = gltf.scene;
    obj.position.set((i % 5) * 5, 0, Math.floor(i / 5) * 5);
    scene.add(obj);

    const speed = 0.005 + Math.random() * 0.01; // unique speed
    animations.push(() => { obj.rotation.y += speed; });
  });
});



## Model & Image URLs
Edit the `modelData` array in `script.js` to add or change models:
```javascript
const modelData = [
  {
    url: "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Duck/glTF/Duck.gltf",
    thumbnail: "https://threejs.org/examples/models/gltf/Duck/screenshot/screenshot.jpg"
  },
  {
    url: "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/BrainStem/glTF/BrainStem.gltf",
    thumbnail: "https://threejs.org/examples/models/gltf/BrainStem/screenshot/screenshot.jpg"
  },
  {
    url: "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Avocado/glTF/Avocado.gltf",
    thumbnail: "https://threejs.org/examples/models/gltf/Avocado/screenshot/screenshot.jpg"
  }
];

```
## Running the Project

1. Start your local server.

2. Open http://localhost:8000.

3. You should see multiple 3D models arranged in a grid, each spinning at a unique speed.



