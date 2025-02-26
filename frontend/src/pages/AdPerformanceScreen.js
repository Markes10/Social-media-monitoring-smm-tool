import React, { useState, useEffect } from "react";
import { View, Text, FlatList, StyleSheet } from "react-native";
import axios from "axios";

const AdPerformanceScreen = () => {
    const [ads, setAds] = useState([]);

    useEffect(() => {
        fetchAds();
    }, []);

    const fetchAds = async () => {
        const response = await axios.get("http://your-api-url/ad-performance");
        setAds(response.data.ad_performance_insights);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>AI-Powered Ad Performance</Text>

            <FlatList
                data={ads}
                keyExtractor={(item, index) => index.toString()}
                renderItem={({ item }) => (
                    <View style={styles.adCard}>
                        <Text>📢 Ad Name: {item.ad_name}</Text>
                        <Text>👀 Impressions: {item.impressions}</Text>
                        <Text>👆 Clicks: {item.clicks}</Text>
                        <Text>💰 CPC: ${item.cost_per_click}</Text>
                        <Text>🔮 Predicted Engagement: {item.predicted_engagement_score}</Text>
                    </View>
                )}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { fontSize: 20, fontWeight: "bold" },
    adCard: { padding: 10, borderBottomWidth: 1, marginVertical: 5 },
});

export default AdPerformanceScreen;
