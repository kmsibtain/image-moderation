import React, { useState } from 'react';

function AuthForm({ setToken, isAdmin, onGenerateToken }) {
    const [inputToken, setInputToken] = useState('');

    const handleTokenSubmit = (e) => {
        e.preventDefault();
        setToken(inputToken);
    };

    return (
        <div style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ccc', borderRadius: '8px' }}>
            <h3>Authentication</h3>
            <form onSubmit={handleTokenSubmit}>
                <label htmlFor="token">Enter Token:</label>
                <input
                    type="text"
                    id="token"
                    value={inputToken}
                    onChange={(e) => setInputToken(e.target.value)}
                    placeholder="Bearer Token"
                    style={{ margin: '0 10px', padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }}
                />
                <button type="submit" style={{ padding: '8px 15px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                    Set Token
                </button>
            </form>

            {isAdmin && (
                <div style={{ marginTop: '15px' }}>
                    <button onClick={() => onGenerateToken(false)} style={{ padding: '8px 15px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', marginRight: '10px' }}>
                        Generate User Token
                    </button>
                    <button onClick={() => onGenerateToken(true)} style={{ padding: '8px 15px', backgroundColor: '#ffc107', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                        Generate Admin Token
                    </button>
                </div>
            )}
        </div>
    );
}

export default AuthForm;