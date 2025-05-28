import React, { useState, useEffect } from 'react';
import AuthForm from '../components/AuthForm';
import ImageUploadForm from '../components/ImageUploadForm';
import ModerationReport from '../components/ModerationReport';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:7000'; // Make sure this matches your backend

function HomePage() {
    const [token, setToken] = useState(localStorage.getItem('authToken') || '');
    const [isAdmin, setIsAdmin] = useState(false); // You might have a way to check this based on the token
    const [moderationReport, setModerationReport] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!token) {
            setToken("admin-123"); // Temporary default
        }
        if (token) {
            localStorage.setItem('authToken', token);
            // You could make an API call to verify token and get admin status
            // For simplicity, let's assume if it's a specific token it's admin
            // This is NOT secure for production; just for this assignment.
            setIsAdmin(token.includes('admin')); // Very basic admin check for demo
        } else {
            localStorage.removeItem('authToken');
            setIsAdmin(false);
        }
    }, [token]);

    const handleGenerateToken = async (adminStatus) => {
    setLoading(true);
    setError(null);
    try {
        const response = await fetch(`${API_BASE_URL}/auth/tokens?is_admin=${adminStatus}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}` // Requires an existing admin token
            }
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to generate token');
        }
        setToken(data.token); // Automatically set the new token
        alert(`New Token: ${data.token}\nIs Admin: ${data.is_admin}`);
    } catch (err) {
        setError(err.message);
        console.error("Error generating token:", err);
    } finally {
        setLoading(false);
    }
};

    const handleImageModerate = async (formData) => {
        setLoading(true);
        setError(null);
        setModerationReport(null);
        try {
            const response = await fetch(`${API_BASE_URL}/moderate`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData,
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail || 'Image moderation failed');
            }
            setModerationReport(data);
        } catch (err) {
            setError(err.message);
            console.error("Error moderating image:", err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: '800px', margin: '20px auto', fontFamily: 'Arial, sans-serif', padding: '20px', border: '1px solid #eee', borderRadius: '10px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
            <h1 style={{ textAlign: 'center', color: '#333' }}>Image Moderation UI</h1>

            <AuthForm setToken={setToken} isAdmin={isAdmin} onGenerateToken={handleGenerateToken} />

            <p style={{ textAlign: 'center', fontSize: '0.9em', color: '#555' }}>
                Current Token: <strong>{token || 'Not set'}</strong> {token && (isAdmin ? '(Admin)' : '(User)')}
            </p>

            <ImageUploadForm token={token} onImageModerate={handleImageModerate} />

            {loading && <p style={{ textAlign: 'center', color: '#007bff' }}>Loading...</p>}
            {error && <p style={{ textAlign: 'center', color: 'red' }}>Error: {error}</p>}

            <ModerationReport report={moderationReport} />
        </div>
    );
}

export default HomePage;