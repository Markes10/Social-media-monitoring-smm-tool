import React, { useState } from "react";
import { View, Text, TextInput, Button, FlatList, StyleSheet } from "react-native";
import axios from "axios";

const FakeNewsMonitor = () => {
    const [platform, setPlatform] = useState("twitter");
    const [keyword, setKeyword] = useState("");
    const [posts, setPosts] = useState([]);
    const [flaggedPosts, setFlaggedPosts] = useState([]);

    const fetchPosts = async () => {
        const response = await axios.get(`http://your-api-url/fake-news/posts?platform=${platform}&keyword=${keyword}`);
        setPosts(response.data);
    };

    const analyzeFakeNews = async () => {
        const response = await axios.post("http://your-api-url/fake-news/analyze", posts);
        setFlaggedPosts(response.data.flagged_posts);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📰 Fake News Detection</Text>

            <TextInput
                placeholder="Enter keyword (e.g. trending topic)"
                value={keyword}
                onChangeText={setKeyword}
                style={styles.input}
            />

            <Button title="📢 Fetch Posts" onPress={fetchPosts} />
            
            <FlatList
                data={posts}
                renderItem={({ item }) => <Text>💬 {item}</Text>}
                keyExtractor={(item, index) => index.toString()}
            />

            <Button title="🛑 Detect Fake News" onPress={analyzeFakeNews} />
            
            {flaggedPosts.length > 0 && (
                <View>
                    <Text style={styles.subheader}>🚨 Flagged Fake News:</Text>
                    {flaggedPosts.map((post, index) => (
                        <Text key={index} style={styles.alert}>
                            ⚠️ {post.text} (Confidence: {post.confidence.toFixed(2)})
                        </Text>
                    ))}
                </View>
            )}
        </View>
    );
};

export default FakeNewsMonitor;
