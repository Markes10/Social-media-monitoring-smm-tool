import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import axios from "axios";

const ContentGenerator = () => {
    const [topic, setTopic] = useState("");
    const [tone, setTone] = useState("casual");
    const [post, setPost] = useState("");

    const generateContent = async () => {
        const response = await axios.get("http://your-api-url/generate-content", {
            params: { topic, tone }
        });
        setPost(response.data.generated_post);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🤖 AI Content Generator</Text>

            <TextInput
                placeholder="Enter topic"
                value={topic}
                onChangeText={setTopic}
                style={styles.input}
            />

            <TextInput
                placeholder="Enter tone (casual, professional, fun, etc.)"
                value={tone}
                onChangeText={setTone}
                style={styles.input}
            />

            <Button title="✨ Generate Post" onPress={generateContent} />

            {post && <Text style={styles.result}>📢 {post}</Text>}
        </View>
    );
};

export default ContentGenerator;
