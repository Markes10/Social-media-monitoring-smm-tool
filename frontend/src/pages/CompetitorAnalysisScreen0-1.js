import React, { useState, useEffect } from "react";
import { View, Text, TextInput, Button, FlatList, StyleSheet } from "react-native";
import axios from "axios";

const CompetitorAnalysisScreen = () => {
    const [insights, setInsights] = useState([]);
    const [username, setUsername] = useState("");
    const [platform, setPlatform] = useState("Instagram");
    const [result, setResult] = useState(null);

    useEffect(() => {
        fetchInsights();
    }, []);

    const fetchInsights = async () => {
        const response = await axios.get("http://your-api-url/competitor-insights");
        setInsights(response.data.competitor_insights);
    };

    const fetchAnalysis = async () => {
        const response = await axios.get(`http://your-api-url/competitor-analysis?username=${username}&platform=${platform}`);
        setResult(response.data.competitor_analysis);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📊 Competitor Analysis</Text>
            <TextInput style={styles.input} placeholder="Enter Competitor Username" value={username} onChangeText={setUsername} />
            <Button title="Analyze" onPress={fetchAnalysis} />
            {result && <Text>🔥 Top Post: {result.top_post}</Text>}
            
            <FlatList
                data={insights}
                keyExtractor={(item, index) => index.toString()}
                renderItem={({ item }) => (
                    <View style={styles.insightCard}>
                        <Text>👥 Competitor: {item.competitor}</Text>
                        <Text>📊 Your Engagement: {item.your_engagement}</Text>
                        <Text>📈 Competitor Engagement: {item.competitor_engagement}</Text>
                        <Text>🔥 Insight: {item.insight}</Text>
                        <Text>💡 Advice: {item.advice}</Text>
                    </View>
                )}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { fontSize: 20, fontWeight: "bold" },
    input: { borderWidth: 1, padding: 10, marginBottom: 10 },
    insightCard: { padding: 10, borderBottomWidth: 1, marginVertical: 5 },
});

export default CompetitorAnalysisScreen;
