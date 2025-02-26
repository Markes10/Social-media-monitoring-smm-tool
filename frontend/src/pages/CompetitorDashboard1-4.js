import React, { useState, useEffect } from "react";
import { View, Text, TextInput, Button, FlatList, StyleSheet } from "react-native";
import axios from "axios";

const CompetitorDashboard = () => {
    const [brand, setBrand] = useState("Nike");
    const [competitor, setCompetitor] = useState("Adidas");
    const [platform, setPlatform] = useState("Twitter");
    const [competitorData, setCompetitorData] = useState(null);
    const [competitors, setCompetitors] = useState("");
    const [customCompetitorData, setCustomCompetitorData] = useState([]);

    const fetchCompetitorData = async () => {
        const response = await axios.get(`http://your-api-url/competitor-benchmark?platform=${platform}&brand=${brand}&competitor=${competitor}`);
        setCompetitorData(response.data.comparison);
    };

    const fetchCustomCompetitorData = async () => {
        const response = await axios.post("http://your-api-url/competitors/analyze", {
            competitors: competitors.split(","),
        });
        setCustomCompetitorData(response.data);
    };

    useEffect(() => {
        fetchCompetitorData();
    }, []);

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🏆 AI-Powered Competitor Analysis</Text>
            <TextInput style={styles.input} placeholder="Your Brand" value={brand} onChangeText={setBrand} />
            <TextInput style={styles.input} placeholder="Competitor Brand" value={competitor} onChangeText={setCompetitor} />
            <Button title="Compare Performance" onPress={fetchCompetitorData} />

            {competitorData && (
                <View style={styles.analytics}>
                    <Text>📊 {brand} vs. {competitor} on {platform}</Text>
                    <Text>🔹 Likes: {competitorData.brand.engagement.likes} vs. {competitorData.competitor.engagement.likes}</Text>
                    <Text>🔹 Shares: {competitorData.brand.engagement.shares} vs. {competitorData.competitor.engagement.shares}</Text>
                    <Text>🔹 Comments: {competitorData.brand.engagement.comments} vs. {competitorData.competitor.engagement.comments}</Text>
                    <Text>🔹 Positive Sentiment: {competitorData.brand.sentiment_trends.positive}% vs. {competitorData.competitor.sentiment_trends.positive}%</Text>
                    <Text>🔹 Negative Sentiment: {competitorData.brand.sentiment_trends.negative}% vs. {competitorData.competitor.sentiment_trends.negative}%</Text>
                </View>
            )}

            <TextInput placeholder="Enter competitor handles (e.g. @competitor1, @competitor2)" value={competitors} onChangeText={setCompetitors} style={styles.input} />
            <Button title="🔍 Analyze Competitors" onPress={fetchCustomCompetitorData} />
            
            <FlatList
                data={customCompetitorData}
                renderItem={({ item }) => (
                    <Text>🔥 {item.competitor}: {item.engagement_score} engagement</Text>
                )}
                keyExtractor={(item, index) => index.toString()}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { fontSize: 20, fontWeight: "bold", marginBottom: 10 },
    input: { borderWidth: 1, padding: 10, marginBottom: 10 },
    analytics: { marginTop: 20 },
});

export default CompetitorDashboard;
