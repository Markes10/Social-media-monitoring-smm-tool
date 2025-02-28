import React, { useState, useEffect } from "react";
import { View, Text, Image, Button, StyleSheet } from "react-native";
import axios from "axios";

const AnalyticsDashboard = () => {
    const [analyticsData, setAnalyticsData] = useState(null);

    const fetchAnalytics = async () => {
        const response = await axios.get("http://your-api-url/analytics");
        setAnalyticsData(response.data.analytics_data);
    };

    useEffect(() => {
        fetchAnalytics();
    }, []);

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📊 AI-Powered Social Media Analytics</Text>
            {analyticsData ? (
                <View>
                    <Text>📅 Highest Engagement Day: {analyticsData.highest_engagement_day}</Text>
                    <Text>📈 Average Engagement Score: {analyticsData.avg_engagement_score.toFixed(2)}</Text>
                    <Text>💡 Insights: {analyticsData.insights}</Text>
                    <Image source={{ uri: "http://your-api-url/static/engagement_trend.png" }} style={styles.chart} />
                </View>
            ) : (
                <Text>Loading analytics...</Text>
            )}
        </View>
    );
};

export default AnalyticsDashboard;
