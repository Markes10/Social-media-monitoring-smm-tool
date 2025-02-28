import React, { useState } from "react";
import { View, Text, TextInput, Button, Picker, StyleSheet } from "react-native";
import axios from "axios";

const EngagementTracker = () => {
    const [postId, setPostId] = useState("");
    const [platform, setPlatform] = useState("twitter");
    const [engagementData, setEngagementData] = useState([]);
    const [comment, setComment] = useState("");

    const fetchEngagement = async () => {
        const response = await axios.get("http://your-api-url/fetch-engagement", {
            params: { platform, post_id: postId }
        });
        setEngagementData(response.data);
    };

    const autoReply = async () => {
        await axios.post("http://your-api-url/auto-reply", {
            platform,
            post_id: postId,
            comment
        });
        alert("Auto-reply posted!");
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>📊 Engagement Tracker</Text>

            <TextInput
                placeholder="Enter Post ID"
                value={postId}
                onChangeText={setPostId}
                style={styles.input}
            />

            <Picker selectedValue={platform} onValueChange={setPlatform} style={styles.input}>
                <Picker.Item label="Twitter" value="twitter" />
                <Picker.Item label="Facebook" value="facebook" />
                <Picker.Item label="Instagram" value="instagram" />
                <Picker.Item label="LinkedIn" value="linkedin" />
            </Picker>

            <Button title="📈 Fetch Engagement" onPress={fetchEngagement} />

            {engagementData.length > 0 && (
                <View>
                    <Text style={styles.subHeader}>Comments:</Text>
                    {engagementData.map((comment, index) => (
                        <Text key={index} style={styles.comment}>{comment.text}</Text>
                    ))}
                </View>
            )}

            <TextInput
                placeholder="Enter Comment for Auto-Reply"
                value={comment}
                onChangeText={setComment}
                style={styles.input}
            />

            <Button title="💬 Auto-Reply" onPress={autoReply} />
        </View>
    );
};

export default EngagementTracker;
