import React, { useState, useEffect } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import axios from "axios";

const ContentStrategy = () => {
    const [brand, setBrand] = useState("Nike");
    const [trend, setTrend] = useState("AI in Sports");
    const [sentiment, setSentiment] = useState("Positive");
    const [recommendations, setRecommendations] = useState(null);

    const fetchRecommendations = async () => {
        const response = await axios.get(`http://your-api-url/content-strategy?brand=${brand}&trend=${trend}&sentiment=${sentiment}`);
        setRecommendations(response.data.recommendations);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📢 AI-Powered Content Strategy</Text>
            <TextInput style={styles.input} placeholder="Brand Name" value={brand} onChangeText={setBrand} />
            <TextInput style={styles.input} placeholder="Trending Topic" value={trend} onChangeText={setTrend} />
            <TextInput style={styles.input} placeholder="Audience Sentiment" value={sentiment} onChangeText={setSentiment} />
            <Button title="Get Content Ideas" onPress={fetchRecommendations} />

            {recommendations && <Text style={styles.result}>{recommendations}</Text>}
        </View>
    );
};

export default ContentStrategy;
