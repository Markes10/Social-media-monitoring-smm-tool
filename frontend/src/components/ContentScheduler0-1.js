import React, { useState } from "react";
import { View, Text, TextInput, Button, Picker, StyleSheet, ScrollView } from "react-native";
import axios from "axios";

const ContentScheduler = () => {
    const [content, setContent] = useState("");
    const [platform, setPlatform] = useState("Twitter");
    const [scheduledTime, setScheduledTime] = useState("");
    const [bestTime, setBestTime] = useState(null);
    const [topic, setTopic] = useState("");
    const [suggestions, setSuggestions] = useState([]);
    const [selectedPost, setSelectedPost] = useState("");
    const [time, setTime] = useState(10);

    const fetchBestTime = async () => {
        try {
            const res = await axios.get("http://your-api-url/best_posting_time");
            setBestTime(res.data.best_posting_hour);
        } catch (error) {
            console.error("Error fetching best time:", error);
        }
    };

    const fetchSuggestions = async () => {
        try {
            const response = await axios.get("http://your-api-url/content_suggestions", {
                params: { topic },
            });
            setSuggestions(response.data.suggestions.split("\n"));
        } catch (error) {
            console.error("Error fetching suggestions:", error);
        }
    };

    const schedulePost = async () => {
        try {
            await axios.post("http://your-api-url/schedule_post", {
                platform,
                content: selectedPost || content,
                scheduled_time: scheduledTime,
                minutes_later: time,
            });
            alert("Post Scheduled Successfully!");
        } catch (error) {
            console.error("Error scheduling post:", error);
        }
    };

    return (
        <ScrollView contentContainerStyle={styles.container}>
            <Text style={styles.header}>📅 AI Content Scheduler</Text>

            <Button title="Get Best Posting Time" onPress={fetchBestTime} />
            {bestTime && <Text>📌 Best Time to Post: {bestTime}:00</Text>}

            <TextInput
                style={styles.input}
                placeholder="Enter your content"
                value={content}
                onChangeText={setContent}
            />

            <TextInput
                style={styles.input}
                placeholder="Enter Topic (e.g., Tech Trends)"
                value={topic}
                onChangeText={setTopic}
            />
            <Button title="Get AI Suggestions" onPress={fetchSuggestions} />

            {suggestions.length > 0 && (
                <View>
                    <Text style={styles.subHeader}>AI-Generated Posts:</Text>
                    {suggestions.map((post, index) => (
                        <Text key={index} style={styles.suggestion} onPress={() => setSelectedPost(post)}>
                            {post}
                        </Text>
                    ))}
                </View>
            )}

            <Picker selectedValue={platform} onValueChange={setPlatform} style={styles.input}>
                <Picker.Item label="Twitter" value="Twitter" />
                <Picker.Item label="Facebook" value="Facebook" />
                <Picker.Item label="Instagram" value="Instagram" />
            </Picker>

            <TextInput
                style={styles.input}
                placeholder="Enter scheduled time (YYYY-MM-DD HH:MM:SS)"
                value={scheduledTime}
                onChangeText={setScheduledTime}
            />

            <TextInput
                style={styles.input}
                placeholder="Minutes Later"
                keyboardType="numeric"
                value={time.toString()}
                onChangeText={(val) => setTime(parseInt(val))}
            />

            <Button title="Schedule Post" onPress={schedulePost} />
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: { flexGrow: 1, padding: 20, backgroundColor: "#fff" },
    header: { fontSize: 24, fontWeight: "bold", marginBottom: 10 },
    input: { borderWidth: 1, borderColor: "#ccc", padding: 10, marginVertical: 10, borderRadius: 5 },
    subHeader: { fontSize: 18, fontWeight: "bold", marginTop: 20 },
    suggestion: { fontSize: 16, marginTop: 5, color: "blue", textDecorationLine: "underline" },
});

export default ContentScheduler;
