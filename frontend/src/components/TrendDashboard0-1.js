import React, { useState, useEffect } from "react";
import { View, Text, FlatList, TextInput, Button, StyleSheet } from "react-native";
import axios from "axios";

const TrendDashboard = () => {
    const [trends, setTrends] = useState([]);
    const [content, setContent] = useState("");
    const [likes, setLikes] = useState("");
    const [shares, setShares] = useState("");
    const [prediction, setPrediction] = useState("");
    const [trendPredictions, setTrendPredictions] = useState(null);

    const fetchTrends = async () => {
        const res = await axios.get("http://your-api-url/trending_topics");
        setTrends(res.data.trending_topics);
    };

    const fetchPrediction = async () => {
        const res = await axios.get(`http://your-api-url/predict_virality?content=${content}&likes=${likes}&shares=${shares}`);
        setPrediction(res.data.prediction);
    };

    const fetchTrendPredictions = async () => {
        const res = await axios.get("http://your-api-url/predict_trends");
        setTrendPredictions(res.data.trend_predictions);
    };

    useEffect(() => {
        fetchTrends();
    }, []);

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🔥 Trending Hashtags</Text>
            <FlatList
                data={trends}
                keyExtractor={(item) => item.name}
                renderItem={({ item }) => (
                    <Text style={styles.trend}>#{item.name} - {item.tweet_volume} tweets</Text>
                )}
            />

            <Text style={styles.header}>📊 Predict Virality of a Post</Text>
            <TextInput placeholder="Enter Post Content" value={content} onChangeText={setContent} style={styles.input} />
            <TextInput placeholder="Likes" value={likes} onChangeText={setLikes} keyboardType="numeric" style={styles.input} />
            <TextInput placeholder="Shares" value={shares} onChangeText={setShares} keyboardType="numeric" style={styles.input} />
            <Button title="🔮 Predict Virality" onPress={fetchPrediction} />
            {prediction && <Text style={styles.result}>📢 Virality Prediction: {prediction}</Text>}

            <Text style={styles.header}>📈 Social Media Trend Predictions</Text>
            <Button title="🔮 Predict Trends" onPress={fetchTrendPredictions} />
            {trendPredictions && <Text style={styles.result}>🔥 AI Trend Forecast: {trendPredictions}</Text>}
        </View>
    );
};

const styles = StyleSheet.create({
    container: { padding: 20 },
    header: { fontSize: 20, fontWeight: "bold", marginBottom: 10 },
    trend: { fontSize: 16, marginBottom: 5 },
    input: { borderWidth: 1, padding: 10, marginVertical: 5, borderRadius: 5 },
    result: { fontSize: 16, marginTop: 10, fontWeight: "bold" },
});

export default TrendDashboard;
