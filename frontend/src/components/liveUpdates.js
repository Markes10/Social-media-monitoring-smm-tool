import React, { useEffect, useState } from "react";
import { Alert, AlertTitle } from "@mui/material";

const LiveUpdates = () => {
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        const socket = new WebSocket("ws://localhost:8000/ws");

        socket.onmessage = (event) => {
            setMessages((prev) => [...prev, event.data]);
        };

        return () => socket.close();
    }, []);

    return (
        <div>
            <h3>🔴 Live Updates</h3>
            {messages.slice(-10).map((msg, index) => (
                msg.includes("🚨") ? (
                    <Alert severity="error" key={index}>
                        <AlertTitle>Critical Alert</AlertTitle>
                        {msg}
                    </Alert>
                ) : msg.includes("🐦") ? (
                    <Alert severity="info" key={index}>
                        <AlertTitle>Twitter Post</AlertTitle>
                        {msg}
                    </Alert>
                ) : msg.includes("📘") ? (
                    <Alert severity="success" key={index}>
                        <AlertTitle>Facebook Post</AlertTitle>
                        {msg}
                    </Alert>
                ) : (
                    <p key={index}>{msg}</p>
                )
            ))}
        </div>
    );
};

export default LiveUpdates;