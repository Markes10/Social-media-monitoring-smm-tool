import React, { useState } from "react";
import { View, Text, TextInput, Button, FlatList, StyleSheet } from "react-native";
import axios from "axios";

const CompetitorMonitor = () => {
    const [competitorUrl, setCompetitorUrl] = useState("");
    const [posts, setPosts] = useState([]);
    const [trendingPosts, setTrendingPosts] = useState([]);

    const fetchPosts = async () => {
        const response = await axios.get(`http://your-api-url/competitor/posts?url=${competitorUrl}`);
        setPosts(response.data);
    };

    const analyzeTrends = async () => {
        const response = await axios.post("http://your-api-url/competitor/trending", posts);
        setTrendingPosts(response.data.trending_posts);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📊 Competitor Monitoring</Text>

            <TextInput
                placeholder="Enter Competitor Profile URL"
                value={competitorUrl}
                onChangeText={setCompetitorUrl}
                style={styles.input}
            />

            <Button title="🔍 Fetch Posts" onPress={fetchPosts} />
            
            <FlatList
                data={posts}
                renderItem={({ item }) => <Text>📢 {item.post} (Engagement: {item.engagement})</Text>}
                keyExtractor={(item, index) => index.toString()}
            />

            <Button title="🔥 Analyze Trends" onPress={analyzeTrends} />
            
            {trendingPosts.length > 0 && (
                <View>
                    <Text style={styles.subheader}>Trending Posts:</Text>
                    {trendingPosts.map((post, index) => (
                        <Text key={index}>🔥 {post}</Text>
                    ))}
                </View>
            )}
        </View>
    );
};

export default CompetitorMonitor;
