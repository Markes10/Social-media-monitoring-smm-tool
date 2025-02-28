import React, { useState } from "react";
import { View, Text, TextInput, Button, ScrollView } from "react-native";
import axios from "axios";

const AutoReply = () => {
    const [brand, setBrand] = useState("");
    const [comment, setComment] = useState("");
    const [sentiment, setSentiment] = useState("");
    const [reply, setReply] = useState(null);

    const fetchReply = async () => {
        const res = await axios.get(`http://your-api-url/generate_auto_reply?brand=${brand}&comment=${comment}&sentiment=${sentiment}`);
        setReply(res.data.reply);
    };

    return (
        <ScrollView>
            <Text>💬 AI Auto-Reply Generator</Text>

            <TextInput
                placeholder="Enter Brand Name (e.g. Nike)"
                value={brand}
                onChangeText={setBrand}
            />
            <TextInput
                placeholder="Enter Comment (e.g. I love these shoes!)"
                value={comment}
                onChangeText={setComment}
            />
            <TextInput
                placeholder="Sentiment (Positive, Neutral, Negative)"
                value={sentiment}
                onChangeText={setSentiment}
            />

            <Button title="🤖 Generate Auto-Reply" onPress={fetchReply} />

            {reply && (
                <View>
                    <Text>📢 Suggested Auto-Reply:</Text>
                    <Text>{reply}</Text>
                </View>
            )}
        </ScrollView>
    );
};

export default AutoReply;
