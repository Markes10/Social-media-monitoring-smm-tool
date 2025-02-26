import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import axios from "axios";

const ContentPrediction = () => {
    const [wordCount, setWordCount] = useState("");
    const [imageCount, setImageCount] = useState("");
    const [hashtagCount, setHashtagCount] = useState("");
    const [postHour, setPostHour] = useState("");
    const [predictedEngagement, setPredictedEngagement] = useState(null);

    const predictEngagement = async () => {
        const response = await axios.get(`http://your-api-url/content-prediction`, {
            params: { 
                word_count: wordCount, 
                image_count: imageCount, 
                hashtag_count: hashtagCount, 
                post_hour: postHour 
            }
        });
        setPredictedEngagement(response.data.predicted_engagement);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📊 AI Content Performance Prediction</Text>
            
            <TextInput placeholder="Word Count" keyboardType="numeric" onChangeText={setWordCount} style={styles.input} />
            <TextInput placeholder="Image Count" keyboardType="numeric" onChangeText={setImageCount} style={styles.input} />
            <TextInput placeholder="Hashtag Count" keyboardType="numeric" onChangeText={setHashtagCount} style={styles.input} />
            <TextInput placeholder="Posting Hour (0-23)" keyboardType="numeric" onChangeText={setPostHour} style={styles.input} />
            
            <Button title="Predict Engagement" onPress={predictEngagement} />

            {predictedEngagement !== null && (
                <Text style={styles.result}>🔥 Predicted Engagement: {predictedEngagement}</Text>
            )}
        </View>
    );
};

export default ContentPrediction;
