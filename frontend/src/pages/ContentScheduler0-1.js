import React, { useState, useEffect } from "react";
import { View, Text, TextInput, Button, Picker, StyleSheet } from "react-native";
import axios from "axios";

const ContentScheduler = () => {
    const [contentData, setContentData] = useState(null);
    const [scheduleData, setScheduleData] = useState(null);
    const [platform, setPlatform] = useState("twitter");
    const [message, setMessage] = useState("");
    const [scheduleTime, setScheduleTime] = useState("");
    const [captionPrompt, setCaptionPrompt] = useState("");
    const [aiCaption, setAiCaption] = useState("");

    const fetchRecommendations = async () => {
        const contentResponse = await axios.get("http://your-api-url/content-recommendation");
        setContentData(contentResponse.data.content_data);
        
        const scheduleResponse = await axios.get("http://your-api-url/post-scheduler");
        setScheduleData(scheduleResponse.data.schedule_data);
    };

    const generateCaption = async () => {
        const response = await axios.post("http://your-api-url/content/generate-caption", { prompt: captionPrompt });
        setAiCaption(response.data.caption);
    };

    const schedulePost = async () => {
        console.log(`Scheduled post on ${platform} at ${scheduleTime}: ${message}`);
    };

    useEffect(() => {
        fetchRecommendations();
    }, []);

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📅 AI-Powered Content & Post Scheduler</Text>
            
            {contentData && (
                <View>
                    <Text>🎨 Best Content Type: {contentData.best_content_type}</Text>
                    <Text>📊 Engagement Score: {contentData.engagement_score}</Text>
                    <Text>💡 Recommendation: {contentData.recommendation}</Text>
                </View>
            )}
            
            {scheduleData && (
                <View>
                    <Text>🕒 Best Time to Post: {scheduleData.best_time}</Text>
                    <Text>✅ Recommendation: {scheduleData.recommendation}</Text>
                </View>
            )}
            
            <TextInput
                placeholder="Enter Caption Prompt"
                value={captionPrompt}
                onChangeText={setCaptionPrompt}
                style={styles.input}
            />
            <Button title="🤖 Generate Caption" onPress={generateCaption} />
            {aiCaption && <Text>Suggested Caption: {aiCaption}</Text>}

            <TextInput
                placeholder="Enter Post Message"
                value={message}
                onChangeText={setMessage}
                style={styles.input}
            />

            <TextInput
                placeholder="Enter Schedule Time (HH:MM)"
                value={scheduleTime}
                onChangeText={setScheduleTime}
                style={styles.input}
            />

            <Picker selectedValue={platform} onValueChange={setPlatform} style={styles.input}>
                <Picker.Item label="Twitter" value="twitter" />
                <Picker.Item label="Facebook" value="facebook" />
                <Picker.Item label="Instagram" value="instagram" />
            </Picker>

            <Button title="📢 Schedule Post" onPress={schedulePost} />
            <Button title="🔄 Refresh Recommendations" onPress={fetchRecommendations} />
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { fontSize: 20, fontWeight: "bold", marginBottom: 10 },
    input: { borderWidth: 1, padding: 10, marginBottom: 10 },
});

export default ContentScheduler;
