import React, { useState } from "react";
import { View, Text, TextInput, Button } from "react-native";
import axios from "axios";

const EngagementDashboard = () => {
    const [message, setMessage] = useState("");
    const [response, setResponse] = useState("");

    const fetchResponse = async () => {
        const res = await axios.get(`http://your-api-url/engage?user_message=${message}`);
        setResponse(res.data.response);
    };

    return (
        <View>
            <Text>🤖 AI Engagement Assistant</Text>
            <TextInput
                placeholder="Enter user message"
                value={message}
                onChangeText={setMessage}
            />
            <Button title="💬 Generate Response" onPress={fetchResponse} />

            {response && (
                <View>
                    <Text>AI Response: {response}</Text>
                </View>
            )}
        </View>
    );
};

export default EngagementDashboard;
