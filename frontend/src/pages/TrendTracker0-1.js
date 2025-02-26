import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import axios from "axios";

const TrendTracker = () => {
    const [trends, setTrends] = useState([]);
    const [competitor, setCompetitor] = useState("");
    const [competitorData, setCompetitorData] = useState(null);

    const fetchTrends = async () => {
        const response = await axios.get("http://your-api-url/trends");
        setTrends(response.data.trending_hashtags);
    };

    const fetchCompetitorData = async () => {
        const response = await axios.get("http://your-api-url/competitor", {
            params: { competitor_handle: competitor }
        });
        setCompetitorData(response.data);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📊 Trend & Competitor Tracker</Text>

            <Button title="🔥 Fetch Trending Topics" onPress={fetchTrends} />

            {trends.length > 0 && (
                <View>
                    <Text style={styles.subHeader}>Trending Hashtags:</Text>
                    {trends.map((hashtag, index) => (
                        <Text key={index} style={styles.trend}>{hashtag}</Text>
                    ))}
                </View>
            )}

            <TextInput
                placeholder="Enter Competitor Handle"
                value={competitor}
                onChangeText={setCompetitor}
                style={styles.input}
            />

            <Button title="🔍 Analyze Competitor" onPress={fetchCompetitorData} />

            {competitorData && (
                <View>
                    <Text style={styles.subHeader}>Competitor Stats:</Text>
                    <Text>Followers: {competitorData.public_metrics.followers_count}</Text>
                    <Text>Tweets: {competitorData.public_metrics.tweet_count}</Text>
                    <Text>Likes: {competitorData.public_metrics.like_count}</Text>
                </View>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { fontSize: 20, fontWeight: "bold", marginBottom: 10 },
    input: { borderWidth: 1, padding: 10, marginBottom: 10 },
    subHeader: { fontSize: 16, fontWeight: "bold", marginTop: 10 },
    trend: { fontSize: 14, marginBottom: 5 }
});

export default TrendTracker;
