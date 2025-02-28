import React, { useState } from "react";
import { View, Text, TextInput, Button, FlatList } from "react-native";
import axios from "axios";

const CompetitorSentiment = () => {
    const [competitor, setCompetitor] = useState("");
    const [data, setData] = useState([]);

    const fetchCompetitorSentiment = async () => {
        const res = await axios.get(`http://your-api-url/competitor_sentiment?competitor=${competitor}`);
        setData(res.data.data);
    };

    return (
        <View>
            <Text>🏆 Competitor Sentiment Analysis</Text>

            <TextInput
                placeholder="Enter competitor name"
                value={competitor}
                onChangeText={setCompetitor}
            />
            <Button title="🔍 Analyze Competitor" onPress={fetchCompetitorSentiment} />

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

export default CompetitorSentiment;
