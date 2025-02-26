import React, { useState, useEffect } from "react";
import { View, Text, TextInput, Button, FlatList, StyleSheet } from "react-native";
import axios from "axios";

const SentimentAnalysisScreen = () => {
    const [keyword, setKeyword] = useState("");
    const [sentiments, setSentiments] = useState([]);

    const fetchSentiment = async () => {
        const response = await axios.get(`http://your-api-url/social-sentiment?keyword=${keyword}`);
        setSentiments(response.data.sentiment_analysis);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🔍 AI-Based Sentiment Analysis</Text>

            <TextInput
                style={styles.input}
                placeholder="Enter Keyword..."
                value={keyword}
                onChangeText={setKeyword}
            />
            <Button title="Analyze" onPress={fetchSentiment} />

            <FlatList
                data={sentiments}
                keyExtractor={(item, index) => index.toString()}
                renderItem={({ item }) => (
                    <View style={styles.commentCard}>
                        <Text>📢 Platform: {item.platform}</Text>
                        <Text>👤 User: {item.username}</Text>
                        <Text>💬 Comment: {item.comment_text}</Text>
                        <Text>📊 Sentiment: {item.sentiment_label} ({item.sentiment_score})</Text>
                    </View>
                )}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { fontSize: 20, fontWeight: "bold" },
    input: { borderWidth: 1, padding: 10, marginVertical: 10 },
    commentCard: { padding: 10, borderBottomWidth: 1, marginVertical: 5 },
});

export default SentimentAnalysisScreen;
