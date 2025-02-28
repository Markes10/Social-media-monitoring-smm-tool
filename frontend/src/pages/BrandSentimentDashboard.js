import React, { useState } from "react";
import { View, Text, TextInput, Button, FlatList, StyleSheet } from "react-native";
import axios from "axios";

const BrandSentimentDashboard = () => {
    const [brand, setBrand] = useState("");
    const [sentimentData, setSentimentData] = useState(null);

    const analyzeBrandSentiment = async () => {
        const response = await axios.get(`http://your-api-url/sentiment/brand?brand=${brand}`);
        setSentimentData(response.data);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📊 Brand Sentiment Analysis</Text>

            <TextInput
                placeholder="Enter a brand name (e.g. Tesla)"
                value={brand}
                onChangeText={setBrand}
                style={styles.input}
            />

            <Button title="🔍 Analyze Brand Sentiment" onPress={analyzeBrandSentiment} />

            {sentimentData && (
                <View>
                    <Text>🔥 Brand: {sentimentData.brand}</Text>
                    <Text>📈 Positive: {sentimentData.sentiment_distribution["Positive"]}</Text>
                    <Text>📉 Negative: {sentimentData.sentiment_distribution["Negative"]}</Text>
                    <Text>😐 Neutral: {sentimentData.sentiment_distribution["Neutral"]}</Text>

                    <Text style={styles.subHeader}>Recent Tweets:</Text>
                    <FlatList
                        data={sentimentData.tweets}
                        renderItem={({ item }) => (
                            <View>
                                <Text>📝 {item.text}</Text>
                                <Text>👍 Likes: {item.likes} 🔁 Retweets: {item.retweets}</Text>
                                <Text>Sentiment: {item.sentiment.bert} (Confidence: {item.sentiment.confidence})</Text>
                            </View>
                        )}
                        keyExtractor={(item, index) => index.toString()}
                    />
                </View>
            )}
        </View>
    );
};

export default BrandSentimentDashboard;
