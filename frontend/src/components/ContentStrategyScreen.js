import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import axios from "axios";

const ContentStrategyScreen = () => {
    const [topic, setTopic] = useState("");
    const [audience, setAudience] = useState("");
    const [platform, setPlatform] = useState("Instagram");
    const [post, setPost] = useState("");

    const fetchContent = async () => {
        const response = await axios.get(`http://your-api-url/ai-content?topic=${topic}&audience=${audience}&platform=${platform}`);
        setPost(response.data.post);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🤖 AI-Powered Content Strategy</Text>
            <TextInput style={styles.input} placeholder="Enter Topic" value={topic} onChangeText={setTopic} />
            <TextInput style={styles.input} placeholder="Enter Target Audience" value={audience} onChangeText={setAudience} />
            <Button title="Generate AI Post" onPress={fetchContent} />
            {post && (
                <Text style={styles.result}>📢 Suggested Post: {post}</Text>
            )}
        </View>
    );
};

export default ContentStrategyScreen;
