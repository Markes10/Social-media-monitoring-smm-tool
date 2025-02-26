import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import axios from "axios";

const InfluencerAnalysisScreen = () => {
    const [username, setUsername] = useState("");
    const [platform, setPlatform] = useState("Instagram");
    const [result, setResult] = useState(null);

    const fetchAnalysis = async () => {
        const response = await axios.get(`http://your-api-url/influencer-analysis?username=${username}&platform=${platform}`);
        setResult(response.data.influencer_analysis);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📊 Influencer Performance Analysis</Text>
            <TextInput style={styles.input} placeholder="Enter Username" value={username} onChangeText={setUsername} />
            <Button title="Analyze" onPress={fetchAnalysis} />
            {result && (
                <Text>🔥 Credibility Score: {result.credibility_score}%</Text>
            )}
        </View>
    );
};

export default InfluencerAnalysisScreen;
