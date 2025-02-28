import React, { useState, useEffect } from "react";
import { View, Text, TextInput, Button, FlatList, StyleSheet } from "react-native";
import axios from "axios";

const InfluencerDashboard = () => {
    const [influencerData, setInfluencerData] = useState(null);
    const [hashtag, setHashtag] = useState("");
    const [influencers, setInfluencers] = useState([]);

    const fetchInfluencerInsights = async () => {
        const response = await axios.get("http://your-api-url/influencer-analysis");
        setInfluencerData(response.data);
    };

    const fetchInfluencersByHashtag = async () => {
        const response = await axios.get(`http://your-api-url/influencers?hashtag=${hashtag}`);
        setInfluencers(response.data);
    };

    useEffect(() => {
        fetchInfluencerInsights();
    }, []);

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📊 AI-Driven Influencer Dashboard</Text>

            {influencerData && (
                <View>
                    <Text>🏆 Top Influencer: {influencerData.top_influencer}</Text>
                    <Text>📊 Engagement Rate: {influencerData.best_engagement_rate}%</Text>
                    <Text>🚫 Fake Followers: {influencerData.lowest_bot_followers}%</Text>
                    <Text>💡 Recommendation: {influencerData.recommendation}</Text>
                </View>
            )}

            <TextInput
                placeholder="Enter hashtag (e.g. #AI)"
                value={hashtag}
                onChangeText={setHashtag}
                style={styles.input}
            />
            <Button title="🔍 Find Influencers" onPress={fetchInfluencersByHashtag} />
            <FlatList
                data={influencers}
                renderItem={({ item }) => (
                    <Text>🔥 @{item.username} - {item.followers} followers, {item.engagement} engagements</Text>
                )}
                keyExtractor={(item, index) => index.toString()}
            />
            <Button title="Refresh Influencer Insights" onPress={fetchInfluencerInsights} />
        </View>
    );
};

const styles = StyleSheet.create({
    container: { padding: 20 },
    header: { fontSize: 20, fontWeight: "bold", marginBottom: 10 },
    input: { borderWidth: 1, padding: 8, marginBottom: 10 }
});

export default InfluencerDashboard;
