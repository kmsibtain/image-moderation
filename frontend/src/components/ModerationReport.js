import React from 'react';

function ModerationReport({ report }) {
    if (!report) {
        return null;
    }

    return (
        <div style={{ padding: '15px', border: '1px solid #ccc', borderRadius: '8px', backgroundColor: '#f8f9fa' }}>
            <h3>Moderation Report</h3>
            <p><strong>Filename:</strong> {report.filename}</p>
            <p><strong>Content Type:</strong> {report.content_type}</p>

            {report.moderation_report && (
                <div>
                    <h4>Safety Analysis:</h4>
                    {Object.entries(report.moderation_report).map(([category, data]) => (
                        <div key={category} style={{ marginBottom: '5px' }}>
                            <strong>{category.replace(/_/g, ' ')}:</strong>
                            {typeof data === 'object' && data !== null ? (
                                <>
                                    <span> Detected: {data.detected ? 'Yes' : 'No'}</span>
                                    {data.confidence !== undefined && <span> (Confidence: {(data.confidence * 100).toFixed(2)}%)</span>}
                                </>
                            ) : (
                                <span> {data}</span>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default ModerationReport;