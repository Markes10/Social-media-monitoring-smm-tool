import React, { useState } from "react";
import { View, Text, TextInput, Button, ScrollView } from "react-native";
import axios from "axios";

const PRResponse = () => {
    const [brand, setBrand] = useState("");
    const [issue, setIssue] = useState("");
    const [sentiment, setSentiment] = useState("");
    const [response, setResponse] = useState(null);

    const fetchResponse = async () => {
        const res = await axios.get(`http://your-api-url/generate_pr_response?brand=${brand}&issue=${issue}&sentiment=${sentiment}`);
        setResponse(res.data.response);
    };

    return (
        <ScrollView>
            <Text>📝 AI-Powered PR Response Generator</Text>

            <TextInput
                placeholder="Enter Brand Name (e.g. Tesla)"
                value={brand}
                onChangeText={setBrand}
            />
            <TextInput
                placeholder="Describe the issue (e.g. battery fire)"
                value={issue}
                onChangeText={setIssue}
            />
            <TextInput
                placeholder="Sentiment (Positive, Neutral, Negative)"
                value={sentiment}
                onChangeText={setSentiment}
            />

            <Button title="🧠 Generate PR Response" onPress={fetchResponse} />

            {response && (
                <View>
                    <Text>📢 Suggested PR Response:</Text>
                    <Text>{response}</Text>
                </View>
            )}
        </ScrollView>
    );
};

export default PRResponse;
