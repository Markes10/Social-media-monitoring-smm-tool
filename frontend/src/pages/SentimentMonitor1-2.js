import React, { useState } from "react";
import { View, Text, TextInput, Button, FlatList, Picker, StyleSheet } from "react-native";
import axios from "axios";

const SentimentMonitor = () => {
    const [comment, setComment] = useState("");
    const [keyword, setKeyword] = useState("");
    const [sentiment, setSentiment] = useState(null);
    const [posts, setPosts] = useState([]);
    const [platform, setPlatform] = useState("twitter");
    const [crisisStatus, setCrisisStatus] = useState(null);
    
    const analyzeSentiment = async () => {
        const response = await axios.post("http://your-api-url/analyze-sentiment", { text: comment });
        setSentiment(response.data);
    };

    const fetchPosts = async () => {
        const response = await axios.get(`http://your-api-url/sentiment/posts?platform=${platform}&keyword=${keyword}`);
        setPosts(response.data);
    };

    const batchAnalyzeSentiment = async () => {
        const response = await axios.post("http://your-api-url/sentiment/analyze", posts);
        setSentiment(response.data);
    };

    const detectCrisis = async () => {
        const response = await axios.post("http://your-api-url/detect-crisis", { text: comment });
        setCrisisStatus(response.data);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📊 Sentiment & Crisis Monitor</Text>

            <TextInput
                placeholder="Enter a comment to analyze"
                value={comment}
                onChangeText={setComment}
                style={styles.input}
            />
            <Button title="🧠 Analyze Sentiment" onPress={analyzeSentiment} />
            {sentiment && <Text>Sentiment: {sentiment.label} ({Math.round(sentiment.score * 100)}%)</Text>}

            <TextInput
                placeholder="Enter keyword (e.g., brand, event)"
                value={keyword}
                onChangeText={setKeyword}
                style={styles.input}
            />
            <Picker selectedValue={platform} onValueChange={setPlatform} style={styles.input}>
                <Picker.Item label="Twitter" value="twitter" />
                <Picker.Item label="Facebook" value="facebook" />
                <Picker.Item label="Instagram" value="instagram" />
                <Picker.Item label="LinkedIn" value="linkedin" />
            </Picker>
            <Button title="📢 Fetch Posts" onPress={fetchPosts} />
            <FlatList
                data={posts}
                renderItem={({ item }) => <Text>💬 {item}</Text>}
                keyExtractor={(item, index) => index.toString()}
            />
            <Button title="📊 Analyze Sentiment of Posts" onPress={batchAnalyzeSentiment} />

            {sentiment && (
                <View>
                    <Text style={styles.subheader}>Sentiment Summary:</Text>
                    <Text>😊 Positive: {sentiment.sentiment_summary.POSITIVE || 0}</Text>
                    <Text>😐 Neutral: {sentiment.sentiment_summary.NEUTRAL || 0}</Text>
                    <Text>😡 Negative: {sentiment.sentiment_summary.NEGATIVE || 0}</Text>
                    <Text>🚨 Crisis Level: {sentiment.crisis_level}</Text>
                </View>
            )}

            <Button title="🚨 Detect Crisis" onPress={detectCrisis} />
            {crisisStatus && <Text>{crisisStatus.crisis_detected ? "⚠️ Crisis Detected!" : "✅ No Crisis Detected"}</Text>}
        </View>
    );
};

const styles = StyleSheet.create({
    container: { padding: 20 },
    header: { fontSize: 20, fontWeight: "bold", marginBottom: 10 },
    input: { borderWidth: 1, padding: 8, marginBottom: 10 },
    subheader: { fontSize: 16, fontWeight: "bold", marginTop: 10 }
});

export default SentimentMonitor;
