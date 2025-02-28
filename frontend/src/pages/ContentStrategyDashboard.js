import React, { useState } from "react";
import { View, Text, TextInput, Button } from "react-native";
import axios from "axios";

const ContentStrategyDashboard = () => {
    const [platform, setPlatform] = useState("");
    const [data, setData] = useState(null);

    const fetchContentStrategy = async () => {
        const res = await axios.get(`http://your-api-url/content_strategy?platform=${platform}`);
        setData(res.data);
    };

    return (
        <View>
            <Text>📈 Content Strategy Optimization</Text>
            <TextInput
                placeholder="Enter platform (Twitter, Instagram, etc.)"
                value={platform}
                onChangeText={setPlatform}
            />
            <Button title="🔍 Optimize Strategy" onPress={fetchContentStrategy} />

            {data && (
                <View>
                    <Text>📝 AI Recommendations: {data.recommendations}</Text>
                    <Text>📊 Top Content: {JSON.stringify(data.top_content, null, 2)}</Text>
                </View>
            )}
        </View>
    );
};

export default ContentStrategyDashboard;
