import React, { useState, useEffect } from "react";
import { View, Text, TextInput, Button, FlatList, Alert, StyleSheet } from "react-native";
import axios from "axios";

const CrisisDashboard = () => {
    const [brand, setBrand] = useState("");
    const [inputText, setInputText] = useState("");
    const [alerts, setAlerts] = useState([]);
    const [crisisData, setCrisisData] = useState(null);
    const [sentiment, setSentiment] = useState("");

    const fetchAlerts = async () => {
        const res = await axios.get("http://your-api-url/crisis_alerts");
        setAlerts(res.data.crisis_alerts);
    };

    const fetchSentiment = async () => {
        const res = await axios.get(`http://your-api-url/analyze_sentiment?text=${inputText}`);
        setSentiment(res.data.sentiment);
    };

    const checkCrisis = async () => {
        const response = await axios.get(`http://your-api-url/crisis?brand=${brand}`);
        setCrisisData(response.data);
        if (response.data.crisis_detected) {
            Alert.alert("🚨 Crisis Alert!", `${brand} is experiencing ${response.data.negative_percentage}% negative sentiment!`);
        }
    };

    useEffect(() => {
        fetchAlerts();
    }, []);

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🚨 Crisis Monitoring Dashboard</Text>

            <TextInput placeholder="Enter a brand name (e.g. Tesla)" value={brand} onChangeText={setBrand} style={styles.input} />
            <Button title="🔍 Check Crisis" onPress={checkCrisis} />

            {crisisData && (
                <Text style={styles.result}>
                    {crisisData.crisis_detected ? `⚠️ Crisis Detected: ${crisisData.negative_percentage}% negative sentiment!` 
                    : `✅ No Crisis: ${crisisData.negative_percentage}% negative sentiment`}
                </Text>
            )}

            <FlatList
                data={alerts}
                keyExtractor={(item) => item.topic}
                renderItem={({ item }) => (
                    <View>
                        <Text>⚠️ {item.topic} - {item.tweets} tweets</Text>
                        <Text>{item.alert}</Text>
                    </View>
                )}
            />

            <Text style={styles.subHeader}>📊 Check Sentiment of a Post</Text>
            <TextInput placeholder="Enter text" value={inputText} onChangeText={setInputText} style={styles.input} />
            <Button title="🔍 Analyze Sentiment" onPress={fetchSentiment} />

            {sentiment && (
                <Text style={styles.result}>📢 Sentiment Analysis: {sentiment}</Text>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { fontSize: 20, fontWeight: "bold", marginBottom: 10 },
    input: { borderWidth: 1, padding: 10, marginBottom: 10 },
    subHeader: { fontSize: 16, fontWeight: "bold", marginTop: 10 },
    result: { marginTop: 10, fontSize: 16 },
});

export default CrisisDashboard;
