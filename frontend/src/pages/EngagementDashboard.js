import React, { useState, useEffect } from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import axios from "axios";

const EngagementDashboard = () => {
    const [engagementData, setEngagementData] = useState(null);

    const fetchEngagementInsights = async () => {
        const response = await axios.get("http://your-api-url/engagement-analysis");
        setEngagementData(response.data);
    };

    useEffect(() => {
        fetchEngagementInsights();
    }, []);

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📊 AI Audience Engagement Analysis</Text>
            
            {engagementData && (
                <View>
                    <Text>🔥 Average Likes: {engagementData.average_likes}</Text>
                    <Text>🔄 Average Shares: {engagementData.average_shares}</Text>

                    <Text>💬 Comment Analysis:</Text>
                    {engagementData.engagement_insights.map((entry, index) => (
                        <View key={index} style={styles.commentBox}>
                            <Text>{entry.comment}</Text>
                            <Text>❤️ Likes: {entry.likes} | 🔄 Shares: {entry.shares}</Text>
                            <Text>🧠 Sentiment: {entry.sentiment}</Text>
                        </View>
                    ))}
                </View>
            )}

            <Button title="Refresh Engagement Data" onPress={fetchEngagementInsights} />
        </View>
    );
};

export default EngagementDashboard;
