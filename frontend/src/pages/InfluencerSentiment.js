import React, { useState } from "react";
import { View, Text, TextInput, Button, FlatList } from "react-native";
import axios from "axios";

const InfluencerSentiment = () => {
    const [influencer, setInfluencer] = useState("");
    const [data, setData] = useState([]);

    const fetchInfluencerSentiment = async () => {
        const res = await axios.get(`http://your-api-url/influencer_sentiment?influencer=${influencer}`);
        setData(res.data.data);
    };

    return (
        <View>
            <Text>🤳 Influencer Sentiment Analysis</Text>

            <TextInput
                placeholder="Enter influencer handle"
                value={influencer}
                onChangeText={setInfluencer}
            />
            <Button title="🔍 Analyze Influencer" onPress={fetchInfluencerSentiment} />

            <FlatList
                data={data}
                keyExtractor={(item) => item.timestamp}
                renderItem={({ item }) => (
                    <View>
                        <Text>{item.timestamp} 📅</Text>
                        <Text>💬 {item.tweet}</Text>
                        <Text>Sentiment: {item.sentiment === "Positive" ? "😊" : item.sentiment === "Negative" ? "😡" : "😐"}</Text>
                    </View>
                )}
            />
        </View>
    );
};

export default InfluencerSentiment;
