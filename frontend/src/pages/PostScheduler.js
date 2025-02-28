import React, { useState } from "react";
import { View, Text, TextInput, Button, Picker, StyleSheet } from "react-native";
import axios from "axios";

const PostScheduler = () => {
    const [content, setContent] = useState("");
    const [platform, setPlatform] = useState("twitter");
    const [scheduledTime, setScheduledTime] = useState("");

    const schedulePost = async () => {
        const response = await axios.post("http://your-api-url/schedule-post", {
            content,
            platform,
            scheduled_time: scheduledTime
        });
        alert(response.data.status);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>⏳ AI Post Scheduler</Text>

            <TextInput
                placeholder="Enter Post Content"
                value={content}
                onChangeText={setContent}
                style={styles.input}
            />

            <Picker selectedValue={platform} onValueChange={setPlatform} style={styles.input}>
                <Picker.Item label="Twitter" value="twitter" />
                <Picker.Item label="Facebook" value="facebook" />
                <Picker.Item label="Instagram" value="instagram" />
                <Picker.Item label="LinkedIn" value="linkedin" />
            </Picker>

            <TextInput
                placeholder="Enter Scheduled Time (YYYY-MM-DD HH:MM:SS)"
                value={scheduledTime}
                onChangeText={setScheduledTime}
                style={styles.input}
            />

            <Button title="📅 Schedule Post" onPress={schedulePost} />
        </View>
    );
};

export default PostScheduler;
