import React, { useState } from 'react';

function ImageUploadForm({ token, onImageModerate }) {
    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileChange = (e) => {
        setSelectedFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!selectedFile) {
            alert('Please select an image file first.');
            return;
        }
        if (!token) {
            alert('Please set your authentication token first.');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        onImageModerate(formData);
    };

    return (
        <div style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ccc', borderRadius: '8px' }}>
            <h3>Upload Image for Moderation</h3>
            <form onSubmit={handleSubmit}>
                <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    style={{ marginBottom: '10px' }}
                />
                <button type="submit" style={{ padding: '8px 15px', backgroundColor: '#17a2b8', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                    Moderate Image
                </button>
            </form>
            {selectedFile && <p>Selected file: {selectedFile.name}</p>}
        </div>
    );
}

export default ImageUploadForm;