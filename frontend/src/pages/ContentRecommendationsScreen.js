import React, { useState, useEffect } from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import axios from "axios";

const ContentRecommendationsScreen = () => {
    const [recommendations, setRecommendations] = useState(null);

    useEffect(() => {
        fetchRecommendations();
    }, []);

    const fetchRecommendations = async () => {
        const response = await axios.get("http://your-api-url/content-recommendations");
        setRecommendations(response.data);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>AI Content Recommendations</Text>

            {recommendations ? (
                <>
                    <Text>✍️ Caption: {recommendations.recommended_caption}</Text>
                    <Text>🏷 Hashtags: {recommendations.suggested_hashtags}</Text>
                    <Text>⏰ Best Posting Time: {recommendations.best_posting_time}</Text>
                </>
            ) : (
                <Text>Loading...</Text>
            )}

            <Button title="Refresh Suggestions" onPress={fetchRecommendations} />
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { fontSize: 20, fontWeight: "bold" },
});

export default ContentRecommendationsScreen;
