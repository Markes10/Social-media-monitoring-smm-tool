import React, { useState } from "react";
import { View, Text, TextInput, Button } from "react-native";
import axios from "axios";

const CrisisResponse = () => {
    const [issue, setIssue] = useState("");
    const [response, setResponse] = useState("");

    const fetchResponse = async () => {
        const res = await axios.get(`http://your-api-url/generate_response?issue=${issue}`);
        setResponse(res.data.response);
    };

    return (
        <View>
            <Text>📝 Crisis Auto-Response Generator</Text>

            <TextInput
                placeholder="Enter complaint or issue"
                value={issue}
                onChangeText={setIssue}
            />
            <Button title="🔍 Generate Response" onPress={fetchResponse} />

            {response && (
                <View>
                    <Text>💬 Suggested Response:</Text>
                    <Text>{response}</Text>
                </View>
            )}
        </View>
    );
};

export default CrisisResponse;
