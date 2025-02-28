import React, { useState } from "react";
import { View, Text, TextInput, Button, FlatList, StyleSheet } from "react-native";
import axios from "axios";

const CompetitorDashboard = () => {
    const [competitor, setCompetitor] = useState("");
    const [handles, setHandles] = useState("");
    const [brands, setBrands] = useState("");
    const [competitorData, setCompetitorData] = useState(null);

    const fetchCompetitorBenchmark = async () => {
        const res = await axios.get(`http://your-api-url/competitor_benchmark?competitor=${competitor}`);
        setCompetitorData(res.data);
    };

    const fetchCompetitorAnalysis = async () => {
        const res = await axios.get(`http://your-api-url/competitor_analysis?handles=${handles}`);
        setCompetitorData(res.data);
    };

    const analyzeCompetitors = async () => {
        const response = await axios.get(`http://your-api-url/competitor/comparison?brands=${brands}`);
        setCompetitorData(response.data);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>⚔️ Competitor Analysis Dashboard</Text>

            <TextInput
                placeholder="Enter Competitor Name"
                value={competitor}
                onChangeText={setCompetitor}
                style={styles.input}
            />
            <Button title="🔍 Benchmark Competitor" onPress={fetchCompetitorBenchmark} />

            <TextInput
                placeholder="Enter Competitor Handles (comma-separated)"
                value={handles}
                onChangeText={setHandles}
                style={styles.input}
            />
            <Button title="🔍 Analyze Competitors" onPress={fetchCompetitorAnalysis} />

            <TextInput
                placeholder="Enter Brands (e.g., Tesla, Ford, BMW)"
                value={brands}
                onChangeText={setBrands}
                style={styles.input}
            />
            <Button title="🔍 Compare Brands" onPress={analyzeCompetitors} />

            {competitorData && (
                <FlatList
                    data={Object.entries(competitorData)}
                    renderItem={({ item }) => {
                        const [brand, data] = item;
                        return (
                            <View>
                                <Text style={styles.subHeader}>🔥 {brand}</Text>
                                <Text>✅ Positive: {data.sentiment_distribution?.["Positive"]}</Text>
                                <Text>❌ Negative: {data.sentiment_distribution?.["Negative"]}</Text>
                                <Text>😐 Neutral: {data.sentiment_distribution?.["Neutral"]}</Text>
                                <Text>❤️ Avg Likes: {data.avg_likes?.toFixed(2)}</Text>
                                <Text>🔁 Avg Retweets: {data.avg_retweets?.toFixed(2)}</Text>
                            </View>
                        );
                    }}
                    keyExtractor={(item) => item[0]}
                />
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { fontSize: 20, fontWeight: "bold", marginBottom: 10 },
    input: { borderWidth: 1, padding: 10, marginBottom: 10 },
    subHeader: { fontSize: 16, fontWeight: "bold", marginTop: 10 },
});

export default CompetitorDashboard;