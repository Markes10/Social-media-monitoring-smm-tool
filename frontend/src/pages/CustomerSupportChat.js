import React, { useState } from "react";
import { View, Text, TextInput, Button } from "react-native";
import axios from "axios";

const CustomerSupportChat = () => {
    const [message, setMessage] = useState("");
    const [response, setResponse] = useState("");

    const sendMessage = async () => {
        const res = await axios.get(`http://your-api-url/customer_support?message=${message}`);
        setResponse(res.data.ai_response);
    };

    return (
        <View>
            <Text>📩 AI Customer Support</Text>
            <TextInput
                placeholder="Type your question..."
                value={message}
                onChangeText={setMessage}
            />
            <Button title="Send" onPress={sendMessage} />
            
            {response && (
                <View>
                    <Text>🤖 AI Response: {response}</Text>
                </View>
            )}
        </View>
    );
};

export default CustomerSupportChat;
