import React, { useState, useEffect } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import axios from "axios";

const TrendDashboard = () => {
    const [hashtag, setHashtag] = useState("");
    const [prediction, setPrediction] = useState(null);
    const [keywords, setKeywords] = useState("");
    const [predictions, setPredictions] = useState(null);

    const predictTrend = async () => {
        const response = await axios.get("http://your-api-url/predict-trend", {
            params: { hashtag }
        });
        setPrediction(response.data.trend_forecast);
    };

    const extractKeywords = async () => {
        const response = await axios.post("http://your-api-url/extract-keywords", { text: keywords });
        setKeywords(response.data.trending_keywords.join(", "));
    };

    const fetchPredictions = async () => {
        const pastData = [
            { date: "2024-02-01", engagement: 100 },
            { date: "2024-02-02", engagement: 120 },
            { date: "2024-02-03", engagement: 150 },
        ];

        const response = await axios.post("http://your-api-url/predict-trends", pastData);
        setPredictions(response.data.predictions);
    };

    useEffect(() => {
        fetchPredictions();
    }, []);

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🔮 AI Trend Prediction & Analysis</Text>

            <TextInput
                placeholder="📌 Enter Hashtag"
                value={hashtag}
                onChangeText={setHashtag}
                style={styles.input}
            />
            <Button title="🚀 Predict Trend" onPress={predictTrend} />
            {prediction && prediction.map((trend, index) => (
                <Text key={index} style={styles.result}>📅 {trend.ds}: 🔥 {trend.yhat} mentions expected</Text>
            ))}

            <TextInput
                placeholder="📜 Paste Text to Extract Keywords"
                value={keywords}
                onChangeText={setKeywords}
                style={styles.input}
            />
            <Button title="🔍 Extract Trending Keywords" onPress={extractKeywords} />
            {keywords && <Text style={styles.result}>🔥 Trending Keywords: {keywords}</Text>}

            <Button title="🔮 Predict Future Trends" onPress={fetchPredictions} />
            {predictions && predictions.map((trend, index) => (
                <Text key={index}>📅 {trend.ds}: Predicted Engagement {Math.round(trend.yhat)}</Text>
            ))}
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { fontSize: 20, fontWeight: "bold", marginBottom: 10 },
    input: { borderWidth: 1, padding: 10, marginBottom: 10 },
    result: { marginTop: 10, fontSize: 16 },
});

export default TrendDashboard;
