import React, { useState } from "react";
import { View, Text, TextInput, Button, ScrollView, StyleSheet } from "react-native";
import axios from "axios";

const ChatbotUI = () => {
    const [message, setMessage] = useState("");
    const [chatHistory, setChatHistory] = useState([]);

    const sendMessage = async () => {
        const response = await axios.post("http://your-api-url/chatbot", { message });
        setChatHistory([...chatHistory, { role: "user", text: message }, { role: "bot", text: response.data.reply }]);
        setMessage("");
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🤖 AI-Powered Social Media Chatbot</Text>
            <ScrollView style={styles.chatBox}>
                {chatHistory.map((msg, index) => (
                    <Text key={index} style={msg.role === "user" ? styles.userMessage : styles.botMessage}>
                        {msg.text}
                    </Text>
                ))}
            </ScrollView>
            <TextInput style={styles.input} placeholder="Type a message..." value={message} onChangeText={setMessage} />
            <Button title="Send" onPress={sendMessage} />
        </View>
    );
};

export default ChatbotUI;
