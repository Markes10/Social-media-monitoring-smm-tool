import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet } from "react-native";
import axios from "axios";

const AnalyticsScreen = () => {
    const [analytics, setAnalytics] = useState({});
    const [prediction, setPrediction] = useState({});

    useEffect(() => {
        const fetchData = async () => {
            const analyticsResponse = await axios.get("http://your-api-url/analytics");
            const predictionResponse = await axios.get("http://your-api-url/predict-engagement");

            setAnalytics(analyticsResponse.data);
            setPrediction(predictionResponse.data);
        };

        fetchData();
    }, []);

    return (
        <View style={styles.container}>
            <Text style={styles.header}>Analytics Dashboard</Text>
            <Text>Total Posts: {analytics.total_posts}</Text>
            <Text>Average Sentiment Score: {analytics.avg_sentiment_score}</Text>
            <Text>Engagement Rate: {analytics.engagement_rate}</Text>
            <Text>Predicted Engagement Rate: {prediction.predicted_engagement_rate}</Text>
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { fontSize: 20, fontWeight: "bold" },
});

export default AnalyticsScreen;
