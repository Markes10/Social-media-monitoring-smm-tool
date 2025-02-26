import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import axios from "axios";

const ChatbotScreen = () => {
    const [message, setMessage] = useState("");
    const [reply, setReply] = useState("");

    const getReply = async () => {
        const response = await axios.post("http://your-api-url/auto-reply", { text: message });
        setReply(response.data.auto_reply);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🤖 AI Chatbot</Text>
            <TextInput style={styles.input} placeholder="Ask something..." value={message} onChangeText={setMessage} />
            <Button title="Get AI Response" onPress={getReply} />
            {reply && (
                <Text style={styles.response}>💬 {reply}</Text>
            )}
        </View>
    );
};

export default ChatbotScreen;
