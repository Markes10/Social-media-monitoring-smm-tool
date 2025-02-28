import React, { useState } from "react";
import { View, Text, TextInput, Button, Picker, StyleSheet } from "react-native";
import axios from "axios";

const SchedulePostScreen = () => {
    const [content, setContent] = useState("");
    const [dateTime, setDateTime] = useState("");
    const [platform, setPlatform] = useState("twitter");

    const schedulePost = async () => {
        await axios.post("http://your-api-url/schedule-post", { 
            content, 
            scheduled_time: dateTime, 
            platform 
        });
        alert("Post Scheduled!");
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>Schedule a Post</Text>

            <TextInput 
                style={styles.input} 
                placeholder="Enter post content..." 
                value={content} 
                onChangeText={setContent} 
            />

            <TextInput 
                style={styles.input} 
                placeholder="YYYY-MM-DD HH:MM:SS" 
                value={dateTime} 
                onChangeText={setDateTime} 
            />

            <Picker selectedValue={platform} onValueChange={setPlatform}>
                <Picker.Item label="Twitter" value="twitter" />
                <Picker.Item label="Facebook" value="facebook" />
                <Picker.Item label="LinkedIn" value="linkedin" />
            </Picker>

            <Button title="Schedule Post" onPress={schedulePost} />
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20 },
    header: { fontSize: 20, fontWeight: "bold" },
    input: { borderWidth: 1, padding: 10, marginVertical: 10 },
});

export default SchedulePostScreen;
