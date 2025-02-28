import React, { useState } from "react";
import { View, Text, TextInput, Button } from "react-native";
import axios from "axios";

const SocialListeningDashboard = () => {
    const [brand, setBrand] = useState("");
    const [data, setData] = useState(null);

    const fetchSocialData = async () => {
        const res = await axios.get(`http://your-api-url/social_listening?brand=${brand}`);
        setData(res.data);
    };

    return (
        <View>
            <Text>📡 Social Listening & Trend Analysis</Text>
            <TextInput
                placeholder="Enter brand name"
                value={brand}
                onChangeText={setBrand}
            />
            <Button title="🔍 Analyze Mentions" onPress={fetchSocialData} />

            {data && (
                <View>
                    <Text>🔥 AI Trend Analysis: {data.trend_analysis}</Text>
                    <Text>📝 Recent Mentions: {JSON.stringify(data.brand_mentions, null, 2)}</Text>
                </View>
            )}
        </View>
    );
};

export default SocialListeningDashboard;
