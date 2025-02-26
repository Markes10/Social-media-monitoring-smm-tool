import React, { useState, useEffect } from "react";
import { View, Text, TextInput, Button, FlatList, StyleSheet } from "react-native";
import axios from "axios";

const HashtagDashboard = () => {
    const [inputText, setInputText] = useState("");
    const [hashtagData, setHashtagData] = useState(null);
    const [trending, setTrending] = useState([]);
    const [analysis, setAnalysis] = useState(null);

    const analyzeHashtags = async () => {
        const response = await axios.post("http://your-api-url/hashtag-analysis", { text: inputText });
        setHashtagData(response.data.hashtag_data);
    };

    const fetchHashtagInsights = async () => {
        const response = await axios.get("http://your-api-url/hashtag-analysis");
        setHashtagData(response.data.hashtag_insights);
    };

    const fetchTrendingHashtags = async () => {
        const response = await axios.get("http://your-api-url/hashtags/trending");
        setTrending(response.data);
    };

    const analyzeHashtag = async (hashtag) => {
        const response = await axios.get(`http://your-api-url/hashtags/analyze?hashtag=${hashtag}`);
        setAnalysis(response.data);
    };

    useEffect(() => {
        fetchHashtagInsights();
    }, []);

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📢 AI-Powered Hashtag Analysis & Trend Optimization</Text>

            <TextInput
                style={styles.input}
                placeholder="Enter a social media post..."
                value={inputText}
                onChangeText={setInputText}
            />
            <Button title="Get Hashtags" onPress={analyzeHashtags} />
            
            {hashtagData && (
                <View>
                    <Text>💬 Text: {hashtagData.text}</Text>
                    <Text>📊 Suggested Hashtags:</Text>
                    {hashtagData.hashtags.map((tag, index) => (
                        <Text key={index}>#{tag}</Text>
                    ))}
                </View>
            )}

            <Button title="🔥 Get Trending Hashtags" onPress={fetchTrendingHashtags} />
            <FlatList
                data={trending}
                renderItem={({ item }) => <Text>#{item}</Text>}
                keyExtractor={(item, index) => index.toString()}
            />

            <TextInput
                placeholder="Enter a hashtag (e.g. #AI)"
                style={styles.input}
                onChangeText={setAnalysis}
            />
            <Button title="🔍 Analyze Hashtag" onPress={() => analyzeHashtag(analysis)} />
            
            {analysis && (
                <View>
                    <Text>🔥 Avg Likes: {analysis.avg_likes}</Text>
                    <Text>🔥 Avg Retweets: {analysis.avg_retweets}</Text>
                    <Text>🔝 Top Words: {analysis.top_words.map(word => word[0]).join(", ")}</Text>
                </View>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { fontSize: 20, fontWeight: "bold", marginBottom: 10 },
    input: { borderWidth: 1, padding: 10, marginBottom: 10 },
});

export default HashtagDashboard;
