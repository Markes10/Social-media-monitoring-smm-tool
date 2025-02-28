import React, { useState } from "react";
import { View, Text, TextInput, Button, FlatList, StyleSheet } from "react-native";
import axios from "axios";

const SocialListening = () => {
    const [platform, setPlatform] = useState("twitter");
    const [keyword, setKeyword] = useState("");
    const [posts, setPosts] = useState([]);
    const [trends, setTrends] = useState([]);

    const fetchPosts = async () => {
        const response = await axios.get(`http://your-api-url/social/listening?platform=${platform}&keyword=${keyword}`);
        setPosts(response.data);
    };

    const analyzeTrends = async () => {
        const response = await axios.post("http://your-api-url/social/trends", posts);
        setTrends(response.data.trending_topics);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🔍 Social Listening & Trends</Text>

            <TextInput
                placeholder="Enter keyword (e.g. AI, fashion, fitness)"
                value={keyword}
                onChangeText={setKeyword}
                style={styles.input}
            />

            <Button title="📢 Fetch Conversations" onPress={fetchPosts} />
            
            <FlatList
                data={posts}
                renderItem={({ item }) => <Text>💬 {item}</Text>}
                keyExtractor={(item, index) => index.toString()}
            />

            <Button title="📊 Analyze Trends" onPress={analyzeTrends} />
            
            {trends.length > 0 && (
                <View>
                    <Text style={styles.subheader}>Trending Topics:</Text>
                    {trends.map((trend, index) => (
                        <Text key={index}>🔥 {trend.keyword} (Score: {trend.trend_score})</Text>
                    ))}
                </View>
            )}
        </View>
    );
};

export default SocialListening;
