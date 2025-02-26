import React, { useState } from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import axios from "axios";

const AutoResponse = () => {
    const [responseStatus, setResponseStatus] = useState("");

    const triggerAutoResponse = async () => {
        const response = await axios.post("http://your-api-url/auto-response");
        setResponseStatus(response.data.message);
    };

    return (
        <View style={styles.container}>
            <Text style={styles.header}>🤖 Auto-Response System</Text>
            <Button title="📢 Trigger Auto-Response" onPress={triggerAutoResponse} />
            {responseStatus && <Text style={styles.status}>{responseStatus}</Text>}
        </View>
    );
};

export default AutoResponse;
