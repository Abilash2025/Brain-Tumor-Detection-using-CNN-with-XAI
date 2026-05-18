import { useState } from "react";
import axios from "axios";

function App() {

  const [selectedFile, setSelectedFile] = useState(null);

  const [preview, setPreview] = useState(null);

  const [prediction, setPrediction] = useState(null);

  const [loading, setLoading] = useState(false);

  // Handle image selection
  const handleFileChange = (event) => {

    const file = event.target.files[0];

    if (!file) return;

    setSelectedFile(file);

    setPreview(URL.createObjectURL(file));

    setPrediction(null);
  };

  // Upload image
  const handleUpload = async () => {

    if (!selectedFile) return;

    setLoading(true);

    try {

      const formData = new FormData();

      formData.append("file", selectedFile);

      const response = await axios.post(
         `${import.meta.env.VITE_API_URL}/predict`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setPrediction(response.data);

    } catch (error) {

      console.error(error);

      alert("Prediction failed.");

    } finally {

      setLoading(false);
    }
  };

  return (

    <div className="min-h-screen bg-gradient-to-b from-[#8E8B7E] to-[#1F1F1F] flex flex-col items-center">

      {/* Header */}
      <div className="w-full max-w-5xl pt-6">

        <h1 className="text-center text-white text-xl font-semibold">

          Brain Tumor Detection using CNN with XAI

        </h1>

        <div className="border-t border-gray-300 mt-3"></div>

      </div>

      {/* Main Container */}
      <div className="flex flex-col items-center justify-center flex-1 w-full px-6">

        {/* Upload Section */}
        {!preview && (

          <div className="bg-[#A29F90]/70 rounded-xl px-8 py-6 flex items-center gap-4 shadow-lg">

  <p className="text-white font-semibold">

    Upload a MRI Scan

  </p>

  {/* Hidden Input */}
  <input
    id="mri-upload"
    type="file"
    accept="image/*"
    onChange={handleFileChange}
    className="hidden"
  />

  {/* Button */}
  <label
    htmlFor="mri-upload"
    className="bg-gray-500 hover:bg-gray-600 transition text-white text-sm px-4 py-1 rounded-full cursor-pointer"
  >

    Choose File

  </label>

</div>
        )}

        {/* Preview Section */}
        {preview && !prediction && (

          <div className="flex items-center gap-8">

            {/* MRI Preview */}
            <div className="w-52 h-52 bg-[#A29F90]/70 rounded-xl flex items-center justify-center overflow-hidden shadow-lg">

              <img
                src={preview}
                alt="MRI Preview"
                className="w-full h-full object-cover"
              />

            </div>

            {/* Analyze Button */}
            <button
              type="button"
              onClick={handleUpload}
              disabled={loading}
              className="bg-[#A29F90]/80 hover:bg-[#B7B4A7] transition text-white font-semibold px-8 py-3 rounded-full shadow-lg"
            >

              {loading
                ? "Analyzing..."
                : "Analyze MRI"}

            </button>

          </div>
        )}

        {/* Results Section */}
        {prediction && (

          <div className="flex flex-col items-center">

            {/* Images */}
            <div className="flex flex-col md:flex-row gap-8">

              {/* Original MRI */}
              <div className="w-64 h-64 bg-[#A29F90]/70 rounded-xl overflow-hidden shadow-lg">

                <img
                  src={preview}
                  alt="MRI"
                  className="w-full h-full object-cover"
                />

              </div>

              {/* Grad-CAM */}
              <div className="w-64 h-64 bg-[#A29F90]/70 rounded-xl overflow-hidden shadow-lg">

                <img
                  src={`http://127.0.0.1:8000${prediction.gradcam_image}`}
                  alt="GradCAM"
                  className="w-full h-full object-cover"
                />

              </div>

            </div>

            {/* Result Card */}
            <div className="mt-8 bg-[#A29F90]/70 px-10 py-4 rounded-xl shadow-lg text-center min-w-[320px]">

              <p className="text-white text-lg font-semibold">

                Predicted Result:
                {" "}
                <span className="capitalize">

                  {prediction.predicted_class}

                </span>

              </p>

              <p className="text-white mt-2">

                Confidence Score:
                {" "}
                {prediction.confidence}%

              </p>

            </div>

            {/* New Scan Button */}
            <button
              onClick={() => {

                setSelectedFile(null);

                setPreview(null);

                setPrediction(null);
              }}
              className="mt-6 bg-white/20 hover:bg-white/30 transition text-white px-6 py-2 rounded-full"
            >

              Upload New Scan

            </button>

          </div>
        )}

      </div>

    </div>
  );
}

export default App;