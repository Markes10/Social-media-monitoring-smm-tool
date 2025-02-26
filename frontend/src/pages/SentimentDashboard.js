import React, { useState, useEffect } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import axios from "axios";

const SentimentDashboard = () => {
    const [inputText, setInputText] = useState("");
    const [sentimentData, setSentimentData] = useState(null);

    const analyzeSentiment = async () => {
        const response = await axios.post("http://your-api-url/sentiment-analysis", { text: inputText });
        setSentimentData(response.data.sentiment_data);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🧠 AI-Powered Sentiment Analysis</Text>
            <TextInput
                style={styles.input}
                placeholder="Enter a social media post..."
                value={inputText}
                onChangeText={setInputText}
            />
            <Button title="Analyze Sentiment" onPress={analyzeSentiment} />
            
            {sentimentData && (
                <View style={styles.result}>
                    <Text>💬 Text: {sentimentData.text}</Text>
                    <Text>📊 Sentiment: {sentimentData.sentiment}</Text>
                    <Text>🔍 Confidence: {sentimentData.confidence}</Text>
                </View>
            )}
        </View>
    );
};

export default SentimentDashboard;
