import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import axios from "axios";

const CrisisMonitor = () => {
    const [posts, setPosts] = useState("");
    const [crisisData, setCrisisData] = useState(null);

    const analyzeCrisis = async () => {
        const postList = posts.split("\n").map((post) => post.trim());
        const response = await axios.post("http://your-api-url/detect-crisis", postList);
        setCrisisData(response.data.crisis_data);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🚨 AI-Powered Crisis Monitor</Text>
            <TextInput
                style={styles.input}
                placeholder="Enter recent social media posts (one per line)"
                multiline
                value={posts}
                onChangeText={setPosts}
            />
            <Button title="Analyze Crisis Risk" onPress={analyzeCrisis} />

            {crisisData && (
                <View>
                    <Text>🛑 Negative Sentiment: {crisisData.negative_percentage.toFixed(2)}%</Text>
                    <Text>📢 Recommended Action: {crisisData.response_strategy}</Text>
                </View>
            )}
        </View>
    );
};

export default CrisisMonitor;
