import React, { useState, useEffect } from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import axios from "axios";

const PostAnalyticsScreen = ({ route }) => {
    const { postId } = route.params;
    const [analytics, setAnalytics] = useState(null);

    useEffect(() => {
        fetchPostAnalytics();
    }, []);

    const fetchPostAnalytics = async () => {
        const response = await axios.get(`http://your-api-url/post-performance/${postId}`);
        setAnalytics(response.data);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>Post Performance</Text>

            {analytics ? (
                <>
                    <Text>📌 Likes: {analytics.likes}</Text>
                    <Text>🔄 Shares: {analytics.shares}</Text>
                    <Text>💬 Comments: {analytics.comments}</Text>
                    <Text>👀 Impressions: {analytics.impressions}</Text>
                    <Text>🔥 Engagement Score: {analytics.engagement_score}</Text>
                </>
            ) : (
                <Text>Loading...</Text>
            )}

            <Button title="Refresh Data" onPress={fetchPostAnalytics} />
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { fontSize: 20, fontWeight: "bold" },
});

export default PostAnalyticsScreen;
